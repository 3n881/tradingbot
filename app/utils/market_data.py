from alpha_vantage.timeseries import TimeSeries
from app.config import ALPHA_VANTAGE_API_KEY

# Initialize Alpha Vantage API
ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY)

def get_stock_data(symbol: str, interval: str = "1min"):
    """
    Fetch real-time stock data for the given symbol.
    Args:
        symbol (str): Stock symbol (e.g., AAPL).
        interval (str): Time interval (e.g., 1min, 5min, daily).
    Returns:
        dict: Stock data or an error message.
    """
    try:
        data, _ = ts.get_intraday(symbol=symbol, interval=interval, outputsize="compact")
        return {"symbol": symbol, "interval": interval, "data": data}
    except Exception as e:
        return {"error": str(e)}
