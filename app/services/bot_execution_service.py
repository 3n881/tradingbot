from app.services.market_data import MarketDataService
from app.services.sentiment_service import SentimentService

class BotExecutionService:
    def __init__(self):
        self.market_service = MarketDataService()
        self.sentiment_service = SentimentService()

    def execute_bot(self, bot):
        stock_symbol = bot["configuration"]["stock_symbol"]
        sentiment_query = bot["configuration"]["sentiment_query"]

        # Fetch market data
        market_data = self.market_service.get_intraday_data(stock_symbol, "1min")

        # Fetch sentiment analysis
        sentiment_data = self.sentiment_service.get_twitter_sentiment(sentiment_query, count=5)

        # Analyze market and sentiment data
        strategy = bot["strategy"]
        configuration = bot["configuration"]
        decision = self.apply_strategy(strategy, market_data, sentiment_data, configuration)

        return decision

    def apply_strategy(self, strategy, market_data, sentiment_data, configuration):
        """Apply the bot's strategy to market and sentiment data."""
        last_price = float(list(market_data.values())[0]["4. close"])
        sentiment_score = sum(item["sentiment"]["score"] for item in sentiment_data) / len(sentiment_data)

        if strategy == "RSI Strategy":
            rsi_threshold = configuration.get("rsi_threshold", 30)
            sentiment_boost = configuration.get("sentiment_boost", 0.5)

            if sentiment_score > sentiment_boost and last_price < rsi_threshold:
                return "BUY"
            elif sentiment_score < -sentiment_boost and last_price > rsi_threshold:
                return "SELL"

        elif strategy == "Moving Average":
            short_ma = configuration.get("short_ma", 5)
            long_ma = configuration.get("long_ma", 20)
            prices = [float(data["4. close"]) for data in list(market_data.values())[:long_ma]]
            short_avg = sum(prices[:short_ma]) / short_ma
            long_avg = sum(prices) / long_ma

            if short_avg > long_avg:
                return "BUY"
            elif short_avg < long_avg:
                return "SELL"

        elif strategy == "Momentum":
            momentum_threshold = configuration.get("momentum_threshold", 0.1)
            momentum = (last_price - float(list(market_data.values())[1]["4. close"])) / last_price

            if momentum > momentum_threshold:
                return "BUY"
            elif momentum < -momentum_threshold:
                return "SELL"

        return "HOLD"

