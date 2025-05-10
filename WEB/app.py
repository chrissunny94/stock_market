import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.fft import fft
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import pytz
from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Parameters
reference_ticker = 'SBICARD.NS'
compare_tickers = ['HDFCBANK.NS', 'ICICIBANK.NS', 'AXISBANK.NS', 'BAJFINANCE.NS', 
                  'KOTAKBANK.NS', 'IDFCFIRSTB.NS', 'SBIN.NS', 'RELIANCE.NS', 'INFY.NS', 
                  'JMFINANCIL.NS', 'INDIGRID.NS']
num_days = 2000

# Time window
end = datetime.now(pytz.timezone("Asia/Kolkata"))
start = end - timedelta(days=num_days)

# Plot directories
plot_dir = 'static/plots'
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

def get_stock_data(ticker):
    data = yf.download(ticker, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))
    if data.empty:
        print(f"Data for {ticker} is empty.")
        return None
    close = data['Close'].ffill()
    norm_close = (close - close.mean()) / close.std()
    fft_vals = np.abs(fft(norm_close.to_numpy()))[:50]
    return close, norm_close, fft_vals

def generate_comparison_plots(selected_ticker):
    # Get data for both stocks
    ref_close, ref_norm, _ = get_stock_data(reference_ticker)
    cmp_close, cmp_norm, _ = get_stock_data(selected_ticker)
    
    if ref_close is None or cmp_close is None:
        return None, None
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: Normalized price comparison
    ref_norm.plot(ax=ax1, label=reference_ticker, color='blue')
    cmp_norm.plot(ax=ax1, label=selected_ticker, color='orange')
    ax1.set_title(f"Normalized Price Comparison: {reference_ticker} vs {selected_ticker}")
    ax1.set_ylabel("Normalized Price")
    ax1.legend()
    ax1.grid(True)
    
    # Plot 2: Actual price comparison (scaled)
    (ref_close/ref_close.iloc[0]).plot(ax=ax2, label=reference_ticker, color='blue')  # Base-100 scaled
    (cmp_close/cmp_close.iloc[0]).plot(ax=ax2, label=selected_ticker, color='orange')
    ax2.set_title(f"Actual Price Trend (Base-100 Scaled)")
    ax2.set_ylabel("Price (Base 100)")
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    
    # Save plot
    plot_path = os.path.join(plot_dir, f"comparison_{selected_ticker}.png")
    fig.savefig(plot_path)
    plt.close(fig)
    
    return plot_path

@app.route("/", methods=["GET", "POST"])
def index():
    similarities = []
    selected_stock = None
    comparison_plot_url = None
    
    if request.method == "POST":
        selected_stock = request.form.get('stock')
        
        # Calculate similarities
        ref_data = get_stock_data(reference_ticker)
        if ref_data is not None:
            _, _, ref_fft_vals = ref_data
            for ticker in compare_tickers:
                cmp_data = get_stock_data(ticker)
                if cmp_data is not None:
                    _, _, cmp_fft_vals = cmp_data
                    score = cosine_similarity(ref_fft_vals.reshape(1, -1), cmp_fft_vals.reshape(1, -1))[0][0]
                    similarities.append((ticker, score))
            similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Generate comparison plot
        if selected_stock:
            comparison_plot_url = generate_comparison_plots(selected_stock)
    
    return render_template("index.html",
                         similarities=similarities,
                         compare_tickers=compare_tickers,
                         selected_stock=selected_stock,
                         comparison_plot_url=comparison_plot_url,
                         reference_ticker=reference_ticker)

@app.route('/static/plots/<filename>')
def plot(filename):
    return send_from_directory(plot_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)