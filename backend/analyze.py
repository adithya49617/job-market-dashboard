import pandas as pd
from collections import Counter

SAMPLE_JOBS = [
  {"title": "Data Scientist", "company": "Google", "location": "San Francisco, CA", "remote": "hybrid", "salary_min": 140000, "salary_max": 180000, "skills": ["Python", "SQL", "Machine Learning", "TensorFlow", "Statistics"]},
  {"title": "Machine Learning Engineer", "company": "Meta", "location": "Seattle, WA", "remote": "onsite", "salary_min": 160000, "salary_max": 220000, "skills": ["Python", "PyTorch", "Deep Learning", "MLOps", "Docker"]},
  {"title": "Data Analyst", "company": "Amazon", "location": "New York, NY", "remote": "remote", "salary_min": 90000, "salary_max": 130000, "skills": ["SQL", "Python", "Tableau", "Excel", "Statistics"]},
  {"title": "Data Scientist", "company": "Apple", "location": "San Francisco, CA", "remote": "onsite", "salary_min": 150000, "salary_max": 200000, "skills": ["Python", "R", "Machine Learning", "SQL", "NLP"]},
  {"title": "ML Engineer", "company": "Netflix", "location": "Los Angeles, CA", "remote": "hybrid", "salary_min": 155000, "salary_max": 210000, "skills": ["Python", "TensorFlow", "Spark", "SQL", "Kubernetes"]},
  {"title": "Data Engineer", "company": "Uber", "location": "San Francisco, CA", "remote": "hybrid", "salary_min": 130000, "salary_max": 170000, "skills": ["Python", "SQL", "Spark", "Airflow", "AWS"]},
  {"title": "Data Scientist", "company": "Microsoft", "location": "Seattle, WA", "remote": "hybrid", "salary_min": 145000, "salary_max": 190000, "skills": ["Python", "SQL", "Machine Learning", "Azure", "Statistics"]},
  {"title": "NLP Engineer", "company": "OpenAI", "location": "San Francisco, CA", "remote": "onsite", "salary_min": 180000, "salary_max": 250000, "skills": ["Python", "NLP", "PyTorch", "Transformers", "LLMs"]},
  {"title": "Data Analyst", "company": "Stripe", "location": "Remote", "remote": "remote", "salary_min": 95000, "salary_max": 135000, "skills": ["SQL", "Python", "Looker", "Statistics", "Excel"]},
  {"title": "ML Research Scientist", "company": "DeepMind", "location": "New York, NY", "remote": "onsite", "salary_min": 200000, "salary_max": 300000, "skills": ["Python", "PyTorch", "Deep Learning", "Research", "Mathematics"]},
  {"title": "Data Scientist", "company": "Airbnb", "location": "San Francisco, CA", "remote": "hybrid", "salary_min": 135000, "salary_max": 175000, "skills": ["Python", "SQL", "R", "Statistics", "A/B Testing"]},
  {"title": "Data Engineer", "company": "Snowflake", "location": "Remote", "remote": "remote", "salary_min": 125000, "salary_max": 165000, "skills": ["SQL", "Python", "dbt", "Snowflake", "Airflow"]},
  {"title": "Computer Vision Engineer", "company": "Tesla", "location": "Austin, TX", "remote": "onsite", "salary_min": 150000, "salary_max": 200000, "skills": ["Python", "PyTorch", "Computer Vision", "C++", "Deep Learning"]},
  {"title": "Data Scientist", "company": "LinkedIn", "location": "Seattle, WA", "remote": "hybrid", "salary_min": 140000, "salary_max": 185000, "skills": ["Python", "SQL", "Machine Learning", "Spark", "Statistics"]},
  {"title": "Analytics Engineer", "company": "Notion", "location": "Remote", "remote": "remote", "salary_min": 115000, "salary_max": 155000, "skills": ["SQL", "dbt", "Python", "Looker", "Data Modeling"]},
  {"title": "MLOps Engineer", "company": "Databricks", "location": "San Francisco, CA", "remote": "hybrid", "salary_min": 145000, "salary_max": 195000, "skills": ["Python", "MLflow", "Kubernetes", "Docker", "Spark"]},
  {"title": "Data Scientist", "company": "Spotify", "location": "New York, NY", "remote": "hybrid", "salary_min": 130000, "salary_max": 170000, "skills": ["Python", "SQL", "Machine Learning", "R", "A/B Testing"]},
  {"title": "AI Engineer", "company": "Anthropic", "location": "San Francisco, CA", "remote": "onsite", "salary_min": 200000, "salary_max": 280000, "skills": ["Python", "LLMs", "PyTorch", "NLP", "Research"]},
  {"title": "Data Analyst", "company": "DoorDash", "location": "San Francisco, CA", "remote": "hybrid", "salary_min": 100000, "salary_max": 140000, "skills": ["SQL", "Python", "Tableau", "Statistics", "Excel"]},
  {"title": "Data Engineer", "company": "Coinbase", "location": "Remote", "remote": "remote", "salary_min": 140000, "salary_max": 180000, "skills": ["Python", "SQL", "Spark", "AWS", "dbt"]},
  {"title": "Data Scientist", "company": "Lyft", "location": "San Francisco, CA", "remote": "hybrid", "salary_min": 135000, "salary_max": 175000, "skills": ["Python", "SQL", "Machine Learning", "Statistics", "Spark"]},
  {"title": "ML Engineer", "company": "Salesforce", "location": "San Francisco, CA", "remote": "hybrid", "salary_min": 145000, "salary_max": 195000, "skills": ["Python", "TensorFlow", "Machine Learning", "AWS", "Docker"]},
  {"title": "Research Scientist", "company": "Google", "location": "New York, NY", "remote": "onsite", "salary_min": 180000, "salary_max": 250000, "skills": ["Python", "PyTorch", "Research", "Mathematics", "Deep Learning"]},
  {"title": "Data Analyst", "company": "Figma", "location": "Remote", "remote": "remote", "salary_min": 95000, "salary_max": 130000, "skills": ["SQL", "Python", "Tableau", "Product Analytics", "Statistics"]},
  {"title": "Data Scientist", "company": "Twitter", "location": "Remote", "remote": "remote", "salary_min": 125000, "salary_max": 165000, "skills": ["Python", "SQL", "Machine Learning", "Scala", "Spark"]}
]

def load_jobs(api_jobs=None):
    if api_jobs:
        return pd.DataFrame(api_jobs)
    return pd.DataFrame(SAMPLE_JOBS)

def get_top_skills(df, top_n=15):
    all_skills = []
    for skills in df["skills"]:
        if isinstance(skills, list):
            all_skills.extend(skills)
        elif isinstance(skills, str):
            all_skills.extend([s.strip() for s in skills.split(",")])
    counts = Counter(all_skills).most_common(top_n)
    return [{"skill": s, "count": c} for s, c in counts]

def get_top_companies(df, top_n=10):
    counts = df["company"].value_counts().head(top_n)
    return [{"company": c, "count": int(n)} for c, n in counts.items()]

def get_remote_breakdown(df):
    counts = df["remote"].value_counts()
    return [{"type": t, "count": int(c)} for t, c in counts.items()]

def get_top_locations(df, top_n=10):
    counts = df["location"].value_counts().head(top_n)
    return [{"location": l, "count": int(c)} for l, c in counts.items()]

def get_top_titles(df, top_n=10):
    counts = df["title"].value_counts().head(top_n)
    return [{"title": t, "count": int(c)} for t, c in counts.items()]

def get_salary_distribution(df):
    df = df.copy()
    df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")
    df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")
    df["salary_avg"] = (df["salary_min"] + df["salary_max"]) / 2
    df_clean = df.dropna(subset=["salary_avg"])
    result = df_clean.groupby("title")["salary_avg"].mean().sort_values(ascending=False).head(10).reset_index()
    return [{"title": row["title"], "avg_salary": round(row["salary_avg"] / 1000, 1)} for _, row in result.iterrows()]

def get_summary_stats(df):
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
