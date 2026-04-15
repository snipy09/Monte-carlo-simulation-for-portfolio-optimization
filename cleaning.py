"""Simplified Data cleaning module"""

import pandas as pd
import numpy as np
import config


def prepare_data(prices: pd.DataFrame) -> tuple:
    """Complete pipeline: clean -> returns -> annualized metrics"""
    # Handle missing data
    prices = prices.ffill().bfill().dropna()

    # Calculate daily returns
    daily_returns = prices.pct_change().dropna()

    # Annualize
    mean_returns = (daily_returns.mean() * config.TRADING_DAYS_PER_YEAR).values
    cov_matrix = (daily_returns.cov() * config.TRADING_DAYS_PER_YEAR).values

    return list(prices.columns), mean_returns, cov_matrix
