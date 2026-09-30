import pandas as pd

def summary_metrics(df):
    total = len(df)
    active_statuses = ["Applied","Screening","Interview"]
    return {
        "total": total,
        "active": int(df["status"].isin(active_statuses).sum()) if total else 0,
        "interviews": int((df["status"]=="Interview").sum()) if total else 0,
        "offers": int((df["status"]=="Offer").sum()) if total else 0,
    }

def status_breakdown(df):
    if df.empty: return pd.Series(dtype="int64")
    return df["status"].value_counts()

def monthly_trend(df):
    if df.empty: return pd.DataFrame()
    x = pd.to_datetime(df["applied_date"], errors="coerce").dropna()
    s = x.dt.to_period("M").astype(str).value_counts().sort_index()
    return s.rename("applications").to_frame()

def source_breakdown(df):
    if df.empty: return pd.Series(dtype="int64")
    return df["source"].value_counts()

def response_rate(df):
    if df.empty: return 0.0
    responded = ~df["status"].isin(["Applied","Ghosted"])
    return responded.mean() * 100
