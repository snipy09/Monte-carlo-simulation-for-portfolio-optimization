# Monte Carlo Portfolio Optimization

A complete Python project for **Monte Carlo Portfolio Optimization with constrained allocation and probabilistic analysis**.

##  Overview

This system enables data-driven portfolio optimization by:

-  Fetching historical stock data from Yahoo Finance
-  Simulating 10,000+ random portfolio allocations using Monte Carlo methods
-  Applying weight constraints (per-stock limits)
-  Computing optimal portfolios based on Sharpe ratio, risk, and return
-  Generating professional visualizations (efficient frontier + distribution)
-  Outputting detailed reports with capital allocation
-  Providing interactive Streamlit UI (optional)

---

##  Features

### Core Functionality

1. **Data Fetching & Validation**
   - Fetch adjusted closing prices from Yahoo Finance
   - Validate data quality and handle missing values
   - Support for custom stock lists

2. **Return Calculations**
   - Daily returns computed as percentage change
   - Annualized metrics (mean returns, covariance matrix)
   - Annualization factor: 252 trading days/year

3. **Monte Carlo Simulation**
   - 10,000+ random portfolio simulations
   - **Constrained weights**: each stock between 0% and 30%
   - Sum of weights = 100% (fully invested)
   - Normalized after constraints applied

4. **Portfolio Analytics**
   - Maximum Sharpe Ratio portfolio (optimal risk-adjusted return)
   - Minimum volatility portfolio (lowest risk)
   - Maximum return portfolio (highest growth potential)
   - Return distribution statistics (mean, std, quantiles, confidence intervals)

5. **Visualizations**
   - **Efficient Frontier**: Scatter plot of portfolios colored by Sharpe ratio
   - **Return Distribution**: Histogram with confidence interval (5%–95%)
   - **Allocation Pie Chart**: Stock weights in optimal portfolio
   - **Interactive Plots**: Matplotlib and optional Plotly

6. **Capital Allocation**
   - Convert portfolio weights to dollar amounts
   - Default capital: $100,000
   - Per-stock allocation table

7. **Reporting**
   - Professional text report with all insights
   - Summary of optimal portfolios
   - Detailed allocation table
   - Risk analysis and constraints applied

---

##  Project Structure

```
MCS Project/
├── config.py                    # Configuration and parameters
├── data.py                      # Data fetching and validation
├── cleaning.py                  # Data preprocessing and returns
├── simulation.py                # Monte Carlo engine
├── analytics.py                 # Optimization and analytics
├── visualization.py             # Plotting and charts
├── report.py                    # Report generation
├── main.py                      # Main orchestrator
├── app.py                       # Streamlit UI (optional)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── output/                      # Generated reports and plots
    ├── portfolio_optimization_report.txt
    ├── efficient_frontier.png
    ├── return_distribution.png
    └── optimal_allocation.png
```

---

##  Quick Start

### 1. Installation

```bash
# Clone or navigate to project directory
cd "MCS Project"

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Portfolio Optimization

```bash
# Run the complete pipeline
python main.py
```

This will:
1. Fetch historical data for 10 default stocks
2. Run 10,000 Monte Carlo simulations
3. Identify optimal portfolios
4. Generate visualizations
5. Create a detailed report

**Output:**
- Console report with all results
- Text file: `output/portfolio_optimization_report.txt`
- Plots: `output/efficient_frontier.png`, `output/return_distribution.png`, `output/optimal_allocation.png`

### 3. Interactive Streamlit UI (Optional)

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

**Features:**
- Select custom stocks
- Adjust simulation parameters
- Set weight constraints
- Interactive visualizations
- Real-time results

---

##  Configuration

Edit `config.py` to customize:

```python
# Stock universe (default: 10 stocks)
DEFAULT_STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", 
                  "TSLA", "JNJ", "V", "WMT", "PG"]

# Data period
DATA_PERIOD_YEARS = 3  # Use 3 years of history

# Monte Carlo simulations
NUM_SIMULATIONS = 10000  # Run 10,000 simulations

# Weight constraints
MIN_WEIGHT = 0.0   # 0% minimum (no short selling)
MAX_WEIGHT = 0.3   # 30% maximum per stock

# Financial parameters
RISK_FREE_RATE = 0.05      # 5% risk-free rate
INITIAL_CAPITAL = 100000   # $100,000 to allocate

# Random seed (for reproducibility)
RANDOM_SEED = 42
```

---

##  Mathematical Formulas

### Portfolio Return
$$R_p = \mathbf{w}^T \boldsymbol{\mu}$$

Where:
- $\mathbf{w}$ = weight vector
- $\boldsymbol{\mu}$ = mean return vector

### Portfolio Volatility (Risk)
$$\sigma_p = \sqrt{\mathbf{w}^T \Sigma \mathbf{w}}$$

Where:
- $\Sigma$ = covariance matrix

### Sharpe Ratio
$$\text{Sharpe} = \frac{R_p - R_f}{\sigma_p}$$

Where:
- $R_f$ = risk-free rate (5%)
- Higher = better risk-adjusted return

---

##  Module Documentation

### `config.py`
Global configuration settings for the entire system.

### `data.py`
```python
fetch_stock_data()      # Download historical prices
validate_data()         # Check data quality
get_stock_data_summary() # Generate data statistics
```

### `cleaning.py`
```python
handle_missing_data()         # Fill or interpolate NaN values
calculate_daily_returns()     # Compute percentage changes
calculate_annualized_metrics() # Scale to annual basis
prepare_data()                # Complete pipeline
```

### `simulation.py`
```python
class MonteCarloSimulator:
    generate_constrained_weights()  # Create random weights
    calculate_portfolio_metrics()   # Compute return/vol/Sharpe
    run_simulation()                # Execute all simulations
```

### `analytics.py`
```python
class PortfolioAnalytics:
    find_optimal_portfolios()    # Identify best portfolios
    calculate_return_statistics() # Compute distribution stats
    allocate_capital()           # Convert weights to dollars
    get_full_analysis()          # Complete analysis
```

### `visualization.py`
```python
class PortfolioVisualizer:
    plot_efficient_frontier()    # Scatter plot with highlights
    plot_return_distribution()   # Histogram + KDE
    plot_asset_allocation()      # Pie chart
    plot_all()                   # Generate all 3 plots
```

### `report.py`
```python
class ReportGenerator:
    generate_report()  # Create text report
    save_report()      # Save to file
```

### `main.py`
```python
run_portfolio_optimization()  # Run complete pipeline
main()                        # CLI entry point
```

---

##  Example Output

### Report Preview

```
================================================================================
                MONTE CARLO PORTFOLIO OPTIMIZATION REPORT
================================================================================

Generated: 2024-04-14 15:32:45

EXECUTIVE SUMMARY
----------------
Stocks analyzed:         AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, JNJ, V, WMT, PG
Number of simulations:   10,000
Risk-free rate:          5.00%
Initial capital:         $100,000.00

OPTIMAL PORTFOLIOS
================================================================================

1. MAXIMUM SHARPE RATIO PORTFOLIO (PRIMARY RECOMMENDATION)
Expected Annual Return:  12.45%
Annual Volatility:       15.23%
Sharpe Ratio:            0.4816

Weight Allocation:
  NVDA:  25.45%  ($25,450.00)
  MSFT:  20.10%  ($20,100.00)
  GOOGL: 18.35%  ($18,350.00)
  ...

RETURN DISTRIBUTION ANALYSIS
================================================================================
Mean Annual Return:      11.34%
Std Dev:                 8.76%
5th percentile:          -3.21%
95th percentile:         28.94%
90% Confidence Interval: [-3.21%, 28.94%]
```

---

##  Generated Plots

### 1. Efficient Frontier
- X-axis: Portfolio volatility (risk)
- Y-axis: Portfolio return
- Colors: Sharpe ratio gradient (viridis colormap)
- **Red star**: Maximum Sharpe ratio portfolio
- **Green diamond**: Minimum volatility portfolio
- **Blue square**: Maximum return portfolio

### 2. Return Distribution
- Histogram of 10,000 simulated portfolio returns
- Red dashed lines: 5th and 95th percentile (90% confidence interval)
- Green line: Mean return
- Green shaded region: Confidence interval

### 3. Allocation Pie Chart
- Stock weights in optimal (max Sharpe) portfolio
- Percentages labeled on each slice

---

##  Advanced Usage

### Custom Stock List

```python
# In main.py or as parameter
results = run_portfolio_optimization(
    stocks=['AAPL', 'MSFT', 'GOOGL', 'AMZN'],
    num_simulations=50000,
    period_years=5
)
```

### Programmatic Access

```python
from data import fetch_stock_data
from cleaning import prepare_data
from simulation import MonteCarloSimulator
from analytics import PortfolioAnalytics

# Fetch and prepare
data = fetch_stock_data(['AAPL', 'MSFT', 'GOOGL'])
stocks, returns, cov_matrix = prepare_data(data)

# Simulate
sim = MonteCarloSimulator(returns, cov_matrix)
results, weights = sim.run_simulation(num_simulations=10000)

# Analyze
analytics = PortfolioAnalytics(results, weights, stocks)
analysis = analytics.get_full_analysis()

# Access results
print(analysis['optimal_portfolios']['max_sharpe'])
```

### Modify Constraints

Edit `config.py`:

```python
MIN_WEIGHT = 0.05   # Minimum 5% per stock
MAX_WEIGHT = 0.20   # Maximum 20% per stock
```

---

##  Interpretation Guide

### Sharpe Ratio
- **Measures**: Risk-adjusted return
- **Formula**: (Return - Risk-Free Rate) / Volatility
- **Higher is better**: A portfolio with Sharpe ratio 0.5 is preferred over 0.3
- **Rule of thumb**: Sharpe > 1.0 is good; > 2.0 is excellent

### Confidence Interval
- **5th percentile**: Risk: 5% chance return will be lower
- **95th percentile**: 5% chance return will be higher
- **Width**: Indicates uncertainty (wider = more variability)

### Volatility (Std Dev)
- **Annual volatility**: Year-to-year price variability
- **Higher volatility**: Greater risk but potential for higher returns
- **Typical ranges**: 10-30% for diversified portfolios

---

##  Constraints & Limitations

1. **No Short Selling**: MIN_WEIGHT ≥ 0 (cannot bet against stocks)
2. **Allocation Limits**: MAX_WEIGHT prevents concentration risk
3. **Equal Weighting Bias**: Initial random weights use Dirichlet distribution
4. **Historical Data**: Past performance ≠ future results
5. **Rebalancing**: Report assumes buy-and-hold strategy

---

##  Troubleshooting

### Issue: "No data retrieved"
```
Solution: Check internet connection and stock symbols. 
Some stocks may be delisted or renamed.
```

### Issue: "Insufficient trading days"
```
Solution: Increase DATA_PERIOD_YEARS in config.py
```

### Issue: Streamlit app not opening
```bash
# Install Streamlit specifically
pip install streamlit>=1.25.0

# Try running again
streamlit run app.py --logger.level=debug
```

### Issue: Missing data in plots
```
Solution: Ensure matplotlib is installed:
pip install matplotlib seaborn
```

---

##  Further Reading

### Topics Covered
- **Monte Carlo Methods**: Random sampling for optimization
- **Portfolio Theory**: Markowitz efficient frontier
- **Sharpe Ratio**: Risk-adjusted performance metric
- **Constraint Optimization**: Linear programming basics
- **Time Series Analysis**: Returns and covariance

### References
- Markowitz, H. (1952). "Portfolio Selection"
- Sharpe, W. F. (1966). "Mutual Fund Performance"
- Black & Litterman (1990). "Global Portfolio Optimization"

---

##  License

MIT License - Free to use and modify.

---

##  Contributing

To extend the project:

1. Add new optimization methods in `analytics.py`
2. Add custom constraints in `simulation.py`
3. Create additional visualizations in `visualization.py`
4. Add risk metrics in `analytics.py`

Example: Value-at-Risk (VaR) metric

```python
# In analytics.py
def calculate_var(self, confidence=0.95):
    """Calculate Value-at-Risk at given confidence level"""
    return self.results['return'].quantile(1 - confidence)
```

---

##  Support

For issues or questions:
1. Check the Troubleshooting section
2. Review log output for error messages
3. Validate configuration in `config.py`
4. Check internet connection for data fetching

---

##  Learning Outcomes

After running this project, you'll understand:

-  How to fetch and preprocess financial data
-  How to implement Monte Carlo simulations
-  How portfolio optimization works mathematically
-  How to interpret Sharpe ratios and efficient frontiers
-  How to build modular Python projects
-  How to visualize complex financial data
-  How to create professional reports

---

##  Next Steps

1. **Run the system**: `python main.py`
2. **Explore the results**: Open plots in `output/`
3. **Read the report**: Check `output/portfolio_optimization_report.txt`
4. **Try Streamlit UI**: `streamlit run app.py`
5. **Customize parameters**: Edit `config.py`
6. **Extend functionality**: Add new features to modules

---

**Built with  for portfolio optimization enthusiasts**

*Version 1.0 - April 2024*
