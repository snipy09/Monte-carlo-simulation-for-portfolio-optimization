# Monte Carlo Simulation for Portfolio Optimization

A quantitative portfolio optimization engine combining Monte Carlo simulation with analytical Markowitz theory, served through an interactive Streamlit dashboard.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

---

## Overview

**Cluster Portfolio Engine** runs 10,000+ vectorized Monte Carlo simulations across a configurable equity universe to map the full risk-return space of possible portfolios. It then applies analytical Markowitz optimization (via SciPy SLSQP) on top of Ledoit-Wolf shrinkage covariance estimation to locate four canonical optimal portfolios on the Efficient Frontier. Results are surfaced through a dark-themed Streamlit dashboard with Plotly charts and can also be driven entirely from the command line.

---

## Features

| Category | Capability |
|---|---|
| Simulation | 10,000+ vectorized simulations via NumPy/Dirichlet distribution |
| Covariance | Ledoit-Wolf shrinkage estimation (scikit-learn) |
| Optimization | Analytical Markowitz via SciPy SLSQP with weight bounds |
| Optimal Portfolios | Max Sharpe, Min Volatility, Max Return, Max Sortino |
| Risk Metrics | VaR (95%), CVaR (95%), Sharpe ratio, Sortino ratio |
| Efficient Frontier | Full curve generation across the risk-return spectrum |
| Projections | Growth projection simulations with configurable capital |
| Data | Real-time OHLCV from Yahoo Finance via yfinance |
| UI | Streamlit dashboard, dark theme, Plotly interactive charts |
| CLI | Full headless orchestration via `main.py` |

---

## Project Structure

```
.
├── app.py              # Streamlit dashboard — main UI entry point
├── main.py             # CLI orchestrator
├── simulation.py       # MonteCarloSimulator class — core simulation engine
├── analytics.py        # PortfolioAnalytics class — Markowitz optimization (SLSQP)
├── data.py             # Stock data fetcher (yfinance)
├── cleaning.py         # Data preparation and preprocessing
├── visualization.py    # Matplotlib plots — efficient frontier, return distributions
├── config.py           # All configuration constants
├── report.py           # Report generation module
├── growth.py           # Growth projection simulations
├── evaluate.py         # Evaluation and backtesting module
├── requirements.txt    # Python dependencies
├── run.bat             # Windows launch script
├── run.sh              # Unix launch script
├── vercel.json         # Vercel deployment configuration
└── api/
    └── index.py        # Vercel serverless entry point
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
git clone https://github.com/snipy09/Monte-carlo-simulation-for-portfolio-optimization.git
cd Monte-carlo-simulation-for-portfolio-optimization
pip install -r requirements.txt
```

### Run — Streamlit Dashboard

```bash
# Unix / macOS
bash run.sh

# Windows
run.bat

# Or directly
streamlit run app.py
```

### Run — Command Line

```bash
python main.py
```

---

## Configuration

All parameters are defined in `config.py`. Key constants:

| Parameter | Default | Description |
|---|---|---|
| `TICKERS` | `AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, JNJ, V, WMT, PG` | Default equity universe |
| `NUM_SIMULATIONS` | `10000` | Monte Carlo simulation count |
| `RISK_FREE_RATE` | `0.05` | Annual risk-free rate (5%) |
| `TRADING_DAYS` | `252` | Trading days per year |
| `INITIAL_CAPITAL` | `100000` | Starting capital in USD |
| `MIN_WEIGHT` | `0.00` | Minimum allocation per asset |
| `MAX_WEIGHT` | `0.30` | Maximum allocation per asset (30%) |

To use a custom ticker list, edit `TICKERS` in `config.py` or pass tickers through the dashboard's sidebar input.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Simulation | NumPy (vectorized Dirichlet sampling) |
| Optimization | SciPy (SLSQP constrained minimization) |
| Covariance | scikit-learn (Ledoit-Wolf shrinkage) |
| Data | pandas, yfinance |
| Visualization | Plotly (interactive), Matplotlib (static charts) |
| Dashboard | Streamlit |
| Deployment | Vercel (serverless via `api/index.py`) |

---

## Optimal Portfolio Types

| Portfolio | Objective | Use Case |
|---|---|---|
| Max Sharpe | Maximize risk-adjusted return | Balanced long-term growth |
| Min Volatility | Minimize portfolio variance | Capital preservation |
| Max Return | Maximize expected annual return | Aggressive growth |
| Max Sortino | Maximize downside-adjusted return | Downside risk aversion |

---

## Deployment

The project includes a `vercel.json` and `api/index.py` for zero-configuration deployment to Vercel.

```bash
vercel deploy
```

Alternatively, deploy to any platform that supports Python WSGI/ASGI or run behind a reverse proxy.

---

## License

This project is licensed under the [MIT License](LICENSE).
