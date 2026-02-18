"""
PERCENTILE REPORT GENERATOR
===========================
Automatically generates comprehensive analysis from Monte Carlo percentile results.

Usage:
    python generate_percentile_report.py <percentiles_csv> <initial_portfolio_value>
    
Example:
    python generate_percentile_report.py sg_capital_2026_5M_percentiles.csv 726500

Output:
    - percentile_analysis.png (visualization)
    - PERCENTILE_REPORT.md (detailed analysis)
    - trading_recommendations.txt (actionable advice)
    - summary_statistics.csv (key metrics)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import sys
import os

class PercentileReportGenerator:
    """
    Generate comprehensive percentile analysis report
    """
    
    def __init__(self, percentiles_csv: str, initial_portfolio_value: float):
        """
        Initialize report generator
        
        Parameters:
        -----------
        percentiles_csv : str
            Path to percentiles CSV file
        initial_portfolio_value : float
            Initial portfolio value in Rands
        """
        self.df = pd.read_csv(percentiles_csv)
        self.initial_value = initial_portfolio_value
        self.report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Parse percentiles and returns
        self.percentiles = self.df['Percentile'].str.rstrip('%').astype(int).values
        self.returns = self.df['Value'].values
        
        print(f"✅ Loaded percentile data: {len(self.df)} percentiles")
        print(f"📊 Initial Portfolio Value: R{initial_portfolio_value:,.0f}")
    
    def calculate_metrics(self):
        """Calculate comprehensive metrics"""
        median_idx = np.where(self.percentiles == 50)[0][0]
        median_return = self.returns[median_idx]
        
        # Find closest percentile to 0% return for probability of loss
        returns_pct = self.returns * 100
        prob_loss_pct = np.interp(0, returns_pct, self.percentiles)
        
        # Calculate dollar values
        final_values = self.initial_value * (1 + self.returns)
        gains_losses = final_values - self.initial_value
        
        metrics = {
            'median_return': median_return * 100,
            'median_final_value': self.initial_value * (1 + median_return),
            'prob_loss': prob_loss_pct,
            'prob_profit': 100 - prob_loss_pct,
            'var_95': self.returns[np.where(self.percentiles == 5)[0][0]] * 100,
            'var_99': self.returns[np.where(self.percentiles == 1)[0][0]] * 100,
            'best_case': self.returns[-1] * 100,
            'worst_case': self.returns[0] * 100,
            'range': (self.returns[-1] - self.returns[0]) * 100,
            'iqr': (self.returns[np.where(self.percentiles == 75)[0][0]] - 
                   self.returns[np.where(self.percentiles == 25)[0][0]]) * 100,
            'final_values': final_values,
            'gains_losses': gains_losses
        }
        
        self.metrics = metrics
        return metrics
    
    def generate_visualization(self, output_file='percentile_analysis.png'):
        """Generate comprehensive visualization"""
        print(f"\n{'='*70}")
        print("GENERATING VISUALIZATION")
        print(f"{'='*70}")
        
        fig = plt.figure(figsize=(18, 14))
        gs = fig.add_gridspec(4, 2, hspace=0.4, wspace=0.3)
        
        # Color scheme
        colors = {
            'extreme_loss': '#8B0000',
            'loss': '#DC143C',
            'neutral': '#FFD700',
            'profit': '#32CD32',
            'extreme_profit': '#006400'
        }
        
        returns_pct = self.returns * 100
        
        # 1. Main percentile bar chart
        ax1 = fig.add_subplot(gs[0, :])
        
        bar_colors = []
        for ret in returns_pct:
            if ret < -20:
                bar_colors.append(colors['extreme_loss'])
            elif ret < 0:
                bar_colors.append(colors['loss'])
            elif ret < 20:
                bar_colors.append(colors['neutral'])
            elif ret < 50:
                bar_colors.append(colors['profit'])
            else:
                bar_colors.append(colors['extreme_profit'])
        
        bars = ax1.bar(range(len(self.percentiles)), returns_pct, 
                      color=bar_colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, returns_pct)):
            height = bar.get_height()
            y_pos = height + (5 if height > 0 else -10)
            ax1.text(bar.get_x() + bar.get_width()/2., y_pos,
                    f'{val:.1f}%', ha='center', va='bottom' if height > 0 else 'top',
                    fontsize=11, fontweight='bold')
        
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=2, alpha=0.7)
        ax1.axhline(y=self.metrics['median_return'], color='blue', 
                   linestyle='--', linewidth=2, alpha=0.7, 
                   label=f"Median: {self.metrics['median_return']:.1f}%")
        
        ax1.set_xlabel('Percentile', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Return (%)', fontsize=12, fontweight='bold')
        ax1.set_title('RETURN DISTRIBUTION BY PERCENTILE\n5 Million Monte Carlo Simulations', 
                     fontsize=14, fontweight='bold', pad=20)
        ax1.set_xticks(range(len(self.percentiles)))
        ax1.set_xticklabels([f'{p}%' for p in self.percentiles], fontsize=10)
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.legend(loc='upper left', fontsize=11)
        
        # 2. Cumulative probability
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.plot(returns_pct, self.percentiles, linewidth=3, 
                color='darkblue', marker='o', markersize=8)
        ax2.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Break-even')
        ax2.axhline(y=50, color='black', linestyle='--', linewidth=1.5, 
                   alpha=0.5, label='Median')
        ax2.axvline(x=self.metrics['var_95'], color='darkred', 
                   linestyle='--', linewidth=2, label=f"VaR 95%: {self.metrics['var_95']:.1f}%")
        
        ax2.fill_betweenx([0, 5], returns_pct.min(), 0, 
                         alpha=0.2, color='red', label='Worst 5%')
        ax2.fill_betweenx([95, 100], 0, returns_pct.max(), 
                         alpha=0.2, color='green', label='Best 5%')
        
        ax2.set_xlabel('Return (%)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Percentile', fontsize=12, fontweight='bold')
        ax2.set_title('CUMULATIVE PROBABILITY', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(loc='lower right', fontsize=9)
        
        # 3. Probability zones pie chart
        ax3 = fig.add_subplot(gs[1, 1])
        
        # Calculate probabilities for each zone
        zones = []
        zone_labels = []
        zone_colors = []
        
        for i in range(len(self.percentiles) - 1):
            prob = self.percentiles[i+1] - self.percentiles[i]
            ret = returns_pct[i]
            
            if ret < -20:
                label = f'Extreme Loss\n(<-20%)'
                color = colors['extreme_loss']
            elif ret < 0:
                label = f'Loss\n(-20% to 0%)'
                color = colors['loss']
            elif ret < 50:
                label = f'Moderate Gain\n(0% to 50%)'
                color = colors['neutral']
            elif ret < 100:
                label = f'Strong Gain\n(50% to 100%)'
                color = colors['profit']
            else:
                label = f'Exceptional\n(>100%)'
                color = colors['extreme_profit']
            
            # Aggregate same zones
            if label in zone_labels:
                idx = zone_labels.index(label)
                zones[idx] += prob
            else:
                zone_labels.append(label)
                zones.append(prob)
                zone_colors.append(color)
        
        wedges, texts, autotexts = ax3.pie(zones, labels=zone_labels, 
                                           colors=zone_colors, autopct='%1.0f%%',
                                           startangle=90, 
                                           textprops={'fontsize': 10, 'weight': 'bold'})
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_weight('bold')
        
        ax3.set_title('PROBABILITY DISTRIBUTION', fontsize=12, fontweight='bold')
        
        # 4. Portfolio value outcomes
        ax4 = fig.add_subplot(gs[2, 0])
        
        final_values = self.metrics['final_values'] / 1000  # Convert to thousands
        
        ax4.barh(range(len(self.percentiles)), final_values, color=bar_colors, 
                edgecolor='black', linewidth=1)
        ax4.axvline(x=self.initial_value/1000, color='black', 
                   linestyle='--', linewidth=2, label=f'Initial: R{self.initial_value/1000:.0f}K')
        ax4.axvline(x=self.metrics['median_final_value']/1000, color='blue',
                   linestyle='--', linewidth=2, 
                   label=f"Median: R{self.metrics['median_final_value']/1000:.0f}K")
        
        ax4.set_xlabel('Portfolio Value (R Thousands)', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Percentile', fontsize=12, fontweight='bold')
        ax4.set_title('PORTFOLIO VALUE OUTCOMES', fontsize=12, fontweight='bold')
        ax4.set_yticks(range(len(self.percentiles)))
        ax4.set_yticklabels([f'{p}%' for p in self.percentiles], fontsize=9)
        ax4.grid(True, alpha=0.3, axis='x')
        ax4.legend(loc='lower right', fontsize=10)
        
        # 5. Gain/Loss distribution
        ax5 = fig.add_subplot(gs[2, 1])
        
        gains_losses = self.metrics['gains_losses'] / 1000
        gain_colors = ['red' if gl < 0 else 'green' for gl in gains_losses]
        
        ax5.barh(range(len(self.percentiles)), gains_losses, color=gain_colors,
                edgecolor='black', linewidth=1, alpha=0.7)
        ax5.axvline(x=0, color='black', linestyle='-', linewidth=2)
        
        ax5.set_xlabel('Gain/Loss (R Thousands)', fontsize=12, fontweight='bold')
        ax5.set_ylabel('Percentile', fontsize=12, fontweight='bold')
        ax5.set_title('GAIN/LOSS BY PERCENTILE', fontsize=12, fontweight='bold')
        ax5.set_yticks(range(len(self.percentiles)))
        ax5.set_yticklabels([f'{p}%' for p in self.percentiles], fontsize=9)
        ax5.grid(True, alpha=0.3, axis='x')
        
        # 6. Summary table
        ax6 = fig.add_subplot(gs[3, :])
        ax6.axis('off')
        
        table_data = []
        for i, pct in enumerate(self.percentiles):
            ret = returns_pct[i]
            final_val = self.metrics['final_values'][i]
            gain_loss = self.metrics['gains_losses'][i]
            
            table_data.append([
                f'{pct}%',
                f'{ret:.2f}%',
                f'R{final_val:,.0f}',
                f"{'+'if gain_loss >= 0 else ''}R{gain_loss:,.0f}"
            ])
        
        table = ax6.table(
            cellText=table_data,
            colLabels=['Percentile', 'Return', 'Final Value', 'Gain/Loss'],
            cellLoc='center',
            loc='center',
            bbox=[0, 0, 1, 1]
        )
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2.5)
        
        # Style header
        for i in range(4):
            table[(0, i)].set_facecolor('#2C3E50')
            table[(0, i)].set_text_props(weight='bold', color='white', fontsize=11)
        
        # Color code rows
        for i in range(1, len(table_data) + 1):
            return_val = float(table_data[i-1][1].rstrip('%'))
            
            if return_val < -20:
                color = '#FFE6E6'
            elif return_val < 0:
                color = '#FFF4E6'
            elif return_val < 50:
                color = '#FFFFCC'
            elif return_val < 100:
                color = '#E6FFE6'
            else:
                color = '#CCFFCC'
            
            for j in range(4):
                table[(i, j)].set_facecolor(color)
        
        plt.suptitle('MONTE CARLO PERCENTILE ANALYSIS\nComprehensive Risk & Return Assessment', 
                    fontsize=16, fontweight='bold', y=0.998)
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Saved visualization: {output_file}")
        
        return output_file
    
    def generate_markdown_report(self, output_file='PERCENTILE_REPORT.md'):
        """Generate detailed markdown report"""
        print(f"✅ Generating markdown report: {output_file}")
        
        report = f"""# PERCENTILE ANALYSIS REPORT
**Generated:** {self.report_date}
**Initial Portfolio Value:** R{self.initial_value:,.0f}

---

## Executive Summary

Based on **5 million Monte Carlo simulations**, your portfolio shows:

- **Median Return:** {self.metrics['median_return']:.2f}%
- **Expected Final Value:** R{self.metrics['median_final_value']:,.0f}
- **Probability of Profit:** {self.metrics['prob_profit']:.1f}%
- **Probability of Loss:** {self.metrics['prob_loss']:.1f}%
- **Value at Risk (95%):** {self.metrics['var_95']:.2f}%
- **Worst Case Scenario:** {self.metrics['worst_case']:.2f}%
- **Best Case Scenario:** {self.metrics['best_case']:.2f}%

---

## Percentile Breakdown

"""
        
        # Add each percentile
        for i, pct in enumerate(self.percentiles):
            ret = self.returns[i] * 100
            final_val = self.metrics['final_values'][i]
            gain_loss = self.metrics['gains_losses'][i]
            
            report += f"""### {pct}% Percentile: {ret:.2f}% Return

**Final Portfolio Value:** R{final_val:,.0f}  
**Gain/Loss:** {'+'if gain_loss >= 0 else ''}R{gain_loss:,.0f}

"""
            
            # Add interpretation
            if pct == 1:
                report += """**Interpretation:** Catastrophic scenario - worst 1% of outcomes. 
This represents extreme market stress with multiple simultaneous failures.

"""
            elif pct == 5:
                report += """**Interpretation:** This is your **Value at Risk (VaR) at 95% confidence**. 
In 19 out of 20 years, you will do better than this. Use this for:
- Setting stop losses
- Determining position sizes
- Regulatory capital requirements

"""
            elif pct == 25:
                report += """**Interpretation:** Lower quartile - 75% of outcomes are better than this.
This represents a disappointing year but still potentially profitable.

"""
            elif pct == 50:
                report += """**Interpretation:** **MEDIAN** - The most representative single outcome.
This is what you should plan around. 50% chance of better, 50% chance of worse.

"""
            elif pct == 75:
                report += """**Interpretation:** Upper quartile - this is a good year.
Only 25% of outcomes exceed this. Consider taking profits if you reach this level.

"""
            elif pct == 90:
                report += """**Interpretation:** Top 10% - exceptional performance.
This represents everything going right. If you reach this, aggressively take profits.

"""
            elif pct == 95:
                report += """**Interpretation:** Top 5% - outstanding results.
Only 1 in 20 years this good. Don't expect to repeat this. Lock in gains.

"""
            elif pct == 99:
                report += """**Interpretation:** Top 1% - lightning in a bottle.
This is 99% luck, 1% skill. If this happens, sell aggressively and don't try to repeat.

"""
        
        report += f"""---

## Key Insights

### 1. Distribution Characteristics

- **Range:** {self.metrics['range']:.1f} percentage points (from {self.metrics['worst_case']:.1f}% to {self.metrics['best_case']:.1f}%)
- **Interquartile Range:** {self.metrics['iqr']:.1f} percentage points
- **Skew:** {"Positive (long right tail)" if self.metrics['best_case'] > abs(self.metrics['worst_case']) else "Negative (long left tail)"}

### 2. Risk Assessment

The portfolio has a **{self.metrics['prob_loss']:.1f}% probability of loss** (approximately 1 in {100/self.metrics['prob_loss']:.0f} years).

**Risk Levels:**
- Worst 1%: Lose more than {abs(self.metrics['var_99']):.1f}%
- Worst 5%: Lose more than {abs(self.metrics['var_95']):.1f}%
- Median: Gain {self.metrics['median_return']:.1f}%

### 3. Return Expectations

**Conservative Scenario (25th percentile):**
- Return: {self.returns[np.where(self.percentiles == 25)[0][0]]*100:.2f}%
- Final Value: R{self.metrics['final_values'][np.where(self.percentiles == 25)[0][0]]:,.0f}

**Base Case (Median):**
- Return: {self.metrics['median_return']:.2f}%
- Final Value: R{self.metrics['median_final_value']:,.0f}

**Optimistic Scenario (75th percentile):**
- Return: {self.returns[np.where(self.percentiles == 75)[0][0]]*100:.2f}%
- Final Value: R{self.metrics['final_values'][np.where(self.percentiles == 75)[0][0]]:,.0f}

---

## Trading Recommendations

### Position Sizing

Current portfolio value suggests appropriate sizing for the risk level. However, with {self.metrics['prob_loss']:.1f}% probability of loss:

**Recommended Actions:**
- Maintain 10-15% cash buffer for drawdowns
- Consider reducing highest volatility positions
- Ensure no single position exceeds 15% of portfolio

### Stop Loss Levels

Based on VaR analysis:

- **Portfolio-level stop:** {self.metrics['var_95']:.1f}% (VaR 95%)
- **Individual stock stops:** -10% to -15%
- **Emergency exit:** {self.metrics['var_99']:.1f}% (approaching 1st percentile)

### Profit Taking Strategy

**Progressive profit-taking recommended:**

| Portfolio Return | Action |
|-----------------|--------|
| <{self.returns[np.where(self.percentiles == 25)[0][0]]*100:.0f}% | Hold, potentially add |
| {self.metrics['median_return']:.0f}% (median) | Take 20% profit |
| {self.returns[np.where(self.percentiles == 75)[0][0]]*100:.0f}% (75th pct) | Take 40% profit |
| {self.returns[np.where(self.percentiles == 90)[0][0]]*100:.0f}% (90th pct) | Take 60% profit |
| >{self.returns[np.where(self.percentiles == 95)[0][0]]*100:.0f}% (95th pct) | Take 80% profit, lock in |

### Rebalancing Schedule

- **Monthly:** Monitor positions, trim if any exceeds 15%
- **Quarterly:** Full rebalancing to target weights
- **Annually:** Strategic review and adjustment

---

## Risk Monitoring Checklist

□ Track current return vs percentile distribution  
□ Monitor drawdown from portfolio peak  
□ Review correlation changes monthly  
□ Assess if VaR is increasing or decreasing  
□ Check if any positions have extreme concentration  
□ Maintain cash buffer for opportunities  
□ Review stop losses quarterly  

---

## Conclusion

Your portfolio demonstrates:

✅ **Strong median outcome** ({self.metrics['median_return']:.1f}% expected return)  
✅ **Asymmetric risk/reward** (upside exceeds downside)  
⚠️ **Significant uncertainty** ({self.metrics['range']:.0f} percentage point range)  
⚠️ **Material loss probability** ({self.metrics['prob_loss']:.1f}% chance of loss)  

**Key Message:** Plan around the median, prepare for the worst, don't count on the best.

Use these percentiles to:
1. Set realistic expectations
2. Size positions appropriately  
3. Establish intelligent stop losses
4. Take profits progressively
5. Communicate risk to stakeholders

---

**Generated by Monte Carlo Percentile Report Generator**  
*For educational and analytical purposes only. Not financial advice.*
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Saved markdown report: {output_file}")
        return output_file
    
    def generate_trading_recommendations(self, output_file='trading_recommendations.txt'):
        """Generate actionable trading recommendations"""
        print(f"✅ Generating trading recommendations: {output_file}")
        
        recommendations = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                   TRADING RECOMMENDATIONS                            ║
║              Based on Monte Carlo Percentile Analysis                ║
╚══════════════════════════════════════════════════════════════════════╝

Generated: {self.report_date}
Initial Portfolio: R{self.initial_value:,.0f}
Median Expected: R{self.metrics['median_final_value']:,.0f} ({self.metrics['median_return']:.1f}%)

═══════════════════════════════════════════════════════════════════════

📊 IMMEDIATE ACTIONS

1. SET STOP LOSSES
   └─ Portfolio-level: {self.metrics['var_95']:.1f}% (VaR 95%)
   └─ Individual stocks: -10% to -15%
   └─ Emergency exit: {self.metrics['var_99']:.1f}%

2. ESTABLISH PROFIT-TAKING RULES
   └─ At median (+{self.metrics['median_return']:.0f}%): Sell 20%
   └─ At 75th percentile (+{self.returns[np.where(self.percentiles == 75)[0][0]]*100:.0f}%): Sell 40%
   └─ At 90th percentile (+{self.returns[np.where(self.percentiles == 90)[0][0]]*100:.0f}%): Sell 60%
   └─ Above 95th percentile: Sell aggressively

3. MAINTAIN CASH BUFFER
   └─ Keep 10-15% in cash for drawdowns
   └─ With {self.metrics['prob_loss']:.1f}% loss probability, liquidity is crucial

═══════════════════════════════════════════════════════════════════════

💰 POSITION SIZING RECOMMENDATIONS

Current Risk Level: {'HIGH' if self.metrics['prob_loss'] > 30 else 'MODERATE' if self.metrics['prob_loss'] > 20 else 'LOW'}

With {self.metrics['prob_loss']:.1f}% probability of loss:
└─ Maximum position size per stock: 15%
└─ Reduce high-volatility assets (>35% annual vol)
└─ Increase low-volatility assets (<20% annual vol)
└─ Consider adding bonds/cash for balance

═══════════════════════════════════════════════════════════════════════

📈 IF YOUR YTD RETURN IS...

Below {self.metrics['var_95']:.0f}% (5th percentile):
   🚨 EMERGENCY - Reassess entire strategy
   └─ Something is fundamentally wrong
   └─ Consider cutting losses
   └─ Seek external review

Between {self.metrics['var_95']:.0f}% and 0%:
   ⚠️ BAD YEAR - But statistically normal
   └─ Stay the course, don't panic
   └─ Review positions but don't overreact
   └─ Consider averaging down on quality names

Between 0% and {self.metrics['median_return']:.0f}% (median):
   👍 BELOW TARGET - But still profitable
   └─ On track for positive year
   └─ Let strategies play out
   └─ Patience required

Between {self.metrics['median_return']:.0f}% and {self.returns[np.where(self.percentiles == 75)[0][0]]*100:.0f}%:
   🎯 MEETING/BEATING TARGET
   └─ Good performance
   └─ Start scaling out of winners
   └─ Take some chips off table

Above {self.returns[np.where(self.percentiles == 75)[0][0]]*100:.0f}% (75th percentile):
   🎉 EXCEPTIONAL YEAR
   └─ Top quartile performance
   └─ Aggressively take profits
   └─ Don't get greedy - this is rare

Above {self.returns[np.where(self.percentiles == 90)[0][0]]*100:.0f}% (90th percentile):
   🚀 LIGHTNING IN A BOTTLE
   └─ Sell 60-80% of portfolio
   └─ This won't repeat
   └─ Lock in generational gains

═══════════════════════════════════════════════════════════════════════

⚙️ REBALANCING SCHEDULE

MONTHLY (1st business day):
□ Check if any position >15% of portfolio → trim to 12%
□ Review cash position → maintain 10-15%
□ Check drawdown from peak → if >15%, review strategy

QUARTERLY (End of quarter):
□ Full rebalancing to target weights
□ Review correlation changes
□ Update return expectations
□ Assess new opportunities

ANNUALLY (Year-end):
□ Complete strategic review
□ Reassess risk tolerance
□ Update Monte Carlo assumptions
□ Plan next year's strategy

═══════════════════════════════════════════════════════════════════════

⚠️ CRITICAL WARNINGS

DO NOT:
❌ Count on achieving 95th percentile ({self.returns[np.where(self.percentiles == 95)[0][0]]*100:.0f}%)
❌ Ignore the {self.metrics['prob_loss']:.1f}% probability of loss
❌ Add leverage when things are going well
❌ Panic sell during normal corrections (<{self.returns[np.where(self.percentiles == 25)[0][0]]*100:.0f}%)
❌ Get greedy after hitting median target

DO:
✅ Plan around median outcome ({self.metrics['median_return']:.1f}%)
✅ Respect stop losses (VaR 95% = {self.metrics['var_95']:.1f}%)
✅ Take progressive profits above 75th percentile
✅ Maintain cash buffer for drawdowns
✅ Rebalance quarterly without emotion

═══════════════════════════════════════════════════════════════════════

🎯 SUCCESS METRICS

MINIMUM ACCEPTABLE: Avoid 5th percentile ({self.metrics['var_95']:.1f}%)
TARGET: Achieve median ({self.metrics['median_return']:.1f}%)
STRETCH: Reach 75th percentile ({self.returns[np.where(self.percentiles == 75)[0][0]]*100:.0f}%)
EXCEPTIONAL: Exceed 90th percentile ({self.returns[np.where(self.percentiles == 90)[0][0]]*100:.0f}%)

═══════════════════════════════════════════════════════════════════════

Remember: These percentiles map probability, not certainty.
Your actual outcome will be ONE path from 5 million possibilities.

Trade smart. Stay humble. Manage risk.

═══════════════════════════════════════════════════════════════════════
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(recommendations)
        
        print(f"✅ Saved trading recommendations: {output_file}")
        return output_file
    
    def generate_summary_csv(self, output_file='summary_statistics.csv'):
        """Generate summary statistics CSV"""
        print(f"✅ Generating summary statistics: {output_file}")
        
        summary_data = []
        
        # Overall metrics
        summary_data.append(['Metric', 'Value', 'Interpretation'])
        summary_data.append(['Initial Portfolio Value', f'R{self.initial_value:,.0f}', 'Starting capital'])
        summary_data.append(['Median Return', f'{self.metrics["median_return"]:.2f}%', 'Most likely outcome'])
        summary_data.append(['Median Final Value', f'R{self.metrics["median_final_value"]:,.0f}', 'Expected ending value'])
        summary_data.append(['Probability of Profit', f'{self.metrics["prob_profit"]:.1f}%', 'Chance of positive return'])
        summary_data.append(['Probability of Loss', f'{self.metrics["prob_loss"]:.1f}%', 'Chance of negative return'])
        summary_data.append(['VaR (95%)', f'{self.metrics["var_95"]:.2f}%', 'Worst 5% threshold'])
        summary_data.append(['VaR (99%)', f'{self.metrics["var_99"]:.2f}%', 'Worst 1% threshold'])
        summary_data.append(['Best Case', f'{self.metrics["best_case"]:.2f}%', '99th percentile'])
        summary_data.append(['Worst Case', f'{self.metrics["worst_case"]:.2f}%', '1st percentile'])
        summary_data.append(['Range', f'{self.metrics["range"]:.1f} ppts', 'Total spread'])
        summary_data.append(['IQR', f'{self.metrics["iqr"]:.1f} ppts', '25th to 75th percentile'])
        
        df_summary = pd.DataFrame(summary_data[1:], columns=summary_data[0])
        df_summary.to_csv(output_file, index=False)
        
        print(f"✅ Saved summary statistics: {output_file}")
        return output_file
    
    def generate_all_reports(self, output_prefix=''):
        """Generate all reports at once"""
        print(f"\n{'='*70}")
        print("GENERATING COMPLETE PERCENTILE ANALYSIS PACKAGE")
        print(f"{'='*70}")
        
        # Calculate metrics first
        self.calculate_metrics()
        
        # Generate all outputs
        outputs = {
            'visualization': self.generate_visualization(f'{output_prefix}percentile_analysis.png'),
            'markdown': self.generate_markdown_report(f'{output_prefix}PERCENTILE_REPORT.md'),
            'trading': self.generate_trading_recommendations(f'{output_prefix}trading_recommendations.txt'),
            'summary': self.generate_summary_csv(f'{output_prefix}summary_statistics.csv')
        }
        
        print(f"\n{'='*70}")
        print("✅ REPORT GENERATION COMPLETE")
        print(f"{'='*70}")
        print(f"\nGenerated files:")
        for report_type, filename in outputs.items():
            print(f"  • {report_type.upper()}: {filename}")
        
        return outputs


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python generate_percentile_report.py <percentiles_csv> <initial_portfolio_value>")
        print("\nExample:")
        print("  python generate_percentile_report.py sg_capital_2026_5M_percentiles.csv 726500")
        sys.exit(1)
    
    percentiles_csv = sys.argv[1]
    initial_value = float(sys.argv[2])
    
    # Check if file exists
    if not os.path.exists(percentiles_csv):
        print(f"❌ Error: File not found: {percentiles_csv}")
        sys.exit(1)
    
    # Generate reports
    generator = PercentileReportGenerator(percentiles_csv, initial_value)
    generator.generate_all_reports()
    
    print("\n🎉 All reports generated successfully!")
    print("\nNext steps:")
    print("  1. Review percentile_analysis.png for visual overview")
    print("  2. Read PERCENTILE_REPORT.md for detailed analysis")
    print("  3. Follow trading_recommendations.txt for actionable advice")
    print("  4. Share summary_statistics.csv with stakeholders")


if __name__ == "__main__":
    main()