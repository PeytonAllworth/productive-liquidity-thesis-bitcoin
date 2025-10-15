#!/usr/bin/env python3
"""
Script 01: Fetch Raw Data

This script fetches raw blockchain data from various sources and saves
to data/raw/.

Data Sources:
- Blockchain.com API (no auth required)
- Mempool.space API (current snapshots)
- Bitcoin Core RPC (optional, requires node)

Usage:
    python scripts/01_fetch_data.py --sources blockchain_com mempool_space
    python scripts/01_fetch_data.py --sources blockchain_com --start-date 2012-01-01
    python scripts/01_fetch_data.py --all
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.config import load_config, get_data_paths
from src.data_sources import blockchain_com, mempool_space, blockchair


def fetch_blockchain_com_data(output_dir: Path, timespan: str = "all") -> dict:
    """
    Fetch all available data from Blockchain.com API.
    
    Args:
        output_dir: Where to save CSVs
        timespan: Time span ('all', '1year', etc.)
    
    Returns:
        Dictionary of downloaded file paths
    """
    print("\n" + "=" * 70)
    print("📥 FETCHING DATA FROM BLOCKCHAIN.COM")
    print("=" * 70)
    
    paths = blockchain_com.fetch_all_metrics(output_dir, timespan=timespan)
    
    # Also compute fees per block
    if 'fees' in paths and 'blocks' in paths:
        print("\n📊 Computing fees per block...")
        fees_per_block_path = blockchain_com.compute_fees_per_block(
            paths['fees'],
            paths['blocks'],
            output_dir
        )
        paths['fees_per_block'] = fees_per_block_path
    
    return paths


def fetch_mempool_space_data(output_dir: Path) -> dict:
    """
    Fetch current mempool snapshot from Mempool.space.
    
    Args:
        output_dir: Where to save JSON
    
    Returns:
        Dictionary with snapshot path
    
    Note: Historical data not available via API
    """
    print("\n" + "=" * 70)
    print("📥 FETCHING MEMPOOL SNAPSHOT FROM MEMPOOL.SPACE")
    print("=" * 70)
    
    try:
        snapshot = mempool_space.snapshot_current_state(output_dir)
        print("\n✅ Mempool snapshot saved")
        print("   💡 For historical data, set up periodic snapshots or use node RPC")
        return {'mempool_snapshot': 'saved'}
    except Exception as e:
        print(f"\n❌ Failed to fetch mempool data: {e}")
        return {}


def fetch_blockchair_data(output_dir: Path, start_date: str, end_date: str) -> dict:
    """
    Fetch real daily blocks data from Blockchair API.
    
    Args:
        output_dir: Where to save CSVs
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
    
    Returns:
        Dictionary of file paths
    
    Note: Blockchair provides real historical block counts, not estimates
    """
    print("\n" + "=" * 70)
    print("📥 FETCHING REAL BLOCKS DATA FROM BLOCKCHAIR")
    print("=" * 70)
    
    try:
        paths = blockchair.fetch_all_metrics(output_dir, start_date, end_date)
        return paths
    except Exception as e:
        print(f"\n❌ Error fetching from Blockchair: {e}")
        return {}


def fetch_node_rpc_data(output_dir: Path, start_date: str, end_date: str) -> dict:
    """
    Fetch data from Bitcoin Core node via RPC.
    
    Args:
        output_dir: Where to save CSVs
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
    
    Returns:
        Dictionary of file paths
    
    Note: Requires node setup (see node_rpc.py docstring)
    """
    print("\n" + "=" * 70)
    print("📥 FETCHING DATA FROM BITCOIN CORE NODE")
    print("=" * 70)
    
    print("\n⚠️  Node RPC data fetching not fully implemented yet")
    print("   Requires:")
    print("   1. Bitcoin Core running with txindex=1")
    print("   2. RPC credentials in config/settings.yaml")
    print("   3. Implementation of fetch functions in node_rpc.py")
    print("\n   For now, use Blockchain.com API data")
    
    return {}


def main():
    """Main entry point for data fetching script."""
    
    parser = argparse.ArgumentParser(
        description="Fetch raw blockchain data for Bitcoin liquidity crisis research",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--sources',
        nargs='+',
        choices=['blockchain_com', 'mempool_space', 'blockchair', 'node_rpc'],
        default=['blockchain_com', 'blockchair'],
        help='Data sources to fetch from (default: blockchain_com, blockchair)'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Fetch from all available sources'
    )
    
    parser.add_argument(
        '--start-date',
        type=str,
        default='2009-01-01',
        help='Start date for historical data (YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--end-date',
        type=str,
        default='2024-12-31',
        help='End date for historical data (YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--timespan',
        type=str,
        default='all',
        choices=['all', '1year', '2years', '30days'],
        help='Blockchain.com timespan parameter'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = load_config()
        paths = get_data_paths(config)
        output_dir = paths['raw']
    except FileNotFoundError:
        print("❌ Configuration file not found!")
        print("   Please copy config/settings.example.yaml to config/settings.yaml")
        sys.exit(1)
    
    # Determine which sources to use
    if args.all:
        sources = ['blockchain_com', 'mempool_space', 'blockchair']
    else:
        sources = args.sources
    
    print("\n" + "=" * 70)
    print("🚀 BITCOIN LIQUIDITY CRISIS DATA FETCHER")
    print("=" * 70)
    print(f"Sources: {', '.join(sources)}")
    print(f"Output directory: {output_dir}")
    print(f"Date range: {args.start_date} to {args.end_date}")
    print("=" * 70)
    
    all_paths = {}
    
    # Fetch from each source
    for source in sources:
        try:
            if source == 'blockchain_com':
                paths = fetch_blockchain_com_data(output_dir, args.timespan)
                all_paths.update(paths)
            
            elif source == 'mempool_space':
                paths = fetch_mempool_space_data(output_dir)
                all_paths.update(paths)
            
            elif source == 'blockchair':
                paths = fetch_blockchair_data(output_dir, args.start_date, args.end_date)
                all_paths.update(paths)
            
            elif source == 'node_rpc':
                paths = fetch_node_rpc_data(output_dir, args.start_date, args.end_date)
                all_paths.update(paths)
        
        except Exception as e:
            print(f"\n❌ Error fetching from {source}: {e}")
            continue
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ DATA FETCHING COMPLETE")
    print("=" * 70)
    print(f"Downloaded {len(all_paths)} datasets to {output_dir}")
    print("\nNext steps:")
    print("1. Run: python scripts/02_compute_metrics.py")
    print("2. Then: python scripts/03_make_figures.py")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

