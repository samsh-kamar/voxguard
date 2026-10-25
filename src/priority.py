def _clamp_number(value, low, high, name):
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be numeric")
    return max(low, min(high, number))

def calculate_priority(severity, engagement, cluster_growth, criticality, trust_score=None):
    """
    Explainable prototype urgency score (0–100).
    Severity and criticality are 1–5; engagement and cluster_growth are counts.
    Evidence confidence is reported separately and does NOT reduce urgency.
    This is not an operational risk model.
    """
    sev = _clamp_number(severity, 1, 5, "severity") / 5
    crit = _clamp_number(criticality, 1, 5, "criticality") / 5
    engage_count = _clamp_number(engagement, 0, 1_000_000, "engagement")
    growth_count = _clamp_number(cluster_growth, 1, 1_000_000, "cluster_growth")
    engage = min(1.0, engage_count / 100)
    growth = min(1.0, max(0.0, growth_count - 1) / 10)

    components = {
        "Severity (40%)": 40 * sev,
        "Engagement (15%)": 15 * engage,
        "Cluster growth (20%)": 20 * growth,
        "Criticality (25%)": 25 * crit,
    }
    score = round(sum(components.values()))
    reasons = [f"{name}: {value:.1f}" for name, value in components.items()]
    if trust_score is not None:
        confidence = _clamp_number(trust_score, 1, 5, "trust_score")
        reasons.append(f"Evidence confidence (1–5, not included in urgency score): {confidence:.1f}")
    return score, reasons
