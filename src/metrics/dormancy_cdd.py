"""
Dormancy & Coin Days Destroyed (CDD/BDD) Metrics

This module analyzes Bitcoin dormancy through Coin Days Destroyed.

What is CDD/BDD?
----------------
Coin Days Destroyed (CDD) or Bitcoin Days Destroyed (BDD) measures
the "age" of coins when they move:

Formula: CDD = Σ (amount_btc × days_since_last_spent)

Example:
    - You receive 1 BTC on Jan 1
    - You spend it on Jan 31 (30 days later)
    - CDD = 1 BTC × 30 days = 30 bitcoin-days destroyed

Theory:
-------
During economic crises, we expect:
- HIGH CDD = Old coins waking up (HODLers liquidating for liquidity)
- This reflects Keynesian liquidity preference: breaking dormancy
  to access liquid funds during uncertainty

Interpretation:
    - Rising BDD = Dormant wealth being mobilized
    - Stable/low BDD = HODLing behavior continues
    
Data Sources:
-------------
1. Blockchain.com API:
   - Provides daily BDD series (easiest option)
   - Historical data available
   
2. Bitcoin Core RPC (advanced):
   - Requires txindex=1
   - For each transaction input:
     a. Look up previous transaction
     b. Calculate age: (current_block_time - prev_tx_time) / 86400 days
     c. Sum: amount × age
   - More precise but computationally intensive

Limitations:
------------
- Affected by exchanges moving old UTXOs (not crisis-related)
- Large wallets rebalancing can create spikes
- Consider normalizing by 30-day moving average
"""

from pathlib import Path
from typing import Optional
import pandas as pd

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.io import save_csv, load_csv
from src.utils.math_stats import rolling_mean


def compute_cdd_from_blockchain_com(
    bdd_csv: Path,
    output_dir: Path
) -> Path:
    """
    Process BDD data from Blockchain.com API.
    
    Args:
        bdd_csv: Path to CSV from blockchain_com.fetch_bitcoin_days_destroyed()
                Columns: [date, bdd]
        output_dir: Where to save processed metrics
    
    Returns:
        Path to processed CSV
    
    Processing:
        1. Load BDD data
        2. Compute 30-day moving average (smooth noise)
        3. Flag large spikes (potential old coin movements)
        4. Save enriched CSV
    
    Output CSV columns:
        - date
        - bdd (raw)
        - bdd_30d_ma (smoothed)
        - bdd_pct_of_ma (spike detector: bdd / bdd_30d_ma)
    """
    print(f"\n📊 Processing Bitcoin Days Destroyed (BDD)...")
    print(f"   Input: {bdd_csv}")
    
    # Load data
    df = load_csv(bdd_csv)
    
    # Compute 30-day moving average for smoothing
    df['bdd_30d_ma'] = rolling_mean(df['bdd'], window=30)
    
    # Spike detector: how much above/below the MA?
    df['bdd_pct_of_ma'] = (df['bdd'] / df['bdd_30d_ma']) * 100
    
    # Save
    output_path = output_dir / "dormancy_bdd_daily.csv"
    save_csv(df, output_path)
    
    print(f"   ✓ Processed {len(df)} days of BDD data")
    print(f"   ✓ Added 30-day MA and spike indicators")
    
    return output_path


def compute_cdd_from_node_rpc(
    start_date: str,
    end_date: str,
    output_dir: Path,
    rpc_connection = None
) -> Optional[Path]:
    """
    Compute CDD directly from blockchain using Bitcoin Core RPC.
    
    Args:
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
        output_dir: Where to save result
        rpc_connection: Active RPC connection (from node_rpc.connect_to_node)
    
    Returns:
        Path to saved CSV, or None if not implemented
    
    Algorithm (Pseudocode):
    -----------------------
    cdd_daily = {}
    
    for each block in date range:
        cdd_block = 0
        
        for each transaction in block (exclude coinbase):
            for each input in transaction:
                # Look up the previous transaction (this input is spending)
                prev_tx = get_transaction(input.prev_txid)
                prev_output = prev_tx.outputs[input.prev_vout]
                
                # Calculate age
                age_seconds = block.time - prev_tx.time
                age_days = age_seconds / 86400
                
                # Calculate coin days destroyed
                amount_btc = prev_output.value
                cdd_block += amount_btc * age_days
        
        date = block.date
        cdd_daily[date] = cdd_block
    
    save to CSV
    
    ⚠️ WARNING: This is computationally intensive!
       - Requires txindex=1
       - Processing millions of transactions
       - Can take hours for long date ranges
       - Consider caching intermediate results
    
    TODO: Implement if you need more precision than Blockchain.com
    """
    print(f"\n📊 Computing CDD from node RPC...")
    print(f"   Date range: {start_date} to {end_date}")
    
    if rpc_connection is None:
        print("   ❌ No RPC connection provided")
        print("   💡 Use blockchain_com API for easier data access")
        return None
    
    # TODO: Implement full algorithm (see pseudocode above)
    # 
    # This is advanced! You'll need to:
    # 1. Query each block in range
    # 2. For each transaction, look up input sources
    # 3. Calculate time difference (age)
    # 4. Accumulate CDD per day
    # 5. Save to CSV
    #
    # Alternatively: Use Blockchain.com BDD API (much faster!)
    
    print("   ⚠️  Not implemented - use blockchain_com.py instead!\n")
    return None


def analyze_bdd_spikes(
    bdd_csv: Path,
    threshold_pct: float = 200.0
) -> pd.DataFrame:
    """
    Identify days with unusually high BDD (old coins waking up).
    
    Args:
        bdd_csv: Processed BDD CSV with 'bdd_pct_of_ma' column
        threshold_pct: Flag days where BDD > threshold% of 30-day MA
    
    Returns:
        DataFrame of spike days with context
    
    Output columns:
        - date
        - bdd
        - bdd_30d_ma
        - bdd_pct_of_ma
        - spike_magnitude (how many standard deviations above mean)
    
    Use Case:
        - Identify potential HODLer capitulation events
        - Cross-reference with crisis dates
        - Qualitative analysis of which old coins moved
    
    TODO: Implement after processing BDD data
    """
    print(f"\n🔍 Analyzing BDD spikes...")
    print(f"   Threshold: {threshold_pct}% of 30-day MA")
    
    # TODO: Implement
    # 
    # df = load_csv(bdd_csv)
    # 
    # # Filter for spikes
    # spikes = df[df['bdd_pct_of_ma'] > threshold_pct].copy()
    # 
    # # Sort by magnitude
    # spikes = spikes.sort_values('bdd_pct_of_ma', ascending=False)
    # 
    # print(f"   ✓ Found {len(spikes)} spike days")
    # print(f"\n   Top 5 spikes:")
    # print(spikes[['date', 'bdd', 'bdd_pct_of_ma']].head())
    # 
    # return spikes
    
    print("   ⚠️  Not implemented yet\n")
    return pd.DataFrame()


def correlate_bdd_with_events(
    bdd_csv: Path,
    events_dict: dict,
    window_days: int = 30
) -> pd.DataFrame:
    """
    Check if BDD spikes align with crisis events.
    
    Args:
        bdd_csv: Processed BDD CSV
        events_dict: {event_name: anchor_date} from config
        window_days: Look ±N days around each event
    
    Returns:
        DataFrame with BDD statistics per event
    
    Output columns:
        - event_name
        - anchor_date
        - bdd_mean_pre (30 days before)
        - bdd_mean_crisis (30 days after)
        - percent_change
        - max_spike_date (date of largest BDD in crisis window)
        - max_spike_value
    
    Use Case:
        - Quick check: Do crises correlate with dormancy breaks?
        - Include in paper's summary tables
    
    TODO: Implement as part of analysis pipeline
    """
    print(f"\n🔗 Correlating BDD with crisis events...")
    
    # TODO: Implement
    # This will be useful for your paper!
    # Compare pre-crisis vs. crisis BDD levels
    
    print("   ⚠️  Not implemented yet\n")
    return pd.DataFrame()


# Real-world interpretation notes for your paper:
"""
Interpreting BDD in Context:
----------------------------

HIGH BDD can indicate:
✅ Liquidity preference (HODLers need cash → sell old BTC)
✅ Strategic reallocation (moving from cold storage → exchange → fiat/goods)
✅ Inheritance/lost-then-recovered keys (old coins awakening)

❌ BUT also non-crisis factors:
   - Exchange wallet consolidation (technical, not behavioral)
   - Satoshi's coins moving (would be enormous spike)
   - Whale repositioning (could be unrelated to macro)

For your thesis:
- Focus on relative changes (pre vs. crisis BDD)
- Compare multiple crises for patterns
- Acknowledge limitations in Discussion section
- Consider segmenting by UTXO age buckets (1-2yr, 2-5yr, 5+yr)
  if data available
"""

if __name__ == "__main__":
    print("Dormancy & CDD Metrics Module")
    print("\n📝 Recommended workflow:")
    print("1. Fetch BDD from Blockchain.com (easiest)")
    print("   → See src/data_sources/blockchain_com.py")
    print("2. Process with compute_cdd_from_blockchain_com()")
    print("3. Analyze spikes with analyze_bdd_spikes()")
    print("4. Correlate with events using correlate_bdd_with_events()")
    print("\n💡 For your paper:")
    print("   'During the Cyprus crisis, BDD increased by X%,")
    print("    suggesting HODLers broke dormancy to access liquidity.'")

