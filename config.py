"""
Configuration settings for Monte Carlo Portfolio Optimization

This module contains all configurable parameters for the portfolio optimization system.
"""

# ====================
# STOCK CONFIGURATION
# ====================

# Default list of stocks for portfolio optimization
DEFAULT_STOCKS = [
    "AAPL",  # Apple
    "MSFT",  # Microsoft
    "GOOGL",  # Alphabet
    "AMZN",  # Amazon
    "NVDA",  # NVIDIA
    "TSLA",  # Tesla
    "JNJ",   # Johnson & Johnson
    "V",     # Visa
    "WMT",   # Walmart
    "PG",    # Procter & Gamble
]

# ====================
# DATA CONFIGURATION
# ====================

# Historical data period (in years)
DATA_PERIOD_YEARS = 3

# Number of trading days per year (standard in finance)
TRADING_DAYS_PER_YEAR = 252

# Frequency of data - valid options: 'daily', 'weekly', 'monthly'
DATA_FREQUENCY = "1d"  # daily

# ====================
# MONTE CARLO CONFIGURATION
# ====================

# Number of simulations to run
NUM_SIMULATIONS = 10000

# Constraint bounds for individual stock weights
MIN_WEIGHT = 0.0   # Minimum allocation per stock (0% = no short selling)
MAX_WEIGHT = 0.3   # Maximum allocation per stock (30%)

# ====================
# FINANCIAL PARAMETERS
# ====================

# Risk-free rate (annual)
RISK_FREE_RATE = 0.05

# Initial capital for allocation
INITIAL_CAPITAL = 100000  # $100,000

# ====================
# VISUALIZATION CONFIGURATION
# ====================

# Figure size for plots
FIGURE_SIZE = (12, 8)

# DPI for plot output
PLOT_DPI = 100

# Color scheme
COLOR_SCHEME = {
    "background": "#f8f9fa",
    "grid": "#e9ecef",
    "line": "#495057",
    "highlight": "#dc3545",  # red
    "positive": "#28a745",   # green
}

# ====================
# REPORTING CONFIGURATION
# ====================

# Output directory for reports
OUTPUT_DIR = "output"

# Report filename
REPORT_FILENAME = "portfolio_optimization_report.txt"

# Growth projection settings
GROWTH_HORIZON_DAYS = 252
GROWTH_SIMULATIONS = 1000
GROWTH_PLOT_FILENAME = "growth_simulation.png"

# ====================
# LOGGING CONFIGURATION
# ====================

# Enable/disable logging
ENABLE_LOGGING = True

# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"

# ====================
# DATA QUALITY CONFIGURATION
# ====================

# Maximum percentage of missing data allowed (drop stocks with more missing data)
MAX_MISSING_DATA_PERCENT = 10

# Method for handling missing data: 'forward_fill' or 'interpolate'
MISSING_DATA_METHOD = "forward_fill"

# ====================
# RANDOM SEED (for reproducibility)
# ====================

# Set to None for random behavior, or set an integer for reproducibility
RANDOM_SEED = 42
