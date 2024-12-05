from fastapi import APIRouter, HTTPException
from app.services.market_data import MarketDataService

router = APIRouter()
market_service = MarketDataService()

@router.get("/intraday/{symbol}")
def get_intraday_data(symbol: str, interval: str = "1min"):
    try:
        data = market_service.get_intraday_data(symbol, interval)
        return {"symbol": symbol, "interval": interval, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching intraday data: {str(e)}")

@router.get("/historical/{symbol}")
def get_historical_data(symbol: str, outputsize: str = "full"):
    try:
        data = market_service.get_historical_data(symbol, outputsize)
        return {"symbol": symbol, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical data: {str(e)}")
