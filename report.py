"""
Report Generation Module

Generates comprehensive text report of optimization results.
"""

import logging
from datetime import datetime
from typing import Dict
import config

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=config.LOG_LEVEL if config.ENABLE_LOGGING else logging.CRITICAL)


class ReportGenerator:
    """
    Generate comprehensive text reports of portfolio optimization results.
    """

    def __init__(self, stock_list: list, data_summary: Dict = None):
        """
        Initialize report generator.

        Parameters:
        -----------
        stock_list : list
            List of stock symbols used in optimization
        data_summary : Dict, optional
            Summary of data used
        """

        self.stock_list = stock_list
        self.data_summary = data_summary or {}
        self.timestamp = datetime.now()

        logger.info("Initialized ReportGenerator")

    def format_number(self, value: float, decimals: int = 4, as_percent: bool = False) -> str:
        """
        Format a number for display.

        Parameters:
        -----------
        value : float
            Number to format
        decimals : int
            Number of decimal places
        as_percent : bool
            Whether to display as percentage

        Returns:
        --------
        str
            Formatted number string
        """

        if as_percent:
            return f"{value*100:.{decimals}f}%"
        else:
            return f"{value:.{decimals}f}"

    def generate_report(
        self,
        optimal_portfolios: Dict,
        return_stats: Dict,
        growth_stats: Dict = None,
        num_simulations: int = None
    ) -> str:
        """
        Generate comprehensive optimization report.

        Parameters:
        -----------
        optimal_portfolios : Dict
            Optimal portfolio data from analytics
        return_stats : Dict
            Return statistics
        num_simulations : int, optional
            Number of simulations run

        Returns:
        --------
        str
            Complete report text
        """

        if num_simulations is None:
            num_simulations = config.NUM_SIMULATIONS

        report = []

        # Header
        report.append("=" * 80)
        report.append("MONTE CARLO PORTFOLIO OPTIMIZATION REPORT".center(80))
        report.append("=" * 80)
        report.append(
            f"\nGenerated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Executive Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 80)
        report.append(f"Stocks analyzed:         {', '.join(self.stock_list)}")
        report.append(f"Number of simulations:   {num_simulations:,}")
        report.append(
            f"Risk-free rate:          {self.format_number(config.RISK_FREE_RATE, as_percent=True)}")
        report.append(
            f"Initial capital:         ${config.INITIAL_CAPITAL:,.2f}\n")

        # Data Summary
        if self.data_summary:
            report.append("DATA SUMMARY")
            report.append("-" * 80)
            if 'start_date' in self.data_summary:
                report.append(
                    f"Start date:              {self.data_summary['start_date']}")
            if 'end_date' in self.data_summary:
                report.append(
                    f"End date:                {self.data_summary['end_date']}")
            if 'trading_days' in self.data_summary:
                report.append(
                    f"Trading days:            {self.data_summary['trading_days']}")
            report.append("")

        # Optimal Portfolios
        report.append("OPTIMAL PORTFOLIOS")
        report.append("=" * 80)

        # Max Sharpe
        max_sharpe = optimal_portfolios['max_sharpe']
        report.append(
            "\n1. MAXIMUM SHARPE RATIO PORTFOLIO (PRIMARY RECOMMENDATION)")
        report.append("-" * 80)
        report.append(
            f"Expected Annual Return:  {self.format_number(max_sharpe['return'], as_percent=True)}")
        report.append(
            f"Annual Volatility:       {self.format_number(max_sharpe['volatility'], as_percent=True)}")
        report.append(
            f"Sharpe Ratio:            {self.format_number(max_sharpe['sharpe_ratio'], decimals=4)}")

        report.append("\nWeight Allocation:")
        for stock, weight in sorted(max_sharpe['weights_dict'].items(), key=lambda x: x[1], reverse=True):
            if weight > 0.001:  # Only show weights > 0.1%
                report.append(f"  {stock:6s}: {self.format_number(weight, decimals=4, as_percent=True):8s}  "
                              f"(${max_sharpe['allocation'][stock]:>12,.2f})")

        # Min Volatility
        min_vol = optimal_portfolios['min_volatility']
        report.append("\n2. MINIMUM VOLATILITY PORTFOLIO")
        report.append("-" * 80)
        report.append(
            f"Expected Annual Return:  {self.format_number(min_vol['return'], as_percent=True)}")
        report.append(
            f"Annual Volatility:       {self.format_number(min_vol['volatility'], as_percent=True)}")
        report.append(
            f"Sharpe Ratio:            {self.format_number(min_vol['sharpe_ratio'], decimals=4)}")

        report.append("\nWeight Allocation:")
        for stock, weight in sorted(min_vol['weights_dict'].items(), key=lambda x: x[1], reverse=True):
            if weight > 0.001:
                report.append(
                    f"  {stock:6s}: {self.format_number(weight, decimals=4, as_percent=True):8s}")

        # Max Return
        max_ret = optimal_portfolios['max_return']
        report.append("\n3. MAXIMUM RETURN PORTFOLIO")
        report.append("-" * 80)
        report.append(
            f"Expected Annual Return:  {self.format_number(max_ret['return'], as_percent=True)}")
        report.append(
            f"Annual Volatility:       {self.format_number(max_ret['volatility'], as_percent=True)}")
        report.append(
            f"Sharpe Ratio:            {self.format_number(max_ret['sharpe_ratio'], decimals=4)}")

        report.append("\nWeight Allocation:")
        for stock, weight in sorted(max_ret['weights_dict'].items(), key=lambda x: x[1], reverse=True):
            if weight > 0.001:
                report.append(
                    f"  {stock:6s}: {self.format_number(weight, decimals=4, as_percent=True):8s}")

        # Return Statistics
        report.append("\n\nRETURN DISTRIBUTION ANALYSIS")
        report.append("=" * 80)
        report.append(
            f"Mean Annual Return:      {self.format_number(return_stats['mean'], as_percent=True)}")
        report.append(
            f"Std Dev:                 {self.format_number(return_stats['std'], as_percent=True)}")
        report.append(
            f"Minimum Return:          {self.format_number(return_stats['min'], as_percent=True)}")
        report.append(
            f"Maximum Return:          {self.format_number(return_stats['max'], as_percent=True)}")
        report.append(
            f"Median Return:           {self.format_number(return_stats['median'], as_percent=True)}")

        report.append("\nPercentiles:")
        report.append(
            f"  5th percentile:        {self.format_number(return_stats['q5'], as_percent=True)}")
        report.append(
            f"  25th percentile:       {self.format_number(return_stats['q25'], as_percent=True)}")
        report.append(
            f"  75th percentile:       {self.format_number(return_stats['q75'], as_percent=True)}")
        report.append(
            f"  95th percentile:       {self.format_number(return_stats['q95'], as_percent=True)}")

        report.append(f"\n90% Confidence Interval: [{self.format_number(return_stats['ci_lower'], as_percent=True)}, "
                      f"{self.format_number(return_stats['ci_upper'], as_percent=True)}]")
        report.append(
            f"Confidence Width:        {self.format_number(return_stats['ci_width'], as_percent=True)}")

        if growth_stats is not None:
            report.append("\n\nPORTFOLIO GROWTH PROJECTION")
            report.append("=" * 80)
            report.append(
                f"Projection horizon:      {growth_stats['days']} trading days")
            report.append(
                f"Monte Carlo paths:       {growth_stats['simulations']:,}")
            report.append(
                f"Initial capital:         ${growth_stats['initial_capital']:,.2f}")
            report.append(
                f"Expected final value:    ${growth_stats['final_mean']:,.2f}")
            report.append(
                f"Worst case (5%):         ${growth_stats['final_5th']:,.2f}")
            report.append(
                f"Best case (95%):         ${growth_stats['final_95th']:,.2f}")

        # Capital Allocation
        report.append(
            "\n\nCAPITAL ALLOCATION (Based on Maximum Sharpe Ratio Portfolio)")
        report.append("=" * 80)
        report.append(
            f"Total Capital:           ${config.INITIAL_CAPITAL:,.2f}\n")

        total_allocated = 0
        allocation_data = []
        for stock, amount in sorted(max_sharpe['allocation'].items(),
                                    key=lambda x: x[1], reverse=True):
            weight = max_sharpe['weights_dict'][stock]
            if weight > 0.001:
                allocation_data.append((stock, weight, amount))
                total_allocated += amount

        report.append(
            f"{'Stock':<8} {'Weight':<12} {'Amount':>14} {'Running Total':<15}")
        report.append("-" * 80)

        running_total = 0
        for stock, weight, amount in allocation_data:
            running_total += amount
            report.append(f"{stock:<8} {self.format_number(weight, as_percent=True):<12} "
                          f"${amount:>12,.2f}  ${running_total:>12,.2f}")

        report.append("-" * 80)
        report.append(f"{'TOTAL':<8} {self.format_number(sum([w for _, w, _ in allocation_data]), as_percent=True):<12} "
                      f"${total_allocated:>12,.2f}")

        # Constraints
        report.append("\n\nCONSTRAINTS APPLIED")
        report.append("=" * 80)
        report.append(
            f"Minimum weight per stock: {self.format_number(config.MIN_WEIGHT, as_percent=True)}")
        report.append(
            f"Maximum weight per stock: {self.format_number(config.MAX_WEIGHT, as_percent=True)}")
        report.append(f"Total weight constraint:  1.0 (100%)")

        # Footer
        report.append("\n" + "=" * 80)
        report.append("END OF REPORT".center(80))
        report.append("=" * 80)
        report.append(f"\nVelocity Finance, {self.timestamp.strftime('%Y')}")
        report.append("Portfolio Optimization System v1.0")

        return "\n".join(report)

    def save_report(self, report_text: str, filepath: str = None) -> str:
        """
        Save report to file.

        Parameters:
        -----------
        report_text : str
            Report content to save
        filepath : str, optional
            Path to save report (default: config.REPORT_FILENAME)

        Returns:
        --------
        str
            Path where report was saved
        """

        if filepath is None:
            import os
            os.makedirs(config.OUTPUT_DIR, exist_ok=True)
            filepath = f"{config.OUTPUT_DIR}/{config.REPORT_FILENAME}"

        with open(filepath, 'w') as f:
            f.write(report_text)

        logger.info(f"Report saved to: {filepath}")

        return filepath
