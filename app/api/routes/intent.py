from fastapi import APIRouter, Query
from utils.llm_fallback import fallback_classifier

router = APIRouter()


@router.get("/classify")
async def classify_endpoint(query: str = Query(..., min_length=1, max_length=2000)):
    from services.classifier import classify

    result = await classify(query)
    if result["intent"] == 'ambiguous':
        intent = fallback_classifier(query)
        result["intent"] = intent
        result["fallback"] = True

    return result