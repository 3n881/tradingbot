from alpha_vantage.timeseries import TimeSeries
from app.config import ALPHA_VANTAGE_API_KEY

class MarketDataService:
    def __init__(self):
        self.ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format="json")

    def get_intraday_data(self, symbol: str, interval: str = "1min"):
        """Fetch real-time intraday data for a given stock symbol."""
        data, _ = self.ts.get_intraday(symbol=symbol, interval=interval, outputsize="compact")
        return data

    def get_historical_data(self, symbol: str, outputsize: str = "full"):
        """Fetch historical daily data for a given stock symbol."""
        data, _ = self.ts.get_daily(symbol=symbol, outputsize=outputsize)
        return data

    def get_company_overview(self, symbol: str):
        """Fetch company overview details."""
        data, _ = self.ts.get_quote_endpoint(symbol)
        return data
