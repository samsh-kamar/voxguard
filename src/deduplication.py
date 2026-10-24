from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_duplicate_candidates(text, existing_reports, threshold=0.28):
    """Return text-similar candidates; this is not proof of duplicate or fraud."""
    valid = [r for r in existing_reports if (r.get("text") or "").strip()]
    if not text.strip() or not valid:
        return []
    corpus = [text] + [r["text"] for r in valid]
    try:
        matrix = TfidfVectorizer(ngram_range=(1, 2), stop_words=None).fit_transform(corpus)
        sims = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    except ValueError:
        return []
    found = []
    for report, score in zip(valid, sims):
        if score >= threshold:
            found.append({
                "candidate_id": report.get("id"),
                "similarity": round(float(score), 3),
                "category": report.get("issue_type"),
                "location": report.get("location_text"),
                "status": report.get("status"),
                "text": report.get("text", "")[:180],
                "review_note": "Candidate only — check location, time, and evidence manually"
            })
    return sorted(found, key=lambda x: x["similarity"], reverse=True)
