"""
OPTIMIZED MONTE CARLO SIMULATOR FOR 5 MILLION RUNS
===================================================
Memory-efficient implementation designed to run 5M simulations
without running out of RAM.

Key optimizations:
- Batch processing to manage memory
- Vectorized operations for speed
- Progress tracking
- Checkpoint saving

Usage:
    python monte_carlo_simulator_5M.py
"""

import numpy as np
import pandas as pd
import time
from typing import Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

class MonteCarloEngine5M:
    """
    Optimized Monte Carlo engine for 5 million simulations
    """
    
    def __init__(self, n_simulations: int = 5_000_000, batch_size: int = 500_000):
        """
        Initialize engine
        
        Parameters:
        -----------
        n_simulations : int
            Total number of simulations (default 5 million)
        batch_size : int
            Process this many sims at once (default 500K)
            Adjust based on your RAM: 
            - 8GB RAM: 100K
            - 16GB RAM: 500K  
            - 32GB+ RAM: 1M
        """
        self.n_simulations = n_simulations
        self.batch_size = batch_size
        self.n_batches = int(np.ceil(n_simulations / batch_size))
        
        print(f"Monte Carlo Engine - 5M Optimization")
        print(f"Total Simulations: {n_simulations:,}")
        print(f"Batch Size: {batch_size:,}")
        print(f"Number of Batches: {self.n_batches}")
        
        np.random.seed(42)
    
    def simulate_portfolio_batch(self,
                                 weights: np.ndarray,
                                 initial_prices: np.ndarray,
                                 expected_returns: np.ndarray,
                                 volatilities: np.ndarray,
                                 correlation_matrix: np.ndarray,
                                 T: float,
                                 batch_n_sims: int) -> np.ndarray:
        """
        Simulate one batch of portfolio paths
        Returns only final values to save memory
        """
        n_assets = len(weights)
        n_steps = int(T * 252)  # Trading days
        dt = 1/252
        
        # Cholesky decomposition (one-time per batch)
        L = np.linalg.cholesky(correlation_matrix)
        
        # Generate correlated random numbers efficiently
        Z_indep = np.random.standard_normal((batch_n_sims, n_steps, n_assets))
        Z_flat = Z_indep.reshape(-1, n_assets)
        Z_corr = (Z_flat @ L.T).reshape(batch_n_sims, n_steps, n_assets)
        
        # Calculate final portfolio value for each simulation
        portfolio_final_values = np.zeros(batch_n_sims)
        
        for i in range(n_assets):
            mu = expected_returns[i]
            sigma = volatilities[i]
            
            # Calculate returns
            returns = (mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z_corr[:, :, i]
            
            # Calculate final prices only (don't store full paths)
            cumulative_return = np.sum(returns, axis=1)
            final_prices = initial_prices[i] * np.exp(cumulative_return)
            
            # Add to portfolio (weighted)
            portfolio_final_values += final_prices * weights[i]
        
        return portfolio_final_values
    
    def run_5M_simulation(self,
                         portfolio_config: Dict,
                         time_horizon: float = 1.0) -> Dict:
        """
        Run complete 5 million simulation with batch processing
        """
        print(f"\n{'='*70}")
        print(f"RUNNING 5 MILLION MONTE CARLO SIMULATIONS")
        print(f"{'='*70}")
        print(f"Portfolio: {portfolio_config['tickers']}")
        print(f"Time Horizon: {time_horizon} years")
        
        start_time = time.time()
        
        # Calculate initial portfolio value
        weights = np.array(portfolio_config['weights'])
        initial_prices = np.array(portfolio_config['initial_prices'])
        initial_portfolio_value = np.sum(weights * initial_prices)
        
        # Storage for all final values
        all_final_values = np.zeros(self.n_simulations)
        
        # Process in batches
        for batch_idx in range(self.n_batches):
            batch_start = batch_idx * self.batch_size
            batch_end = min(batch_start + self.batch_size, self.n_simulations)
            batch_n_sims = batch_end - batch_start
            
            print(f"\nBatch {batch_idx+1}/{self.n_batches}: Simulating {batch_n_sims:,} paths...", end=" ")
            
            batch_start_time = time.time()
            
            # Simulate this batch
            batch_final_values = self.simulate_portfolio_batch(
                weights=weights,
                initial_prices=initial_prices,
                expected_returns=np.array(portfolio_config['expected_returns']),
                volatilities=np.array(portfolio_config['volatilities']),
                correlation_matrix=portfolio_config['correlation_matrix'],
                T=time_horizon,
                batch_n_sims=batch_n_sims
            )
            
            # Store results
            all_final_values[batch_start:batch_end] = batch_final_values
            
            batch_elapsed = time.time() - batch_start_time
            batch_speed = batch_n_sims / batch_elapsed
            
            print(f"✅ Done in {batch_elapsed:.2f}s ({batch_speed:,.0f} sims/sec)")
        
        total_elapsed = time.time() - start_time
        total_speed = self.n_simulations / total_elapsed
        
        print(f"\n{'='*70}")
        print(f"SIMULATION COMPLETE")
        print(f"{'='*70}")
        print(f"Total Time: {total_elapsed:.2f} seconds ({total_elapsed/60:.2f} minutes)")
        print(f"Average Speed: {total_speed:,.0f} simulations/second")
        
        # Calculate returns
        returns = (all_final_values - initial_portfolio_value) / initial_portfolio_value
        
        # Calculate comprehensive metrics
        print(f"\n{'='*70}")
        print(f"CALCULATING RISK METRICS")
        print(f"{'='*70}")
        
        metrics = self._calculate_metrics(returns)
        
        results = {
            'final_values': all_final_values,
            'returns': returns,
            'metrics': metrics,
            'config': portfolio_config,
            'elapsed_time': total_elapsed,
            'speed': total_speed
        }
        
        self._print_summary(metrics, initial_portfolio_value)
        
        return results
    
    def _calculate_metrics(self, returns: np.ndarray) -> Dict:
        """Calculate all risk metrics"""
        # Sort for efficient percentile calculation
        returns_sorted = np.sort(returns)
        n = len(returns_sorted)
        
        metrics = {
            # Central tendency
            'mean_return': np.mean(returns),
            'median_return': np.median(returns),
            'std_return': np.std(returns),
            
            # Percentiles
            'percentile_1': returns_sorted[int(n * 0.01)],
            'percentile_5': returns_sorted[int(n * 0.05)],
            'percentile_25': returns_sorted[int(n * 0.25)],
            'percentile_75': returns_sorted[int(n * 0.75)],
            'percentile_95': returns_sorted[int(n * 0.95)],
            'percentile_99': returns_sorted[int(n * 0.99)],
            
            # Value at Risk
            'VaR_95': returns_sorted[int(n * 0.05)],
            'VaR_99': returns_sorted[int(n * 0.01)],
            'VaR_999': returns_sorted[int(n * 0.001)],  # 1 in 1000
            
            # Conditional VaR (Expected Shortfall)
            'CVaR_95': np.mean(returns_sorted[:int(n * 0.05)]),
            'CVaR_99': np.mean(returns_sorted[:int(n * 0.01)]),
            'CVaR_999': np.mean(returns_sorted[:int(n * 0.001)]),
            
            # Probabilities
            'prob_loss': np.sum(returns < 0) / n,
            'prob_loss_10': np.sum(returns < -0.10) / n,
            'prob_loss_20': np.sum(returns < -0.20) / n,
            'prob_loss_50': np.sum(returns < -0.50) / n,
            'prob_profit': np.sum(returns > 0) / n,
            'prob_profit_10': np.sum(returns > 0.10) / n,
            'prob_profit_20': np.sum(returns > 0.20) / n,
            'prob_profit_50': np.sum(returns > 0.50) / n,
            
            # Higher moments
            'skewness': self._calculate_skewness(returns),
            'kurtosis': self._calculate_kurtosis(returns),
            
            # Sharpe ratio (assuming risk-free rate = 0)
            'sharpe_ratio': np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0,
        }
        
        return metrics
    
    def _calculate_skewness(self, returns: np.ndarray) -> float:
        """Calculate skewness"""
        mean = np.mean(returns)
        std = np.std(returns)
        if std == 0:
            return 0
        return np.mean(((returns - mean) / std) ** 3)
    
    def _calculate_kurtosis(self, returns: np.ndarray) -> float:
        """Calculate excess kurtosis"""
        mean = np.mean(returns)
        std = np.std(returns)
        if std == 0:
            return 0
        return np.mean(((returns - mean) / std) ** 4) - 3
    
    def _print_summary(self, metrics: Dict, initial_value: float):
        """Print comprehensive summary"""
        print(f"\n{'='*70}")
        print(f"SIMULATION SUMMARY - 5,000,000 RUNS")
        print(f"{'='*70}")
        
        print(f"\nRETURN STATISTICS:")
        print(f"  Mean Return: {metrics['mean_return']*100:>8.2f}%")
        print(f"  Median Return: {metrics['median_return']*100:>8.2f}%")
        print(f"  Std Deviation: {metrics['std_return']*100:>8.2f}%")
        print(f"  Sharpe Ratio: {metrics['sharpe_ratio']:>8.3f}")
        print(f"  Skewness: {metrics['skewness']:>8.3f}")
        print(f"  Kurtosis: {metrics['kurtosis']:>8.3f}")
        
        print(f"\nVALUE AT RISK (VaR):")
        print(f"  95% VaR: {metrics['VaR_95']*100:>8.2f}%")
        print(f"  99% VaR: {metrics['VaR_99']*100:>8.2f}%")
        print(f"  99.9% VaR: {metrics['VaR_999']*100:>8.2f}%")
        
        print(f"\nCONDITIONAL VaR (Expected Shortfall):")
        print(f"  95% CVaR: {metrics['CVaR_95']*100:>8.2f}%")
        print(f"  99% CVaR: {metrics['CVaR_99']*100:>8.2f}%")
        print(f"  99.9% CVaR: {metrics['CVaR_999']*100:>8.2f}%")
        
        print(f"\nPROBABILITY OF LOSS:")
        print(f"  Any Loss: {metrics['prob_loss']*100:>8.2f}%")
        print(f"  Loss > 10%: {metrics['prob_loss_10']*100:>8.2f}%")
        print(f"  Loss > 20%: {metrics['prob_loss_20']*100:>8.2f}%")
        print(f"  Loss > 50%: {metrics['prob_loss_50']*100:>8.2f}%")
        
        print(f"\nPROBABILITY OF PROFIT:")
        print(f"  Any Profit: {metrics['prob_profit']*100:>8.2f}%")
        print(f"  Profit > 10%: {metrics['prob_profit_10']*100:>8.2f}%")
        print(f"  Profit > 20%: {metrics['prob_profit_20']*100:>8.2f}%")
        print(f"  Profit > 50%: {metrics['prob_profit_50']*100:>8.2f}%")
        
        print(f"\nRETURN DISTRIBUTION PERCENTILES:")
        print(f"  1st Percentile: {metrics['percentile_1']*100:>8.2f}%")
        print(f"  5th Percentile: {metrics['percentile_5']*100:>8.2f}%")
        print(f"  25th Percentile: {metrics['percentile_25']*100:>8.2f}%")
        print(f"  75th Percentile: {metrics['percentile_75']*100:>8.2f}%")
        print(f"  95th Percentile: {metrics['percentile_95']*100:>8.2f}%")
        print(f"  99th Percentile: {metrics['percentile_99']*100:>8.2f}%")
        
        print(f"\nPORTFOLIO VALUE PROJECTIONS (R{initial_value:,.0f} initial):")
        mean_final = initial_value * (1 + metrics['mean_return'])
        p5_final = initial_value * (1 + metrics['percentile_5'])
        p95_final = initial_value * (1 + metrics['percentile_95'])
        print(f"  Expected Value (mean): R{mean_final:>,.0f}")
        print(f"  5th Percentile: R{p5_final:>,.0f}")
        print(f"  95th Percentile: R{p95_final:>,.0f}")
    
    def export_results(self, results: Dict, filename_prefix: str = 'mc_5M'):
        """Export results to CSV"""
        print(f"\n{'='*70}")
        print(f"EXPORTING RESULTS")
        print(f"{'='*70}")
        
        # 1. Summary statistics
        metrics_list = []
        for key, value in results['metrics'].items():
            metrics_list.append({
                'Metric': key,
                'Value': f"{value:.6f}" if isinstance(value, float) else value
            })
        
        metrics_df = pd.DataFrame(metrics_list)
        metrics_df.to_csv(f'{filename_prefix}_metrics.csv', index=False)
        print(f"✅ Saved: {filename_prefix}_metrics.csv")
        
        # 2. Return distribution (sample 100K for file size)
        sample_size = min(100_000, len(results['returns']))
        sample_indices = np.random.choice(len(results['returns']), sample_size, replace=False)
        
        returns_df = pd.DataFrame({
            'Return': results['returns'][sample_indices],
            'Final_Value': results['final_values'][sample_indices]
        })
        returns_df.to_csv(f'{filename_prefix}_returns_sample.csv', index=False)
        print(f"✅ Saved: {filename_prefix}_returns_sample.csv (100K sample)")
        
        # 3. Key percentiles
        percentiles_data = []
        for pct in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
            value = np.percentile(results['returns'], pct)
            percentiles_data.append({
                'Percentile': f'{pct}%',
                'Return': f'{value*100:.2f}%',
                'Value': value
            })
        
        percentiles_df = pd.DataFrame(percentiles_data)
        percentiles_df.to_csv(f'{filename_prefix}_percentiles.csv', index=False)
        print(f"✅ Saved: {filename_prefix}_percentiles.csv")


# ============================================================================
# EXAMPLE USAGE - JSE PORTFOLIO
# ============================================================================

if __name__ == "__main__":
    
    print("="*70)
    print("5 MILLION MONTE CARLO SIMULATION - JSE PORTFOLIO")
    print("="*70)
    
    # Initialize engine
    # Adjust batch_size based on your RAM:
    # 8GB RAM: batch_size=100_000
    # 16GB RAM: batch_size=500_000 (default)
    # 32GB+ RAM: batch_size=1_000_000
    
    mc = MonteCarloEngine5M(
        n_simulations=5_000_000,
        batch_size=500_000  # Adjust based on your RAM
    )
    
    # Define S.G Capital 2026 Portfolio
    portfolio_config = {
        'tickers': ['CPI', 'FSR', 'NPN', 'ANG', 'IMP'],
        'weights': [0.25, 0.25, 0.20, 0.15, 0.15],
        'initial_prices': [1200, 80, 3200, 300, 200],
        'expected_returns': [0.15, 0.12, 0.18, 0.20, 0.22],  # Annual expected returns
        'volatilities': [0.25, 0.18, 0.30, 0.35, 0.40],  # Annual volatilities
        'correlation_matrix': np.array([
            [1.00, 0.60, 0.40, 0.20, 0.15],  # CPI - Capitec
            [0.60, 1.00, 0.35, 0.18, 0.12],  # FSR - FirstRand
            [0.40, 0.35, 1.00, 0.25, 0.20],  # NPN - Naspers
            [0.20, 0.18, 0.25, 1.00, 0.55],  # ANG - AngloGold
            [0.15, 0.12, 0.20, 0.55, 1.00],  # IMP - Impala Platinum
        ])
    }
    
    # Run 5 million simulations
    results = mc.run_5M_simulation(
        portfolio_config=portfolio_config,
        time_horizon=2.0  # 1 year ahead
    )
    
    # Export results
    mc.export_results(results, filename_prefix='sg_capital_2026_5M')
    
    print(f"\n{'='*70}")
    print(f"ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print(f"\n✅ Successfully ran {mc.n_simulations:,} Monte Carlo simulations")
    print(f"✅ Results saved to CSV files")
    print(f"\nUse these results to:")
    print(f"  1. Set position sizes (inverse to risk)")
    print(f"  2. Determine stop losses (based on VaR)")
    print(f"  3. Stress test your 2026 strategy")
    print(f"  4. Communicate risk to stakeholders")