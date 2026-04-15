"""
Main Orchestration Module

Runs the complete Monte Carlo Portfolio Optimization pipeline.
"""

import logging
import sys
import os
from typing import Dict

# Import all modules
import config
from data import fetch_stock_data, validate_data, get_stock_data_summary
from cleaning import prepare_data
from simulation import MonteCarloSimulator
from analytics import PortfolioAnalytics
from growth import simulate_portfolio_growth
from visualization import PortfolioVisualizer
from report import ReportGenerator

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL if config.ENABLE_LOGGING else logging.CRITICAL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_portfolio_optimization(
    stocks: list = None,
    num_simulations: int = None,
    period_years: int = None
) -> Dict:
    """
    Run complete portfolio optimization pipeline.

    Parameters:
    -----------
    stocks : list, optional
        List of stock symbols
    num_simulations : int, optional
        Number of Monte Carlo simulations
    period_years : int, optional
        Years of historical data to use

    Returns:
    --------
    Dict
        Complete analysis results
    """

    if stocks is None:
        stocks = config.DEFAULT_STOCKS
    if num_simulations is None:
        num_simulations = config.NUM_SIMULATIONS
    if period_years is None:
        period_years = config.DATA_PERIOD_YEARS

    logger.info("=" * 80)
    logger.info("MONTE CARLO PORTFOLIO OPTIMIZATION".center(80))
    logger.info("=" * 80)

    # ============================
    # STEP 1: FETCH DATA
    # ============================
    logger.info("\n[STEP 1/6] Fetching historical stock data...")
    try:
        raw_data = fetch_stock_data(stocks, period_years)
        logger.info(f" Fetched data for {len(raw_data.columns)} stocks")
    except Exception as e:
        logger.error(f" Failed to fetch data: {str(e)}")
        return None

    # ============================
    # STEP 2: VALIDATE DATA
    # ============================
    logger.info("\n[STEP 2/6] Validating data quality...")
    try:
        clean_data, validation_report = validate_data(raw_data)
        logger.info(
            f" Retained {len(clean_data.columns)} stocks with good data quality")
    except Exception as e:
        logger.error(f" Data validation failed: {str(e)}")
        return None

    # Get data summary
    data_summary = get_stock_data_summary(clean_data)
    logger.info(
        f"  Trading period: {data_summary['start_date']} to {data_summary['end_date']}")
    logger.info(f"  Trading days: {data_summary['trading_days']}")

    # ============================
    # STEP 3: PREPARE DATA (RETURNS & ANNUALIZE)
    # ============================
    logger.info("\n[STEP 3/6] Preparing data (calculating returns)...")
    try:
        stock_list, mean_returns, cov_matrix = prepare_data(clean_data)
        logger.info(f" Prepared data for {len(stock_list)} assets")
    except Exception as e:
        logger.error(f" Data preparation failed: {str(e)}")
        return None

    # ============================
    # STEP 4: MONTE CARLO SIMULATION
    # ============================
    logger.info(
        f"\n[STEP 4/6] Running Monte Carlo simulations ({num_simulations:,})...")
    try:
        simulator = MonteCarloSimulator(mean_returns, cov_matrix)
        results, weights_array = simulator.run_simulation(num_simulations)
        logger.info(f" Completed {num_simulations:,} simulations")
    except Exception as e:
        logger.error(f" Simulation failed: {str(e)}")
        return None

    # ============================
    # STEP 5: ANALYTICS & OPTIMIZATION
    # ============================
    logger.info(
        "\n[STEP 5/7] Analyzing results and identifying optimal portfolios...")
    try:
        analytics = PortfolioAnalytics(results, weights_array, stock_list)
        full_analysis = analytics.get_full_analysis()
        logger.info(f" Analysis complete")
    except Exception as e:
        logger.error(f" Analysis failed: {str(e)}")
        return None

    # ============================
    # STEP 6: GROWTH PROJECTION
    # ============================
    logger.info("\n[STEP 6/7] Simulating future portfolio growth...")
    try:
        max_sharpe_weights = full_analysis['optimal_portfolios']['max_sharpe']['weights']
        growth_paths, growth_stats = simulate_portfolio_growth(
            max_sharpe_weights,
            mean_returns,
            cov_matrix,
            days=config.GROWTH_HORIZON_DAYS,
            simulations=config.GROWTH_SIMULATIONS,
            initial_capital=config.INITIAL_CAPITAL,
            seed=config.RANDOM_SEED,
        )
        logger.info(" Growth projection complete")
    except Exception as e:
        logger.error(f" Growth projection failed: {str(e)}")
        return None

    # ============================
    # STEP 7: VISUALIZATION & REPORTING
    # ============================
    logger.info(
        "\n[STEP 7/7] Creating visualizations and generating reports...")
    try:
        # Visualizations
        visualizer = PortfolioVisualizer()
        figures = visualizer.plot_all(
            results,
            full_analysis['optimal_portfolios'],
            full_analysis['return_statistics'],
            growth_paths=growth_paths,
            growth_stats=growth_stats
        )
        logger.info(f" Created {len(figures)} visualizations")

        # Report
        report_gen = ReportGenerator(stock_list, data_summary)
        report_text = report_gen.generate_report(
            full_analysis['optimal_portfolios'],
            full_analysis['return_statistics'],
            growth_stats=growth_stats,
            num_simulations=num_simulations
        )
        report_path = report_gen.save_report(report_text)
        logger.info(f" Report saved to: {report_path}")

    except Exception as e:
        logger.error(f" Visualization/reporting failed: {str(e)}")
        return None

    # ============================
    # COMPLETE
    # ============================
    logger.info("\n" + "=" * 80)
    logger.info("OPTIMIZATION COMPLETE".center(80))
    logger.info("=" * 80)

    # Print report to console
    print("\n\n")
    print(report_text)

    # Return complete results
    return {
        'simulation_results': results,
        'weights_array': weights_array,
        'analysis': full_analysis,
        'stock_list': stock_list,
        'data_summary': data_summary,
        'figures': figures,
        'report_text': report_text,
        'report_path': report_path,
        'growth_paths': growth_paths,
        'growth_stats': growth_stats,
    }


def main():
    """Main entry point with command-line interface."""

    print("\n" + "=" * 80)
    print("MONTE CARLO PORTFOLIO OPTIMIZATION SYSTEM".center(80))
    print("=" * 80 + "\n")

    # Use default configuration
    logger.info(f"Configuration:")
    logger.info(f"  Stocks: {', '.join(config.DEFAULT_STOCKS)}")
    logger.info(f"  Simulations: {config.NUM_SIMULATIONS:,}")
    logger.info(f"  Data period: {config.DATA_PERIOD_YEARS} years")
    logger.info(
        f"  Min/Max weight per stock: {config.MIN_WEIGHT:.0%}/{config.MAX_WEIGHT:.0%}")

    # Run optimization
    results = run_portfolio_optimization()

    if results:
        print("\n\n" + "=" * 80)
        print("OUTPUT FILES GENERATED:".center(80))
        print("=" * 80)
        print(f"\nReport:             {results['report_path']}")
        print(f"Output directory:   {config.OUTPUT_DIR}/")
        print("  - efficient_frontier.png")
        print("  - return_distribution.png")
        print("  - optimal_allocation.png")
        print("  - growth_simulation.png")
        print("\nTo visualize plots, open the PNG files in ./output/")

        # Optional: Display optimal allocation
        print("\n" + "=" * 80)
        print("OPTIMAL PORTFOLIO ALLOCATION")
        print("=" * 80)
        max_sharpe_alloc = results['analysis']['optimal_portfolios']['max_sharpe']['allocation']
        for stock in sorted(max_sharpe_alloc.keys()):
            amount = max_sharpe_alloc[stock]
            print(f"  {stock}: ${amount:>12,.2f}")

        # Portfolio growth projection summary
        growth_stats = results.get('growth_stats')
        if growth_stats is not None:
            print("\n" + "=" * 80)
            print("PORTFOLIO GROWTH PROJECTION")
            print("=" * 80)
            print(f"Expected Value:  ${growth_stats['final_mean']:,.2f}")
            print(f"Worst Case (5%): ${growth_stats['final_5th']:,.2f}")
            print(f"Best Case (95%): ${growth_stats['final_95th']:,.2f}")
    else:
        print("\n Optimization failed. Check logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
