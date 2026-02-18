"""
FACTOR RISK DECOMPOSITION SYSTEM
=================================
Analyzes systematic factors and idiosyncratic risks in JSE portfolio.

Decomposes portfolio risk into:
1. Systematic Risk (Market factors)
   - Market beta
   - Sector exposures
   - Size factor (small vs large cap)
   - Value factor (value vs growth)
   - Momentum factor
   - Quality factor
   - Currency exposure (Rand strength/weakness)
   - Commodity exposure (gold, platinum)

2. Idiosyncratic Risk (Stock-specific)
   - Company-specific volatility
   - Earnings surprises
   - Management decisions
   - Regulatory risks
   - Unexplained by systematic factors

Usage:
    python factor_risk_decomposition.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class FactorRiskAnalyzer:
    """
    Comprehensive factor risk analysis for JSE portfolio
    """
    
    def __init__(self, portfolio_config: Dict):
        """
        Initialize factor analyzer
        
        Parameters:
        -----------
        portfolio_config : Dict
            Portfolio configuration with stocks, weights, and characteristics
        """
        self.portfolio = portfolio_config
        self.factor_exposures = None
        self.risk_decomposition = None
        
        print("=" * 80)
        print("FACTOR RISK DECOMPOSITION SYSTEM")
        print("=" * 80)
        print(f"\nPortfolio: {portfolio_config['tickers']}")
        print(f"Weights: {portfolio_config['weights']}")
    
    def define_factor_model(self):
        """
        Define multi-factor risk model for JSE stocks
        
        Factors:
        1. Market (JSE All Share beta)
        2. Sector (Banks, Miners, Tech, Consumer)
        3. Size (Market cap)
        4. Value (P/E, P/B ratios)
        5. Momentum (12-month return)
        6. Quality (ROE, debt/equity)
        7. Currency (Rand sensitivity)
        8. Commodity (Gold/Platinum prices)
        """
        
        # Stock characteristics (in real implementation, fetch from data)
        stock_factors = {
            'CPI': {  # Capitec
                'market_beta': 1.15,
                'sector': 'Financials',
                'sector_beta': 1.25,
                'size_factor': 0.80,  # Large cap
                'value_factor': -0.40,  # Growth stock (low P/E relative)
                'momentum_factor': 0.65,
                'quality_factor': 1.50,  # Very high ROE
                'rand_beta': 0.30,  # Domestic focused
                'commodity_beta': 0.05,
                'idiosyncratic_vol': 0.22,  # Stock-specific volatility
            },
            'FSR': {  # FirstRand
                'market_beta': 1.10,
                'sector': 'Financials',
                'sector_beta': 1.20,
                'size_factor': 0.85,
                'value_factor': 0.20,  # More value-oriented
                'momentum_factor': 0.45,
                'quality_factor': 1.20,
                'rand_beta': 0.35,
                'commodity_beta': 0.05,
                'idiosyncratic_vol': 0.18,
            },
            'NPN': {  # Naspers
                'market_beta': 1.35,
                'sector': 'Technology',
                'sector_beta': 1.60,
                'size_factor': 0.90,
                'value_factor': -0.80,  # Deep growth
                'momentum_factor': 0.30,
                'quality_factor': 0.60,
                'rand_beta': -0.50,  # Benefits from weak rand
                'commodity_beta': -0.10,
                'idiosyncratic_vol': 0.28,
            },
            'ANG': {  # AngloGold
                'market_beta': 1.25,
                'sector': 'Materials',
                'sector_beta': 1.55,
                'size_factor': 0.70,
                'value_factor': 0.30,
                'momentum_factor': 0.80,
                'quality_factor': 0.40,
                'rand_beta': -0.60,  # Benefits from weak rand
                'commodity_beta': 1.80,  # High gold exposure
                'idiosyncratic_vol': 0.32,
            },
            'IMP': {  # Impala Platinum
                'market_beta': 1.40,
                'sector': 'Materials',
                'sector_beta': 1.70,
                'size_factor': 0.50,  # Smaller cap
                'value_factor': 0.50,
                'momentum_factor': 0.60,
                'quality_factor': 0.20,  # Lower quality
                'rand_beta': -0.55,
                'commodity_beta': 1.90,  # High PGM exposure
                'idiosyncratic_vol': 0.38,
            }
        }
        
        self.stock_factors = stock_factors
        
        # Factor volatilities (annual)
        self.factor_volatilities = {
            'market': 0.18,  # JSE All Share volatility
            'financials_sector': 0.22,
            'technology_sector': 0.35,
            'materials_sector': 0.40,
            'size': 0.08,
            'value': 0.12,
            'momentum': 0.15,
            'quality': 0.10,
            'rand': 0.25,  # Rand/Dollar volatility
            'commodity': 0.35,  # Gold/Platinum volatility
        }
        
        # Factor correlations (simplified)
        self.factor_correlations = pd.DataFrame({
            'market':      [1.00, 0.70, 0.40, 0.75, 0.20, 0.15, 0.30, 0.25, -0.30, 0.40],
            'financials':  [0.70, 1.00, 0.25, 0.50, 0.15, 0.20, 0.25, 0.30, -0.20, 0.25],
            'technology':  [0.40, 0.25, 1.00, 0.30, 0.10, -0.40, 0.35, 0.15, -0.35, 0.15],
            'materials':   [0.75, 0.50, 0.30, 1.00, 0.05, 0.25, 0.20, 0.10, -0.50, 0.85],
            'size':        [0.20, 0.15, 0.10, 0.05, 1.00, 0.30, 0.15, 0.20, -0.10, 0.00],
            'value':       [0.15, 0.20, -0.40, 0.25, 0.30, 1.00, -0.25, 0.40, -0.15, 0.20],
            'momentum':    [0.30, 0.25, 0.35, 0.20, 0.15, -0.25, 1.00, 0.20, -0.20, 0.25],
            'quality':     [0.25, 0.30, 0.15, 0.10, 0.20, 0.40, 0.20, 1.00, -0.10, 0.05],
            'rand':        [-0.30, -0.20, -0.35, -0.50, -0.10, -0.15, -0.20, -0.10, 1.00, -0.60],
            'commodity':   [0.40, 0.25, 0.15, 0.85, 0.00, 0.20, 0.25, 0.05, -0.60, 1.00],
        }, index=['market', 'financials', 'technology', 'materials', 'size', 
                 'value', 'momentum', 'quality', 'rand', 'commodity'])
        
        print("\n✅ Factor model defined with 10 systematic factors")
        
        return stock_factors
    
    def calculate_portfolio_factor_exposures(self):
        """
        Calculate portfolio-level factor exposures (weighted average)
        """
        print("\n" + "=" * 80)
        print("CALCULATING PORTFOLIO FACTOR EXPOSURES")
        print("=" * 80)
        
        tickers = self.portfolio['tickers']
        weights = np.array(self.portfolio['weights'])
        
        # Initialize exposure dictionary
        exposures = {
            'market_beta': 0,
            'financials_beta': 0,
            'technology_beta': 0,
            'materials_beta': 0,
            'size_factor': 0,
            'value_factor': 0,
            'momentum_factor': 0,
            'quality_factor': 0,
            'rand_beta': 0,
            'commodity_beta': 0,
        }
        
        # Calculate weighted exposures
        for i, ticker in enumerate(tickers):
            weight = weights[i]
            factors = self.stock_factors[ticker]
            
            exposures['market_beta'] += weight * factors['market_beta']
            
            # Sector exposures
            if factors['sector'] == 'Financials':
                exposures['financials_beta'] += weight * factors['sector_beta']
            elif factors['sector'] == 'Technology':
                exposures['technology_beta'] += weight * factors['sector_beta']
            elif factors['sector'] == 'Materials':
                exposures['materials_beta'] += weight * factors['sector_beta']
            
            exposures['size_factor'] += weight * factors['size_factor']
            exposures['value_factor'] += weight * factors['value_factor']
            exposures['momentum_factor'] += weight * factors['momentum_factor']
            exposures['quality_factor'] += weight * factors['quality_factor']
            exposures['rand_beta'] += weight * factors['rand_beta']
            exposures['commodity_beta'] += weight * factors['commodity_beta']
        
        self.factor_exposures = exposures
        
        # Print exposures
        print("\nPORTFOLIO FACTOR EXPOSURES:")
        print("-" * 80)
        print(f"{'Factor':<25} {'Exposure':<15} {'Interpretation'}")
        print("-" * 80)
        
        interpretations = {
            'market_beta': lambda x: f"{'High' if x > 1.1 else 'Moderate' if x > 0.9 else 'Low'} market sensitivity",
            'financials_beta': lambda x: f"{'High' if x > 0.5 else 'Moderate' if x > 0.2 else 'Low'} bank exposure",
            'technology_beta': lambda x: f"{'High' if x > 0.5 else 'Moderate' if x > 0.2 else 'Low'} tech exposure",
            'materials_beta': lambda x: f"{'High' if x > 0.5 else 'Moderate' if x > 0.2 else 'Low'} mining exposure",
            'size_factor': lambda x: f"{'Large' if x > 0.7 else 'Mid' if x > 0.4 else 'Small'} cap tilt",
            'value_factor': lambda x: f"{'Value' if x > 0.2 else 'Balanced' if x > -0.2 else 'Growth'} orientation",
            'momentum_factor': lambda x: f"{'Strong' if x > 0.5 else 'Moderate' if x > 0.2 else 'Weak'} momentum",
            'quality_factor': lambda x: f"{'High' if x > 0.8 else 'Medium' if x > 0.4 else 'Low'} quality",
            'rand_beta': lambda x: f"{'Benefits from weak' if x < -0.2 else 'Neutral' if abs(x) <= 0.2 else 'Hurt by weak'} rand",
            'commodity_beta': lambda x: f"{'High' if x > 0.8 else 'Moderate' if x > 0.3 else 'Low'} commodity exposure",
        }
        
        for factor, exposure in exposures.items():
            interp = interpretations[factor](exposure)
            print(f"{factor:<25} {exposure:>8.2f}        {interp}")
        
        return exposures
    
    def decompose_portfolio_risk(self):
        """
        Decompose total portfolio risk into systematic and idiosyncratic components
        
        Total Variance = Systematic Variance + Idiosyncratic Variance
        """
        print("\n" + "=" * 80)
        print("DECOMPOSING PORTFOLIO RISK")
        print("=" * 80)
        
        tickers = self.portfolio['tickers']
        weights = np.array(self.portfolio['weights'])
        
        # Calculate systematic risk contribution from each factor
        factor_contributions = {}
        
        # 1. Market factor
        market_beta = self.factor_exposures['market_beta']
        market_vol = self.factor_volatilities['market']
        market_var = (market_beta * market_vol) ** 2
        factor_contributions['Market'] = market_var
        
        # 2. Sector factors
        sector_var = 0
        for sector in ['financials', 'technology', 'materials']:
            beta_key = f'{sector}_beta'
            if beta_key in self.factor_exposures:
                beta = self.factor_exposures[beta_key]
                vol = self.factor_volatilities[f'{sector}_sector']
                sector_var += (beta * vol) ** 2
        factor_contributions['Sectors'] = sector_var
        
        # 3. Style factors
        style_factors = ['size', 'value', 'momentum', 'quality']
        style_var = 0
        for factor in style_factors:
            exposure = self.factor_exposures[f'{factor}_factor']
            vol = self.factor_volatilities[factor]
            style_var += (exposure * vol) ** 2
        factor_contributions['Style'] = style_var
        
        # 4. Macro factors
        rand_beta = self.factor_exposures['rand_beta']
        rand_vol = self.factor_volatilities['rand']
        factor_contributions['Currency'] = (rand_beta * rand_vol) ** 2
        
        commodity_beta = self.factor_exposures['commodity_beta']
        commodity_vol = self.factor_volatilities['commodity']
        factor_contributions['Commodity'] = (commodity_beta * commodity_vol) ** 2
        
        # Total systematic variance (with correlations - simplified)
        total_systematic_var = sum(factor_contributions.values()) * 0.85  # Correlation adjustment
        
        # 5. Idiosyncratic risk (stock-specific)
        idiosyncratic_var = 0
        for i, ticker in enumerate(tickers):
            weight = weights[i]
            idio_vol = self.stock_factors[ticker]['idiosyncratic_vol']
            idiosyncratic_var += (weight * idio_vol) ** 2
        
        factor_contributions['Idiosyncratic'] = idiosyncratic_var
        
        # Total portfolio variance
        total_var = total_systematic_var + idiosyncratic_var
        total_vol = np.sqrt(total_var)
        
        # Calculate percentage contributions
        systematic_pct = total_systematic_var / total_var * 100
        idiosyncratic_pct = idiosyncratic_var / total_var * 100
        
        self.risk_decomposition = {
            'factor_contributions': factor_contributions,
            'total_variance': total_var,
            'total_volatility': total_vol,
            'systematic_variance': total_systematic_var,
            'systematic_volatility': np.sqrt(total_systematic_var),
            'systematic_pct': systematic_pct,
            'idiosyncratic_variance': idiosyncratic_var,
            'idiosyncratic_volatility': np.sqrt(idiosyncratic_var),
            'idiosyncratic_pct': idiosyncratic_pct,
        }
        
        # Print results
        print("\nRISK DECOMPOSITION:")
        print("-" * 80)
        print(f"Total Portfolio Volatility: {total_vol*100:.2f}%")
        print(f"\nSystematic Risk:        {np.sqrt(total_systematic_var)*100:.2f}% ({systematic_pct:.1f}% of total)")
        print(f"Idiosyncratic Risk:     {np.sqrt(idiosyncratic_var)*100:.2f}% ({idiosyncratic_pct:.1f}% of total)")
        
        print("\n" + "=" * 80)
        print("FACTOR CONTRIBUTION TO SYSTEMATIC RISK:")
        print("=" * 80)
        
        # Sort factors by contribution
        factor_vols = {k: np.sqrt(v)*100 for k, v in factor_contributions.items() if k != 'Idiosyncratic'}
        sorted_factors = sorted(factor_vols.items(), key=lambda x: x[1], reverse=True)
        
        for factor, vol in sorted_factors:
            pct_of_systematic = (factor_contributions[factor] / total_systematic_var) * 100
            pct_of_total = (factor_contributions[factor] / total_var) * 100
            print(f"{factor:<20} {vol:>6.2f}%  ({pct_of_systematic:>5.1f}% of systematic, {pct_of_total:>5.1f}% of total)")
        
        return self.risk_decomposition
    
    def calculate_marginal_risk_contributions(self):
        """
        Calculate how much risk each stock contributes to portfolio
        """
        print("\n" + "=" * 80)
        print("MARGINAL RISK CONTRIBUTION BY STOCK")
        print("=" * 80)
        
        tickers = self.portfolio['tickers']
        weights = np.array(self.portfolio['weights'])
        
        # Calculate each stock's contribution to portfolio risk
        stock_contributions = []
        
        for i, ticker in enumerate(tickers):
            weight = weights[i]
            factors = self.stock_factors[ticker]
            
            # Systematic contribution
            systematic_contrib = 0
            systematic_contrib += (weight * factors['market_beta'] * 
                                 self.factor_volatilities['market']) ** 2
            
            # Sector contribution
            if factors['sector'] == 'Financials':
                systematic_contrib += (weight * factors['sector_beta'] * 
                                     self.factor_volatilities['financials_sector']) ** 2
            elif factors['sector'] == 'Technology':
                systematic_contrib += (weight * factors['sector_beta'] * 
                                     self.factor_volatilities['technology_sector']) ** 2
            elif factors['sector'] == 'Materials':
                systematic_contrib += (weight * factors['sector_beta'] * 
                                     self.factor_volatilities['materials_sector']) ** 2
            
            # Idiosyncratic contribution
            idio_contrib = (weight * factors['idiosyncratic_vol']) ** 2
            
            # Total contribution
            total_contrib = systematic_contrib + idio_contrib
            
            stock_contributions.append({
                'Ticker': ticker,
                'Weight': weight * 100,
                'Systematic Risk': np.sqrt(systematic_contrib) * 100,
                'Idiosyncratic Risk': np.sqrt(idio_contrib) * 100,
                'Total Risk': np.sqrt(total_contrib) * 100,
                'Risk/Weight Ratio': np.sqrt(total_contrib) / weight if weight > 0 else 0,
            })
        
        df = pd.DataFrame(stock_contributions)
        
        print("\n")
        print(df.to_string(index=False))
        
        # Calculate diversification benefit
        sum_individual_variance = sum([x['Total Risk']**2 for x in stock_contributions])
        portfolio_variance = (self.risk_decomposition['total_volatility'] * 100) ** 2
        diversification_benefit = (sum_individual_variance - portfolio_variance) / sum_individual_variance * 100
        
        print(f"\n{'='*80}")
        print(f"Diversification Benefit: {diversification_benefit:.1f}%")
        print(f"(Risk reduced by {diversification_benefit:.1f}% due to diversification)")
        
        return df
    
    def identify_risk_concentrations(self):
        """
        Identify where risks are concentrated
        """
        print("\n" + "=" * 80)
        print("RISK CONCENTRATION ANALYSIS")
        print("=" * 80)
        
        exposures = self.factor_exposures
        decomp = self.risk_decomposition
        
        # Check for concerning concentrations
        warnings = []
        
        # Market beta
        if exposures['market_beta'] > 1.3:
            warnings.append(f"⚠️  HIGH MARKET BETA ({exposures['market_beta']:.2f}): Portfolio is {(exposures['market_beta']-1)*100:.0f}% more volatile than market")
        
        # Sector concentrations
        if exposures['financials_beta'] > 0.6:
            warnings.append(f"⚠️  HIGH FINANCIALS EXPOSURE ({exposures['financials_beta']:.2f}): Vulnerable to interest rate changes")
        
        if exposures['materials_beta'] > 0.6:
            warnings.append(f"⚠️  HIGH MATERIALS EXPOSURE ({exposures['materials_beta']:.2f}): Vulnerable to commodity price swings")
        
        # Commodity exposure
        if abs(exposures['commodity_beta']) > 1.0:
            warnings.append(f"⚠️  HIGH COMMODITY EXPOSURE ({exposures['commodity_beta']:.2f}): Gold/PGM prices are major driver")
        
        # Currency exposure
        if abs(exposures['rand_beta']) > 0.4:
            direction = "weak" if exposures['rand_beta'] < 0 else "strong"
            warnings.append(f"⚠️  HIGH RAND SENSITIVITY ({exposures['rand_beta']:.2f}): Portfolio benefits from {direction} rand")
        
        # Quality
        if exposures['quality_factor'] < 0.5:
            warnings.append(f"⚠️  LOW QUALITY TILT ({exposures['quality_factor']:.2f}): Portfolio tilted toward lower-quality companies")
        
        # Idiosyncratic risk
        if decomp['idiosyncratic_pct'] > 40:
            warnings.append(f"⚠️  HIGH IDIOSYNCRATIC RISK ({decomp['idiosyncratic_pct']:.1f}%): Stock-specific risks dominate")
        
        if warnings:
            print("\nRISK CONCENTRATIONS IDENTIFIED:\n")
            for warning in warnings:
                print(warning)
        else:
            print("\n✅ No significant risk concentrations identified")
        
        # Provide recommendations
        print("\n" + "=" * 80)
        print("RISK MANAGEMENT RECOMMENDATIONS")
        print("=" * 80)
        
        recommendations = []
        
        if exposures['market_beta'] > 1.2:
            recommendations.append("• Consider adding low-beta stocks or bonds to reduce market sensitivity")
        
        if exposures['commodity_beta'] > 0.8:
            recommendations.append("• Add non-commodity stocks to reduce exposure to gold/PGM prices")
        
        if decomp['idiosyncratic_pct'] > 35:
            recommendations.append("• Diversify further to reduce stock-specific risk")
        
        if exposures['quality_factor'] < 0.6:
            recommendations.append("• Consider increasing allocation to higher-quality companies")
        
        if abs(exposures['rand_beta']) > 0.4:
            recommendations.append("• Consider currency hedging or adding rand-neutral stocks")
        
        if recommendations:
            print("\n" + "\n".join(recommendations))
        else:
            print("\n✅ Portfolio is well-balanced across risk factors")
        
        return warnings
    
    def generate_visualization(self, output_file='factor_risk_analysis.png'):
        """
        Create comprehensive visualization
        """
        print(f"\n{'='*80}")
        print("GENERATING VISUALIZATIONS")
        print(f"{'='*80}")
        
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
        
        # 1. Factor exposures radar chart
        ax1 = fig.add_subplot(gs[0, :2], projection='polar')
        
        factors = ['Market', 'Financials', 'Technology', 'Materials', 
                  'Size', 'Value', 'Momentum', 'Quality', 'Currency', 'Commodity']
        exposures_list = [
            self.factor_exposures['market_beta'],
            self.factor_exposures['financials_beta'],
            self.factor_exposures['technology_beta'],
            self.factor_exposures['materials_beta'],
            self.factor_exposures['size_factor'],
            self.factor_exposures['value_factor'],
            self.factor_exposures['momentum_factor'],
            self.factor_exposures['quality_factor'],
            self.factor_exposures['rand_beta'],
            self.factor_exposures['commodity_beta'],
        ]
        
        # Normalize for radar chart
        angles = np.linspace(0, 2 * np.pi, len(factors), endpoint=False).tolist()
        exposures_list += exposures_list[:1]
        angles += angles[:1]
        
        ax1.plot(angles, exposures_list, 'o-', linewidth=2, color='darkblue')
        ax1.fill(angles, exposures_list, alpha=0.25, color='blue')
        ax1.set_xticks(angles[:-1])
        ax1.set_xticklabels(factors, fontsize=9)
        ax1.set_ylim(-1, 2)
        ax1.set_title('PORTFOLIO FACTOR EXPOSURES', fontsize=12, fontweight='bold', pad=20)
        ax1.grid(True)
        
        # 2. Risk decomposition pie chart
        ax2 = fig.add_subplot(gs[0, 2])
        
        systematic_pct = self.risk_decomposition['systematic_pct']
        idiosyncratic_pct = self.risk_decomposition['idiosyncratic_pct']
        
        colors = ['#FF6B6B', '#4ECDC4']
        wedges, texts, autotexts = ax2.pie(
            [systematic_pct, idiosyncratic_pct],
            labels=['Systematic\nRisk', 'Idiosyncratic\nRisk'],
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 10, 'weight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
        
        ax2.set_title('TOTAL RISK BREAKDOWN', fontsize=12, fontweight='bold')
        
        # 3. Factor contribution to systematic risk
        ax3 = fig.add_subplot(gs[1, :])
        
        factor_contribs = self.risk_decomposition['factor_contributions']
        factor_vols = {k: np.sqrt(v)*100 for k, v in factor_contribs.items() 
                      if k != 'Idiosyncratic'}
        
        sorted_factors = sorted(factor_vols.items(), key=lambda x: x[1], reverse=True)
        factor_names = [f[0] for f in sorted_factors]
        factor_values = [f[1] for f in sorted_factors]
        
        colors_bar = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(factor_names)))
        bars = ax3.barh(factor_names, factor_values, color=colors_bar, edgecolor='black')
        
        # Add value labels
        for bar, val in zip(bars, factor_values):
            width = bar.get_width()
            ax3.text(width + 0.3, bar.get_y() + bar.get_height()/2.,
                    f'{val:.2f}%', ha='left', va='center', fontsize=10, fontweight='bold')
        
        ax3.set_xlabel('Volatility Contribution (%)', fontsize=11, fontweight='bold')
        ax3.set_title('SYSTEMATIC RISK FACTOR CONTRIBUTIONS', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='x')
        
        # 4. Stock-level risk contributions
        ax4 = fig.add_subplot(gs[2, 0])
        
        tickers = self.portfolio['tickers']
        weights = np.array(self.portfolio['weights']) * 100
        
        systematic_risks = []
        idio_risks = []
        
        for ticker in tickers:
            factors = self.stock_factors[ticker]
            weight = self.portfolio['weights'][self.portfolio['tickers'].index(ticker)]
            
            # Approximate systematic risk
            sys_risk = weight * factors['market_beta'] * self.factor_volatilities['market'] * 100
            systematic_risks.append(sys_risk)
            
            # Idiosyncratic risk
            idio_risk = weight * factors['idiosyncratic_vol'] * 100
            idio_risks.append(idio_risk)
        
        x = np.arange(len(tickers))
        width = 0.35
        
        bars1 = ax4.bar(x - width/2, systematic_risks, width, label='Systematic', 
                       color='#FF6B6B', edgecolor='black')
        bars2 = ax4.bar(x + width/2, idio_risks, width, label='Idiosyncratic',
                       color='#4ECDC4', edgecolor='black')
        
        ax4.set_xlabel('Stock', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Risk Contribution (%)', fontsize=11, fontweight='bold')
        ax4.set_title('RISK CONTRIBUTION BY STOCK', fontsize=12, fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels(tickers, fontsize=10)
        ax4.legend()
        ax4.grid(True, alpha=0.3, axis='y')
        
        # 5. Weight vs Risk scatter
        ax5 = fig.add_subplot(gs[2, 1])
        
        total_risks = np.array(systematic_risks) + np.array(idio_risks)
        
        scatter = ax5.scatter(weights, total_risks, s=200, c=total_risks, 
                            cmap='RdYlGn_r', edgecolors='black', linewidth=2)
        
        # Add labels
        for i, ticker in enumerate(tickers):
            ax5.annotate(ticker, (weights[i], total_risks[i]), 
                        textcoords="offset points", xytext=(0,10),
                        ha='center', fontsize=10, fontweight='bold')
        
        # Add diagonal line (proportional risk)
        max_val = max(max(weights), max(total_risks))
        ax5.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, label='Proportional')
        
        ax5.set_xlabel('Portfolio Weight (%)', fontsize=11, fontweight='bold')
        ax5.set_ylabel('Risk Contribution (%)', fontsize=11, fontweight='bold')
        ax5.set_title('WEIGHT vs RISK CONTRIBUTION', fontsize=12, fontweight='bold')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Summary table
        ax6 = fig.add_subplot(gs[2, 2])
        ax6.axis('off')
        
        table_data = [
            ['Total Volatility', f"{self.risk_decomposition['total_volatility']*100:.2f}%"],
            ['Systematic Vol', f"{self.risk_decomposition['systematic_volatility']*100:.2f}%"],
            ['Idiosyncratic Vol', f"{self.risk_decomposition['idiosyncratic_volatility']*100:.2f}%"],
            ['', ''],
            ['Market Beta', f"{self.factor_exposures['market_beta']:.2f}"],
            ['Quality Factor', f"{self.factor_exposures['quality_factor']:.2f}"],
            ['Commodity Beta', f"{self.factor_exposures['commodity_beta']:.2f}"],
            ['Currency Beta', f"{self.factor_exposures['rand_beta']:.2f}"],
        ]
        
        table = ax6.table(cellText=table_data, cellLoc='left', loc='center',
                         colLabels=['Metric', 'Value'], bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2.5)
        
        for i in range(2):
            table[(0, i)].set_facecolor('#2C3E50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        plt.suptitle('FACTOR RISK DECOMPOSITION ANALYSIS\nSystematic vs Idiosyncratic Risk', 
                    fontsize=14, fontweight='bold', y=0.995)
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Saved visualization: {output_file}")
        
        return output_file
    
    def generate_report(self, output_file='factor_risk_report.txt'):
        """
        Generate comprehensive text report
        """
        print(f"✅ Generating report: {output_file}")
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║              FACTOR RISK DECOMPOSITION REPORT                        ║
║         Systematic and Idiosyncratic Risk Analysis                   ║
╚══════════════════════════════════════════════════════════════════════╝

Portfolio: {', '.join(self.portfolio['tickers'])}
Weights: {[f'{w*100:.1f}%' for w in self.portfolio['weights']]}

═══════════════════════════════════════════════════════════════════════

📊 RISK DECOMPOSITION SUMMARY

Total Portfolio Volatility: {self.risk_decomposition['total_volatility']*100:.2f}%

Systematic Risk:      {self.risk_decomposition['systematic_volatility']*100:.2f}% 
                     ({self.risk_decomposition['systematic_pct']:.1f}% of total variance)

Idiosyncratic Risk:   {self.risk_decomposition['idiosyncratic_volatility']*100:.2f}%
                     ({self.risk_decomposition['idiosyncratic_pct']:.1f}% of total variance)

═══════════════════════════════════════════════════════════════════════

🎯 PORTFOLIO FACTOR EXPOSURES

Market Beta:          {self.factor_exposures['market_beta']:.2f}
                     → Portfolio is {abs(self.factor_exposures['market_beta']-1)*100:.0f}% {'more' if self.factor_exposures['market_beta'] > 1 else 'less'} volatile than JSE All Share

Sector Exposures:
  Financials:         {self.factor_exposures['financials_beta']:.2f}
  Technology:         {self.factor_exposures['technology_beta']:.2f}
  Materials:          {self.factor_exposures['materials_beta']:.2f}

Style Factors:
  Size (Large Cap):   {self.factor_exposures['size_factor']:.2f}
  Value/Growth:       {self.factor_exposures['value_factor']:.2f} ({'Value' if self.factor_exposures['value_factor'] > 0 else 'Growth'} tilt)
  Momentum:           {self.factor_exposures['momentum_factor']:.2f}
  Quality:            {self.factor_exposures['quality_factor']:.2f}

Macro Exposures:
  Currency (Rand):    {self.factor_exposures['rand_beta']:.2f}
                     → {'Benefits from weak' if self.factor_exposures['rand_beta'] < 0 else 'Hurt by weak'} rand
  Commodity (Au/Pt):  {self.factor_exposures['commodity_beta']:.2f}
                     → {'High' if abs(self.factor_exposures['commodity_beta']) > 1 else 'Moderate'} exposure to precious metals

═══════════════════════════════════════════════════════════════════════

📈 SYSTEMATIC RISK BREAKDOWN

"""
        
        # Add factor contributions
        factor_contribs = self.risk_decomposition['factor_contributions']
        factor_vols = {k: np.sqrt(v)*100 for k, v in factor_contribs.items() 
                      if k != 'Idiosyncratic'}
        sorted_factors = sorted(factor_vols.items(), key=lambda x: x[1], reverse=True)
        
        for factor, vol in sorted_factors:
            pct = (factor_contribs[factor] / self.risk_decomposition['systematic_variance']) * 100
            report += f"{factor:<20} {vol:>6.2f}%  ({pct:>5.1f}% of systematic risk)\n"
        
        report += f"""
═══════════════════════════════════════════════════════════════════════

💡 KEY INSIGHTS

1. RISK COMPOSITION
   • Your portfolio has {self.risk_decomposition['systematic_pct']:.0f}% systematic risk
   • This means {self.risk_decomposition['systematic_pct']:.0f}% of volatility comes from market factors
   • The remaining {self.risk_decomposition['idiosyncratic_pct']:.0f}% is stock-specific risk

2. DIVERSIFICATION LEVEL
   • {"Well diversified" if self.risk_decomposition['idiosyncratic_pct'] < 30 else "Moderately diversified" if self.risk_decomposition['idiosyncratic_pct'] < 40 else "Under-diversified"}
   • Idiosyncratic risk of {self.risk_decomposition['idiosyncratic_pct']:.0f}% is {"low" if self.risk_decomposition['idiosyncratic_pct'] < 25 else "moderate" if self.risk_decomposition['idiosyncratic_pct'] < 35 else "high"}
   • {"Can reduce further by adding more stocks" if self.risk_decomposition['idiosyncratic_pct'] > 30 else "Already well-diversified"}

3. FACTOR CONCENTRATIONS
"""
        
        # Add warnings about concentrations
        if self.factor_exposures['commodity_beta'] > 0.8:
            report += f"   ⚠️  HIGH COMMODITY EXPOSURE ({self.factor_exposures['commodity_beta']:.2f})\n"
            report += "      Gold/Platinum prices are a major portfolio driver\n"
        
        if abs(self.factor_exposures['rand_beta']) > 0.3:
            report += f"   ⚠️  SIGNIFICANT RAND SENSITIVITY ({self.factor_exposures['rand_beta']:.2f})\n"
            report += "      Portfolio heavily influenced by USD/ZAR moves\n"
        
        if self.factor_exposures['market_beta'] > 1.2:
            report += f"   ⚠️  HIGH MARKET BETA ({self.factor_exposures['market_beta']:.2f})\n"
            report += f"      Portfolio {(self.factor_exposures['market_beta']-1)*100:.0f}% more volatile than market\n"
        
        report += f"""
═══════════════════════════════════════════════════════════════════════

🎯 RISK MANAGEMENT RECOMMENDATIONS

IMMEDIATE ACTIONS:
"""
        
        # Add specific recommendations
        if self.risk_decomposition['idiosyncratic_pct'] > 35:
            report += "\n  1. DIVERSIFY FURTHER\n"
            report += "     • Add 2-3 more stocks to reduce idiosyncratic risk\n"
            report += "     • Target: Bring idiosyncratic risk below 30%\n"
        
        if self.factor_exposures['commodity_beta'] > 1.0:
            report += "\n  2. REDUCE COMMODITY CONCENTRATION\n"
            report += "     • Trim mining exposure (ANG, IMP)\n"
            report += "     • Add non-commodity stocks (retailers, industrials)\n"
        
        if self.factor_exposures['market_beta'] > 1.2:
            report += "\n  3. LOWER MARKET BETA\n"
            report += "     • Add low-beta defensive stocks\n"
            report += "     • Consider bonds for portfolio ballast\n"
        
        if abs(self.factor_exposures['rand_beta']) > 0.4:
            report += "\n  4. HEDGE CURRENCY RISK\n"
            report += "     • Consider rand hedging strategies\n"
            report += "     • Add more rand-neutral stocks\n"
        
        if self.factor_exposures['quality_factor'] < 0.6:
            report += "\n  5. IMPROVE QUALITY\n"
            report += "     • Increase allocation to high-ROE companies\n"
            report += "     • Reduce exposure to lower-quality names\n"
        
        report += """

MONITORING CHECKLIST:
□ Track factor exposures monthly
□ Rebalance when exposures drift >20%
□ Monitor commodity prices (if high exposure)
□ Track USD/ZAR (if high currency sensitivity)
□ Review idiosyncratic risk quarterly
□ Stress test against factor shocks

═══════════════════════════════════════════════════════════════════════

Generated by Factor Risk Decomposition System
For portfolio risk management and analysis purposes
"""
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        print(f"✅ Saved report: {output_file}")
        return output_file
    
    def run_complete_analysis(self):
        """
        Run complete factor risk analysis
        """
        # Define factor model
        self.define_factor_model()
        
        # Calculate exposures
        self.calculate_portfolio_factor_exposures()
        
        # Decompose risk
        self.decompose_portfolio_risk()
        
        # Marginal contributions
        self.calculate_marginal_risk_contributions()
        
        # Identify concentrations
        self.identify_risk_concentrations()
        
        # Generate outputs
        self.generate_visualization()
        self.generate_report()
        
        print(f"\n{'='*80}")
        print("✅ FACTOR RISK ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print("\nGenerated files:")
        print("  • factor_risk_analysis.png")
        print("  • factor_risk_report.txt")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    
    # S.G Capital 2026 Portfolio
    portfolio_config = {
        'tickers': ['CPI', 'FSR', 'NPN', 'ANG', 'IMP'],
        'weights': [0.25, 0.25, 0.20, 0.15, 0.15],
    }
    
    # Run analysis
    analyzer = FactorRiskAnalyzer(portfolio_config)
    analyzer.run_complete_analysis()
    
    print("\n🎉 Factor risk decomposition complete!")
    print("\nUse this analysis to:")
    print("  1. Understand where your risk comes from")
    print("  2. Identify concentration risks")
    print("  3. Make informed rebalancing decisions")
    print("  4. Hedge specific factor exposures")
