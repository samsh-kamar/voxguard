import pytest
from src.priority import calculate_priority

def test_score_range_and_reasons():
    score, reasons = calculate_priority(5, 100, 10, 5, 5)
    assert 0 <= score <= 100
    assert reasons

def test_higher_severity_increases_score():
    low, _ = calculate_priority(1, 0, 1, 1)
    high, _ = calculate_priority(5, 0, 1, 1)
    assert high > low

def test_invalid_numeric_input_is_rejected():
    with pytest.raises(ValueError):
        calculate_priority("high", 0, 1, 1)
