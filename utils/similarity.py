from rapidfuzz import fuzz # pyright: ignore[reportMissingImports]


def similarity_score(a, b):
    return fuzz.ratio(a.lower(), b.lower())