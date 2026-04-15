"""Simplified Data fetching module"""

import logging
from typing import Dict, List, Tuple
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import config

logger = logging.getLogger(__name__)


def fetch_stock_data(stocks: List[str] = None, period_years: int = None) -> pd.DataFrame:
    """Fetch stock data from Yahoo Finance"""
    stocks = stocks or config.DEFAULT_STOCKS
    period_years = period_years or config.DATA_PERIOD_YEARS
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_years * 365)

    try:
        data = yf.download(stocks, start=start_date,
                           end=end_date, progress=False, repair=True)

        # Handle edge cases for yfinance return types
        if isinstance(data, pd.Series):
            # Single stock returns a Series
            stock_name = stocks[0] if isinstance(stocks, list) else stocks
            data = data.to_frame(name=stock_name)
        elif isinstance(data.columns, pd.MultiIndex):
            # Multiple stocks return DataFrame with MultiIndex columns
            # Extract price column (Adj Close preferred, then Close, then first)
            price_columns = data.columns.get_level_values(0).unique()

            if "Adj Close" in price_columns:
                data = data["Adj Close"]
            elif "Close" in price_columns:
                data = data["Close"]
            else:
                data = data[price_columns[0]]

        # Ensure we have a DataFrame
        if not isinstance(data, pd.DataFrame):
            data = data.to_frame()

        # Ensure column names are strings
        data.columns = [str(col) for col in data.columns]

        logger.info(
            f" Fetched {len(data.columns)} stocks, {len(data)} trading days")
        return data

    except Exception as e:
        raise ValueError(f"Failed to fetch data: {str(e)}")


def validate_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """Validate data and remove stocks with too much missing data"""
    if not isinstance(data, pd.DataFrame) or data.empty:
        raise ValueError("Invalid data: expected non-empty DataFrame")

    missing_pct = (data.isnull().sum() / len(data)) * 100
    valid_stocks = missing_pct[missing_pct <=
                               config.MAX_MISSING_DATA_PERCENT].index.tolist()

    if len(valid_stocks) < 2:
        raise ValueError("Fewer than 2 stocks with acceptable data quality")

    return data[valid_stocks], {
        'retained': valid_stocks,
        'removed': list(set(data.columns) - set(valid_stocks))
    }


def get_stock_data_summary(data: pd.DataFrame) -> Dict:
    """Get data summary"""
    return {
        'start_date': data.index.min().date(),
        'end_date': data.index.max().date(),
        'trading_days': len(data),
        'stocks': list(data.columns),
        'num_stocks': len(data.columns),
    }
