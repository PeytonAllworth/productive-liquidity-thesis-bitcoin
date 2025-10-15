"""
Fee Rate & Urgency Metrics

This module computes:
1. Median fee rate (sat/vB) - baseline willingness to pay
2. 90th percentile fee rate - high-priority transactions
3. Urgency spread (p90 - p50) - premium for fast confirmation

Theory:
-------
During economic crises, we expect:
- Median fee rate to increase (more people moving BTC)
- p90 to increase MORE (urgency for liquidity)
- Urgency spread to widen (greater fee-rate diversity)

This reflects Keynesian liquidity preference: users value immediate
access to funds and are willing to pay premiums for speed.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
import numpy as np

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.io import save_csv, load_csv
from src.utils.math_stats import compute_percentiles, urgency_spread


def compute_daily_fee_rate_metrics(
    fee_rates_df: pd.DataFrame,
    date_column: str = 'date',
    fee_rate_column: str = 'fee_rate_sat_vb'
) -> pd.DataFrame:
    """
    Compute daily median and p90 fee rates from transaction-level data.
    
    Args:
        fee_rates_df: DataFrame with columns [date, fee_rate_sat_vb]
                     (one row per transaction)
        date_column: Name of date column
        fee_rate_column: Name of fee rate column (sat/vB)
    
    Returns:
        DataFrame with daily aggregates:
            - date
            - median_sat_vb: Median fee rate
            - p90_sat_vb: 90th percentile fee rate
            - urgency_spread_sat_vb: p90 - p50
            - tx_count: Number of transactions (for validation)
    
    Example:
        >>> # Assume we have transaction-level data
        >>> tx_df = pd.DataFrame({
        ...     'date': ['2013-03-16', '2013-03-16', '2013-03-17'],
        ...     'fee_rate_sat_vb': [50, 100, 75]
        ... })
        >>> tx_df['date'] = pd.to_datetime(tx_df['date'])
        >>> daily = compute_daily_fee_rate_metrics(tx_df)
        >>> print(daily)
               date  median_sat_vb  p90_sat_vb  urgency_spread_sat_vb  tx_count
        0 2013-03-16           75.0       95.0                   20.0         2
        1 2013-03-17           75.0       75.0                    0.0         1
    
    Data Sources:
        - Bitcoin Core RPC (node_rpc.py) - per-transaction fee rates
        - Pre-computed CSV from blockchain explorer
    """
    # Group by date and compute percentiles
    daily_metrics = fee_rates_df.groupby(date_column).agg({
        fee_rate_column: [
            ('median_sat_vb', lambda x: np.percentile(x, 50)),
            ('p90_sat_vb', lambda x: np.percentile(x, 90)),
            ('tx_count', 'count')
        ]
    })
    
    # Flatten column names
    daily_metrics.columns = ['median_sat_vb', 'p90_sat_vb', 'tx_count']
    daily_metrics = daily_metrics.reset_index()
    
    # Compute urgency spread
    daily_metrics['urgency_spread_sat_vb'] = (
        daily_metrics['p90_sat_vb'] - daily_metrics['median_sat_vb']
    )
    
    return daily_metrics


def compute_from_block_aggregates(
    blocks_df: pd.DataFrame,
    output_path: Path
) -> Path:
    """
    Compute fee rate metrics from pre-aggregated block data.
    
    Args:
        blocks_df: DataFrame with columns [date, median_sat_vb, p90_sat_vb]
                  (already aggregated at block or day level)
        output_path: Where to save result
    
    Returns:
        Path to saved CSV
    
    Use Case:
        If you already have daily/block-level median and p90 from an API
        or node, just compute urgency spread and save.
    
    TODO: Implement if using pre-aggregated data
    """
    # If data is already at daily level with median/p90, just compute spread
    if 'median_sat_vb' in blocks_df.columns and 'p90_sat_vb' in blocks_df.columns:
        blocks_df['urgency_spread_sat_vb'] = (
            blocks_df['p90_sat_vb'] - blocks_df['median_sat_vb']
        )
        
        save_csv(blocks_df, output_path)
        return output_path
    else:
        raise ValueError("blocks_df must have 'median_sat_vb' and 'p90_sat_vb' columns")


def load_and_compute_fee_rate_metrics(
    input_csv: Path,
    output_dir: Path,
    date_column: str = 'date',
    fee_rate_column: str = 'fee_rate_sat_vb'
) -> Path:
    """
    Load transaction-level data and compute daily fee rate metrics.
    
    Args:
        input_csv: Path to CSV with per-transaction fee rates
        output_dir: Where to save computed metrics
        date_column: Name of date column
        fee_rate_column: Name of fee rate column
    
    Returns:
        Path to saved metrics CSV
    
    Workflow:
        1. Load transaction-level CSV
        2. Compute daily median, p90, urgency spread
        3. Save to processed/ directory
    """
    print(f"\n📊 Computing fee rate & urgency metrics...")
    print(f"   Input: {input_csv}")
    
    # Load data
    df = load_csv(input_csv)
    
    # Compute metrics
    daily_metrics = compute_daily_fee_rate_metrics(
        df,
        date_column=date_column,
        fee_rate_column=fee_rate_column
    )
    
    # Save
    output_path = output_dir / "fee_rate_urgency_daily.csv"
    save_csv(daily_metrics, output_path)
    
    print(f"   ✓ Saved {len(daily_metrics)} days of fee metrics")
    return output_path


def estimate_fee_rates_from_aggregates(
    fees_per_block_csv: Path,
    tx_per_day_csv: Path,
    output_dir: Path
) -> Path:
    """
    Estimate fee rate metrics from aggregate data when transaction-level data unavailable.
    
    This is a simplified approach that estimates median and p90 fee rates
    based on total fees and transaction counts.
    
    Args:
        fees_per_block_csv: CSV with [date, fees_per_block_btc]
        tx_per_day_csv: CSV with [date, tx_per_day]
        output_dir: Where to save result
    
    Returns:
        Path to saved CSV
    
    Methodology:
        - Assumes average transaction size of ~500 vB (typical)
        - Estimates median fee rate from total fees / total vB
        - Estimates p90 as 2x median (urgency premium)
        - Computes urgency spread = p90 - median
    
    Limitations:
        - Less precise than per-transaction analysis
        - Assumes constant transaction size distribution
        - May not capture true fee rate distribution
    
    Use Case:
        - When transaction-level data unavailable
        - For initial analysis and validation
        - Better than no fee rate data at all
    """
    print(f"\n📊 Estimating fee rate metrics from aggregates...")
    print(f"   Fees CSV: {fees_per_block_csv}")
    print(f"   TX CSV: {tx_per_day_csv}")
    
    # Load data
    fees_df = load_csv(fees_per_block_csv)
    tx_df = load_csv(tx_per_day_csv)
    
    # Merge on date
    df = fees_df.merge(tx_df, on='date', how='inner')
    
    # Estimate average transaction size (vB)
    # Typical Bitcoin transaction: ~250-500 vB
    # We'll use 400 vB as a reasonable average
    avg_tx_size_vb = 400
    
    # Estimate total vB per day
    df['total_vb_per_day'] = df['tx_per_day'] * avg_tx_size_vb
    
    # Estimate average fee rate (sat/vB)
    df['avg_fee_rate_sat_vb'] = (df['fees_per_block_btc'] * 100_000_000) / df['total_vb_per_day']
    
    # Estimate median fee rate (assume median ≈ average for simplicity)
    df['median_sat_vb'] = df['avg_fee_rate_sat_vb']
    
    # Estimate p90 fee rate (assume 2x median for urgency premium)
    df['p90_sat_vb'] = df['median_sat_vb'] * 2.0
    
    # Compute urgency spread
    df['urgency_spread_sat_vb'] = df['p90_sat_vb'] - df['median_sat_vb']
    
    # Keep only relevant columns
    result_df = df[['date', 'median_sat_vb', 'p90_sat_vb', 'urgency_spread_sat_vb', 'tx_per_day']].copy()
    
    # Save
    output_path = output_dir / "fee_rate_urgency_estimated.csv"
    save_csv(result_df, output_path)
    
    print(f"   ✓ Estimated fee rates for {len(result_df)} days")
    print(f"   ⚠️  Note: This is an estimation - actual fee rates may vary")
    
    return output_path


# Pseudocode for alternative approach (if no transaction-level data):
"""
Alternative: Use Blockchain.com or other APIs that provide daily median fees

def estimate_urgency_from_mempool():
    '''
    If historical per-tx data is unavailable, estimate urgency from:
    - Mempool.space fee estimates (current only)
    - Blockchain.com average fees (limited granularity)
    
    Limitation: Less precise than per-transaction analysis
    '''
    # Fetch current fee estimates
    from src.data_sources.mempool_space import fetch_fee_estimates
    fees = fetch_fee_estimates()
    
    # Map to urgency proxy:
    # median ~ "hourFee" or similar
    # p90 ~ "fastestFee"
    # spread ~ fastestFee - hourFee
    
    # For historical: look for archived snapshots or community datasets
    pass
"""

if __name__ == "__main__":
    print("Fee Rate & Urgency Metrics Module")
    print("\n📝 Implementation steps:")
    print("1. Collect transaction-level fee rate data (see node_rpc.py)")
    print("2. Run compute_daily_fee_rate_metrics() on your data")
    print("3. Save to data/processed/fee_rate_urgency_daily.csv")
    print("\nAlternatively: Use pre-aggregated block/daily data if available")

