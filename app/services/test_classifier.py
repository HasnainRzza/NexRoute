from classifier import classify

queries = [
    "what is the hajj",
    "read the file",
    "write a summary",
]

for query in queries:
    result = classify(query)

    print("\n" + "=" * 60)
    print("USER:")
    print(query)
    print()
    print("INTENT:")
    print(result["intent"])
    print()
    print("CONFIDENCE:")
    print(result["confidence"])
    print()
    print("MARGIN:")
    print(result["margin"])
    print()
    print("SCORES:")
    print(result["scores"])