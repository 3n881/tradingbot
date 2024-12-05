from fastapi import APIRouter, HTTPException
from app.services.sentiment_service import SentimentService

router = APIRouter()
sentiment_service = SentimentService()

@router.get("/twitter")
def get_twitter_sentiment(query: str, count: int = 10):
    try:
        data = sentiment_service.get_twitter_sentiment(query, count)
        return {"query": query, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Twitter sentiment: {str(e)}")

@router.get("/reddit")
def get_reddit_sentiment(subreddit: str, limit: int = 10):
    try:
        data = sentiment_service.get_reddit_sentiment(subreddit, limit)
        return {"subreddit": subreddit, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Reddit sentiment: {str(e)}")
