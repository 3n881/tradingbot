import tweepy
import praw
from transformers import pipeline
from app.config import (
    TWITTER_API_KEY, TWITTER_API_SECRET, 
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET,
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
)

# Initialize Sentiment Analysis Model
sentiment_model = pipeline("sentiment-analysis")

# Twitter API Setup
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)

# Reddit API Setup
reddit_api = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

class SentimentService:
    def get_twitter_sentiment(self, query: str, count: int = 10):
        """Fetch and analyze sentiment of tweets."""
        tweets = twitter_api.search_tweets(q=query, count=count, lang="en")
        results = []
        for tweet in tweets:
            sentiment = sentiment_model(tweet.text)[0]
            results.append({"text": tweet.text, "sentiment": sentiment})
        return results

    def get_reddit_sentiment(self, subreddit: str, limit: int = 10):
        """Fetch and analyze sentiment of Reddit posts."""
        posts = reddit_api.subreddit(subreddit).hot(limit=limit)
        results = []
        for post in posts:
            sentiment = sentiment_model(post.title)[0]
            results.append({"title": post.title, "sentiment": sentiment})
        return results
