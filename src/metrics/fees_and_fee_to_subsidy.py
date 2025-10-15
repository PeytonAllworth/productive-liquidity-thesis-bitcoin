"""
Fees & Fee-to-Subsidy Ratio Metrics

This module computes:
1. Fees per block (BTC) - direct miner revenue from fees
2. Fee-to-Subsidy ratio - fees / (fees + subsidy)

Theory:
-------
As Bitcoin matures, the fee market becomes increasingly important for
securing the network. During crises:
- Fees per block should increase (more transactions, higher urgency)
- Fee-to-Subsidy ratio should increase (fees become larger share of reward)

This demonstrates that Bitcoin's productive layer (mining/security) benefits
from economic crises through increased fee market activity - a counter-cyclical
force without requiring monetary expansion.

Post-halving, this effect becomes even more critical as subsidies decline.
"""

from pathlib import Path
from typing import Dict, Optional
import pandas as pd

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.io import save_csv, load_csv


def block_subsidy(height: int) -> float:
    """
    Calculate block subsidy (coinbase reward) at a given block height.
    
    Args:
        height: Block height (integer)
    
    Returns:
        Subsidy in BTC (float)
    
    Formula:
        - Initial subsidy: 50 BTC (block 0)
        - Halves every 210,000 blocks (~4 years)
        - Formula: 50 / (2 ^ halvings)
    
    Example:
        >>> block_subsidy(0)
        50.0
        >>> block_subsidy(210000)
        25.0
        >>> block_subsidy(420000)
        12.5
        >>> block_subsidy(630000)
        6.25
        >>> block_subsidy(840000)
        3.125
    
    Key Halvings:
        - Block 210,000 (Nov 2012): 50 → 25 BTC
        - Block 420,000 (Jul 2016): 25 → 12.5 BTC
        - Block 630,000 (May 2020): 12.5 → 6.25 BTC
        - Block 840,000 (Apr 2024): 6.25 → 3.125 BTC
    """
    initial_subsidy = 50.0
    halvings = height // 210000
    return initial_subsidy / (2 ** halvings)


def height_to_date_approx(height: int) -> str:
    """
    Approximate date for a given block height.
    
    Args:
        height: Block height
    
    Returns:
        Approximate date string (YYYY-MM-DD)
    
    Formula:
        - Genesis: Block 0 = 2009-01-03
        - Average: 144 blocks/day (10 min blocks)
        - Date ≈ genesis + (height / 144) days
    
    Note: This is approximate! Actual block times vary.
          For precise mapping, query a node or use an API.
    
    TODO: Implement or use a lookup table for accuracy
    """
    from datetime import datetime, timedelta
    
    genesis_date = datetime(2009, 1, 3)
    days_since_genesis = height / 144  # Approximate
    approx_date = genesis_date + timedelta(days=days_since_genesis)
    
    return approx_date.strftime("%Y-%m-%d")


def compute_fee_to_subsidy(
    fees_btc: float,
    subsidy_btc: float
) -> float:
    """
    Compute fee-to-subsidy ratio.
    
    Args:
        fees_btc: Total fees in BTC
        subsidy_btc: Block subsidy in BTC
    
    Returns:
        Ratio: fees / (fees + subsidy)
    
    Interpretation:
        - 0.00 = 0% of block reward from fees (all from subsidy)
        - 0.50 = 50% from fees, 50% from subsidy
        - 1.00 = 100% from fees (subsidy negligible or zero)
    
    Example:
        >>> compute_fee_to_subsidy(1.0, 6.25)
        0.1379  # ~13.8% from fees
        >>> compute_fee_to_subsidy(3.0, 3.125)
        0.4898  # ~49% from fees
    
    Use Case:
        Track Bitcoin's transition from subsidy-dependent to fee-dependent security.
        During crises, expect this ratio to spike temporarily.
    """
    total_reward = fees_btc + subsidy_btc
    if total_reward == 0:
        return 0.0
    return fees_btc / total_reward


def compute_fees_per_block(
    fees_per_day_csv: Path,
    blocks_per_day_csv: Path,
    output_dir: Path
) -> Path:
    """
    Compute fees per block from daily aggregates.
    
    Args:
        fees_per_day_csv: CSV with columns [date, fees_btc_day]
        blocks_per_day_csv: CSV with columns [date, blocks_per_day]
        output_dir: Where to save result
    
    Returns:
        Path to saved CSV
    
    Output CSV columns:
        - date
        - fees_btc_day
        - blocks_per_day
        - fees_per_block_btc
    
    Formula:
        fees_per_block = fees_btc_day / blocks_per_day
    
    Data Sources:
        - Blockchain.com API (see blockchain_com.py)
        - Bitcoin Core RPC (see node_rpc.py)
    """
    print(f"\n📊 Computing fees per block...")
    print(f"   Fees CSV: {fees_per_day_csv}")
    print(f"   Blocks CSV: {blocks_per_day_csv}")
    
    # Load CSVs
    fees_df = load_csv(fees_per_day_csv)
    blocks_df = load_csv(blocks_per_day_csv)
    
    # Merge on date
    df = fees_df.merge(blocks_df, on='date', how='inner')
    
    # Compute fees per block
    df['fees_per_block_btc'] = df['fees_btc_day'] / df['blocks_per_day']
    
    # Save
    output_path = output_dir / "fees_per_block_btc.csv"
    save_csv(df, output_path)
    
    print(f"   ✓ Computed fees per block for {len(df)} days")
    return output_path


def compute_fee_to_subsidy_ratio(
    fees_per_block_csv: Path,
    output_dir: Path,
    height_column: Optional[str] = None
) -> Path:
    """
    Compute fee-to-subsidy ratio for each day/block.
    
    Args:
        fees_per_block_csv: CSV with [date, fees_per_block_btc]
                           Optionally: [date, height, fees_per_block_btc]
        output_dir: Where to save result
        height_column: If provided, use exact block heights for subsidy
                      If None, approximate from date
    
    Returns:
        Path to saved CSV
    
    Output CSV columns:
        - date
        - fees_per_block_btc
        - subsidy_btc (computed from height or date)
        - fee_to_subsidy (ratio)
    """
    print(f"\n📊 Computing fee-to-subsidy ratio...")
    print(f"   Input: {fees_per_block_csv}")
    
    # Load data
    df = load_csv(fees_per_block_csv)
    
    if height_column and height_column in df.columns:
        # Use exact heights
        df['subsidy_btc'] = df[height_column].apply(block_subsidy)
    else:
        # Approximate from date
        print("   ⚠️  No height column found - using approximate subsidy")
        df['approx_height'] = ((df['date'] - pd.Timestamp('2009-01-03')).dt.days * 144).astype(int)
        df['subsidy_btc'] = df['approx_height'].apply(block_subsidy)
    
    # Compute ratio
    df['fee_to_subsidy'] = df.apply(
        lambda row: compute_fee_to_subsidy(row['fees_per_block_btc'], row['subsidy_btc']),
        axis=1
    )
    
    # Save
    output_path = output_dir / "fee_to_subsidy_daily.csv"
    save_csv(df, output_path)
    
    print(f"   ✓ Computed fee-to-subsidy for {len(df)} days")
    return output_path


def add_halving_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add column indicating halving era.
    
    Args:
        df: DataFrame with 'date' or 'height' column
    
    Returns:
        DataFrame with added 'halving_era' column
    
    Halving Eras:
        0: 50 BTC (2009-2012)
        1: 25 BTC (2012-2016)
        2: 12.5 BTC (2016-2020)
        3: 6.25 BTC (2020-2024)
        4: 3.125 BTC (2024+)
    
    Use Case:
        - Control for halving effects in analysis
        - Visualize era boundaries on charts
    
    TODO: Implement if needed for analysis
    """
    # TODO: Add implementation
    # 
    # if 'height' in df.columns:
    #     df['halving_era'] = df['height'] // 210000
    # elif 'date' in df.columns:
    #     # Use approximate height from date
    #     df['approx_height'] = ((df['date'] - pd.Timestamp('2009-01-03')).dt.days * 144).astype(int)
    #     df['halving_era'] = df['approx_height'] // 210000
    # 
    # return df
    
    pass


if __name__ == "__main__":
    print("Fees & Fee-to-Subsidy Module")
    print("\n📝 Implementation steps:")
    print("1. Fetch fees_per_day and blocks_per_day (see blockchain_com.py)")
    print("2. Compute fees_per_block using compute_fees_per_block()")
    print("3. Compute fee-to-subsidy ratio using compute_fee_to_subsidy_ratio()")
    print("\nKey insight: Fee-to-subsidy increases during crises = productive asset!")
    
    # Demo: Block subsidy calculation
    print("\n📈 Block subsidy examples:")
    for height in [0, 210000, 420000, 630000, 840000]:
        subsidy = block_subsidy(height)
        date_approx = height_to_date_approx(height)
        print(f"   Height {height:>7} (~{date_approx}): {subsidy:>6.3f} BTC")

