---
title: Job Market Dashboard
emoji: 📊
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
---

# Job Market Analytics Dashboard

An interactive dashboard that analyzes job market trends for data science and ML roles — top skills, salaries, hiring companies, remote breakdown, and more.

## Live Demo
🚀 [Try it on Hugging Face Spaces](https://huggingface.co/spaces/adithyakunapareddy/job-market-dashboard)

## Features
- **Top in-demand skills** — bar chart of most requested technologies
- **Salary by role** — average compensation per job title
- **Remote vs Onsite vs Hybrid** — donut chart breakdown
- **Top hiring companies** — ranked by job count
- **Top locations** — where the jobs are
- **Search by role & location** — filter the analytics in real time

## Tech Stack
- **Backend:** Python · Flask · Pandas · NumPy
- **Frontend:** React · Vite · Custom SVG charts
- **Data:** JSearch API (RapidAPI) · Sample dataset included
- **Deployment:** Hugging Face Spaces · Docker

## Run locally

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3002

### Optional: Enable live job data
Get a free API key from [RapidAPI JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) and set:
```bash
export RAPIDAPI_KEY=your_key_here
```
