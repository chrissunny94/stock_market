import yfinance as yf
from datetime import datetime, timedelta

def get_52_week_range(ticker):
    # Define the date range (past 52 weeks)
    end_date = datetime.today()
    start_date = end_date - timedelta(weeks=52)

    # Fetch historical data
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

    if hist.empty:
        print(f"No data found for {ticker}")
        return None

    low_52w = hist['Low'].min()
    high_52w = hist['High'].max()

    return (ticker, low_52w, high_52w)

# List of stock tickers (NSE or global - use appropriate suffix for NSE like '.NS')
tickers = ['SBICARD.NS', 'RELIANCE.NS', 'TCS.NS', 'AAPL', 'GOOGL']

# Fetch and print 52-week range for each stock
print(f"{'Ticker':<10} {'52W Low':>12} {'52W High':>12}")
print("="*36)
for ticker in tickers:
    result = get_52_week_range(ticker)
    if result:
        print(f"{result[0]:<10} {result[1]:>12.2f} {result[2]:>12.2f}")

