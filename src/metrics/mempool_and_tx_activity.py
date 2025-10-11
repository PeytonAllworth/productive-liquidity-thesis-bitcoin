"""
Mempool & Transaction Activity Metrics

This module tracks base-layer activity pressure:
1. Mempool backlog (vbytes) - unconfirmed transaction pressure
2. Transactions per day - base-layer usage intensity

Theory:
-------
During economic crises, we expect:
- INCREASED tx/day: More people moving BTC for liquidity
- INCREASED mempool backlog: Network congestion from demand surge
- This creates fee pressure → benefits miners → productive asset thesis

These metrics complement fee rates (they show *volume* not just *price*).

Data Sources:
-------------
1. Transactions per day:
   - Blockchain.com API (historical, easy)
   - Bitcoin Core RPC (requires full node)

2. Mempool backlog:
   - Mempool.space API (current only, limited historical)
   - Manual snapshots (if you set up regular logging)
   - Estimate from tx confirmation delays (indirect proxy)

Limitations:
------------
- Inscriptions/Ordinals inflate tx counts (non-monetary use)
- Lightning Network shifts activity off-chain (reduces base-layer tx)
- Batching by exchanges can obscure individual user behavior
- Mempool historical data is scarce (snapshots needed)
"""

from pathlib import Path
from typing import Optional
import pandas as pd

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.io import save_csv, load_csv
from src.utils.math_stats import rolling_mean


def process_transactions_per_day(
    tx_per_day_csv: Path,
    output_dir: Path
) -> Path:
    """
    Process transactions per day data from Blockchain.com.
    
    Args:
        tx_per_day_csv: CSV with columns [date, tx_per_day]
                       From blockchain_com.fetch_transactions_per_day()
        output_dir: Where to save processed metrics
    
    Returns:
        Path to processed CSV
    
    Processing:
        1. Load tx/day data
        2. Compute 30-day moving average (smooth volatility)
        3. Compute percent change from MA (detect surges)
        4. Optionally: Flag anomalous days
    
    Output CSV columns:
        - date
        - tx_per_day (raw)
        - tx_per_day_30d_ma (smoothed)
        - tx_pct_of_ma (surge detector)
    """
    print(f"\n📊 Processing transactions per day...")
    print(f"   Input: {tx_per_day_csv}")
    
    # Load data
    df = load_csv(tx_per_day_csv)
    
    # Compute 30-day moving average
    df['tx_per_day_30d_ma'] = rolling_mean(df['tx_per_day'], window=30)
    
    # Detect surges
    df['tx_pct_of_ma'] = (df['tx_per_day'] / df['tx_per_day_30d_ma']) * 100
    
    # Save
    output_path = output_dir / "tx_activity_daily.csv"
    save_csv(df, output_path)
    
    print(f"   ✓ Processed {len(df)} days of tx activity")
    
    return output_path


def process_mempool_backlog(
    mempool_csv: Path,
    output_dir: Path
) -> Optional[Path]:
    """
    Process mempool backlog data (if available).
    
    Args:
        mempool_csv: CSV with columns [timestamp, mempool_size_vbytes]
        output_dir: Where to save processed metrics
    
    Returns:
        Path to processed CSV, or None if data unavailable
    
    ⚠️ LIMITATION: Historical mempool data is scarce!
       - Mempool.space doesn't provide deep history via API
       - You may need manual snapshots or community archives
       - Alternative: Use indirect proxies (e.g., avg confirmation time)
    
    Processing:
        1. Aggregate to daily (if timestamps are hourly/minute-level)
        2. Compute rolling averages
        3. Detect congestion events (high backlog)
    
    Output CSV columns:
        - date
        - mempool_vbytes_mean (daily average)
        - mempool_vbytes_max (daily peak)
        - mempool_vbytes_7d_ma (smoothed)
    
    TODO: Implement when historical mempool data is obtained
    """
    print(f"\n📊 Processing mempool backlog...")
    print(f"   Input: {mempool_csv}")
    
    # Check if file exists
    if not Path(mempool_csv).exists():
        print("   ❌ Mempool data not found")
        print("   💡 Options:")
        print("      1. Set up periodic snapshots (mempool_space.snapshot_current_state)")
        print("      2. Find community-archived mempool datasets")
        print("      3. Use indirect proxies (e.g., fee rate variance)")
        return None
    
    # TODO: Implement processing
    # 
    # df = load_csv(mempool_csv)
    # 
    # # If timestamps are not daily, aggregate
    # df['date'] = pd.to_datetime(df['timestamp']).dt.date
    # daily = df.groupby('date').agg({
    #     'mempool_size_vbytes': ['mean', 'max']
    # })
    # daily.columns = ['mempool_vbytes_mean', 'mempool_vbytes_max']
    # daily = daily.reset_index()
    # 
    # # Compute rolling average
    # daily['mempool_vbytes_7d_ma'] = rolling_mean(daily['mempool_vbytes_mean'], window=7)
    # 
    # # Save
    # output_path = output_dir / "mempool_backlog_daily.csv"
    # save_csv(daily, output_path)
    # 
    # print(f"   ✓ Processed mempool backlog")
    # return output_path
    
    print("   ⚠️  Not implemented yet\n")
    return None


def compute_tx_per_block(
    tx_per_day_csv: Path,
    blocks_per_day_csv: Path,
    output_dir: Path
) -> Path:
    """
    Compute average transactions per block.
    
    Args:
        tx_per_day_csv: CSV with [date, tx_per_day]
        blocks_per_day_csv: CSV with [date, blocks_per_day]
        output_dir: Where to save result
    
    Returns:
        Path to saved CSV
    
    Formula:
        tx_per_block = tx_per_day / blocks_per_day
    
    Use Case:
        - Normalizes for mining luck (variable blocks/day)
        - Shows block fullness trend
    
    TODO: Implement when you have both datasets
    """
    print(f"\n📊 Computing transactions per block...")
    
    # TODO: Implement
    # 
    # tx_df = load_csv(tx_per_day_csv)
    # blocks_df = load_csv(blocks_per_day_csv)
    # 
    # df = tx_df.merge(blocks_df, on='date', how='inner')
    # df['tx_per_block'] = df['tx_per_day'] / df['blocks_per_day']
    # 
    # output_path = output_dir / "tx_per_block_daily.csv"
    # save_csv(df, output_path)
    # 
    # return output_path
    
    print("   ⚠️  Not implemented yet\n")
    return None


def detect_activity_surges(
    tx_activity_csv: Path,
    threshold_pct: float = 150.0
) -> pd.DataFrame:
    """
    Identify days with unusually high transaction activity.
    
    Args:
        tx_activity_csv: Processed tx/day CSV with 'tx_pct_of_ma'
        threshold_pct: Flag days where tx > threshold% of 30-day MA
    
    Returns:
        DataFrame of surge days
    
    Output columns:
        - date
        - tx_per_day
        - tx_per_day_30d_ma
        - tx_pct_of_ma
        - pct_above_normal
    
    Use Case:
        - Identify transaction surges
        - Cross-reference with crisis dates
        - Distinguish monetary use from spam (e.g., ordinals surge in 2023)
    
    TODO: Implement after processing tx/day data
    """
    print(f"\n🔍 Detecting transaction activity surges...")
    print(f"   Threshold: {threshold_pct}% of 30-day MA")
    
    # TODO: Implement
    # Similar to BDD spike detection in dormancy_cdd.py
    
    print("   ⚠️  Not implemented yet\n")
    return pd.DataFrame()


# Alternative approach if historical mempool data is unavailable:
def estimate_mempool_pressure_from_fee_variance(
    fee_rate_csv: Path,
    output_dir: Path
) -> Path:
    """
    Estimate mempool pressure using fee rate variance as proxy.
    
    Theory:
        - High mempool backlog → wide fee rate distribution
        - Users bid aggressively → high urgency spread
        - Fee variance correlates with congestion
    
    Args:
        fee_rate_csv: CSV with [date, median_sat_vb, p90_sat_vb, urgency_spread]
        output_dir: Where to save proxy
    
    Returns:
        Path to CSV with estimated pressure metric
    
    Formula:
        mempool_pressure_proxy = urgency_spread / median_sat_vb
        (Normalized urgency relative to baseline)
    
    Limitations:
        - Indirect measure (not actual vbytes)
        - Assumes urgency correlates with backlog
        - Better than nothing if direct data unavailable!
    
    TODO: Implement as fallback option
    """
    print(f"\n📊 Estimating mempool pressure from fee variance...")
    
    # TODO: Implement
    # 
    # df = load_csv(fee_rate_csv)
    # 
    # # Compute normalized urgency
    # df['mempool_pressure_proxy'] = df['urgency_spread_sat_vb'] / df['median_sat_vb']
    # 
    # # Save
    # output_path = output_dir / "mempool_pressure_proxy.csv"
    # save_csv(df, output_path)
    # 
    # return output_path
    
    print("   ⚠️  Not implemented yet\n")
    return None


if __name__ == "__main__":
    print("Mempool & Transaction Activity Module")
    print("\n📝 Recommended workflow:")
    print("1. Fetch tx/day from Blockchain.com")
    print("   → See blockchain_com.fetch_transactions_per_day()")
    print("2. Process with process_transactions_per_day()")
    print("3. Detect surges with detect_activity_surges()")
    print("\nFor mempool backlog:")
    print("   ⚠️  Historical data is LIMITED")
    print("   → Use fee variance proxy OR set up manual snapshots")
    print("\n💡 For your paper:")
    print("   'Transaction volume increased by X% during the crisis,")
    print("    demonstrating increased on-chain liquidity demand.'")

