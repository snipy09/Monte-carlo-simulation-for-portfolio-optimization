# 📊 QuantumPort: Monte Carlo Portfolio Optimization Engine

<div align="center">

**Institutional-Grade Portfolio Optimization & Risk Engine with SciPy SLSQP Markowitz Frontier & Ledoit-Wolf Covariance**

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)
![Optimization](https://img.shields.io/badge/Optimization-SciPy%20SLSQP-indigo?style=flat-square)
![Vercel](https://img.shields.io/badge/Deployment-Vercel%20Live-brightgreen?style=flat-square&logo=vercel)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

[🚀 Live Interactive Web App](https://mcs-portfolio-optimizer.vercel.app) • [GitHub Repository](https://github.com/snipy09/MCS-Project)

</div>

---

## 💡 Overview

**QuantumPort** is a quantitative finance library and web application for constrained portfolio optimization, risk analytics, and Markowitz Efficient Frontier generation. It empowers quantitative researchers and portfolio managers to compute optimal capital allocations using vectorized Monte Carlo simulations combined with exact Quadratic Programming (SciPy SLSQP).

### Key Features
- ⚡ **Vectorized Monte Carlo Engine**: Simulates 100,000+ portfolios in $< 0.1$ seconds using NumPy matrix einsum and Dirichlet distributions.
- 📐 **SciPy SLSQP Markowitz Optimization**: Analytical quadratic programming solver for exact Maximum Sharpe Ratio, Minimum Volatility, and continuous Efficient Frontier curve points.
- 🛡️ **Advanced Risk Analytics**: Calculates Value at Risk (95% & 99% VaR), Expected Shortfall (CVaR), Sortino Ratio (downside deviation), and Calmar Ratio.
- 📈 **Ledoit-Wolf Shrinkage Covariance**: Eliminates noise in high-dimensional stock covariance matrices.
- 🌐 **Wall Street Glassmorphic Terminal**: Live Vercel dashboard with interactive Plotly.js charts, real-time ticker selection, and preset asset classes.

---

## 🧮 Mathematical & Algorithmic Foundation

### 1. Vectorized Portfolio Risk & Return
For $N$ assets with mean return vector $\boldsymbol{\mu} \in \mathbb{R}^N$ and covariance matrix $\boldsymbol{\Sigma} \in \mathbb{R}^{N \times N}$, portfolio allocation $\mathbf{w} \in \mathbb{R}^N$ yields:

$$\mathbb{E}[R_p] = \mathbf{w}^T \boldsymbol{\mu}, \quad \sigma_p = \sqrt{\mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w}}$$

### 2. Exact Maximum Sharpe Ratio Optimization
$$\max_{\mathbf{w}} \; \frac{\mathbf{w}^T \boldsymbol{\mu} - R_f}{\sqrt{\mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w}}} \quad \text{s.t.} \quad \sum_{i=1}^N w_i = 1, \quad w_{\min} \le w_i \le w_{\max}$$

---

## 🚀 Quick Start

### Local Setup
```bash
git clone https://github.com/snipy09/MCS-Project.git
cd MCS-Project

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run CLI Simulation & Report Generator
python3 main.py

# Run Local Streamlit UI
streamlit run app.py
```

---

## 🌐 Live Web Deployment

Deployed live on Vercel: **[https://mcs-portfolio-optimizer.vercel.app](https://mcs-portfolio-optimizer.vercel.app)**
