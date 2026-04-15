"""Simplified Monte Carlo Simulation Engine"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict
import config

class MonteCarloSimulator:
    """Monte Carlo portfolio simulator with constrained random allocations"""
    
    def __init__(self, mean_returns: np.ndarray, cov_matrix: np.ndarray, risk_free_rate: float = None, seed: int = None):
        self.mean_returns = mean_returns
        self.cov_matrix = cov_matrix
        self.num_assets = len(mean_returns)
        self.risk_free_rate = risk_free_rate or config.RISK_FREE_RATE
        
        if seed is not None:
            np.random.seed(seed)
    
    def generate_weights(self, min_w: float = None, max_w: float = None) -> np.ndarray:
        """Generate random constrained portfolio weights"""
        min_w = min_w or config.MIN_WEIGHT
        max_w = max_w or config.MAX_WEIGHT
        
        weights = np.random.dirichlet(np.ones(self.num_assets))
        weights = np.clip(weights, min_w, max_w)
        return weights / weights.sum()
    
    def calc_metrics(self, weights: np.ndarray) -> Dict[str, float]:
        """Calculate portfolio metrics"""
        ret = np.dot(weights, self.mean_returns)
        vol = np.sqrt(np.dot(weights, np.dot(self.cov_matrix, weights)))
        sharpe = (ret - self.risk_free_rate) / vol
        return {'return': ret, 'volatility': vol, 'sharpe_ratio': sharpe}
    
    def run_simulation(self, num_sims: int = None, min_w: float = None, max_w: float = None) -> Tuple[pd.DataFrame, np.ndarray]:
        """Run Monte Carlo simulations"""
        num_sims = num_sims or config.NUM_SIMULATIONS
        
        results = np.zeros((num_sims, 3))
        weights_array = np.zeros((num_sims, self.num_assets))
        
        for i in range(num_sims):
            w = self.generate_weights(min_w, max_w)
            weights_array[i] = w
            m = self.calc_metrics(w)
            results[i] = [m['return'], m['volatility'], m['sharpe_ratio']]
        
        return pd.DataFrame(results, columns=['return', 'volatility', 'sharpe_ratio']), weights_array
