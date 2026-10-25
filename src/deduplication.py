from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_duplicate_candidates(new_text, rows, threshold=0.35):
    """
    Return text-similar candidates for human review.
    This does not prove that reports describe the same event or that evidence is fake.
    `rows` may contain dicts with a `text` field or plain strings.
    """
    query = str(new_text or "").strip()
    if not query or not rows:
        return []

    valid = []
    texts = []
    for index, item in enumerate(rows):
        body = str(item.get("text", "") if isinstance(item, dict) else item or "").strip()
        if body:
            valid.append((index, item, body))
            texts.append(body)
    if not texts:
        return []

    try:
        # Do not use English-only stop words: reports may be Hindi/Hinglish or regional.
        matrix = TfidfVectorizer(ngram_range=(1, 2), min_df=1).fit_transform([query] + texts)
        scores = cosine_similarity(matrix[0:1], matrix[1:]).ravel()
    except ValueError:
        return []

    candidates = []
    for (original_index, item, body), score in zip(valid, scores):
        if float(score) >= float(threshold):
            row = item if isinstance(item, dict) else {}
            candidates.append({
                "candidate_id": row.get("id", original_index),
                "similarity": round(float(score), 3),
                "category": row.get("issue_type", ""),
                "location": row.get("location_text", ""),
                "status": row.get("status", ""),
                "text": body[:240],
                "review_note": "Text-similarity candidate only; human review required for location, time, and evidence."
            })
    return sorted(candidates, key=lambda item: item["similarity"], reverse=True)
