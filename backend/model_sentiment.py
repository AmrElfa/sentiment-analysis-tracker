from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

def analyze_reviews(reviews):
    analyzer = SentimentIntensityAnalyzer()
    total = 0
    pos = 0
    neu = 0
    neg = 0
    cnt = 0
    for txt in reviews:
        score = analyzer.polarity_scores(txt)
        total += score['compound']
        pos += score['pos']
        neu += score['neu']
        neg += score['neg']
        cnt += 1
    overall = (total/cnt + 1)*5
    # scale 1-10
    return {
      "overall": round(overall,2),
      "positive": round(pos/cnt,2),
      "neutral": round(neu/cnt,2),
      "negative": round(neg/cnt,2)
    }
