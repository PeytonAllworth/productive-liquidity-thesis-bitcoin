#!/usr/bin/env python3
"""
Script 02: Compute Metrics

This script processes raw data from data/raw/ and computes BTC-native metrics,
saving results to data/processed/.

Metrics Computed:
1. Fee rate & urgency (median sat/vB, p90, urgency spread)
2. Fees per block & fee-to-subsidy ratio
3. Dormancy proxy (Bitcoin Days Destroyed)
4. Transaction activity (tx/day, mempool pressure)

Usage:
    python scripts/02_compute_metrics.py
    python scripts/02_compute_metrics.py --metrics fees dormancy
    python scripts/02_compute_metrics.py --skip-missing
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.config import load_config, get_data_paths
from src.metrics import (
    fee_rate_urgency,
    fees_and_fee_to_subsidy,
    dormancy_cdd,
    mempool_and_tx_activity
)


def compute_fee_metrics(raw_dir: Path, processed_dir: Path) -> bool:
    """
    Compute fee-related metrics.
    
    Args:
        raw_dir: Path to raw data
        processed_dir: Path to save processed metrics
    
    Returns:
        True if successful, False otherwise
    """
    print("\n" + "=" * 70)
    print("📊 COMPUTING FEE METRICS")
    print("=" * 70)
    
    try:
        # Check for required files
        fees_per_block_csv = raw_dir / "blockchain_com_fees_per_block_btc.csv"
        fees_csv = raw_dir / "blockchain_com_fees_btc_day.csv"
        
        # Try Blockchair blocks data first, fallback to blockchain_com
        blocks_csv = raw_dir / "blockchair_blocks_per_day.csv"
        if not blocks_csv.exists():
            blocks_csv = raw_dir / "blockchain_com_blocks_per_day.csv"
        
        if not fees_per_block_csv.exists():
            print(f"❌ Required file not found: {fees_per_block_csv}")
            print("   Run 01_fetch_data.py first")
            return False
        
        # Compute fee-to-subsidy ratio
        print("\n📈 Computing fee-to-subsidy ratio...")
        output_path = fees_and_fee_to_subsidy.compute_fee_to_subsidy_ratio(
            fees_per_block_csv,
            processed_dir
        )
        
        if output_path:
            print(f"   ✓ Saved: {output_path}")
        else:
            print("   ❌ Failed to compute fee-to-subsidy ratio")
            return False
        
        # Estimate fee rate metrics from aggregates
        if fees_csv.exists() and blocks_csv.exists():
            print("\n📈 Estimating fee rate metrics...")
            from src.metrics.fee_rate_urgency import estimate_fee_rates_from_aggregates
            from src.metrics.fees_and_fee_to_subsidy import compute_fees_per_block
            
            # First compute fees per block if not already done
            if not fees_per_block_csv.exists():
                fees_per_block_path = compute_fees_per_block(fees_csv, blocks_csv, raw_dir)
            else:
                fees_per_block_path = fees_per_block_csv
            
            # Estimate fee rates
            fee_rate_path = estimate_fee_rates_from_aggregates(
                fees_per_block_path,
                raw_dir / "blockchain_com_tx_per_day.csv",
                processed_dir
            )
            
            if fee_rate_path:
                print(f"   ✓ Saved: {fee_rate_path}")
            else:
                print("   ❌ Failed to estimate fee rates")
                return False
        
        return True
    
    except Exception as e:
        print(f"❌ Error computing fee metrics: {e}")
        return False


def compute_dormancy_metrics(raw_dir: Path, processed_dir: Path) -> bool:
    """
    Compute dormancy (BDD) metrics.
    
    Args:
        raw_dir: Path to raw data
        processed_dir: Path to save processed metrics
    
    Returns:
        True if successful, False otherwise
    """
    print("\n" + "=" * 70)
    print("📊 COMPUTING DORMANCY (BDD) METRICS")
    print("=" * 70)
    
    try:
        bdd_csv = raw_dir / "blockchain_com_bdd.csv"
        
        if not bdd_csv.exists():
            print(f"❌ Required file not found: {bdd_csv}")
            return False
        
        output_path = dormancy_cdd.compute_cdd_from_blockchain_com(
            bdd_csv,
            processed_dir
        )
        
        if output_path:
            print(f"   ✓ Saved: {output_path}")
            return True
        else:
            return False
    
    except Exception as e:
        print(f"❌ Error computing dormancy metrics: {e}")
        return False


def compute_activity_metrics(raw_dir: Path, processed_dir: Path) -> bool:
    """
    Compute transaction activity metrics.
    
    Args:
        raw_dir: Path to raw data
        processed_dir: Path to save processed metrics
    
    Returns:
        True if successful, False otherwise
    """
    print("\n" + "=" * 70)
    print("📊 COMPUTING ACTIVITY METRICS")
    print("=" * 70)
    
    try:
        tx_per_day_csv = raw_dir / "blockchain_com_tx_per_day.csv"
        
        if not tx_per_day_csv.exists():
            print(f"❌ Required file not found: {tx_per_day_csv}")
            return False
        
        output_path = mempool_and_tx_activity.process_transactions_per_day(
            tx_per_day_csv,
            processed_dir
        )
        
        if output_path:
            print(f"   ✓ Saved: {output_path}")
            return True
        else:
            return False
    
    except Exception as e:
        print(f"❌ Error computing activity metrics: {e}")
        return False


def main():
    """Main entry point for metrics computation script."""
    
    parser = argparse.ArgumentParser(
        description="Compute BTC-native metrics for Bitcoin liquidity crisis research"
    )
    
    parser.add_argument(
        '--metrics',
        nargs='+',
        choices=['fees', 'dormancy', 'activity', 'all'],
        default=['all'],
        help='Which metrics to compute (default: all)'
    )
    
    parser.add_argument(
        '--skip-missing',
        action='store_true',
        help='Skip metrics with missing input files instead of failing'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = load_config()
        paths = get_data_paths(config)
        raw_dir = paths['raw']
        processed_dir = paths['processed']
    except FileNotFoundError:
        print("❌ Configuration file not found!")
        sys.exit(1)
    
    # Determine which metrics to compute
    if 'all' in args.metrics:
        metrics_to_compute = ['fees', 'dormancy', 'activity']
    else:
        metrics_to_compute = args.metrics
    
    print("\n" + "=" * 70)
    print("🚀 BITCOIN LIQUIDITY CRISIS METRICS COMPUTER")
    print("=" * 70)
    print(f"Metrics: {', '.join(metrics_to_compute)}")
    print(f"Raw data: {raw_dir}")
    print(f"Output: {processed_dir}")
    print("=" * 70)
    
    results = {}
    
    # Compute each metric
    if 'fees' in metrics_to_compute:
        results['fees'] = compute_fee_metrics(raw_dir, processed_dir)
    
    if 'dormancy' in metrics_to_compute:
        results['dormancy'] = compute_dormancy_metrics(raw_dir, processed_dir)
    
    if 'activity' in metrics_to_compute:
        results['activity'] = compute_activity_metrics(raw_dir, processed_dir)
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ METRICS COMPUTATION COMPLETE")
    print("=" * 70)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    print(f"Successfully computed: {success_count}/{total_count} metric groups")
    
    for metric, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {metric}")
    
    if success_count > 0:
        print("\nNext steps:")
        print("1. Review processed metrics in data/processed/")
        print("2. Run: python scripts/03_make_figures.py")
    else:
        print("\n⚠️  No metrics computed successfully")
        print("   Check that raw data exists in data/raw/")
        print("   Run: python scripts/01_fetch_data.py")
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

