from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://amr@localhost/sentimentdb")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class SentimentRecord(Base):
    __tablename__ = "sentiment_records"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String)
    score = Column(Float)
    positive = Column(Float)
    neutral = Column(Float)
    negative = Column(Float)
    timestamp = Column(DateTime)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_sentiment(record):
    db = SessionLocal()
    db.add(record)
    db.commit()
    db.close()

def get_sentiment_history(company, limit=10):
    db = SessionLocal()
    results = db.query(SentimentRecord)\
                .filter(SentimentRecord.company.ilike(company))\
                .order_by(SentimentRecord.timestamp.asc())\
                .limit(limit).all()
    db.close()
    return results
