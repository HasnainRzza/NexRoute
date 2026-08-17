import asyncio
import logging
import os
import pickle
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_FILE = BASE_DIR / "models" / "intent_model.pkl"

with open(MODEL_FILE, "rb") as file:
    classifier_data = pickle.load(file)

TEXTS = list(classifier_data["texts"])
LABELS = list(classifier_data["labels"])
MODEL_NAME = classifier_data["model_name"]
CONFIG = classifier_data["config"]
INTENT_LIST = [str(intent).lower() for intent in classifier_data.get("intents", ["read", "write"])]

TOP_K = int(CONFIG["top_k"])
MIN_SCORE = float(CONFIG["min_score"])
MIN_MARGIN = float(CONFIG["min_margin"])

# Use a small, bounded pool so concurrent requests are handled without unbounded-thread behavior.
# 2-4 workers is conservative and usually enough for this model and dataset size.
DEFAULT_MAX_WORKERS = max(2, min(4, os.cpu_count() or 1))
EMBEDDING_EXECUTOR = ThreadPoolExecutor(
    max_workers=DEFAULT_MAX_WORKERS,
    thread_name_prefix="fastembed-inference",
)

MODEL = TextEmbedding(model_name=MODEL_NAME)

TRAINING_EMBEDDINGS = np.asarray(classifier_data["embeddings"], dtype=np.float32)
if TRAINING_EMBEDDINGS.ndim == 1:
    TRAINING_EMBEDDINGS = TRAINING_EMBEDDINGS.reshape(1, -1)

TRAINING_EMBEDDING_NORMS = np.linalg.norm(TRAINING_EMBEDDINGS, axis=1, keepdims=True)
TRAINING_EMBEDDING_NORMS[TRAINING_EMBEDDING_NORMS == 0.0] = 1.0
TRAINING_EMBEDDINGS_NORMALIZED = TRAINING_EMBEDDINGS / TRAINING_EMBEDDING_NORMS

INTENT_ORDER = [intent for intent in INTENT_LIST if intent in {"read", "write"}] or ["read", "write"]


def _embed_query_sync(query: str) -> np.ndarray:
    """Embed a single query text with the globally loaded model."""
    if not isinstance(query, str):
        raise TypeError("Query must be a string.")

    candidate = next(iter(MODEL.embed([query])), None)
    if candidate is None:
        return np.zeros(1, dtype=np.float32)

    return np.asarray(candidate, dtype=np.float32).reshape(-1)


def _top_k_indices(similarities: np.ndarray, k: int) -> np.ndarray:
    k = max(1, min(int(k), similarities.size))
    if k >= similarities.size:
        return np.argsort(similarities)[::-1]

    top_candidates = np.argpartition(similarities, -k)[-k:]
    top_candidates = top_candidates[np.argsort(similarities[top_candidates])[::-1]]
    return top_candidates


async def classify(query: str, top_k: int = TOP_K):
    """Classify a query by comparing against the stored normalized embeddings."""
    cleaned_query = (query or "").strip()

    if not cleaned_query:
        return {
            "intent": "ambiguous",
            "confidence": 0.0,
            "margin": 0.0,
            "scores": {intent: 0.0 for intent in INTENT_ORDER},
        }

    loop = asyncio.get_running_loop()
    query_embedding = await loop.run_in_executor(EMBEDDING_EXECUTOR, _embed_query_sync, cleaned_query)
    query_norm = float(np.linalg.norm(query_embedding))

    if query_norm == 0.0:
        return {
            "intent": "ambiguous",
            "confidence": 0.0,
            "margin": 0.0,
            "scores": {intent: 0.0 for intent in INTENT_ORDER},
        }

    normalized_query = query_embedding / query_norm
    similarities = TRAINING_EMBEDDINGS_NORMALIZED @ normalized_query
    top_indices = _top_k_indices(similarities, top_k)

    intent_scores: dict[str, list[float]] = {intent: [] for intent in INTENT_ORDER}
    for index in top_indices:
        intent_name = str(LABELS[int(index)]).lower()
        if intent_name not in intent_scores:
            intent_scores[intent_name] = []
        intent_scores[intent_name].append(float(similarities[int(index)]))

    aggregated = {
        intent: float(sum(scores) / len(scores)) if scores else 0.0
        for intent, scores in intent_scores.items()
    }

    ranked_intents = sorted(aggregated.items(), key=lambda item: item[1], reverse=True)
    if not ranked_intents:
        return {
            "intent": "ambiguous",
            "confidence": 0.0,
            "margin": 0.0,
            "scores": {intent: 0.0 for intent in INTENT_ORDER},
        }

    best_intent, best_score = ranked_intents[0]
    second_score = ranked_intents[1][1] if len(ranked_intents) > 1 else 0.0
    margin = float(best_score - second_score)

    final_intent = "ambiguous"
    if best_score >= MIN_SCORE and margin >= MIN_MARGIN:
        final_intent = best_intent

    ordered_scores = {intent: round(float(aggregated.get(intent, 0.0)), 4) for intent in INTENT_ORDER}
    return {
        "intent": str(final_intent),
        "confidence": round(float(best_score), 4),
        "margin": round(float(margin), 4),
        "scores": ordered_scores,
    }


__all__ = ["classify", "MODEL", "EMBEDDING_EXECUTOR", "TOP_K", "MIN_SCORE", "MIN_MARGIN"]