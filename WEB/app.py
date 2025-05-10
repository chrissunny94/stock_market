from comparison_plot import *
from common import *
app = Flask(__name__)






@app.route("/", methods=["GET", "POST"])
def index():
    similarities = []
    selected_stock = None
    comparison_plot_url = None
    ref_candle_url = None
    cmp_candle_url = None
    
    if request.method == "POST":
        selected_stock = request.form.get('stock')
        
        # Calculate similarities
        ref_data, _, ref_fft_vals = get_stock_data(reference_ticker)
        if ref_data is not None:
            for ticker in compare_tickers:
                cmp_data, _, cmp_fft_vals = get_stock_data(ticker)
                if cmp_data is not None:
                    score = cosine_similarity(ref_fft_vals.reshape(1, -1), cmp_fft_vals.reshape(1, -1))[0][0]
                    similarities.append((ticker, score))
            similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Generate comparison plot
        if selected_stock:
            comparison_plot_url, ref_candle_url, cmp_candle_url = generate_comparison_plots(selected_stock)
    
    return render_template("index.html",
                         similarities=similarities,
                         compare_tickers=compare_tickers,
                         selected_stock=selected_stock,
                         comparison_plot_url=comparison_plot_url,
                         ref_candle_url=ref_candle_url,
                         cmp_candle_url=cmp_candle_url,
                         reference_ticker=reference_ticker)

@app.route('/static/plots/<filename>')
def plot(filename):
    return send_from_directory(plot_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)