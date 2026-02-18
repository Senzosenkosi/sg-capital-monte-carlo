# SG Capital UI Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB INTERFACE                      │
│                         (app.py)                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Dashboard   │  │ Monte Carlo  │  │ Percentile   │          │
│  │              │  │  Simulator   │  │   Analysis   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ Factor Risk  │  │ Data Mgt     │                            │
│  │ Analysis     │  │ (Upload)     │                            │
│  └──────────────┘  └──────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Integration     │  │ Data Processing  │  │ Visualization    │
│  Helper          │  │ (Pandas/NumPy)   │  │ (Matplotlib)     │
│ (integration_    │  │                  │  │                  │
│  helper.py)      │  │                  │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Monte Carlo      │  │ Percentile       │  │ Factor Risk      │
│ Engine           │  │ Report Generator │  │ Decomposition    │
│(Monte_Carlo_     │  │(Percentale_      │  │(factor_risk_     │
│ SIM.py)          │  │ Report.py)       │  │decomposition.py) │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                   DATA & OUTPUT FILES                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input:                          Output:                        │
│  • Portfolio data                • Percentile CSV               │
│  • Market parameters             • Metrics CSV                  │
│  • Historical returns            • Summary Statistics           │
│                                  • Markdown Report              │
│                                  • Trading Recommendations      │
│                                  • Visualizations (PNG)         │
│                                  • Factor Analysis              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
User Interaction (UI)
        │
        ▼
┌───────────────────┐
│ Configure         │
│ Parameters        │
└───────────────────┘
        │
        ├─── Dashboard: View summary
        │
        ├─── Monte Carlo: Set parameters
        │        ├─ Simulations (100K-5M)
        │        ├─ Portfolio metrics
        │        └─ Time horizon
        │        │
        │        ▼
        │    Run Simulation
        │        │
        │        ▼
        │    Generate Results
        │
        ├─── Percentile Analysis: View results
        │        │
        │        ▼
        │    Load CSV Data
        │        │
        │        ├─ Calculate percentiles
        │        ├─ Generate charts
        │        └─ Create reports
        │
        ├─── Factor Risk: Analyze decomposition
        │        │
        │        ▼
        │    Calculate Factor Contributions
        │        │
        │        ├─ Systematic factors
        │        ├─ Idiosyncratic risk
        │        └─ Risk visualization
        │
        └─── Data Management: Export/Import
                 │
                 ▼
            Download/Upload Data
```

---

## Component Interaction

```
┌────────────────────────────────────────────────────────────────┐
│ STREAMLIT UI (app.py)                                          │
│                                                                │
│ Sidebar Module Navigation                                     │
│   │                                                            │
│   ├─ Dashboard                                                │
│   │   └─ integration_helper.get_project_status()             │
│   │                                                            │
│   ├─ Monte Carlo Simulator                                    │
│   │   └─ integration_helper.run_monte_carlo_simulation()      │
│   │   └─ Visualizations (Matplotlib)                         │
│   │                                                            │
│   ├─ Percentile Analysis                                      │
│   │   └─ integration_helper.load_percentile_data()           │
│   │   └─ integration_helper.load_metrics_data()              │
│   │   └─ Charts & Statistics                                 │
│   │                                                            │
│   ├─ Factor Risk Analysis                                     │
│   │   └─ integration_helper.get_factor_analysis()            │
│   │   └─ Risk decomposition visualization                    │
│   │                                                            │
│   └─ Data Management                                          │
│       └─ File browser                                         │
│       └─ Data upload/preview                                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

```
Frontend:
├─ Streamlit          Web framework & UI
├─ Matplotlib         Charting & visualization
├─ Seaborn           Statistical data visualization
└─ HTML/CSS          Styling

Backend:
├─ Python 3.8+       Language
├─ Pandas            Data manipulation
├─ NumPy             Numerical computing
├─ Scipy             Scientific computing
└─ Scikit-learn      Machine learning (for analysis)

Integration:
├─ integration_helper.py    Module connector
├─ Monte_Carlo_SIM.py       Simulation engine
├─ Percentale_Report.py     Report generator
└─ factor_risk_decomposition.py    Risk analysis

Data:
├─ CSV Files         Structured data
├─ Markdown Files    Reports & documentation
└─ PNG Images        Visualizations
```

---

## Deployment Architecture

```
Local Development:
├─ Windows/Mac/Linux
├─ Python 3.8+
├─ Streamlit server
└─ Browser (localhost:8501)

Production Ready:
├─ Deploy on Streamlit Cloud
├─ Or self-hosted with Docker
├─ Central data repository
└─ Multi-user access

Corporate Integration:
├─ Intranet deployment
├─ Single sign-on (SSO)
├─ Central data warehouse
└─ Audit logging
```

---

## File Dependencies

```
app.py (Main UI)
  ├─ requires: streamlit, pandas, numpy, matplotlib, seaborn
  ├─ imports: integration_helper
  ├─ reads: *.csv, *.md
  └─ outputs: Display in browser

integration_helper.py
  ├─ requires: pandas, numpy
  ├─ imports: Monte_Carlo_SIM, Percentale_Report, factor_risk_decomposition
  ├─ reads: CSV files
  └─ outputs: DataFrames, dicts

Monte_Carlo_SIM.py
  ├─ requires: numpy, pandas
  ├─ outputs: percentiles.csv, metrics.csv, returns.csv

Percentale_Report.py
  ├─ requires: pandas, matplotlib
  ├─ reads: percentiles.csv
  └─ outputs: .md, .txt, .csv, .png

factor_risk_decomposition.py
  ├─ requires: numpy, pandas, matplotlib
  └─ outputs: Risk analysis, visualizations
```

---

## Module Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│ app.py - User Interface Layer                              │
├─────────────────────────────────────────────────────────────┤
│ Responsibility: Display & user interaction                 │
│ Input: User selections                                     │
│ Output: Visual dashboard                                   │
│ Dependencies: streamlit, matplotlib, pandas                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ integration_helper.py - Application Logic Layer            │
├─────────────────────────────────────────────────────────────┤
│ Responsibility: Coordinate modules & data                  │
│ Input: UI parameters                                       │
│ Output: Analysis results                                   │
│ Dependencies: pandas, numpy, analysis modules              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Analysis Modules - Business Logic Layer                    │
├─────────────────────────────────────────────────────────────┤
│ Monte_Carlo_SIM.py                                         │
│   └─ Responsibility: Run simulations                       │
│   └─ Input: Parameters                                     │
│   └─ Output: Results CSV                                   │
│                                                             │
│ Percentale_Report.py                                       │
│   └─ Responsibility: Generate reports                      │
│   └─ Input: Percentile CSV                                 │
│   └─ Output: Reports & visualizations                      │
│                                                             │
│ factor_risk_decomposition.py                               │
│   └─ Responsibility: Risk analysis                         │
│   └─ Input: Portfolio data                                 │
│   └─ Output: Factor analysis                               │
│                                                             │
│ Dependencies: numpy, pandas, matplotlib                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Data Layer                                                  │
├─────────────────────────────────────────────────────────────┤
│ CSV Files, Markdown Reports, PNG Visualizations           │
│ Stored locally in project directory                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Runtime Flow

```
START
  │
  └─► Streamlit loads app.py
       │
       ├─► Sidebar: Navigation menu
       │
       ├─► Page selection
       │
       └─► Load selected module
            │
            ├─► Dashboard
            │    └─► integration_helper.get_project_status()
            │    └─► Display summary
            │
            ├─► Monte Carlo Simulator
            │    └─► Get user parameters
            │    └─► Call run_monte_carlo_simulation()
            │    └─► Generate visualizations
            │    └─► Display results
            │
            ├─► Percentile Analysis
            │    └─► Load percentile CSV
            │    └─► Calculate statistics
            │    └─► Generate charts
            │    └─► Display report
            │
            ├─► Factor Risk Analysis
            │    └─► Get factor data
            │    └─► Calculate contributions
            │    └─► Visualize breakdown
            │
            └─► Data Management
                 └─► File browser
                 └─► Upload interface
                 └─► Data preview
  │
  └─► User closes browser or stops server
       │
       └─► END
```

---

## Quick Start Sequence

```
1. run_ui.bat (or: streamlit run app.py)
   │
   ├─► Check dependencies
   ├─► Install if missing
   └─► Start Streamlit server
       │
       └─► Open browser: http://localhost:8501
           │
           ├─► Load Dashboard
           │    └─► Show project overview
           │
           ├─► Navigate to module
           │    └─► Execute analysis
           │    └─► Display results
           │
           └─► Download/Export
                └─► Save to local files
```

---

## Performance Characteristics

```
Module                  Time       Memory    Dependency
────────────────────────────────────────────────────────
Monte Carlo (5M)        2-5 min    2-4 GB    NumPy, CPU
Percentile Analysis     <1 sec     100 MB    Pandas, CSV
Factor Risk Analysis    1-2 sec    200 MB    NumPy, Pandas
Report Generation       <1 sec     100 MB    Markdown
Visualization           < 1 sec    300 MB    Matplotlib
Data Upload             <1 sec     50 MB     Pandas
────────────────────────────────────────────────────────
Total UI Load Time      <2 sec
First Simulation Run    2-5 min
Subsequent Loads        < 2 sec
────────────────────────────────────────────────────────
```

---

## File Size Reference

```
Source Code:
├─ app.py                    ~15 KB
├─ integration_helper.py     ~12 KB
├─ Monte_Carlo_SIM.py        ~20 KB
├─ Percentale_Report.py      ~25 KB
└─ factor_risk_decomposition.py  ~30 KB
   Total: ~102 KB

Dependencies (after pip install):
├─ Streamlit              ~50 MB
├─ Pandas                ~25 MB
├─ NumPy                 ~50 MB
├─ Matplotlib            ~12 MB
├─ Seaborn               ~5 MB
└─ Others                ~30 MB
   Total: ~172 MB

Data Files:
├─ CSV files (5M runs)    ~500 MB
├─ PNG visualizations     ~2-5 MB
├─ Markdown reports       ~500 KB
└─ Total: ~503 MB

Complete Project:
└─ Approximately 600-800 MB (with dependencies)
```

---

## Scalability

```
Current: Single machine, local deployment
├─ Simulations: 1-5M
├─ Performance: Minutes for full run
└─ Users: 1 local

Future: Multi-user deployment
├─ Streamlit Cloud hosting
├─ Multiple concurrent users
├─ Cached results
└─ Database backend

Enterprise: Corporate integration
├─ Docker containerization
├─ Kubernetes orchestration
├─ Central data repository
├─ Authentication & authorization
└─ Audit logging & compliance
```

---

**Version:** 1.0
**Date:** February 2026
**Status:** Complete & Ready for Use
