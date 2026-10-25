import pandas as pd
from src.analytics import spike_summary

def test_empty_analytics_is_safe():
    assert "Not enough data" in spike_summary(pd.DataFrame())

def test_small_dataset_does_not_claim_spike():
    df = pd.DataFrame({"created_at": ["2026-10-20T10:00:00Z", "2026-10-20T10:00:10Z"]})
    assert "unavailable" in spike_summary(df).lower()
