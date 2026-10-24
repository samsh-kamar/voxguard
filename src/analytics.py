def spike_summary(df):
    if df.empty or "created_at" not in df:
        return "Not enough data to estimate complaint-volume changes."
    import pandas as pd
    times = pd.to_datetime(df["created_at"], errors="coerce").dropna()
    if len(times) < 4:
        return "Spike alert unavailable: add more timestamped sample reports."
    counts = times.dt.floor("h").value_counts().sort_index()
    if len(counts) < 2:
        return "Spike alert unavailable: reports currently fall within one hourly bucket."
    latest = counts.iloc[-1]
    baseline = counts.iloc[:-1].median()
    if baseline > 0 and latest >= 3 * baseline and latest >= 3:
        return f"Review alert: latest hourly bucket has {latest} reports versus historical median {baseline:.1f}. This is a signal for human review, not proof of coordinated activity."
    return f"No spike threshold crossed in this small dataset. Latest hourly bucket: {latest}; baseline median: {baseline:.1f}."
