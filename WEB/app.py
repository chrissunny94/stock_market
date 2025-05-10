import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import matplotlib.pyplot as plt

import yfinance as yf
import numpy as np
import pandas as pd
from scipy.fft import fft
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import pytz
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Set up parameters
reference_ticker = 'SBICARD.NS'
compare_tickers = ['HDFCBANK.NS', 'ICICIBANK.NS', 'AXISBANK.NS', 'BAJFINANCE.NS', 
                   'KOTAKBANK.NS', 'IDFCFIRSTB.NS', 'SBIN.NS', 'RELIANCE.NS', 'INFY.NS','JMFINANCIL.NS']
num_days = 1000  # ~1 year

# Time window
end = datetime.now(pytz.timezone("Asia/Kolkata"))
start = end - timedelta(days=num_days)

# Path to save plot
plot_dir = 'static/plots'
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# Helper: Get normalized closing price and its FFT
def get_normalized_close_fft(ticker):
    data = yf.download(ticker, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))
    if data.empty:
        print(f"Data for {ticker} is empty.")
        return None
    close = data['Close'].ffill()
    norm_close = (close - close.mean()) / close.std()
    fft_vals = np.abs(fft(norm_close.to_numpy()))[:50]
    return norm_close, fft_vals

# Helper: Generate plot of stock data
def generate_plot(ticker):
    norm_close, _ = get_normalized_close_fft(ticker)
    if norm_close is not None:
        fig, ax = plt.subplots(figsize=(10, 6))
        norm_close.plot(ax=ax)
        ax.set_title(f"Normalized Closing Price for {ticker}")
        plot_path = os.path.join(plot_dir, f"{ticker}_plot.png")
        fig.savefig(plot_path)
        plt.close(fig)
        return plot_path
    return None

# Route for displaying the stock list and results
@app.route("/", methods=["GET", "POST"])
def index():
    similarities = []
    selected_stock = None
    plot_url = None
    if request.method == "POST":
        selected_stock = request.form.get('stock')
        ref_fft = get_normalized_close_fft(reference_ticker)
        if ref_fft is not None:
            _, ref_fft_vals = ref_fft
            for ticker in compare_tickers:
                cmp_fft = get_normalized_close_fft(ticker)
                if cmp_fft is not None:
                    _, cmp_fft_vals = cmp_fft
                    score = cosine_similarity(ref_fft_vals.reshape(1, -1), cmp_fft_vals.reshape(1, -1))[0][0]
                    similarities.append((ticker, score))
            similarities.sort(key=lambda x: x[1], reverse=True)

        # Generate plot for the selected stock
        if selected_stock:
            plot_url = generate_plot(selected_stock)

    return render_template("index.html", 
                         similarities=similarities, 
                         compare_tickers=compare_tickers, 
                         selected_stock=selected_stock, 
                         plot_url=plot_url,
                         reference_ticker=reference_ticker)

# Route to serve the plot image
@app.route('/static/plots/<filename>')
def plot(filename):
    return send_from_directory(plot_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)