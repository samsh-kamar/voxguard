from src.deduplication import find_duplicate_candidates

def test_similar_text_returns_candidate():
    rows = [{"id": 1, "text": "Large pothole on Boring Road causing traffic", "issue_type": "Road", "location_text": "Boring Road", "status": "New"}]
    result = find_duplicate_candidates("Pothole on Boring Road causing traffic jam", rows, threshold=0.2)
    assert result
