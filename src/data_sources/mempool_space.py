"""
Mempool.space API data source adapter.

This module fetches real-time and historical mempool data from mempool.space.
No authentication required!

Key Metrics:
- Current mempool size (vbytes)
- Fee rate estimates (sat/vB for different priority levels)
- Historical fee rates (limited availability)

API Documentation: https://mempool.space/docs/api/rest

⚠️ LIMITATION: Historical data availability is limited!
   - mempool.space focuses on recent data
   - For deep historical analysis (pre-2020), you may need:
     1. A full Bitcoin Core node with historical mempool snapshots
     2. Archived data from community sources
     3. On-chain fee analysis from confirmed blocks (see node_rpc.py)

Alternative Approach:
   - Use on-chain fee rates from confirmed blocks (available via node RPC)
   - This shows *actual* fees paid, not mempool estimates
   - More reliable for historical crisis analysis
"""

import time
from typing import Dict, List, Optional
from pathlib import Path
import pandas as pd
import requests

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.io import save_csv, save_json, ensure_dir


def fetch_current_mempool_info(
    base_url: str = "https://mempool.space/api"
) -> dict:
    """
    Fetch current mempool statistics.
    
    Args:
        base_url: Mempool.space API base URL
    
    Returns:
        Dictionary with mempool info
    
    Response fields:
        - size: Current mempool size in vbytes
        - bytes: Same as size (legacy field)
        - usage: Mempool memory usage
        - maxmempool: Max mempool size
        - mempoolminfee: Minimum fee rate to enter mempool
        - minrelaytxfee: Minimum relay fee rate
    
    Example:
        >>> info = fetch_current_mempool_info()
        >>> print(f"Mempool size: {info['size']:,} vbytes")
        Mempool size: 150,000,000 vbytes
    
    API Endpoint: GET /mempool
    """
    url = f"{base_url}/mempool"
    
    print(f"Fetching current mempool info from {url}...")
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    
    data = response.json()
    print(f"  ✓ Mempool size: {data.get('size', 0):,} vbytes")
    
    return data


def fetch_fee_estimates(
    base_url: str = "https://mempool.space/api"
) -> dict:
    """
    Fetch current fee rate estimates for different confirmation priorities.
    
    Args:
        base_url: Mempool.space API base URL
    
    Returns:
        Dictionary with fee estimates in sat/vB
        Keys: '1' (fastest), '3', '6', '12', '24', '72', '144', '504', '1008'
        (Numbers represent target blocks for confirmation)
    
    Example:
        >>> estimates = fetch_fee_estimates()
        >>> print(f"Next block fee: {estimates['1']} sat/vB")
        Next block fee: 150 sat/vB
    
    API Endpoint: GET /v1/fees/recommended
    
    Note:
        - Higher sat/vB = faster confirmation (higher priority)
        - During crises, we expect large spreads (urgency!)
    """
    url = f"{base_url}/v1/fees/recommended"
    
    print(f"Fetching fee estimates from {url}...")
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    
    data = response.json()
    
    # Response format: {"fastestFee": 150, "halfHourFee": 100, "hourFee": 80, ...}
    print(f"  ✓ Fastest fee: {data.get('fastestFee')} sat/vB")
    
    return data


def snapshot_current_state(output_dir: Path) -> dict:
    """
    Take a snapshot of current mempool + fee state and save to JSON.
    
    Args:
        output_dir: Directory to save snapshot
    
    Returns:
        Dictionary with timestamp and data
    
    Output JSON structure:
        {
            "timestamp": "2024-01-15T12:00:00",
            "mempool": {...},
            "fees": {...}
        }
    
    Use Case:
        - Run this periodically (e.g., daily cron job) to build historical dataset
        - For real-time crisis monitoring
    
    Example:
        >>> from pathlib import Path
        >>> snapshot_current_state(Path("data/raw"))
    """
    from datetime import datetime
    
    timestamp = datetime.utcnow().isoformat()
    
    # Fetch data
    mempool_info = fetch_current_mempool_info()
    fee_estimates = fetch_fee_estimates()
    
    # Combine into snapshot
    snapshot = {
        'timestamp': timestamp,
        'mempool': mempool_info,
        'fees': fee_estimates
    }
    
    # Save with timestamp in filename
    filename = f"mempool_snapshot_{timestamp.replace(':', '-')}.json"
    output_path = Path(output_dir) / filename
    save_json(snapshot, output_path)
    
    return snapshot


def fetch_historical_fee_rates_placeholder(
    start_date: str,
    end_date: str,
    output_dir: Path
) -> Optional[Path]:
    """
    Placeholder for historical fee rate fetching.
    
    ⚠️ IMPORTANT: Mempool.space does NOT provide deep historical fee data via API!
    
    Alternative Approaches:
    
    1. Use Bitcoin Core RPC (see node_rpc.py):
       - Query confirmed blocks in date range
       - Extract fee rates from each transaction
       - Compute daily median, p90, etc.
       - ✅ This is the RECOMMENDED approach for historical analysis
    
    2. Use archived data:
       - Check if mempool.space publishes historical datasets
       - Look for community-maintained CSV archives
       - Import manually into data/raw/
    
    3. Use other APIs:
       - Blockchair.com (some free tier)
       - Blockchain.com (limited granularity)
       - Coinmetrics.io (paid)
    
    Args:
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
        output_dir: Where to save (if data found)
    
    Returns:
        Path to CSV if successful, None if not implemented
    
    TODO: Implement one of the alternatives above!
    """
    print("\n⚠️  Historical fee rate fetching not yet implemented!")
    print("    Mempool.space API does not provide deep historical data.")
    print("\n    Recommended approach:")
    print("    1. Use Bitcoin Core RPC (see node_rpc.py)")
    print("    2. Query blocks in date range")
    print("    3. Compute fee rates from transactions")
    print("\n    Or: Import pre-downloaded CSV into data/raw/\n")
    
    # Pseudocode for implementation:
    # 
    # if using_node_rpc:
    #     from src.data_sources.node_rpc import fetch_block_fee_rates
    #     return fetch_block_fee_rates(start_date, end_date, output_dir)
    # else:
    #     # Look for manual CSV import
    #     csv_path = output_dir / "historical_fee_rates_manual.csv"
    #     if csv_path.exists():
    #         return csv_path
    #     else:
    #         return None
    
    return None


# Example usage
if __name__ == "__main__":
    from pathlib import Path
    
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw"
    ensure_dir(output_dir)
    
    # Take a snapshot of current state
    print("Taking mempool snapshot...")
    snapshot_current_state(output_dir)
    
    print("\n✅ Done! For historical analysis, see node_rpc.py or import CSVs manually.")

