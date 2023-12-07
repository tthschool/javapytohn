import yfinance as yf
def get_stock_price(symbol: str) -> float:
    stock = yf.Ticker(symbol)
    price = stock.history(period="1mo")['Close'].iloc[-1]
    return price
print(get_stock_price("AAPL"))