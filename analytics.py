"""Simplified Analytics and Portfolio Optimization Module"""

import numpy as np
import pandas as pd
from typing import Dict
import config

class PortfolioAnalytics:
    """Analyze simulation results and identify optimal portfolios"""
    
    def __init__(self, results: pd.DataFrame, weights_array: np.ndarray, stock_list: list):
        self.results = results
        self.weights_array = weights_array
        self.stock_list = stock_list
    
    def find_optimal_portfolios(self) -> Dict:
        """Find max Sharpe, min volatility, and max return portfolios"""
        idx_sharpe = self.results['sharpe_ratio'].idxmax()
        idx_vol = self.results['volatility'].idxmin()
        idx_ret = self.results['return'].idxmax()
        
        def get_portfolio(idx):
            return {
                'return': self.results.loc[idx, 'return'],
                'volatility': self.results.loc[idx, 'volatility'],
                'sharpe_ratio': self.results.loc[idx, 'sharpe_ratio'],
                'weights': self.weights_array[idx],
                'weights_dict': {s: w for s, w in zip(self.stock_list, self.weights_array[idx])},
                'allocation': {s: w * config.INITIAL_CAPITAL for s, w in zip(self.stock_list, self.weights_array[idx])}
            }
        
        return {
            'max_sharpe': get_portfolio(idx_sharpe),
            'min_volatility': get_portfolio(idx_vol),
            'max_return': get_portfolio(idx_ret),
        }
    
    def calculate_return_statistics(self) -> Dict:
        """Calculate return distribution statistics"""
        r = self.results['return']
        return {
            'mean': r.mean(),
            'std': r.std(),
            'min': r.min(),
            'max': r.max(),
            'median': r.median(),
            'q5': r.quantile(0.05),
            'q25': r.quantile(0.25),
            'q75': r.quantile(0.75),
            'q95': r.quantile(0.95),
            'ci_lower': r.quantile(0.05),
            'ci_upper': r.quantile(0.95),
            'ci_width': r.quantile(0.95) - r.quantile(0.05),
        }
    
    def get_full_analysis(self) -> Dict:
        """Get complete analysis"""
        return {
            'optimal_portfolios': self.find_optimal_portfolios(),
            'return_statistics': self.calculate_return_statistics(),
        }
