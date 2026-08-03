"""
Analytical Markowitz Portfolio Optimization & Frontier Engine
Supports exact quadratic optimization (SLSQP), Max Sharpe, Min Volatility, Max Sortino, and Efficient Frontier curve generation.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from scipy.optimize import minimize
import config

class PortfolioAnalytics:
    """Analytical optimization and simulation analyzer using SciPy SLSQP & NumPy."""
    
    def __init__(
        self,
        results: pd.DataFrame,
        weights_array: np.ndarray,
        stock_list: List[str],
        mean_returns: Optional[np.ndarray] = None,
        cov_matrix: Optional[np.ndarray] = None,
        risk_free_rate: Optional[float] = None
    ):
        self.results = results
        self.weights_array = weights_array
        self.stock_list = stock_list
        self.num_assets = len(stock_list)
        self.mean_returns = mean_returns
        self.cov_matrix = cov_matrix
        self.risk_free_rate = risk_free_rate if risk_free_rate is not None else float(config.RISK_FREE_RATE)
        
    def find_optimal_portfolios(self) -> Dict:
        """Find max Sharpe, min volatility, max return, and max Sortino portfolios."""
        idx_sharpe = self.results['sharpe_ratio'].idxmax()
        idx_vol = self.results['volatility'].idxmin()
        idx_ret = self.results['return'].idxmax()
        
        idx_sortino = self.results['sortino_ratio'].idxmax() if 'sortino_ratio' in self.results else idx_sharpe

        def build_portfolio_dict(idx):
            w = self.weights_array[idx]
            ret = float(self.results.loc[idx, 'return'])
            vol = float(self.results.loc[idx, 'volatility'])
            sharpe = float(self.results.loc[idx, 'sharpe_ratio'])
            sortino = float(self.results.loc[idx, 'sortino_ratio']) if 'sortino_ratio' in self.results else sharpe
            var95 = float(self.results.loc[idx, 'var_95']) if 'var_95' in self.results else 1.645 * vol - ret
            cvar95 = float(self.results.loc[idx, 'cvar_95']) if 'cvar_95' in self.results else 2.06 * vol - ret
            
            return {
                'return': ret,
                'volatility': vol,
                'sharpe_ratio': sharpe,
                'sortino_ratio': sortino,
                'var_95': var95,
                'cvar_95': cvar95,
                'weights': w,
                'weights_dict': {s: float(w[i]) for i, s in enumerate(self.stock_list)},
                'allocation': {s: float(w[i] * config.INITIAL_CAPITAL) for i, s in enumerate(self.stock_list)}
            }
        
        sim_optimal = {
            'max_sharpe': build_portfolio_dict(idx_sharpe),
            'min_volatility': build_portfolio_dict(idx_vol),
            'max_return': build_portfolio_dict(idx_ret),
            'max_sortino': build_portfolio_dict(idx_sortino)
        }
        
        # Add exact SLSQP Optimization if mean_returns & cov_matrix are present
        if self.mean_returns is not None and self.cov_matrix is not None:
            exact_sharpe = self.optimize_exact_max_sharpe()
            exact_minvol = self.optimize_exact_min_volatility()
            sim_optimal['exact_max_sharpe'] = exact_sharpe
            sim_optimal['exact_min_volatility'] = exact_minvol
            
        return sim_optimal

    def optimize_exact_max_sharpe(self, min_w: float = 0.0, max_w: float = 0.3) -> Dict:
        """SciPy SLSQP exact Maximum Sharpe Ratio optimization."""
        bounds = tuple((min_w, max_w) for _ in range(self.num_assets))
        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})
        init_w = np.ones(self.num_assets) / self.num_assets
        
        def neg_sharpe(w):
            r = np.dot(w, self.mean_returns)
            v = np.sqrt(np.dot(w, np.dot(self.cov_matrix, w)))
            return -(r - self.risk_free_rate) / (v + 1e-8)
            
        res = minimize(neg_sharpe, init_w, method='SLSQP', bounds=bounds, constraints=constraints)
        opt_w = res.x / np.sum(res.x)
        
        ret = float(np.dot(opt_w, self.mean_returns))
        vol = float(np.sqrt(np.dot(opt_w, np.dot(self.cov_matrix, opt_w))))
        sharpe = float((ret - self.risk_free_rate) / vol)
        
        return {
            'return': ret,
            'volatility': vol,
            'sharpe_ratio': sharpe,
            'weights': opt_w,
            'weights_dict': {s: float(opt_w[i]) for i, s in enumerate(self.stock_list)},
            'allocation': {s: float(opt_w[i] * config.INITIAL_CAPITAL) for i, s in enumerate(self.stock_list)}
        }

    def optimize_exact_min_volatility(self, min_w: float = 0.0, max_w: float = 0.3) -> Dict:
        """SciPy SLSQP exact Minimum Volatility optimization."""
        bounds = tuple((min_w, max_w) for _ in range(self.num_assets))
        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})
        init_w = np.ones(self.num_assets) / self.num_assets
        
        def portfolio_vol(w):
            return np.sqrt(np.dot(w, np.dot(self.cov_matrix, w)))
            
        res = minimize(portfolio_vol, init_w, method='SLSQP', bounds=bounds, constraints=constraints)
        opt_w = res.x / np.sum(res.x)
        
        ret = float(np.dot(opt_w, self.mean_returns))
        vol = float(np.sqrt(np.dot(opt_w, np.dot(self.cov_matrix, opt_w))))
        sharpe = float((ret - self.risk_free_rate) / vol)
        
        return {
            'return': ret,
            'volatility': vol,
            'sharpe_ratio': sharpe,
            'weights': opt_w,
            'weights_dict': {s: float(opt_w[i]) for i, s in enumerate(self.stock_list)},
            'allocation': {s: float(opt_w[i] * config.INITIAL_CAPITAL) for i, s in enumerate(self.stock_list)}
        }

    def calculate_efficient_frontier_curve(self, n_points: int = 50, min_w: float = 0.0, max_w: float = 0.3) -> List[Dict]:
        """Compute exact continuous Markowitz Efficient Frontier curve across target return spectrum."""
        if self.mean_returns is None or self.cov_matrix is None:
            return []
            
        min_vol_port = self.optimize_exact_min_volatility(min_w, max_w)
        max_ret_port = float(np.max(self.mean_returns))
        
        target_returns = np.linspace(min_vol_port['return'], max_ret_port * 0.98, n_points)
        frontier = []
        bounds = tuple((min_w, max_w) for _ in range(self.num_assets))
        
        init_w = min_vol_port['weights']
        for target_r in target_returns:
            constraints = (
                {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0},
                {'type': 'eq', 'fun': lambda w, r=target_r: np.dot(w, self.mean_returns) - r}
            )
            res = minimize(lambda w: np.sqrt(np.dot(w, np.dot(self.cov_matrix, w))), init_w, method='SLSQP', bounds=bounds, constraints=constraints)
            if res.success:
                w = res.x / np.sum(res.x)
                v = float(np.sqrt(np.dot(w, np.dot(self.cov_matrix, w))))
                r = float(np.dot(w, self.mean_returns))
                sr = float((r - self.risk_free_rate) / v)
                frontier.append({'return': r, 'volatility': v, 'sharpe_ratio': sr, 'weights': w.tolist()})
                init_w = w  # Warm start next optimization point
                
        return frontier

    def calculate_return_statistics(self) -> Dict:
        """Calculate return distribution statistics."""
        r = self.results['return']
        return {
            'mean': float(r.mean()),
            'std': float(r.std()),
            'min': float(r.min()),
            'max': float(r.max()),
            'median': float(r.median()),
            'q5': float(r.quantile(0.05)),
            'q25': float(r.quantile(0.25)),
            'q75': float(r.quantile(0.75)),
            'q95': float(r.quantile(0.95)),
            'ci_lower': float(r.quantile(0.05)),
            'ci_upper': float(r.quantile(0.95)),
            'ci_width': float(r.quantile(0.95) - r.quantile(0.05)),
        }

    def get_full_analysis(self) -> Dict:
        """Get complete portfolio optimization and risk report."""
        return {
            'optimal_portfolios': self.find_optimal_portfolios(),
            'return_statistics': self.calculate_return_statistics(),
            'efficient_frontier': self.calculate_efficient_frontier_curve()
        }
