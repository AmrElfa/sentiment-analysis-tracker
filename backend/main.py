from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_reddit_reviews
from model_sentiment import analyze_reviews
from database import init_db, save_sentiment, get_sentiment_history, SentimentRecord
from summarizer import summarize_text
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/analyze")
def analyze(company: str):
    if not company:
        raise HTTPException(status_code=400, detail="Company name required")
    
    reviews = get_reddit_reviews(company)
    if not reviews:
        return {"error": "No reviews found"}
    
    sentiment_data = analyze_reviews(reviews)
    
    combined_text = (
        "Summarize the following reviews for " + company +
        " focusing on the key words and opinions that explain why the overall sentiment score is " +
        str(sentiment_data['overall']) +
        ". Only mention points directly related to " + company + ". Reviews: " +
        " ".join(reviews)
    )
    try:
        summary = summarize_text(combined_text)
    except Exception as e:
        print("Summarizer error:", e)
        summary = "Summary could not be generated."
    
    new_record = SentimentRecord(
        company=company,
        score=sentiment_data["overall"],
        positive=sentiment_data["positive"],
        neutral=sentiment_data["neutral"],
        negative=sentiment_data["negative"],
        timestamp=datetime.datetime.utcnow()
    )
    save_sentiment(new_record)

    return {
        "overall": sentiment_data["overall"],
        "positive": sentiment_data["positive"],
        "neutral": sentiment_data["neutral"],
        "negative": sentiment_data["negative"],
        "reviews": reviews,
        "summary": summary
    }

@app.get("/history")
def history(company: str):
    records = get_sentiment_history(company)
    data_list = []
    for r in records:
        data_list.append({
            "score": r.score,
            "positive": r.positive,
            "neutral": r.neutral,
            "negative": r.negative,
            "timestamp": r.timestamp.isoformat()
        })
    return {
        "company": company,
        "history": data_list
    }
