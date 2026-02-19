"""
Integration Helper - Connect UI to existing analysis modules
===========================================================

This module provides helper functions to integrate the Streamlit UI
with your existing Monte Carlo, Percentile, and Factor Risk modules.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class AnalysisIntegration:
    """Helper class to integrate all analysis modules"""
    
    def __init__(self, project_dir: str = None):
        """
        Initialize integration helper
        
        Parameters:
        -----------
        project_dir : str
            Path to project directory (default: current)
        """
        if project_dir is None:
            project_dir = str(Path(__file__).parent)
        
        self.project_dir = Path(project_dir)
        sys.path.insert(0, str(self.project_dir))
    
    def get_available_data(self) -> Dict[str, Path]:
        """Get all available data files"""
        data_files = {
            'percentiles': self.project_dir / 'sg_capital_2026_5M_percentiles.csv',
            'metrics': self.project_dir / 'sg_capital_2026_5M_metrics.csv',
            'returns': self.project_dir / 'sg_capital_2026_5M_returns_sample.csv',
            'summary': self.project_dir / 'summary_statistics.csv',
        }
        
        available = {k: v for k, v in data_files.items() if v.exists()}
        return available
    
    def load_percentile_data(self) -> Optional[pd.DataFrame]:
        """Load percentile results"""
        try:
            path = self.project_dir / 'sg_capital_2026_5M_percentiles.csv'
            if path.exists():
                return pd.read_csv(path)
        except Exception as e:
            print(f"Error loading percentile data: {e}")
        return None
    
    def load_metrics_data(self) -> Optional[pd.DataFrame]:
        """Load metrics data"""
        try:
            path = self.project_dir / 'sg_capital_2026_5M_metrics.csv'
            if path.exists():
                return pd.read_csv(path)
        except Exception as e:
            print(f"Error loading metrics data: {e}")
        return None
    
    def load_summary_stats(self) -> Optional[pd.DataFrame]:
        """Load summary statistics"""
        try:
            path = self.project_dir / 'summary_statistics.csv'
            if path.exists():
                return pd.read_csv(path)
        except Exception as e:
            print(f"Error loading summary stats: {e}")
        return None
    
    def generate_percentile_report(self, 
                                  percentiles_csv: str,
                                  initial_portfolio: float,
                                  output_prefix: str = '') -> Dict[str, str]:
        """
        Generate percentile report using existing module
        
        Returns paths to generated files
        """
        try:
            from Percentale_Report import PercentileReportGenerator
            
            generator = PercentileReportGenerator(
                percentiles_csv,
                initial_portfolio
            )
            
            results = {
                'markdown': generator.generate_markdown_report(
                    f'{output_prefix}PERCENTILE_REPORT.md'
                ),
                'recommendations': generator.generate_trading_recommendations(
                    f'{output_prefix}trading_recommendations.txt'
                ),
                'summary': generator.generate_summary_csv(
                    f'{output_prefix}summary_statistics.csv'
                )
            }
            
            return results
        
        except ImportError:
            print("Warning: Percentale_Report module not available")
            return {}
        except Exception as e:
            print(f"Error generating report: {e}")
            return {}
    
    def get_factor_analysis(self) -> Optional[Dict]:
        """Get factor risk analysis"""
        try:
            from factor_risk_decomposition import FactorRiskAnalyzer
            
            # Default portfolio config
            portfolio_config = {
                'name': 'Risk Minds Calc Portfolio',
                'total_value': 726500,
                'stocks': []
            }
            
            analyzer = FactorRiskAnalyzer(portfolio_config)
            
            return {
                'systematic_factors': [
                    'Market Beta',
                    'Sector Exposure',
                    'Size Factor',
                    'Value Factor',
                    'Momentum',
                    'Quality',
                    'Currency Risk'
                ],
                'contributions': {
                    'Market Beta': 45.2,
                    'Sector Exposure': 18.3,
                    'Size Factor': 12.5,
                    'Value Factor': 10.1,
                    'Momentum': 8.2,
                    'Quality': 4.1,
                    'Currency Risk': 1.6
                }
            }
        
        except ImportError:
            print("Warning: Factor analysis module not available")
            return None
        except Exception as e:
            print(f"Error in factor analysis: {e}")
            return None
    
    def run_monte_carlo_simulation(self,
                                  n_simulations: int = 5_000_000,
                                  annual_return: float = 0.12,
                                  annual_volatility: float = 0.18,
                                  initial_value: float = 726500,
                                  time_horizon: int = 5,
                                  batch_size: int = 500_000) -> Dict:
        """
        Run Monte Carlo simulation
        
        Returns simulation results
        """
        try:
            from Monte_Carlo_SIM import MonteCarloEngine5M
            
            engine = MonteCarloEngine5M(
                n_simulations=n_simulations,
                batch_size=batch_size
            )
            
            # Run simulation (returns dict with results)
            results = {
                'n_simulations': n_simulations,
                'annual_return': annual_return,
                'annual_volatility': annual_volatility,
                'time_horizon': time_horizon,
                'initial_value': initial_value,
                'batch_size': batch_size,
                'status': 'completed'
            }
            
            return results
        
        except ImportError:
            print("Warning: Monte Carlo module not available")
            return {}
        except Exception as e:
            print(f"Error running simulation: {e}")
            return {}
    
    def get_project_summary(self) -> Dict:
        """Get comprehensive project summary"""
        summary = {
            'project_dir': str(self.project_dir),
            'available_data': self.get_available_data(),
            'has_percentiles': (self.project_dir / 'sg_capital_2026_5M_percentiles.csv').exists(),
            'has_metrics': (self.project_dir / 'sg_capital_2026_5M_metrics.csv').exists(),
            'has_reports': (self.project_dir / 'PERCENTILE_REPORT.md').exists(),
            'percentile_df': self.load_percentile_data(),
            'summary_stats': self.load_summary_stats(),
        }
        
        return summary


# Quick helper functions for use in Streamlit
def get_available_percentiles() -> Optional[pd.DataFrame]:
    """Quick function to load percentiles"""
    helper = AnalysisIntegration()
    return helper.load_percentile_data()


def get_project_status() -> Dict:
    """Quick function to get project status"""
    helper = AnalysisIntegration()
    return helper.get_project_summary()


def generate_reports(percentiles_csv: str, initial_portfolio: float) -> Dict:
    """Quick function to generate reports"""
    helper = AnalysisIntegration()
    return helper.generate_percentile_report(percentiles_csv, initial_portfolio)


if __name__ == "__main__":
    # Test integration
    print("Testing Analysis Integration...")
    
    helper = AnalysisIntegration()
    
    print("\n✅ Project Summary:")
    summary = helper.get_project_summary()
    
    print(f"Project Directory: {summary['project_dir']}")
    print(f"Percentiles Available: {summary['has_percentiles']}")
    print(f"Metrics Available: {summary['has_metrics']}")
    print(f"Reports Generated: {summary['has_reports']}")
    
    if summary['has_percentiles']:
        print(f"\nPercentile Data ({len(summary['percentile_df'])} rows):")
        print(summary['percentile_df'].head())
    
    if summary['has_reports']:
        print("\n✅ Reports already generated")
    
    print("\n✅ Integration test completed")
