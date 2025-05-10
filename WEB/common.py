import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.fft import fft
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import pytz
from flask import Flask, render_template, request, send_from_directory
import os

# Parameters
reference_ticker = 'SBICARD.NS'
compare_tickers = ['HDFCBANK.NS', 'ICICIBANK.NS', 'AXISBANK.NS', 'BAJFINANCE.NS', 
                  'KOTAKBANK.NS', 'IDFCFIRSTB.NS', 'SBIN.NS', 'RELIANCE.NS', 'INFY.NS', 
                  'JMFINANCIL.NS', 'INDIGRID.NS']


num_days = 1000

# Time window
end = datetime.now(pytz.timezone("Asia/Kolkata"))
start = end - timedelta(days=num_days)

# Plot directories
plot_dir = 'static/plots'
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)