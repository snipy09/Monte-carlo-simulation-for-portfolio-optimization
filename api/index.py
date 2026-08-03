"""
Vercel Serverless API Endpoint for Monte Carlo Portfolio Optimization Engine
"""

from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Any

from simulation import MonteCarloSimulator
from analytics import PortfolioAnalytics
import config

app = Flask(__name__)

def sanitize_json(obj: Any) -> Any:
    """Recursively convert NumPy data types to Python native types for JSON serialization."""
    if isinstance(obj, dict):
        return {k: sanitize_json(v) for k, v in obj.items()}
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [sanitize_json(v) for v in obj]
    elif isinstance(obj, np.ndarray):
        return [sanitize_json(v) for v in obj.tolist()]
    elif isinstance(obj, (np.float32, np.float64, np.floating)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64, np.integer)):
        return int(obj)
    elif isinstance(obj, (np.bool_)):
        return bool(obj)
    else:
        return obj

def fetch_data(stocks: List[str], years: int = 3) -> pd.DataFrame:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    
    raw_data: Any = yf.download(stocks, start=start_date, end=end_date, progress=False)
    if raw_data is None or len(raw_data) == 0:
        return pd.DataFrame()
        
    data = raw_data
    if isinstance(data.columns, pd.MultiIndex):
        level_0 = data.columns.get_level_values(0)
        if "Adj Close" in level_0:
            data = data["Adj Close"]
        elif "Close" in level_0:
            data = data["Close"]
        else:
            data = data[level_0[0]]
            
    if isinstance(data, pd.Series):
        data = data.to_frame()
        
    df = pd.DataFrame(data).dropna(axis=1, how='all').ffill().bfill()
    return df

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'online', 'system': 'Monte Carlo Portfolio Optimizer v2.0', 'default_stocks': config.DEFAULT_STOCKS})

@app.route('/api/simulate', methods=['POST', 'GET'])
def simulate():
    try:
        if request.method == 'POST':
            req = request.get_json(force=True) or {}
            stocks = req.get('stocks', config.DEFAULT_STOCKS)
            num_sims = int(req.get('num_simulations', 5000))
            min_w = float(req.get('min_weight', 0.0))
            max_w = float(req.get('max_weight', 0.35))
            rf = float(req.get('risk_free_rate', 0.045))
        else:
            stocks = request.args.get('stocks', 'AAPL,MSFT,GOOGL,AMZN,NVDA').split(',')
            num_sims = int(request.args.get('num_simulations', 5000))
            min_w = float(request.args.get('min_weight', 0.0))
            max_w = float(request.args.get('max_weight', 0.35))
            rf = float(request.args.get('risk_free_rate', 0.045))

        stocks = [s.strip().upper() for s in stocks if s.strip()]
        if len(stocks) < 2:
            return jsonify({'error': 'Please select at least 2 stock tickers'}), 400

        # Fetch data
        price_df = fetch_data(stocks)
        if price_df.empty or len(price_df.columns) < 2:
            return jsonify({'error': 'Failed to fetch sufficient stock data'}), 400

        retained_stocks = [str(c) for c in price_df.columns]
        daily_returns = price_df.pct_change().dropna()
        
        mean_returns = daily_returns.mean().to_numpy() * float(config.TRADING_DAYS_PER_YEAR)
        cov_matrix = daily_returns.cov().to_numpy() * float(config.TRADING_DAYS_PER_YEAR)

        # Run vectorized simulation
        simulator = MonteCarloSimulator(
            mean_returns=mean_returns,
            cov_matrix=cov_matrix,
            daily_returns=daily_returns,
            risk_free_rate=rf,
            use_ledoit_wolf=True,
            seed=42
        )
        
        df_results, weights_matrix = simulator.run_simulation(
            num_sims=num_sims,
            min_w=min_w,
            max_w=max_w
        )

        analytics = PortfolioAnalytics(
            results=df_results,
            weights_array=weights_matrix,
            stock_list=retained_stocks,
            mean_returns=mean_returns,
            cov_matrix=cov_matrix,
            risk_free_rate=rf
        )

        analysis = analytics.get_full_analysis()
        
        # Subsample scatter points for fast rendering on frontend
        scatter_sample_size = min(2000, len(df_results))
        sample_indices = np.random.choice(len(df_results), size=scatter_sample_size, replace=False)
        
        scatter_data = {
            'returns': df_results['return'].iloc[sample_indices].tolist(),
            'volatilities': df_results['volatility'].iloc[sample_indices].tolist(),
            'sharpe_ratios': df_results['sharpe_ratio'].iloc[sample_indices].tolist()
        }

        response_payload = {
            'success': True,
            'stocks': retained_stocks,
            'trading_days': len(price_df),
            'scatter_data': scatter_data,
            'optimal_portfolios': analysis['optimal_portfolios'],
            'return_statistics': analysis['return_statistics'],
            'efficient_frontier': analysis['efficient_frontier']
        }
        
        return jsonify(sanitize_json(response_payload))

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel entrypoint handler
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
