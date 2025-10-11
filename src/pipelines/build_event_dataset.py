"""
Build Event Dataset Pipeline

This module creates event-specific datasets by:
1. Loading all computed metrics from data/processed/
2. Merging on date
3. Slicing to event windows (±90 days by default)
4. Adding period labels ('pre' vs 'crisis')
5. Saving event-specific CSVs for analysis

Output:
    data/processed/event_cyprus_2013.csv
    data/processed/event_venezuela_2017.csv
    data/processed/event_covid_cpi_peak_2022.csv

These CSVs contain all metrics aligned for statistical analysis.
"""

from pathlib import Path
from typing import Dict, List
import pandas as pd

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.config import load_config, get_data_paths
from src.utils.date_windows import build_event_window, slice_dataframe_by_window, add_period_labels
from src.utils.io import save_csv, load_csv


def load_all_metrics(processed_dir: Path) -> Dict[str, pd.DataFrame]:
    """
    Load all computed metric CSVs from processed/ directory.
    
    Args:
        processed_dir: Path to data/processed/
    
    Returns:
        Dictionary {metric_name: dataframe}
    
    Expected CSVs:
        - fee_rate_urgency_daily.csv
        - fees_per_block_btc.csv
        - fee_to_subsidy_daily.csv
        - dormancy_bdd_daily.csv
        - tx_activity_daily.csv
        - mempool_backlog_daily.csv (optional)
    
    Example:
        >>> metrics = load_all_metrics(Path('data/processed'))
        >>> print(metrics.keys())
        dict_keys(['fee_rate_urgency', 'fees_per_block', ...])
    
    TODO: Implement after metric computation is complete
    """
    print("\n📂 Loading all computed metrics...")
    
    metrics = {}
    
    # TODO: Add file loading logic
    # 
    # # Fee rate & urgency
    # csv_path = processed_dir / "fee_rate_urgency_daily.csv"
    # if csv_path.exists():
    #     metrics['fee_rate_urgency'] = load_csv(csv_path)
    # 
    # # Fees per block
    # csv_path = processed_dir / "fees_per_block_btc.csv"
    # if csv_path.exists():
    #     metrics['fees_per_block'] = load_csv(csv_path)
    # 
    # # Fee-to-subsidy
    # csv_path = processed_dir / "fee_to_subsidy_daily.csv"
    # if csv_path.exists():
    #     metrics['fee_to_subsidy'] = load_csv(csv_path)
    # 
    # # Dormancy (BDD)
    # csv_path = processed_dir / "dormancy_bdd_daily.csv"
    # if csv_path.exists():
    #     metrics['dormancy'] = load_csv(csv_path)
    # 
    # # Transaction activity
    # csv_path = processed_dir / "tx_activity_daily.csv"
    # if csv_path.exists():
    #     metrics['tx_activity'] = load_csv(csv_path)
    # 
    # # Mempool (optional)
    # csv_path = processed_dir / "mempool_backlog_daily.csv"
    # if csv_path.exists():
    #     metrics['mempool'] = load_csv(csv_path)
    # 
    # print(f"   ✓ Loaded {len(metrics)} metric datasets")
    
    print("   ⚠️  Not implemented yet - waiting for metric computation\n")
    
    return metrics


def merge_metrics_on_date(metrics_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merge all metric DataFrames on 'date' column.
    
    Args:
        metrics_dict: Dictionary of {name: dataframe}
    
    Returns:
        Single merged DataFrame with all metrics
    
    Merge Strategy:
        - Inner join (only keep dates present in all datasets)
        - OR: Outer join with forward fill (for missing dates)
    
    Example:
        >>> merged = merge_metrics_on_date(metrics)
        >>> print(merged.columns)
        Index(['date', 'median_sat_vb', 'fees_per_block_btc', 'bdd', ...])
    
    TODO: Implement
    """
    if not metrics_dict:
        print("   ❌ No metrics to merge")
        return pd.DataFrame()
    
    # TODO: Implement merging logic
    # 
    # # Start with first dataframe
    # merged = list(metrics_dict.values())[0].copy()
    # 
    # # Merge remaining dataframes
    # for name, df in list(metrics_dict.items())[1:]:
    #     merged = merged.merge(df, on='date', how='inner', suffixes=('', f'_{name}'))
    # 
    # # Sort by date
    # merged = merged.sort_values('date').reset_index(drop=True)
    # 
    # print(f"   ✓ Merged metrics: {len(merged)} days, {len(merged.columns)} columns")
    # 
    # return merged
    
    print("   ⚠️  Merge not implemented yet\n")
    return pd.DataFrame()


def build_event_dataset(
    event_name: str,
    anchor_date: str,
    days_before: int,
    days_after: int,
    merged_metrics: pd.DataFrame,
    output_dir: Path
) -> Path:
    """
    Build event-specific dataset with window slicing and period labels.
    
    Args:
        event_name: Event identifier (e.g., 'cyprus_2013')
        anchor_date: Crisis anchor date (YYYY-MM-DD)
        days_before: Pre-crisis window size
        days_after: Crisis window size
        merged_metrics: DataFrame with all metrics
        output_dir: Where to save event CSV
    
    Returns:
        Path to saved event CSV
    
    Output CSV structure:
        - date
        - period ('pre' or 'crisis')
        - days_from_anchor (negative for pre, 0=anchor, positive for crisis)
        - [all metric columns]
    
    Example:
        >>> path = build_event_dataset('cyprus_2013', '2013-03-16', 90, 90, 
        ...                            merged_df, Path('data/processed'))
    
    TODO: Implement
    """
    print(f"\n📊 Building event dataset: {event_name}")
    print(f"   Anchor: {anchor_date}")
    print(f"   Window: {days_before} days before, {days_after} days after")
    
    # TODO: Implement
    # 
    # # Build event window
    # window = build_event_window(anchor_date, days_before, days_after)
    # 
    # # Slice to window
    # pre_start, pre_end = window['pre']
    # crisis_start, crisis_end = window['crisis']
    # 
    # # Get pre-crisis data
    # pre_df = slice_dataframe_by_window(merged_metrics, pre_start, pre_end)
    # pre_df['period'] = 'pre'
    # 
    # # Get crisis data
    # crisis_df = slice_dataframe_by_window(merged_metrics, crisis_start, crisis_end)
    # crisis_df['period'] = 'crisis'
    # 
    # # Combine
    # event_df = pd.concat([pre_df, crisis_df], ignore_index=True)
    # 
    # # Add days_from_anchor column
    # anchor = pd.Timestamp(anchor_date)
    # event_df['days_from_anchor'] = (event_df['date'] - anchor).dt.days
    # 
    # # Save
    # output_path = output_dir / f"event_{event_name}.csv"
    # save_csv(event_df, output_path)
    # 
    # print(f"   ✓ Saved event dataset: {len(event_df)} days")
    # return output_path
    
    print("   ⚠️  Not implemented yet\n")
    return None


def build_all_event_datasets(
    config: dict = None,
    processed_dir: Path = None,
    output_dir: Path = None
) -> Dict[str, Path]:
    """
    Build event datasets for all configured crises.
    
    Args:
        config: Configuration dictionary (if None, loads from settings.yaml)
        processed_dir: Path to processed metrics (if None, uses config)
        output_dir: Path to save events (if None, uses processed_dir)
    
    Returns:
        Dictionary {event_name: csv_path}
    
    Workflow:
        1. Load config
        2. Load all metrics from processed/
        3. Merge metrics on date
        4. For each event in config:
           a. Build event window
           b. Slice and label data
           c. Save event CSV
    
    Example:
        >>> from src.config import load_config
        >>> cfg = load_config()
        >>> paths = build_all_event_datasets(cfg)
        >>> print(paths.keys())
        dict_keys(['cyprus_2013', 'venezuela_2017', 'covid_cpi_peak_2022'])
    
    TODO: Implement as main pipeline entry point
    """
    # Load config if not provided
    if config is None:
        config = load_config()
    
    # Get paths
    if processed_dir is None:
        paths = get_data_paths(config)
        processed_dir = paths['processed']
    
    if output_dir is None:
        output_dir = processed_dir
    
    print("\n" + "=" * 70)
    print("🏗️  BUILDING EVENT DATASETS")
    print("=" * 70)
    
    # Load all metrics
    metrics = load_all_metrics(processed_dir)
    
    if not metrics:
        print("\n❌ No metrics found - run compute_metrics.py first!")
        return {}
    
    # Merge metrics
    merged = merge_metrics_on_date(metrics)
    
    if merged.empty:
        print("\n❌ Failed to merge metrics")
        return {}
    
    # Build event datasets
    event_paths = {}
    
    events = config['events']
    days_before = config['windows']['days_before']
    days_after = config['windows']['days_after']
    
    for event_name, anchor_date in events.items():
        try:
            path = build_event_dataset(
                event_name,
                anchor_date,
                days_before,
                days_after,
                merged,
                output_dir
            )
            
            if path:
                event_paths[event_name] = path
        
        except Exception as e:
            print(f"   ❌ Failed to build {event_name}: {e}")
    
    print("\n" + "=" * 70)
    print(f"✅ Built {len(event_paths)} event datasets")
    print("=" * 70 + "\n")
    
    return event_paths


# CLI interface
if __name__ == "__main__":
    print("Event Dataset Builder Pipeline")
    print("\n📝 This pipeline:")
    print("1. Loads all computed metrics from data/processed/")
    print("2. Merges them on date")
    print("3. Slices to event windows")
    print("4. Saves event-specific CSVs")
    print("\n🚀 Run this after computing all metrics (02_compute_metrics.py)")
    print("\n" + "=" * 70)
    
    # Run pipeline
    try:
        event_paths = build_all_event_datasets()
        
        if event_paths:
            print("\n✅ Event datasets ready for analysis!")
            for event, path in event_paths.items():
                print(f"   {event}: {path}")
        else:
            print("\n⚠️  No event datasets created - check metric files")
    
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        print("   Make sure config/settings.yaml exists and metrics are computed")

