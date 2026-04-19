import os
import requests

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")

def fetch_jobs(query="data scientist", location="United States", num_pages=1):
    """
    Fetch jobs from JSearch API via RapidAPI.
    Falls back to None if no API key configured.
    """
    if not RAPIDAPI_KEY:
        return None  # Will use sample data

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    all_jobs = []
    for page in range(1, num_pages + 1):
        params = {
            "query": f"{query} in {location}",
            "page": str(page),
            "num_pages": "1",
            "date_posted": "month"
        }
        try:
            res = requests.get(url, headers=headers, params=params, timeout=15)
            data = res.json()
            jobs = data.get("data", [])
            for job in jobs:
                all_jobs.append({
                    "title": job.get("job_title", ""),
                    "company": job.get("employer_name", ""),
                    "location": f"{job.get('job_city', '')}, {job.get('job_state', '')}".strip(", "),
                    "remote": "remote" if job.get("job_is_remote") else "onsite",
                    "salary_min": job.get("job_min_salary") or 0,
                    "salary_max": job.get("job_max_salary") or 0,
                    "skills": job.get("job_required_skills") or [],
                    "posted_date": job.get("job_posted_at_datetime_utc", "")[:10]
                })
        except Exception:
            continue

    return all_jobs if all_jobs else None
