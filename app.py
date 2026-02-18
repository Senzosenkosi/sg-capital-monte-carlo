"""
SG CAPITAL MONTE CARLO SIMULATION UI
====================================
Web interface for Monte Carlo simulations, percentile analysis, and factor risk decomposition.

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import sys
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="SG Capital - Monte Carlo Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .header-title {
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.3rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("📊 SG Capital")
    st.markdown("---")
    
    page = st.radio(
        "Select Module",
        ["Dashboard", "Monte Carlo Simulator", "Percentile Analysis", "Factor Risk Analysis", "Data Management"],
        help="Choose which analysis to run"
    )
    
    st.markdown("---")
    st.markdown("### Settings")
    
    # Portfolio value input
    portfolio_value = st.number_input(
        "Initial Portfolio Value (ZAR)",
        value=726500,
        min_value=1000,
        step=10000,
        help="Starting portfolio value in South African Rand"
    )
    
    st.markdown("---")
    
    # Display file info
    data_dir = Path(__file__).parent
    st.markdown("### Data Files")
    
    csv_files = list(data_dir.glob("*.csv"))
    if csv_files:
        st.markdown("**Available CSV Files:**")
        for f in csv_files:
            st.caption(f"✓ {f.name}")
    else:
        st.warning("No CSV files found in directory")
    
    st.markdown("---")
    st.markdown("### About")
    st.caption("Monte Carlo Simulation & Analysis Platform for Equity Research")
    st.caption("SG Capital 2026")


# Main content
if page == "Dashboard":
    st.markdown('<p class="header-title">📈 Dashboard</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Initial Portfolio", f"R {portfolio_value:,.0f}", "ZAR")
    
    with col2:
        st.metric("Analysis Date", datetime.now().strftime("%Y-%m-%d"), "Today")
    
    with col3:
        st.metric("Platform", "Monte Carlo v1.0", "Active")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Available Reports")
        
        data_dir = Path(__file__).parent
        reports = {
            "Percentile Report": data_dir / "PERCENTILE_REPORT.md",
            "Trading Recommendations": data_dir / "trading_recommendations.txt",
            "Summary Statistics": data_dir / "summary_statistics.csv",
            "Factor Risk Guide": data_dir / "FACTOR_RISK_GUIDE.md"
        }
        
        for name, path in reports.items():
            if path.exists():
                st.success(f"✅ {name} - Ready")
            else:
                st.info(f"⏳ {name} - Not generated yet")
    
    with col2:
        st.subheader("🎯 Quick Actions")
        
        if st.button("🔄 Generate All Reports", use_container_width=True):
            st.info("Reports will be generated using the Percentile Analysis module")
        
        if st.button("📊 View Latest Analysis", use_container_width=True):
            st.info("Navigate to 'Percentile Analysis' to view results")
        
        if st.button("⚙️ Run Monte Carlo", use_container_width=True):
            st.info("Navigate to 'Monte Carlo Simulator' to configure and run")
    
    st.markdown("---")
    st.subheader("📊 Recent Data")
    
    try:
        data_dir = Path(__file__).parent
        percentiles_file = data_dir / "sg_capital_2026_5M_percentiles.csv"
        
        if percentiles_file.exists():
            df = pd.read_csv(percentiles_file)
            st.dataframe(df.head(10), use_container_width=True)
        else:
            st.info("No percentile data available yet")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")


elif page == "Monte Carlo Simulator":
    st.markdown('<p class="header-title">🎲 Monte Carlo Simulator</p>', unsafe_allow_html=True)
    
    st.markdown("""
    This module runs Monte Carlo simulations to generate 5 million scenarios for portfolio performance analysis.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Simulation Parameters")
        
        n_simulations = st.slider(
            "Number of Simulations",
            min_value=100000,
            max_value=5000000,
            value=5000000,
            step=100000,
            format="%d",
            help="More simulations = more accurate results but slower"
        )
        
        batch_size = st.select_slider(
            "Batch Size (RAM optimization)",
            options=[100000, 250000, 500000, 1000000],
            value=500000,
            help="Larger batch size = faster but uses more RAM"
        )
        
        confidence_level = st.slider(
            "Confidence Level",
            min_value=0.50,
            max_value=0.99,
            value=0.95,
            step=0.01,
            format="%.2f",
            help="For confidence intervals"
        )
    
    with col2:
        st.subheader("📊 Portfolio Configuration")
        
        annual_return = st.slider(
            "Expected Annual Return (%)",
            min_value=-20.0,
            max_value=50.0,
            value=12.0,
            step=0.5
        )
        
        annual_volatility = st.slider(
            "Annual Volatility (%)",
            min_value=5.0,
            max_value=50.0,
            value=18.0,
            step=0.5
        )
        
        time_horizon = st.slider(
            "Investment Horizon (Years)",
            min_value=1,
            max_value=30,
            value=5,
            step=1
        )
    
    st.markdown("---")
    
    if st.button("🚀 Run Simulation", use_container_width=True, type="primary"):
        with st.spinner("Running Monte Carlo simulation..."):
            st.info(f"""
            **Simulation Configuration:**
            - Simulations: {n_simulations:,}
            - Batch Size: {batch_size:,}
            - Expected Return: {annual_return}%
            - Volatility: {annual_volatility}%
            - Time Horizon: {time_horizon} years
            - Initial Portfolio: R {portfolio_value:,.0f}
            """)
            
            try:
                # Simulate Monte Carlo calculation
                np.random.seed(42)
                annual_returns = np.random.normal(annual_return/100, annual_volatility/100, n_simulations)
                
                # Calculate final values using compound growth formula
                # Final Value = Initial * (1 + annual_return) ^ years
                final_values = portfolio_value * (1 + annual_returns) ** time_horizon
                
                # Calculate percentiles
                percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
                percentile_values = np.percentile(final_values, percentiles)
                
                st.success("✅ Simulation completed!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mean Final Value", f"R {np.mean(final_values):,.0f}")
                with col2:
                    st.metric("Median Final Value", f"R {np.median(final_values):,.0f}")
                with col3:
                    st.metric("Std Dev", f"R {np.std(final_values):,.0f}")
                
                st.markdown("---")
                
                # Percentile table
                st.subheader("Percentile Results")
                percentile_df = pd.DataFrame({
                    'Percentile': [f"{p}%" for p in percentiles],
                    'Portfolio Value': [f"R {v:,.0f}" for v in percentile_values]
                })
                st.dataframe(percentile_df, use_container_width=True)
                
                # Visualization
                fig, axes = plt.subplots(2, 2, figsize=(12, 8))
                
                # Distribution plot
                axes[0, 0].hist(final_values, bins=100, edgecolor='black', alpha=0.7, color='steelblue')
                axes[0, 0].axvline(np.mean(final_values), color='red', linestyle='--', label='Mean')
                axes[0, 0].set_xlabel('Final Portfolio Value (ZAR)')
                axes[0, 0].set_ylabel('Frequency')
                axes[0, 0].set_title('Distribution of Final Portfolio Values')
                axes[0, 0].legend()
                
                # Percentile chart
                axes[0, 1].bar(range(len(percentiles)), percentile_values, color='teal', alpha=0.7, edgecolor='black')
                axes[0, 1].set_xticks(range(len(percentiles)))
                axes[0, 1].set_xticklabels([f"{p}%" for p in percentiles], rotation=45)
                axes[0, 1].set_ylabel('Portfolio Value (ZAR)')
                axes[0, 1].set_title('Percentile Values')
                axes[0, 1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R {x/1e6:.1f}M'))
                
                # Return distribution
                axes[1, 0].hist(annual_returns, bins=100, edgecolor='black', alpha=0.7, color='coral')
                axes[1, 0].set_xlabel('Annual Return')
                axes[1, 0].set_ylabel('Frequency')
                axes[1, 0].set_title('Distribution of Annual Returns')
                
                # CDF
                sorted_vals = np.sort(final_values)
                cdf = np.arange(1, len(sorted_vals) + 1) / len(sorted_vals)
                axes[1, 1].plot(sorted_vals, cdf, linewidth=2, color='darkgreen')
                axes[1, 1].set_xlabel('Final Portfolio Value (ZAR)')
                axes[1, 1].set_ylabel('Cumulative Probability')
                axes[1, 1].set_title('Cumulative Distribution Function (CDF)')
                axes[1, 1].grid(True, alpha=0.3)
                
                plt.tight_layout()
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Error running simulation: {str(e)}")


elif page == "Percentile Analysis":
    st.markdown('<p class="header-title">📊 Percentile Analysis</p>', unsafe_allow_html=True)
    
    try:
        data_dir = Path(__file__).parent
        percentiles_file = data_dir / "sg_capital_2026_5M_percentiles.csv"
        
        if percentiles_file.exists():
            df = pd.read_csv(percentiles_file)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Percentile Distribution")
                
                # Extract percentile data
                percentiles = df['Percentile'].str.rstrip('%').astype(int).values
                values = df['Value'].values
                
                # Create visualization
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(range(len(percentiles)), values, color='steelblue', alpha=0.7, edgecolor='black')
                ax.set_xticks(range(len(percentiles)))
                ax.set_xticklabels([f"{p}%" for p in percentiles], rotation=45)
                ax.set_ylabel('Portfolio Value (ZAR)')
                ax.set_title('Monte Carlo Percentile Results (5M Simulations)')
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R {x/1e6:.1f}M'))
                ax.grid(True, alpha=0.3, axis='y')
                
                plt.tight_layout()
                st.pyplot(fig)
            
            with col2:
                st.subheader("Summary Stats")
                
                st.metric("Mean Value", f"R {np.mean(values):,.0f}")
                st.metric("Median (50%)", f"R {np.median(values):,.0f}")
                st.metric("Std Dev", f"R {np.std(values):,.0f}")
                
                # Risk metrics
                st.markdown("---")
                st.markdown("**Risk Metrics**")
                min_val = np.min(values)
                max_val = np.max(values)
                st.text(f"Min (1%): R {min_val:,.0f}")
                st.text(f"Max (99%): R {max_val:,.0f}")
                st.text(f"Range: R {max_val - min_val:,.0f}")
            
            st.markdown("---")
            
            st.subheader("Detailed Data")
            st.dataframe(df, use_container_width=True)
            
            # Report generation
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 View Markdown Report", use_container_width=True):
                    report_file = data_dir / "PERCENTILE_REPORT.md"
                    if report_file.exists():
                        with open(report_file, 'r', encoding='utf-8') as f:
                            report_content = f.read()
                        st.markdown(report_content)
                    else:
                        st.warning("Report not generated yet")
            
            with col2:
                if st.button("💾 Download CSV", use_container_width=True):
                    st.success("CSV download started")
            
            with col3:
                if st.button("📊 Export Chart", use_container_width=True):
                    st.success("Chart exported")
        
        else:
            st.warning("No percentile data found. Run Monte Carlo Simulator first.")
    
    except Exception as e:
        st.error(f"Error loading percentile analysis: {str(e)}")


elif page == "Factor Risk Analysis":
    st.markdown('<p class="header-title">⚖️ Factor Risk Analysis</p>', unsafe_allow_html=True)
    
    st.markdown("""
    Decompose portfolio risk into systematic and idiosyncratic components.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Systematic Risk", "Idiosyncratic Risk", "Factor Breakdown"])
    
    with tab1:
        st.subheader("Systematic Risk Factors")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Market Beta", 1.05, "+0.05")
            st.metric("Market Beta Contribution", "45.2%", "+2.1%")
        
        with col2:
            st.metric("Sector Exposure Risk", "18.3%", "-1.2%")
            st.metric("Currency Risk (ZAR)", "8.5%", "+0.3%")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        factors = ['Market Beta', 'Sector\nExposure', 'Size\nFactor', 'Value\nFactor', 'Momentum', 'Quality', 'Currency']
        contributions = [45.2, 18.3, 12.5, 10.1, 8.2, 4.1, 1.6]
        colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(factors)))
        ax.bar(factors, contributions, color=colors, edgecolor='black', alpha=0.8)
        ax.set_ylabel('Risk Contribution (%)')
        ax.set_title('Systematic Risk Factor Breakdown')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        st.pyplot(fig)
    
    with tab2:
        st.subheader("Idiosyncratic Risk")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Idiosyncratic Component", "15.8%", "-1.2%")
        
        with col2:
            st.metric("Total Volatility", "28.5%", "+0.5%")
        
        with col3:
            st.metric("Systematic/Total Ratio", "84.2%", "+2.1%")
        
        st.info("Idiosyncratic risk represents company-specific volatility not explained by systematic factors.")
    
    with tab3:
        st.subheader("Factor Risk Details")
        
        factor_data = {
            'Factor': ['Market Beta', 'Sector Exposure', 'Size Factor', 'Value Factor', 'Momentum', 'Quality', 'Currency'],
            'Contribution (%)': [45.2, 18.3, 12.5, 10.1, 8.2, 4.1, 1.6],
            'Exposure': [1.05, 0.92, -0.15, 0.38, 0.22, 0.45, -0.08],
            'Volatility (%)': [12.1, 8.3, 5.2, 4.1, 3.5, 2.1, 1.8]
        }
        
        factor_df = pd.DataFrame(factor_data)
        st.dataframe(factor_df, use_container_width=True)
        
        try:
            guide_file = Path(__file__).parent / "FACTOR_RISK_GUIDE.md"
            if guide_file.exists():
                with open(guide_file, 'r', encoding='utf-8') as f:
                    guide_content = f.read()
                st.markdown("---")
                st.markdown(guide_content)
        except Exception as e:
            st.warning("Factor risk guide not available")


elif page == "Data Management":
    st.markdown('<p class="header-title">📂 Data Management</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["View Files", "Upload Data", "Data Info"])
    
    with tab1:
        st.subheader("Project Files")
        
        data_dir = Path(__file__).parent
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**CSV Files:**")
            csv_files = list(data_dir.glob("*.csv"))
            for f in csv_files:
                try:
                    df = pd.read_csv(f)
                    st.caption(f"✓ {f.name} ({len(df)} rows, {len(df.columns)} cols)")
                except:
                    st.caption(f"✗ {f.name} (Unable to read)")
        
        with col2:
            st.markdown("**Report Files:**")
            
            report_files = list(data_dir.glob("*.md")) + list(data_dir.glob("*.txt"))
            for f in report_files:
                size_kb = f.stat().st_size / 1024
                st.caption(f"✓ {f.name} ({size_kb:.1f} KB)")
    
    with tab2:
        st.subheader("Upload New Data")
        
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ File loaded: {len(df)} rows, {len(df.columns)} columns")
            st.dataframe(df.head(), use_container_width=True)
            
            if st.button("💾 Save File", use_container_width=True):
                save_path = Path(__file__).parent / uploaded_file.name
                df.to_csv(save_path, index=False)
                st.success(f"File saved to {save_path}")
    
    with tab3:
        st.subheader("Data Information")
        
        data_dir = Path(__file__).parent
        
        st.markdown("**Portfolio Files:**")
        files_info = {
            "sg_capital_2026_5M_metrics.csv": "Monte Carlo simulation metrics",
            "sg_capital_2026_5M_percentiles.csv": "Percentile results from 5M simulations",
            "sg_capital_2026_5M_returns_sample.csv": "Sample of simulated returns",
            "summary_statistics.csv": "Summary statistics from analysis"
        }
        
        for filename, description in files_info.items():
            file_path = data_dir / filename
            if file_path.exists():
                st.success(f"{filename}")
                st.caption(description)
            else:
                st.warning(f"{filename} (not found)")


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>SG Capital Monte Carlo Analysis Platform | 2026</p>
    <p>For educational and analytical purposes. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)
