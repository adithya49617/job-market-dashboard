import pandas as pd
import json
from collections import Counter
from pathlib import Path

SAMPLE_DATA_PATH = Path(__file__).parent.parent / "data" / "sample_jobs.json"

def load_jobs(api_jobs=None):
    """Load jobs from API result or fall back to sample data."""
    if api_jobs:
        return pd.DataFrame(api_jobs)
    with open(SAMPLE_DATA_PATH) as f:
        return pd.DataFrame(json.load(f))

def get_top_skills(df, top_n=15):
    """Count skill frequency across all jobs."""
    all_skills = []
    for skills in df["skills"]:
        if isinstance(skills, list):
            all_skills.extend(skills)
        elif isinstance(skills, str):
            all_skills.extend([s.strip() for s in skills.split(",")])
    counts = Counter(all_skills).most_common(top_n)
    return [{"skill": s, "count": c} for s, c in counts]

def get_top_companies(df, top_n=10):
    """Count jobs per company."""
    counts = df["company"].value_counts().head(top_n)
    return [{"company": c, "count": int(n)} for c, n in counts.items()]

def get_remote_breakdown(df):
    """Remote vs onsite vs hybrid distribution."""
    counts = df["remote"].value_counts()
    return [{"type": t, "count": int(c)} for t, c in counts.items()]

def get_top_locations(df, top_n=10):
    """Top hiring locations."""
    counts = df["location"].value_counts().head(top_n)
    return [{"location": l, "count": int(c)} for l, c in counts.items()]

def get_top_titles(df, top_n=10):
    """Most common job titles."""
    counts = df["title"].value_counts().head(top_n)
    return [{"title": t, "count": int(c)} for t, c in counts.items()]

def get_salary_distribution(df):
    """Average salary range per job title."""
    df = df.copy()
    df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")
    df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")
    df["salary_avg"] = (df["salary_min"] + df["salary_max"]) / 2
    df_clean = df.dropna(subset=["salary_avg"])

    result = (
        df_clean.groupby("title")["salary_avg"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    return [
        {"title": row["title"], "avg_salary": round(row["salary_avg"] / 1000, 1)}
        for _, row in result.iterrows()
    ]

def get_summary_stats(df):
    """High-level summary numbers."""
    df = df.copy()
    df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")
    df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")
    df["salary_avg"] = (df["salary_min"] + df["salary_max"]) / 2

    return {
        "total_jobs": len(df),
        "total_companies": df["company"].nunique(),
        "total_locations": df["location"].nunique(),
        "avg_salary": round(df["salary_avg"].mean() / 1000, 1),
        "remote_pct": round((df["remote"] == "remote").sum() / len(df) * 100),
        "top_skill": get_top_skills(df, top_n=1)[0]["skill"] if len(df) > 0 else "N/A"
    }

def run_all_analytics(api_jobs=None):
    """Run all analytics and return combined result."""
    df = load_jobs(api_jobs)
    return {
        "summary": get_summary_stats(df),
        "top_skills": get_top_skills(df),
        "top_companies": get_top_companies(df),
        "remote_breakdown": get_remote_breakdown(df),
        "top_locations": get_top_locations(df),
        "top_titles": get_top_titles(df),
        "salary_distribution": get_salary_distribution(df),
        "total_jobs": len(df)
    }
