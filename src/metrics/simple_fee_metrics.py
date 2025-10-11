"""
Simple Fee Metrics - No Block Normalization

This module computes straightforward fee metrics using daily totals:
1. Total fees per day (BTC) - Direct miner revenue
2. Average fee per transaction - Urgency proxy
3. Fee-to-subsidy ratio - Using date-based subsidy schedule

No assumptions about blocks per day - just clean daily aggregates.
"""

from pathlib import Path
import pandas as pd

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.io import save_csv, load_csv


def get_subsidy_on_date(date_str: str) -> float:
    """
    Get block subsidy based on date using Bitcoin's halving schedule.
    
    Args:
        date_str: Date in YYYY-MM-DD format
    
    Returns:
        Block subsidy in BTC
    
    Halving Schedule:
        2009-01-03 to 2012-11-27: 50 BTC
        2012-11-28 to 2016-07-08: 25 BTC
        2016-07-09 to 2020-05-10: 12.5 BTC
        2020-05-11 to 2024-04-18: 6.25 BTC
        2024-04-19 onwards: 3.125 BTC
    """
    date = pd.Timestamp(date_str)
    
    if date < pd.Timestamp('2012-11-28'):
        return 50.0
    elif date < pd.Timestamp('2016-07-09'):
        return 25.0
    elif date < pd.Timestamp('2020-05-11'):
        return 12.5
    elif date < pd.Timestamp('2024-04-19'):
        return 6.25
    else:
        return 3.125


def compute_fee_metrics(
    fees_csv: Path,
    tx_csv: Path,
    output_dir: Path
) -> Path:
    """
    Compute all fee metrics from daily data.
    
    Args:
        fees_csv: Path to blockchain_com_fees_btc_day.csv
        tx_csv: Path to blockchain_com_tx_per_day.csv
        output_dir: Where to save computed metrics
    
    Returns:
        Path to saved metrics CSV
    
    Output CSV columns:
        - date: YYYY-MM-DD
        - fees_btc_day: Total fees in BTC (miner revenue)
        - tx_per_day: Number of transactions
        - avg_fee_per_tx: fees_btc_day / tx_per_day (urgency proxy)
        - subsidy_btc: Block subsidy on that date
        - daily_subsidy_total: ~144 * subsidy (approximate daily issuance)
        - fee_to_subsidy: fees / (fees + daily_subsidy_total)
    """
    print("\n📊 Computing fee metrics from daily data...")
    
    # Load data
    fees_df = load_csv(fees_csv)
    tx_df = load_csv(tx_csv)
    
    # Merge on date
    df = fees_df.merge(tx_df, on='date', how='inner')
    
    print(f"   Merged {len(df)} days of data")
    
    # Compute average fee per transaction
    df['avg_fee_per_tx'] = df['fees_btc_day'] / df['tx_per_day']
    
    # Get subsidy for each date
    df['subsidy_btc'] = df['date'].apply(get_subsidy_on_date)
    
    # Estimate daily subsidy issuance (~144 blocks/day)
    # This is ONLY for the ratio calculation, not per-block normalization
    df['daily_subsidy_total'] = df['subsidy_btc'] * 144
    
    # Compute fee-to-subsidy ratio
    df['fee_to_subsidy'] = df['fees_btc_day'] / (df['fees_btc_day'] + df['daily_subsidy_total'])
    
    # Reorder columns for clarity
    columns = [
        'date',
        'fees_btc_day',
        'tx_per_day', 
        'avg_fee_per_tx',
        'subsidy_btc',
        'daily_subsidy_total',
        'fee_to_subsidy'
    ]
    df = df[columns]
    
    # Save
    output_path = output_dir / "fee_metrics_daily.csv"
    save_csv(df, output_path)
    
    print(f"   ✓ Computed metrics for {len(df)} days")
    print(f"   ✓ Saved to {output_path}")
    
    # Print summary stats
    print(f"\n   Summary Statistics:")
    print(f"   Fees (BTC/day): {df['fees_btc_day'].mean():.4f} avg, {df['fees_btc_day'].max():.4f} max")
    print(f"   Tx/day: {df['tx_per_day'].mean():.0f} avg, {df['tx_per_day'].max():.0f} max")
    print(f"   Avg fee/tx: {df['avg_fee_per_tx'].mean():.6f} BTC avg")
    print(f"   Fee-to-subsidy: {df['fee_to_subsidy'].mean():.4f} avg, {df['fee_to_subsidy'].max():.4f} max")
    
    return output_path


if __name__ == "__main__":
    from pathlib import Path
    
    # Define paths
    project_root = Path(__file__).parent.parent.parent
    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    
    # Compute metrics
    fees_csv = raw_dir / "blockchain_com_fees_btc_day.csv"
    tx_csv = raw_dir / "blockchain_com_tx_per_day.csv"
    
    if fees_csv.exists() and tx_csv.exists():
        compute_fee_metrics(fees_csv, tx_csv, processed_dir)
    else:
        print("❌ Raw data files not found. Run 01_fetch_data.py first.")

