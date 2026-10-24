def calculate_priority(severity, engagement, cluster_growth, criticality, trust_score):
    """
    Explainable 0–100 heuristic. Inputs: severity/criticality/trust 1–5;
    engagement and cluster_growth are counts. Weights are a prototype choice,
    not an operational police risk model.
    """
    sev = max(1, min(5, int(severity))) / 5
    crit = max(1, min(5, int(criticality))) / 5
    trust = max(1, min(5, int(trust_score))) / 5
    engage = min(1.0, max(0, float(engagement)) / 100)
    growth = min(1.0, max(0, float(cluster_growth) - 1) / 10)
    components = {
        "Severity (40%)": 40 * sev,
        "Engagement (15%)": 15 * engage,
        "Cluster growth (20%)": 20 * growth,
        "Criticality (20%)": 20 * crit,
        "Trust signal (5%)": 5 * trust,
    }
    score = round(sum(components.values()))
    reasons = [f"{name}: {value:.1f}" for name, value in components.items()]
    return score, reasons
