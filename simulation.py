"""
Monte Carlo & Portfolio Optimization Engine
Vectorized Monte Carlo simulation, Ledoit-Wolf shrinkage covariance, VaR/CVaR/Sortino calculations.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Optional
from sklearn.covariance import LedoitWolf
import config

class MonteCarloSimulator:
    """High-performance vectorized Monte Carlo portfolio simulator."""
    
    def __init__(
        self,
        mean_returns: np.ndarray,
        cov_matrix: np.ndarray,
        daily_returns: Optional[pd.DataFrame] = None,
        risk_free_rate: Optional[float] = None,
        use_ledoit_wolf: bool = True,
        seed: Optional[int] = None
    ):
        self.mean_returns = mean_returns
        self.cov_matrix = cov_matrix
        self.daily_returns = daily_returns
        self.num_assets = len(mean_returns)
        self.risk_free_rate = risk_free_rate if risk_free_rate is not None else float(config.RISK_FREE_RATE)
        
        if use_ledoit_wolf and daily_returns is not None and len(daily_returns) > 5:
            try:
                lw = LedoitWolf()
                lw_cov_daily = lw.fit(daily_returns.dropna().values).covariance_
                self.cov_matrix = lw_cov_daily * config.TRADING_DAYS_PER_YEAR
            except Exception:
                pass  # Fallback to standard empirical covariance
        
        if seed is not None:
            np.random.seed(seed)

    def run_simulation(
        self,
        num_sims: Optional[int] = None,
        min_w: Optional[float] = None,
        max_w: Optional[float] = None
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Run vectorized Monte Carlo simulations.
        Calculates Return, Volatility, Sharpe Ratio, Sortino Ratio, VaR (95%), CVaR (95%).
        """
        sims: int = num_sims if num_sims is not None else int(config.NUM_SIMULATIONS)
        min_weight: float = min_w if min_w is not None else float(config.MIN_WEIGHT)
        max_weight: float = max_w if max_w is not None else float(config.MAX_WEIGHT)
        
        # 1. Vectorized Weight Generation via Dirichlet Distribution
        alpha = np.ones(self.num_assets)
        raw_weights = np.random.dirichlet(alpha, size=sims)
        
        # Apply min/max weight constraints
        weights = np.clip(raw_weights, min_weight, max_weight)
        weights /= weights.sum(axis=1, keepdims=True)
        
        # 2. Vectorized Performance Metrics
        rets = weights @ self.mean_returns
        # Einsum for ultra-fast quadratic form w^T * Sigma * w for N portfolios
        vols = np.sqrt(np.einsum('ij,jk,ik->i', weights, self.cov_matrix, weights))
        
        # Avoid division by zero
        vols = np.maximum(vols, 1e-8)
        sharpes = (rets - self.risk_free_rate) / vols
        
        # 3. Downside Risk Metrics (Sortino, VaR, CVaR)
        if self.daily_returns is not None:
            daily_asset_rets = self.daily_returns.dropna().values  # (T, N)
            # Daily portfolio returns matrix (sims, T)
            port_daily_rets = weights @ daily_asset_rets.T  # (sims, T)
            
            # Sortino ratio: downside std dev (returns < daily risk free rate)
            daily_rf = self.risk_free_rate / config.TRADING_DAYS_PER_YEAR
            downside_rets = np.minimum(0, port_daily_rets - daily_rf)
            downside_std = np.sqrt(np.mean(downside_rets**2, axis=1)) * np.sqrt(config.TRADING_DAYS_PER_YEAR)
            downside_std = np.maximum(downside_std, 1e-8)
            sortinos = (rets - self.risk_free_rate) / downside_std
            
            # Parametric/Historical Value at Risk (VaR 95% & 99%) & Expected Shortfall (CVaR)
            var_95 = -np.percentile(port_daily_rets, 5, axis=1) * np.sqrt(config.TRADING_DAYS_PER_YEAR)
            cvar_95 = np.zeros(sims)
            for i in range(sims):
                cutoff = -np.percentile(port_daily_rets[i], 5)
                tail_losses = -port_daily_rets[i][-port_daily_rets[i] >= cutoff]
                cvar_95[i] = (tail_losses.mean() if len(tail_losses) > 0 else cutoff) * np.sqrt(config.TRADING_DAYS_PER_YEAR)
        else:
            # Analytical Gaussian approximations if daily returns not provided
            sortinos = sharpes
            var_95 = 1.645 * vols - rets
            cvar_95 = 2.06 * vols - rets

        df_results = pd.DataFrame({
            'return': rets,
            'volatility': vols,
            'sharpe_ratio': sharpes,
            'sortino_ratio': sortinos,
            'var_95': var_95,
            'cvar_95': cvar_95
        })
        
        return df_results, weights
