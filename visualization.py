"""
Visualization Module

Creates plots for efficient frontier and return distribution.
"""

import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Dict, Tuple
import config

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=config.LOG_LEVEL if config.ENABLE_LOGGING else logging.CRITICAL)


class PortfolioVisualizer:
    """
    Create visualizations for portfolio optimization results.
    """

    def __init__(self, figsize: Tuple[int, int] = None, dpi: int = None):
        """
        Initialize visualizer with matplotlib settings.

        Parameters:
        -----------
        figsize : Tuple[int, int], optional
            Figure size (width, height)
        dpi : int, optional
            Figure DPI
        """

        if figsize is None:
            figsize = config.FIGURE_SIZE
        if dpi is None:
            dpi = config.PLOT_DPI

        self.figsize = figsize
        self.dpi = dpi

        # Set matplotlib style
        plt.style.use('seaborn-v0_8-darkgrid')

        logger.info(
            f"Initialized PortfolioVisualizer: figsize={figsize}, dpi={dpi}")

    def plot_efficient_frontier(
        self,
        results: pd.DataFrame,
        optimal_portfolios: Dict,
        save_path: str = None
    ) -> plt.Figure:
        """
        Plot Monte Carlo scatter with efficient frontier.

        Parameters:
        -----------
        results : pd.DataFrame
            Simulation results with 'return', 'volatility', 'sharpe_ratio'
        optimal_portfolios : Dict
            Dictionary with optimal portfolio candidates
        save_path : str, optional
            Path to save figure

        Returns:
        --------
        plt.Figure
            The matplotlib figure object
        """

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # Create scatter plot colored by Sharpe ratio
        scatter = ax.scatter(
            results['volatility'],
            results['return'],
            c=results['sharpe_ratio'],
            cmap='viridis',
            alpha=0.5,
            s=20,
            edgecolors='none'
        )

        # Highlight optimal portfolios
        max_sharpe = optimal_portfolios['max_sharpe']
        min_vol = optimal_portfolios['min_volatility']
        max_return = optimal_portfolios['max_return']

        # Max Sharpe (red star)
        ax.scatter(
            max_sharpe['volatility'],
            max_sharpe['return'],
            marker='*',
            color='red',
            s=800,
            edgecolors='darkred',
            linewidths=2,
            label=f"Max Sharpe ({max_sharpe['sharpe_ratio']:.2f})",
            zorder=5
        )

        # Min Volatility (green diamond)
        ax.scatter(
            min_vol['volatility'],
            min_vol['return'],
            marker='D',
            color='green',
            s=200,
            edgecolors='darkgreen',
            linewidths=2,
            label=f"Min Volatility ({min_vol['volatility']:.4f})",
            zorder=5
        )

        # Max Return (blue square)
        ax.scatter(
            max_return['volatility'],
            max_return['return'],
            marker='s',
            color='blue',
            s=200,
            edgecolors='darkblue',
            linewidths=2,
            label=f"Max Return ({max_return['return']:.4f})",
            zorder=5
        )

        # Labels and formatting
        ax.set_xlabel('Volatility (Annual Std Dev)',
                      fontsize=12, fontweight='bold')
        ax.set_ylabel('Expected Return (Annual)',
                      fontsize=12, fontweight='bold')
        ax.set_title('Monte Carlo Portfolio Optimization\n(Efficient Frontier)',
                     fontsize=14, fontweight='bold')

        # Format axes as percentages
        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(lambda y, _: '{:.2%}'.format(y)))
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda y, _: '{:.2%}'.format(y)))

        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Sharpe Ratio', fontsize=11, fontweight='bold')

        # Legend and grid
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved efficient frontier plot to: {save_path}")

        return fig

    def plot_return_distribution(
        self,
        results: pd.DataFrame,
        return_stats: Dict,
        save_path: str = None
    ) -> plt.Figure:
        """
        Plot histogram and KDE of portfolio returns.

        Parameters:
        -----------
        results : pd.DataFrame
            Simulation results
        return_stats : Dict
            Statistics including confidence interval
        save_path : str, optional
            Path to save figure

        Returns:
        --------
        plt.Figure
            The matplotlib figure object
        """

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        returns = results['return']

        # Histogram
        ax.hist(returns, bins=50, alpha=0.7, color='skyblue', edgecolor='black',
                label='Simulated Returns')

        # KDE (kernel density estimation)
        from scipy import stats
        kde = stats.gaussian_kde(returns)
        x_range = np.linspace(returns.min(), returns.max(), 200)
        ax.plot(x_range, kde(x_range) * len(returns) * (returns.max() - returns.min()) / 50,
                'r-', linewidth=2, label='Density')

        # Mark confidence interval (5%-95%)
        ci_lower = return_stats['ci_lower']
        ci_upper = return_stats['ci_upper']

        ax.axvline(ci_lower, color='orange', linestyle='--', linewidth=2,
                   label=f"5th percentile ({ci_lower:.4f})")
        ax.axvline(ci_upper, color='orange', linestyle='--', linewidth=2,
                   label=f"95th percentile ({ci_upper:.4f})")

        # Mark mean
        ax.axvline(return_stats['mean'], color='green', linestyle='-', linewidth=2.5,
                   label=f"Mean ({return_stats['mean']:.4f})")

        # Shade confidence region
        ax.axvspan(ci_lower, ci_upper, alpha=0.1, color='green')

        # Labels and formatting
        ax.set_xlabel('Annual Return', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Simulated Portfolio Returns\n(10,000 Monte Carlo Simulations)',
                     fontsize=14, fontweight='bold')

        # Format x-axis as percentage
        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(lambda y, _: '{:.2%}'.format(y)))

        # Legend and grid
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved return distribution plot to: {save_path}")

        return fig

    def plot_asset_allocation(
        self,
        weights_dict: Dict[str, float],
        title: str = "Optimal Portfolio Allocation",
        save_path: str = None
    ) -> plt.Figure:
        """
        Create pie chart of portfolio allocation.

        Parameters:
        -----------
        weights_dict : Dict[str, float]
            Dictionary with stock symbols and weights
        title : str, optional
            Chart title
        save_path : str, optional
            Path to save figure

        Returns:
        --------
        plt.Figure
            The matplotlib figure object
        """

        fig, ax = plt.subplots(figsize=(10, 8), dpi=self.dpi)

        stocks = list(weights_dict.keys())
        weights = list(weights_dict.values())

        # Create pie chart
        colors = plt.cm.Set3(np.linspace(0, 1, len(stocks)))
        wedges, texts, autotexts = ax.pie(
            weights,
            labels=stocks,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 11}
        )

        # Format percentage text
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)

        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved allocation chart to: {save_path}")

        return fig

    def plot_growth_simulation(
        self,
        growth_paths: np.ndarray,
        growth_stats: Dict,
        save_path: str = None
    ) -> plt.Figure:
        """
        Plot simulated growth of the optimal portfolio over time.

        Parameters:
        -----------
        growth_paths : np.ndarray
            Array of portfolio value paths with shape (simulations, days + 1).
        growth_stats : Dict
            Summary statistics for the growth simulation.
        save_path : str, optional
            Path to save figure.

        Returns:
        --------
        plt.Figure
            The matplotlib figure object.
        """

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        num_paths = growth_paths.shape[0]
        num_days = growth_paths.shape[1] - 1
        x = np.arange(0, num_days + 1)

        sample_size = min(100, num_paths)
        sample_indices = np.random.choice(
            num_paths, size=sample_size, replace=False)
        for idx in sample_indices:
            ax.plot(x, growth_paths[idx],
                    color='skyblue', alpha=0.08, linewidth=1)

        mean_path = growth_stats['mean_path']
        p5_path = growth_stats['p5_path']
        p95_path = growth_stats['p95_path']

        ax.plot(x, mean_path, color='#1f77b4',
                linewidth=3, label='Mean trajectory')
        ax.fill_between(x, p5_path, p95_path, color='#1f77b4', alpha=0.12,
                        label='5-95% confidence band')

        ax.set_title('Portfolio Growth Simulation',
                     fontsize=14, fontweight='bold')
        ax.set_xlabel('Trading Days', fontsize=12, fontweight='bold')
        ax.set_ylabel('Portfolio Value ($)', fontsize=12, fontweight='bold')

        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda y, _: f'${y:,.0f}')
        )

        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved growth simulation plot to: {save_path}")

        return fig

    def plot_all(
        self,
        results: pd.DataFrame,
        optimal_portfolios: Dict,
        return_stats: Dict,
        growth_paths: np.ndarray = None,
        growth_stats: Dict = None,
        output_dir: str = None
    ) -> Dict:
        """
        Create all visualizations.

        Parameters:
        -----------
        results : pd.DataFrame
            Simulation results
        optimal_portfolios : Dict
            Optimal portfolio data
        return_stats : Dict
            Return statistics
        output_dir : str, optional
            Directory to save plots

        Returns:
        --------
        Dict
            Dictionary with figure references
        """

        if output_dir is None:
            output_dir = config.OUTPUT_DIR

        import os
        os.makedirs(output_dir, exist_ok=True)

        figures = {}

        # Efficient frontier
        frontier_path = f"{output_dir}/efficient_frontier.png" if output_dir else None
        figures['efficient_frontier'] = self.plot_efficient_frontier(
            results,
            optimal_portfolios,
            save_path=frontier_path
        )

        # Return distribution
        dist_path = f"{output_dir}/return_distribution.png" if output_dir else None
        figures['return_distribution'] = self.plot_return_distribution(
            results,
            return_stats,
            save_path=dist_path
        )

        # Allocation pie chart
        max_sharpe_weights = optimal_portfolios['max_sharpe']['weights_dict']
        alloc_path = f"{output_dir}/optimal_allocation.png" if output_dir else None
        figures['allocation'] = self.plot_asset_allocation(
            max_sharpe_weights,
            title="Optimal Portfolio Allocation (Max Sharpe Ratio)",
            save_path=alloc_path
        )

        if growth_paths is not None and growth_stats is not None:
            growth_path = f"{output_dir}/{config.GROWTH_PLOT_FILENAME}" if output_dir else None
            figures['growth_projection'] = self.plot_growth_simulation(
                growth_paths,
                growth_stats,
                save_path=growth_path
            )

        logger.info(f"Created {len(figures)} visualizations")

        return figures
