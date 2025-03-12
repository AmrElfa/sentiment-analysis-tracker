# Sentiment Analysis & Trend Tracking Platform

A simple platform that scrapes real-time product or company reviews, analyzes sentiment using NLP, and visualizes trends in an interactive dashboard.

## Overview
- **Scraping**: Fetches recent Reddit posts using PRAW.
- **NLP**: Uses VADER (or similar) to score reviews as positive, neutral, or negative.
- **Storage**: Saves data in PostgreSQL to track historical sentiment.
- **Frontend**: React app with Chart.js for bar/line charts and a neat UI.

## How It Works
1. **Backend** (FastAPI + Python)
   - Endpoints to scrape data and perform sentiment analysis.
   - Stores aggregated scores (overall, positive, neutral, negative) in PostgreSQL.
2. **Frontend** (React)
   - Input box to enter a company or product name.
   - Displays sentiment scores and historical charts.
3. **Trend Tracking**
   - Each time you analyze the same company, new data points get added.
   - The line chart shows how sentiment changes over time.

## Setup
1. **Backend**  
   - `cd backend`  
   - `python3 -m venv venv` and `source venv/bin/activate`  
   - `pip install -r requirements.txt`  
   - Set `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and `DATABASE_URL` as environment variables.  
   - Run with `uvicorn main:app --reload`.

2. **Frontend**  
   - `cd frontend`  
   - `npm install`  
   - `npm start`  
   - Go to `http://localhost:3000`.

3. **Usage**  
   - Type a company/product name and click “Analyze.”
   - See the sentiment breakdown, overall score, and trend chart if multiple entries exist.

## Notes
- You can tweak the number of Reddit posts in `scraper.py`.
- Historical data grows each time you re-analyze the same term.
- If you need deeper summaries, you can integrate a more advanced model (like BART).
