from src.priority import calculate_priority

def test_score_range():
    score, reasons = calculate_priority(5, 100, 10, 5, 5)
    assert 0 <= score <= 100
    assert reasons

def test_higher_severity_increases_score():
    low, _ = calculate_priority(1, 0, 1, 1, 1)
    high, _ = calculate_priority(5, 0, 1, 1, 1)
    assert high > low
