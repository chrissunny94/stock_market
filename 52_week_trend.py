import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz

# Set timezone-aware current time
today = datetime.now(pytz.timezone("Asia/Kolkata"))
start_5y = today - timedelta(days=5*365)

ticker = 'SBICARD.NS'
stock = yf.Ticker(ticker)
data = stock.history(start=start_5y.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))

# Slice last 1 year of data
data_1y = data[data.index >= (today - timedelta(weeks=52))]
low_52w = data_1y['Low'].min()
high_52w = data_1y['High'].max()

# Resample to yearly highs and lows
yearly_high = data['High'].resample('Y').max()
yearly_low = data['Low'].resample('Y').min()

# Plotting
plt.figure(figsize=(14, 6))
plt.plot(data['Close'], label='Close Price', linewidth=1)
plt.axhline(low_52w, color='green', linestyle='--', label=f'52W Low: ₹{low_52w:.2f}')
plt.axhline(high_52w, color='red', linestyle='--', label=f'52W High: ₹{high_52w:.2f}')
plt.scatter(yearly_high.index, yearly_high, color='red', label='Yearly Highs')
plt.scatter(yearly_low.index, yearly_low, color='green', label='Yearly Lows')

plt.title("SBICARD.NS - 5 Year Trend with 52W High/Low")
plt.xlabel("Year")
plt.ylabel("Price (INR)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
