import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf
from scipy.fft import fft
from datetime import datetime, timedelta

# Configuration
plot_dir = 'static/plots'
os.makedirs(plot_dir, exist_ok=True)
reference_ticker = '^NSEI'  # Nifty 50 as reference

# Date range - 1 year of data
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

def clean_dataframe(df, ticker):
    """
    Convert MultiIndex DataFrame to single index and ensure proper column names
    Returns DataFrame with standard OHLC column names
    """
    # Handle MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = ['_'.join(col).replace(f'.{ticker.split(".")[-1]}','') 
                     for col in df.columns]
    
    # Standardize column names
    column_map = {
        'Open': [col for col in df.columns if 'Open' in col],
        'High': [col for col in df.columns if 'High' in col],
        'Low': [col for col in df.columns if 'Low' in col],
        'Close': [col for col in df.columns if 'Close' in col],
        'Volume': [col for col in df.columns if 'Volume' in col]
    }
    
    clean_df = pd.DataFrame()
    for standard_name, possible_names in column_map.items():
        if possible_names:
            clean_df[standard_name] = df[possible_names[0]]
    
    return clean_df

def generate_candlestick_plot(ticker, data):
    """Generate candlestick plot for given ticker data"""
    try:
        # Prepare data
        plot_data = data[['Open', 'High', 'Low', 'Close']].copy()
        plot_data = plot_data.apply(pd.to_numeric, errors='coerce').dropna()
        
        if plot_data.empty:
            raise ValueError("No valid data to plot after cleaning")
        
        # Generate plot
        fig, ax = plt.subplots(figsize=(12, 6))
        mpf.plot(plot_data,
                 type='candle',
                 style='charles',
                 title=f'{ticker} Candlestick (Last 100 Days)',
                 ylabel='Price (₹)',
                 ax=ax,
                 show_nontrading=True)
        
        plot_path = os.path.join(plot_dir, f"candle_{ticker.replace('.','_')}.png")
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()
        return plot_path
    
    except Exception as e:
        print(f"Failed to generate candlestick for {ticker}: {str(e)}")
        return None

def get_stock_data(ticker):
    """Fetch and process stock data"""
    try:
        print(f"Fetching data for {ticker}...")
        data = yf.download(ticker, 
                          start=start_date.strftime('%Y-%m-%d'),
                          end=end_date.strftime('%Y-%m-%d'),
                          progress=False)
        
        if data.empty:
            print(f"No data for {ticker}")
            return None, None, None
        
        # Clean and standardize dataframe
        clean_data = clean_dataframe(data, ticker)
        
        # Ensure numeric values
        numeric_cols = ['Open', 'High', 'Low', 'Close']
        clean_data[numeric_cols] = clean_data[numeric_cols].apply(
            pd.to_numeric, errors='coerce')
        
        # Handle missing data
        clean_data = clean_data.ffill().bfill().dropna()
        
        # Normalize close prices
        close = clean_data['Close']
        norm_close = (close - close.mean()) / close.std()
        
        # FFT analysis
        fft_vals = np.abs(fft(norm_close.to_numpy()))[:50]
        
        return clean_data, norm_close, fft_vals
    
    except Exception as e:
        print(f"Error processing {ticker}: {str(e)}")
        return None, None, None

def generate_comparison_plots(selected_ticker):
    """Main function to generate all comparison plots"""
    print(f"\nGenerating plots for {selected_ticker} vs {reference_ticker}")
    
    # Get data for both stocks
    ref_data, ref_norm, _ = get_stock_data(reference_ticker)
    cmp_data, cmp_norm, _ = get_stock_data(selected_ticker)
    
    if ref_data is None or cmp_data is None:
        print("Missing data - cannot generate plots")
        return None, None, None
    
    # Prepare last 100 days data
    ref_data_100 = ref_data.iloc[-100:].copy()
    cmp_data_100 = cmp_data.iloc[-100:].copy()
    
    # Create comparison figure
    fig = plt.figure(figsize=(12, 18))
    
    # Plot 1: Normalized price comparison
    ax1 = plt.subplot(3, 1, 1)
    ref_norm.plot(ax=ax1, label=reference_ticker, color='blue')
    cmp_norm.plot(ax=ax1, label=selected_ticker, color='orange')
    ax1.set_title("Normalized Price Comparison")
    ax1.set_ylabel("Normalized Price")
    ax1.legend()
    ax1.grid(True)
    
    # Plot 2: Actual price comparison
    ax2 = plt.subplot(3, 1, 2)
    ref_data['Close'].plot(ax=ax2, label=reference_ticker, color='blue')
    cmp_data['Close'].plot(ax=ax2, label=selected_ticker, color='orange')
    ax2.set_title("Actual Price Trend")
    ax2.set_ylabel("Price (₹)")
    ax2.legend()
    ax2.grid(True)
    
    # Plot 3: Candlestick comparison
    ax3 = plt.subplot(3, 1, 3)
    
    try:
        # Plot reference candlestick
        mpf.plot(ref_data_100[['Open', 'High', 'Low', 'Close']],
                type='candle',
                style='charles',
                ax=ax3)
        
        # Plot comparison candlestick
        mpf.plot(cmp_data_100[['Open', 'High', 'Low', 'Close']],
                type='candle',
                style='binance',
                ax=ax3)
        
        ax3.set_title("Candlestick Comparison (Last 100 Days)")
    except Exception as e:
        print(f"Failed to plot candlesticks: {str(e)}")
        plt.close(fig)
        return None, None, None
    
    plt.tight_layout()
    
    # Save comparison plot
    comparison_path = os.path.join(plot_dir, f"compare_{selected_ticker.replace('.','_')}.png")
    fig.savefig(comparison_path, bbox_inches='tight')
    plt.close(fig)
    
    # Generate individual candlestick plots
    ref_candle_path = generate_candlestick_plot(reference_ticker, ref_data_100)
    cmp_candle_path = generate_candlestick_plot(selected_ticker, cmp_data_100)
    
    return comparison_path, ref_candle_path, cmp_candle_path