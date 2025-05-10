import yfinance as yf
import numpy as np
import pandas as pd
from scipy.fft import fft
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import pytz

# Set up parameters
reference_ticker = 'SBICARD.NS'
compare_tickers = ['HDFCBANK.NS', 'ICICIBANK.NS', 'AXISBANK.NS', 'BAJFINANCE.NS', 
                   'KOTAKBANK.NS', 'IDFCFIRSTB.NS', 'SBIN.NS', 'RELIANCE.NS', 'INFY.NS']
num_days = 252  # ~1 year

# Time window
end = datetime.now(pytz.timezone("Asia/Kolkata"))
start = end - timedelta(days=num_days)

# Helper: Get normalized closing price
def get_normalized_close_fft(ticker):
    data = yf.download(ticker, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))
    if data.empty:
        return None
    close = data['Close'].ffill()  # Forward fill missing data
    norm_close = (close - close.mean()) / close.std()  # Normalize the closing prices
    fft_vals = np.abs(fft(norm_close.to_numpy()))[:50]  # Perform FFT and keep top 50 frequencies
    return fft_vals

# Get FFT of reference stock
ref_fft = get_normalized_close_fft(reference_ticker)

# Compare with other stocks
similarities = []
for ticker in compare_tickers:
    cmp_fft = get_normalized_close_fft(ticker)
    if cmp_fft is not None:
        # Reshape to 2D array (1, -1) for cosine_similarity
        score = cosine_similarity(ref_fft.reshape(1, -1), cmp_fft.reshape(1, -1))[0][0]
        similarities.append((ticker, score))

# Sort by similarity
similarities.sort(key=lambda x: x[1], reverse=True)

# Show results
df_result = pd.DataFrame(similarities, columns=["Ticker", "Similarity"])
print(df_result)
