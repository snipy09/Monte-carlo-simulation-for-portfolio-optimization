"""
Cluster Portfolio Engine – Monte Carlo Portfolio Optimization Tool
Professional quant finance dashboard for portfolio analysis and optimization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import config

from data import fetch_stock_data, validate_data, get_stock_data_summary
from cleaning import prepare_data
from simulation import MonteCarloSimulator
from analytics import PortfolioAnalytics



# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Cluster Portfolio Engine",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL STYLING & THEME
# ============================================================================
st.markdown("""
<style>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Global Typography */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Color Scheme & Background */
    :root {
        --bg-primary: #05010a;
        --bg-secondary: #0c0817;
        --text-primary: #ffffff;
        --text-secondary: #94a3b8;
        --accent-purple: #a855f7;
        --accent-blue: #6366f1;
        --glass-bg: rgba(255, 255, 255, 0.02);
        --glass-border: rgba(255, 255, 255, 0.08);
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        color: var(--text-primary);
        background-attachment: fixed;
    }
    
    /* Header & Dividers */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }
    
    hr {
        border-color: rgba(255,255,255,0.05) !important;
    }

    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 24px 0 16px 0;
        border-bottom: 1px solid var(--glass-border);
        margin-bottom: 24px;
        background: linear-gradient(90deg, rgba(168,85,247,0) 0%, rgba(168,85,247,0.1) 50%, rgba(168,85,247,0) 100%);
        border-radius: 8px;
    }
    
    /* Metric Cards - Glassmorphism */
    .metric-card {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 24px 20px;
        border-radius: 16px;
        border: 1px solid var(--glass-border);
        text-align: center;
        color: #ffffff;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
    }
    
    /* Card Glow Effect */
    .metric-card::before {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 50%; height: 100%;
        background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0) 100%);
        transform: skewX(-20deg);
        transition: all 0.7s ease;
    }

    .metric-card:hover {
        transform: translateY(-6px);
        border-color: rgba(168, 85, 247, 0.4);
        box-shadow: 0 12px 40px 0 rgba(168, 85, 247, 0.15);
    }
    
    .metric-card:hover::before {
        left: 200%;
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: 700;
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.85em;
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Native Metric Override */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* Expander / Containers */
    [data-testid="stExpander"] {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    /* Tabs Customization */
    [data-testid="stTabs"] button {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        font-size: 1.1em;
        color: var(--text-secondary) !important;
        transition: all 0.3s ease;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #ffffff !important;
        background: rgba(168,85,247,0.1);
        border-bottom-color: var(--accent-purple) !important;
        border-radius: 8px 8px 0 0;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        padding: 16px 24px;
        font-size: 1.1em !important;
        font-weight: 600 !important;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1) !important;
        background: linear-gradient(135deg, var(--accent-purple) 0%, var(--accent-blue) 100%) !important;
        color: white !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 10px 30px rgba(168, 85, 247, 0.5) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }
    .stButton > button:active {
        transform: translateY(0) scale(0.98) !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.2); 
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(168,85,247,0.4); 
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(168,85,247,0.7); 
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================


def init_session():
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None
    if 'stocks' not in st.session_state:
        st.session_state.stocks = None
    if 'summary' not in st.session_state:
        st.session_state.summary = None


init_session()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def format_percentage(value):
    """Format as percentage"""
    return f"{value*100:.2f}%"


def format_currency(value):
    """Format as currency"""
    return f"${value:,.2f}"


def create_metric_card(label, value, delta=None, delta_type="normal"):
    """Create a styled metric card"""
    delta_str = ""
    delta_color = "#10b981" if delta_type == "normal" else "#ef4444"
    if delta:
        delta_str = f"<span style='color: {delta_color}; font-size: 0.9em;'>{delta}</span>"

    return f"""
    <div class='metric-card'>
        <div class='metric-label'>{label}</div>
        <div class='metric-value'>{value}</div>
        <div>{delta_str}</div>
    </div>
    """


def create_efficient_frontier_2d(results, analysis):
    """Create 2D efficient frontier scatter plot"""
    vol = np.array(results['volatility'])
    ret = np.array(results['return'])
    sharpe = np.array(results['sharpe_ratio'])

    opt_sh = analysis['optimal_portfolios']['max_sharpe']
    opt_vol = analysis['optimal_portfolios']['min_volatility']

    fig = go.Figure()

    # Background scatter - all portfolios
    fig.add_trace(go.Scatter(
        x=vol * 100,
        y=ret * 100,
        mode='markers',
        marker=dict(
            size=5,
            color=sharpe,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Sharpe Ratio", thickness=15, len=0.7),
            opacity=0.6
        ),
        text=[f"<b>Portfolio</b><br>Risk: {r:.2f}%<br>Return: {ret_val:.2f}%<br>Sharpe: {s:.4f}"
              for r, ret_val, s in zip(vol*100, ret*100, sharpe)],
        hoverinfo='text',
        name='All Portfolios'
    ))

    # Max Sharpe Ratio (red star)
    fig.add_trace(go.Scatter(
        x=[opt_sh['volatility']*100],
        y=[opt_sh['return']*100],
        mode='markers+text',
        marker=dict(size=20, color='#ef4444', symbol='star',
                    line=dict(color='white', width=2)),
        text=['Max Sharpe'],
        textposition='top center',
        name=' Max Sharpe Ratio',
        hovertemplate='<b> Max Sharpe Ratio</b><br>Risk: %{x:.2f}%<br>Return: %{y:.2f}%<extra></extra>'
    ))

    # Min Volatility (blue circle)
    fig.add_trace(go.Scatter(
        x=[opt_vol['volatility']*100],
        y=[opt_vol['return']*100],
        mode='markers+text',
        marker=dict(size=16, color='#a855f7', symbol='circle',
                    line=dict(color='white', width=2)),
        text=['Min Risk'],
        textposition='bottom center',
        name=' Minimum Risk',
        hovertemplate='<b> Minimum Risk</b><br>Risk: %{x:.2f}%<br>Return: %{y:.2f}%<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': "Efficient Frontier Simulation",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#ffffff'}
        },
        xaxis_title="Volatility (Risk) %",
        yaxis_title="Expected Return %",
        height=800,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', showgrid=True),
        hovermode='closest',
        margin=dict(l=60, r=60, t=60, b=60),
        font=dict(family='Outfit, sans-serif', size=12, color='#ffffff'),
        legend=dict(
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=0.01,
            bgcolor='rgba(17, 17, 17, 0.9)',
            bordercolor='#333333',
            borderwidth=1
        )
    )

    return fig


def create_efficient_frontier_3d(results, analysis):
    """Create 3D efficient frontier scatter plot"""
    vol = np.array(results['volatility']) * 100
    ret = np.array(results['return']) * 100
    sharpe = np.array(results['sharpe_ratio'])

    opt_sh = analysis['optimal_portfolios']['max_sharpe']
    opt_vol = analysis['optimal_portfolios']['min_volatility']

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=vol, y=ret, z=sharpe,
        mode='markers',
        marker=dict(
            size=3,
            color=sharpe,
            colorscale='Purples',
            showscale=True,
            colorbar=dict(title="Sharpe Ratio", thickness=15, len=0.7),
            opacity=0.7
        ),
        text=[f"Risk: {r:.2f}%<br>Return: {ret_val:.2f}%<br>Sharpe: {s:.4f}"
              for r, ret_val, s in zip(vol, ret, sharpe)],
        hoverinfo='text',
        name='All Portfolios'
    ))

    fig.add_trace(go.Scatter3d(
        x=[opt_sh['volatility']*100], y=[opt_sh['return']*100], z=[opt_sh['sharpe_ratio']],
        mode='markers+text',
        marker=dict(size=8, color='#ef4444', symbol='diamond'),
        text=['Max Sharpe'], textposition='top center', name='Max Sharpe Ratio'
    ))

    fig.update_layout(
        title={'text': "Efficient Frontier 3D Simulation", 'x': 0.5, 'xanchor': 'center', 'font': {'size': 18, 'color': '#ffffff'}},
        scene=dict(
            xaxis_title="Volatility %",
            yaxis_title="Return %",
            zaxis_title="Sharpe Ratio",
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', backgroundcolor='rgba(0,0,0,0)'),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', backgroundcolor='rgba(0,0,0,0)'),
            zaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', backgroundcolor='rgba(0,0,0,0)')
        ),
        height=800,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=60, b=0),
        font=dict(family='Outfit, sans-serif', size=12, color='#ffffff'),
        legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01, bgcolor='rgba(17, 17, 17, 0.9)', bordercolor='#333333', borderwidth=1)
    )
    return fig


def create_return_distribution(results, analysis):
    """Create return distribution plot"""
    ret_stats = analysis['return_statistics']

    fig = go.Figure()

    # Histogram
    fig.add_trace(go.Histogram(
        x=results['return'] * 100,
        nbinsx=40,
        name='Distribution',
        marker=dict(
            color='#a855f7',
            line=dict(color='#7e22ce', width=0.5)
        ),
        opacity=0.75
    ))

    # Mean line
    fig.add_vline(
        x=ret_stats['mean']*100,
        line_dash='solid',
        line_color='#10b981',
        annotation_text=f"Mean: {ret_stats['mean']*100:.2f}%",
        annotation_position='top right'
    )

    # Confidence interval lines
    fig.add_vline(
        x=ret_stats['ci_lower']*100,
        line_dash='dash',
        line_color='#ef4444',
        annotation_text=f"95% CI Lower: {ret_stats['ci_lower']*100:.2f}%",
        annotation_position='bottom right'
    )
    fig.add_vline(
        x=ret_stats['ci_upper']*100,
        line_dash='dash',
        line_color='#ef4444',
        annotation_text=f"95% CI Upper: {ret_stats['ci_upper']*100:.2f}%",
        annotation_position='bottom left'
    )

    fig.update_layout(
        title={
            'text': "Return Distribution",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#ffffff'}
        },
        xaxis_title="Expected Return %",
        yaxis_title="Frequency",
        height=400,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=False,
        margin=dict(l=60, r=60, t=60, b=60),
        font=dict(family='Outfit, sans-serif', size=12, color='#ffffff')
    )

    return fig


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    if st.session_state.results is None:
        # Initial Screen
        st.markdown("<h1 style='text-align: center;'>Cluster Portfolio Engine</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b;'>Advanced Monte Carlo Portfolio Optimization & Analysis</p>", unsafe_allow_html=True)
        st.divider()

        st.markdown("<div class='section-header' style='justify-content: center;'><h2>CONFIGURATION PANEL</h2></div>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("### Portfolio Strategy")
            available_stocks = config.DEFAULT_STOCKS
            selected_stocks = st.multiselect(
                "Select 5-10 stocks:",
                options=available_stocks,
                default=available_stocks[:10],
                max_selections=10
            )

            st.write("") # spacer
            
            with st.expander("⚙️ Advanced Parameters (Constraints & Simulation)", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Weight Constraints")
                    min_weight = st.number_input("Min Allocation (%):", min_value=0.0, max_value=20.0, value=0.0, step=1.0) / 100
                    max_weight = st.number_input("Max Allocation (%):", min_value=5.0, max_value=100.0, value=30.0, step=1.0) / 100

                with col2:
                    st.markdown("#### Simulation Engine")
                    num_sims = st.slider("Monte Carlo Iterations:", min_value=1000, max_value=50000, value=10000, step=1000)
                    risk_free_rate = st.number_input("Risk-Free Rate (%):", min_value=0.0, max_value=10.0, value=5.0, step=0.5) / 100
                    capital = st.number_input("Total Capital Allocation ($):", min_value=1000, max_value=10000000, value=100000, step=10000)
                
        st.markdown("<br>", unsafe_allow_html=True)
        run_optimization = st.button("RUN SIMULATION", use_container_width=True, type="primary")

        if run_optimization:
            if len(selected_stocks) < 2:
                st.error("Please select at least 2 stocks")
                return
            if max_weight <= min_weight:
                st.error("Maximum weight must be strictly greater than minimum weight")
                return
                
            with st.spinner("Running Monte Carlo Optimization Engine... Please wait!"):
                try:
                    # Fetch and process data
                    raw_data = fetch_stock_data(selected_stocks, 3)
                    clean_data, _ = validate_data(raw_data)
                    summary = get_stock_data_summary(clean_data)

                    stocks, returns, cov = prepare_data(clean_data)

                    sim = MonteCarloSimulator(returns, cov)
                    results, weights = sim.run_simulation(num_sims)

                    analytics = PortfolioAnalytics(results, weights, stocks)
                    analysis = analytics.get_full_analysis()

                    st.session_state.results = results
                    st.session_state.analysis = analysis
                    st.session_state.stocks = stocks
                    st.session_state.summary = summary
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    return

    else:
        import streamlit.components.v1 as components
        components.html(
            """
            <script>
                var mainWindow = window.parent;
                if (mainWindow) {
                    mainWindow.scrollTo(0,0);
                    var appContainer = mainWindow.document.querySelector('[data-testid="stAppViewContainer"]');
                    if (appContainer) { appContainer.scrollTo(0,0); }
                    var mainContainer = mainWindow.document.querySelector('.main');
                    if (mainContainer) { mainContainer.scrollTo(0,0); }
                }
            </script>
            """,
            height=0
        )
        
        # Results Dashboard
        col_back, col_title = st.columns([1, 4])
        with col_back:
            if st.button("← Back to Configuration", use_container_width=True):
                st.session_state.results = None
                st.session_state.analysis = None
                st.rerun()
        with col_title:
            st.markdown("<h1>Optimization Results</h1>", unsafe_allow_html=True)
            
        results = st.session_state.results
        analysis = st.session_state.analysis
        stocks = st.session_state.stocks
        
        opt = analysis['optimal_portfolios']['max_sharpe']
        opt_vol = analysis['optimal_portfolios']['min_volatility']
        ret_stats = analysis['return_statistics']
        
        tab1, tab2, tab3 = st.tabs(["Monte Carlo Analysis", "Bell Curve / Risk", "Stock Distribution"])
        
        with tab1:
            st.markdown("### Summary Metrics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(create_metric_card("Expected Return", format_percentage(opt['return']), f"+{format_percentage(opt['return'])}", "normal"), unsafe_allow_html=True)
            with col2:
                st.markdown(create_metric_card("Annual Volatility", format_percentage(opt['volatility']), f"±{format_percentage(opt['volatility'])}", "inverse"), unsafe_allow_html=True)
            with col3:
                st.markdown(create_metric_card("Sharpe Ratio", f"{opt['sharpe_ratio']:.4f}", f"Optimal", "normal"), unsafe_allow_html=True)
            with col4:
                ci_width = ret_stats['ci_width']
                st.markdown(create_metric_card("95% Confidence", f"±{format_percentage(ci_width/2)}", f"Width: {format_percentage(ci_width)}", "normal"), unsafe_allow_html=True)

            st.markdown("### Portfolio Analysis")

            fig_scatter_2d = create_efficient_frontier_2d(results, analysis)
            st.plotly_chart(fig_scatter_2d, use_container_width=True)

            st.markdown("---")

            fig_scatter_3d = create_efficient_frontier_3d(results, analysis)
            st.plotly_chart(fig_scatter_3d, use_container_width=True)
                
            st.markdown("### Portfolio Summary")
            col_sub1, col_sub2, col_sub3, col_sub4 = st.columns(4)
            with col_sub1:
                st.metric("⚡ Max Sharpe", f"{opt['sharpe_ratio']:.4f}")
            with col_sub2:
                st.metric("🛡️ Min Risk", f"{format_percentage(opt_vol['volatility'])}")
            with col_sub3:
                st.metric("🎲 Total Portfolios", f"{len(results['return']):,}")
            with col_sub4:
                st.metric("⚖️ Avg Sharpe", f"{np.mean(results['sharpe_ratio']):.4f}")

        with tab2:
            st.markdown("### Return Distribution")
            fig_dist = create_return_distribution(results, analysis)
            st.plotly_chart(fig_dist, use_container_width=True)
            
            st.info(f"**Interpretation:** There is a 95% probability that portfolio returns will lie between **{format_percentage(ret_stats['ci_lower'])}** and **{format_percentage(ret_stats['ci_upper'])}** annually. The expected return is **{format_percentage(ret_stats['mean'])}** with a standard deviation of **{format_percentage(ret_stats['std'])}**.")
            
            st.markdown("### Risk Analysis")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean Return", format_percentage(ret_stats['mean']))
            with col2:
                st.metric("Std Deviation", format_percentage(ret_stats['std']))
            with col3:
                st.metric("5th Percentile", format_percentage(ret_stats['q5']), "Worst Case")
            with col4:
                st.metric("95th Percentile", format_percentage(ret_stats['q95']), "Best Case")

        with tab3:
            st.markdown("### Optimal Portfolio Allocation")
            weights_dict = opt['weights_dict']
            allocation_dict = opt['allocation']

            col_pie, col_table = st.columns(2)
            with col_pie:
                import pandas as pd
                df_alloc = pd.DataFrame({'Stock': list(allocation_dict.keys()), 'Amount': list(allocation_dict.values())}).sort_values('Amount', ascending=False)
                import plotly.express as px
                custom_colors = ['#a855f7', '#6366f1', '#3b82f6', '#14b8a6', '#f59e0b', '#ec4899', '#8b5cf6', '#0ea5e9']
                fig_pie = px.pie(df_alloc, values='Amount', names='Stock', title="Capital Allocation", color_discrete_sequence=custom_colors)
                fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1)))
                fig_pie.update_layout(
                    font=dict(family='Outfit, sans-serif', size=12, color='#ffffff'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title={'x': 0.5, 'xanchor': 'center'}
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_table:
                df_table = pd.DataFrame({
                    'Stock': list(weights_dict.keys()),
                    'Weight (%)': [f"{w*100:.2f}%" for w in weights_dict.values()],
                    'Allocation ($)': [f"{allocation_dict[s]:,.2f}" for s in weights_dict.keys()]
                }).sort_values('Allocation ($)', key=lambda x: x.str.replace('$', '').str.replace(',', '').astype(float), ascending=False)

                st.markdown("### Allocation Breakdown")
                st.dataframe(df_table, use_container_width=True, hide_index=True)

            st.markdown("### Optimal Portfolios Comparison")
            opt_comp = analysis['optimal_portfolios']
            comp_data = {
                'Strategy': ['Max Sharpe Ratio', 'Minimum Risk', 'Maximum Return'],
                'Expected Return': [
                    format_percentage(opt_comp['max_sharpe']['return']),
                    format_percentage(opt_comp['min_volatility']['return']),
                    format_percentage(opt_comp['max_return']['return'])
                ],
                'Volatility': [
                    format_percentage(opt_comp['max_sharpe']['volatility']),
                    format_percentage(opt_comp['min_volatility']['volatility']),
                    format_percentage(opt_comp['max_return']['volatility'])
                ],
                'Sharpe Ratio': [
                    f"{opt_comp['max_sharpe']['sharpe_ratio']:.4f}",
                    f"{opt_comp['min_volatility']['sharpe_ratio']:.4f}",
                    f"{opt_comp['max_return']['sharpe_ratio']:.4f}"
                ]
            }
            df_comp = pd.DataFrame(comp_data)
            st.dataframe(df_comp, use_container_width=True, hide_index=True)



if __name__ == "__main__":
    main()
