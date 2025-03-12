import praw
import os
import re
from summarizer import summarize_text

def clean_review(text):
    words = text.split()
    if len(words) > 30:
        try:
            return summarize_text(text)
        except Exception as e:
            print("Summarizer error on review:", e)
            return text
    return text

def get_reddit_reviews(comp):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="sentiment_app"
    )
    posts = []
    query = f'title:"{comp}" AND selftext:"{comp}" AND review'
    try:
        for submission in reddit.subreddit("all").search(query, sort="new", time_filter="year", limit=20):
            text = (submission.title + " " + submission.selftext).strip()
            occurrences = len(re.findall(re.escape(comp), text, flags=re.IGNORECASE))
            if occurrences < 2:
                continue
            cleaned = clean_review(text)
            posts.append(cleaned)
    except Exception as e:
        print("Error:", e)
    return posts
