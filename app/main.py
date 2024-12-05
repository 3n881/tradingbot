
from fastapi import FastAPI
from app.routers import auth, strategies
from app.routers import market
from app.routers import sentiment
from app.routers import bots
from app.routers import analytics
from app.routers import dashboard
import os
from sqlalchemy import create_engine


app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mahadevs123@db:5432/ai_trading")
engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("Database connection successful!")
    connection.close()
except Exception as e:
    print(f"Database connection failed: {e}")

# Include routers with prefixes and tags
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(bots.router, prefix="/bots", tags=["Trading Bots"])
app.include_router(bots.router, prefix="/bots", tags=["bots"])
app.include_router(strategies.router, prefix="/strategies", tags=["Strategies"])
app.include_router(market.router, prefix="/market", tags=["Market Data"])
app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment Analysis"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])


@app.get("/")
@app.get("/routes")
def list_routes():
    return [{"path": route.path, "name": route.name} for route in app.router.routes]

def read_root():
    return {"message": "Welcome to the AI Trading Platform",
             "version": "0.1.0",
        "available_services": [
            "/market",
            "/bots",
            "/strategies"
        ]}