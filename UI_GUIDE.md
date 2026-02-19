# Risk Minds Calc Monte Carlo Analysis Platform - UI Guide

## 🚀 Quick Start

### Installation

1. **Install Streamlit and dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

3. **Open in browser:**
   The app will automatically open at `http://localhost:8501`

---

## 📊 Features

### 1. **Dashboard**
   - Quick overview of your portfolio
   - Available reports status
   - Quick action buttons
   - Recent data preview

### 2. **Monte Carlo Simulator**
   - Configure simulation parameters
   - Set portfolio expectations (return, volatility)
   - Adjust time horizon
   - Batch processing for memory optimization
   - Real-time result visualization

   **Parameters:**
   - **Number of Simulations**: 100K to 5M (more = more accurate but slower)
   - **Batch Size**: 100K, 250K, 500K, 1M (larger = faster but more RAM required)
   - **Expected Return**: Portfolio's expected annual return
   - **Volatility**: Portfolio's expected annualized volatility
   - **Time Horizon**: Investment period in years

### 3. **Percentile Analysis**
   - View percentile distribution of outcomes
   - Interactive charts and statistics
   - Export data and reports
   - View detailed markdown reports
   - Summary statistics

   **Metrics Shown:**
   - Mean portfolio value
   - Median (50th percentile) value
   - Risk metrics (1st to 99th percentiles)
   - Value at risk (VaR)
   - Confidence intervals

### 4. **Factor Risk Analysis**
   - Systematic risk decomposition
   - Idiosyncratic risk calculation
   - Factor exposure breakdown
   - Risk contribution by factor

   **Factors Analyzed:**
   - Market Beta
   - Sector Exposure
   - Size Factor (Small cap vs Large cap)
   - Value Factor (Value vs Growth)
   - Momentum
   - Quality
   - Currency Risk (ZAR)

### 5. **Data Management**
   - View all project files
   - Upload new data
   - Data information and stats
   - CSV and report file browser

---

## 📁 Project Structure

```
Monte_Carlo_Simulations/
├── app.py                                    # Main Streamlit UI
├── requirements.txt                          # Python dependencies
├── Monte_Carlo_SIM.py                        # Monte Carlo engine (5M optimized)
├── Percentale_Report.py                      # Report generator
├── factor_risk_decomposition.py              # Factor analysis engine
│
├── Data Files/
│   ├── sg_capital_2026_5M_metrics.csv       # Simulation metrics
│   ├── sg_capital_2026_5M_percentiles.csv   # Percentile results
│   ├── sg_capital_2026_5M_returns_sample.csv # Return samples
│   ├── summary_statistics.csv                # Summary stats
│   └── SG_Capital_PF_202501.xlsx            # Portfolio data
│
├── Output/
│   ├── PERCENTILE_REPORT.md                 # Detailed percentile report
│   ├── trading_recommendations.txt          # Trading recommendations
│   ├── percentile_analysis.png              # Visualization
│   └── FACTOR_RISK_GUIDE.md                 # Factor risk guide
```

---

## 🔧 Configuration

### Initial Portfolio Value
Set in the sidebar (default: R 726,500)

### Simulation Parameters
Configure in the Monte Carlo Simulator tab:
- Number of simulations (1-5M)
- Batch size for memory management
- Portfolio metrics (return, volatility)
- Investment horizon (years)

### Portfolio Configuration
Edit directly in the UI or modify the underlying Python scripts:
- `Monte_Carlo_SIM.py` - Simulation parameters
- `Percentale_Report.py` - Report generation settings
- `factor_risk_decomposition.py` - Factor definitions

---

## 📈 Workflow

### Typical Analysis Flow:

1. **Start at Dashboard**
   - Review available data and reports
   - Check file status

2. **Run Monte Carlo Simulation** (if new data needed)
   - Set simulation parameters
   - Run 5M simulations
   - Generate output files

3. **Analyze Results**
   - View percentile distributions
   - Check risk metrics
   - Review trading recommendations

4. **Deep Dive into Risk**
   - Examine factor contributions
   - Understand systematic vs idiosyncratic risk
   - Adjust portfolio based on risk profile

5. **Export & Report**
   - Download CSV data
   - Export charts
   - Share markdown reports

---

## 💡 Tips & Best Practices

### Memory Management
- **Limited RAM (8GB):** Use 100K batch size
- **Standard RAM (16GB):** Use 500K batch size
- **High RAM (32GB+):** Use 1M batch size

### Simulation Accuracy
- **Quick preview:** 100K-500K simulations
- **Standard analysis:** 1-2M simulations
- **Production:** 5M simulations

### Report Generation
- Markdown reports are human-readable and shareable
- CSV files are importable to Excel for further analysis
- Charts are PNG format, suitable for presentations

---

## 🐛 Troubleshooting

### App Won't Start
```bash
# Clear Streamlit cache
streamlit cache clear

# Try running again
streamlit run app.py
```

### Out of Memory During Simulation
- Reduce number of simulations
- Decrease batch size
- Close other applications

### Missing Data Files
- Ensure Monte Carlo simulation has been run first
- Check file paths are correct
- Verify CSV files are in the project directory

### Unicode Encoding Issues
- Already fixed! Files now save with UTF-8 encoding
- Supports all special characters and symbols

---

## 📊 Output Files Generated

| File | Type | Purpose |
|------|------|---------|
| `sg_capital_2026_5M_percentiles.csv` | CSV | Percentile results |
| `sg_capital_2026_5M_metrics.csv` | CSV | Detailed metrics |
| `sg_capital_2026_5M_returns_sample.csv` | CSV | Sample of simulated returns |
| `summary_statistics.csv` | CSV | Summary statistics |
| `PERCENTILE_REPORT.md` | Markdown | Detailed analysis report |
| `trading_recommendations.txt` | Text | Actionable recommendations |
| `percentile_analysis.png` | Image | Visualization |

---

## 🔐 Data Security

- All analysis is performed locally
- No data is sent to external servers
- Output files are stored in the project directory
- Compatible with corporate data policies

---

## 📞 Support

### Common Questions

**Q: How long does a 5M simulation take?**
A: ~2-5 minutes depending on CPU and batch size

**Q: Can I modify the factors analyzed?**
A: Yes! Edit `factor_risk_decomposition.py` to add/remove factors

**Q: How do I export results?**
A: Use the Data Management tab or download buttons in each module

**Q: Is this financial advice?**
A: No. This is an analytical tool for educational purposes only.

---

## 📄 License

Risk Minds Calc 2026 | Monte Carlo Analysis Platform
For educational and analytical purposes only.

---

## 🚀 Advanced Usage

### Running from Command Line

```bash
# Run with specific portfolio value
streamlit run app.py -- --portfolio-value 1000000

# Run in production mode
streamlit run app.py --logger.level=warning

# Run headless (for automation)
streamlit run app.py --headless
```

### Integrating Custom Scripts

You can import and use the analysis modules in your own scripts:

```python
from Monte_Carlo_SIM import MonteCarloEngine5M
from Percentale_Report import PercentileReportGenerator

# Run simulation
engine = MonteCarloEngine5M(n_simulations=5_000_000)
results = engine.run_simulation()

# Generate report
generator = PercentileReportGenerator('results.csv', 726500)
generator.generate_all_reports()
```

---

**Last Updated:** February 18, 2026
**Version:** 1.0
