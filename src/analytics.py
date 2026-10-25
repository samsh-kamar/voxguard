def spike_summary(df):
    """Small-data review alert based on hourly bins; not proof of coordination."""
    if df.empty or "created_at" not in df:
        return "Not enough data to estimate complaint-volume changes."
    import pandas as pd
    times = pd.to_datetime(df["created_at"], errors="coerce", utc=True).dropna()
    if len(times) < 4 or times.nunique() < 4:
        return "Spike alert unavailable: add at least four timestamped reports across multiple hours."
    hourly = times.dt.floor("h").value_counts().sort_index()
    full_hours = pd.date_range(hourly.index.min(), hourly.index.max(), freq="h", tz="UTC")
    hourly = hourly.reindex(full_hours, fill_value=0)
    if len(hourly) < 2:
        return "Spike alert unavailable: reports currently fall within one hourly bucket."
    latest = int(hourly.iloc[-1])
    baseline_values = hourly.iloc[:-1]
    baseline = float(baseline_values.median()) if len(baseline_values) else 0.0
    if latest >= 3 and latest >= 3 * max(baseline, 1):
        return (f"Review alert: latest hour has {latest} reports versus prior-hour median "
                f"{baseline:.1f}. This is a signal for human review, not proof of coordination.")
    return f"No spike threshold crossed. Latest hour: {latest}; previous-hour median: {baseline:.1f}."
