"""Portfolio growth projection module.

Simulates future portfolio value paths using daily multivariate normal returns.
"""

import numpy as np
from typing import Dict, Tuple
import config


def simulate_portfolio_growth(
    weights: np.ndarray,
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    days: int = None,
    simulations: int = None,
    initial_capital: float = None,
    seed: int = None,
) -> Tuple[np.ndarray, Dict]:
    """Simulate future portfolio growth over a set number of days.

    Parameters:
    -----------
    weights : np.ndarray
        Portfolio weights for each asset.
    mean_returns : np.ndarray
        Annual mean returns for each asset.
    cov_matrix : np.ndarray
        Annual covariance matrix of asset returns.
    days : int, optional
        Number of trading days to simulate.
    simulations : int, optional
        Number of Monte Carlo paths to generate.
    initial_capital : float, optional
        Starting portfolio capital.
    seed : int, optional
        Random seed for reproducibility.

    Returns:
    --------
    Tuple[np.ndarray, Dict]
        Simulation paths and summary statistics.
    """

    if days is None:
        days = config.GROWTH_HORIZON_DAYS
    if simulations is None:
        simulations = config.GROWTH_SIMULATIONS
    if initial_capital is None:
        initial_capital = config.INITIAL_CAPITAL
    if seed is None:
        seed = config.RANDOM_SEED

    daily_mean = mean_returns / config.TRADING_DAYS_PER_YEAR
    daily_cov = cov_matrix / config.TRADING_DAYS_PER_YEAR

    rng = np.random.default_rng(seed)
    daily_returns = rng.multivariate_normal(
        daily_mean, daily_cov, size=(simulations, days))

    portfolio_daily_returns = daily_returns.dot(weights)
    cumulative_returns = np.cumprod(1 + portfolio_daily_returns, axis=1)

    paths = np.empty((simulations, days + 1), dtype=float)
    paths[:, 0] = initial_capital
    paths[:, 1:] = initial_capital * cumulative_returns

    final_values = paths[:, -1]

    stats = {
        'days': days,
        'simulations': simulations,
        'initial_capital': initial_capital,
        'final_mean': float(np.mean(final_values)),
        'final_5th': float(np.percentile(final_values, 5)),
        'final_95th': float(np.percentile(final_values, 95)),
        'mean_path': np.mean(paths, axis=0),
        'p5_path': np.percentile(paths, 5, axis=0),
        'p95_path': np.percentile(paths, 95, axis=0),
        'daily_mean_return': float(np.mean(portfolio_daily_returns)),
    }

    return paths, stats
