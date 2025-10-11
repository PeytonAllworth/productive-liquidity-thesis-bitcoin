"""
Compute Summary Tables Pipeline

This module generates statistical summary tables comparing pre-crisis vs. crisis periods:
- Mean values for each metric
- Percent changes
- Percentage point changes (for ratios)
- Standard deviations
- Sample sizes

Output:
    data/processed/summary_table_all_events.csv
    data/processed/summary_table_cyprus_2013.csv
    data/processed/summary_table_venezuela_2017.csv
    ...

These tables are ready for inclusion in your paper!
"""

from pathlib import Path
from typing import Dict, List
import pandas as pd

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.config import load_config, get_data_paths
from src.utils.io import save_csv, load_csv
from src.utils.math_stats import percent_change, pp_change, compare_periods


def compute_event_summary_stats(
    event_csv: Path,
    event_name: str
) -> pd.DataFrame:
    """
    Compute summary statistics for a single event.
    
    Args:
        event_csv: Path to event CSV (from build_event_dataset.py)
        event_name: Event identifier
    
    Returns:
        DataFrame with summary statistics
    
    Output structure:
        Columns: metric, pre_mean, crisis_mean, pre_std, crisis_std, 
                 percent_change, sample_size_pre, sample_size_crisis
    
    Example:
        >>> summary = compute_event_summary_stats(
        ...     Path('data/processed/event_cyprus_2013.csv'),
        ...     'cyprus_2013'
        ... )
        >>> print(summary)
              metric  pre_mean  crisis_mean  percent_change
        0  median_sat_vb     45.2         68.7          +51.9
        1  fees_per_block    0.12         0.18          +50.0
        ...
    
    TODO: Implement
    """
    print(f"\n📊 Computing summary for {event_name}...")
    
    # TODO: Implement
    # 
    # # Load event data
    # df = load_csv(event_csv)
    # 
    # # Split by period
    # pre_df = df[df['period'] == 'pre']
    # crisis_df = df[df['period'] == 'crisis']
    # 
    # # Identify metric columns (exclude date, period, days_from_anchor)
    # exclude_cols = ['date', 'period', 'days_from_anchor']
    # metric_cols = [col for col in df.columns if col not in exclude_cols]
    # 
    # summary_rows = []
    # 
    # for metric in metric_cols:
    #     # Compute statistics
    #     pre_mean = pre_df[metric].mean()
    #     crisis_mean = crisis_df[metric].mean()
    #     pre_std = pre_df[metric].std()
    #     crisis_std = crisis_df[metric].std()
    #     
    #     # Percent change
    #     pct_chg = percent_change(crisis_mean, pre_mean)
    #     
    #     # Sample sizes
    #     n_pre = pre_df[metric].notna().sum()
    #     n_crisis = crisis_df[metric].notna().sum()
    #     
    #     summary_rows.append({
    #         'event': event_name,
    #         'metric': metric,
    #         'pre_mean': round(pre_mean, 4),
    #         'crisis_mean': round(crisis_mean, 4),
    #         'pre_std': round(pre_std, 4),
    #         'crisis_std': round(crisis_std, 4),
    #         'percent_change': pct_chg,
    #         'n_pre': n_pre,
    #         'n_crisis': n_crisis
    #     })
    # 
    # summary_df = pd.DataFrame(summary_rows)
    # 
    # print(f"   ✓ Computed statistics for {len(summary_rows)} metrics")
    # 
    # return summary_df
    
    print("   ⚠️  Not implemented yet\n")
    return pd.DataFrame()


def compute_all_event_summaries(
    config: dict = None,
    processed_dir: Path = None
) -> pd.DataFrame:
    """
    Compute summary statistics for all events and combine.
    
    Args:
        config: Configuration dictionary
        processed_dir: Path to processed data directory
    
    Returns:
        Combined DataFrame with all events
    
    Example:
        >>> all_summaries = compute_all_event_summaries()
        >>> print(all_summaries)
                  event         metric  pre_mean  crisis_mean  percent_change
        0  cyprus_2013  median_sat_vb      45.2         68.7           +51.9
        1  cyprus_2013  fees_per_block     0.12         0.18           +50.0
        2  venezuela_2017  median_sat_vb   120.5        195.3           +62.0
        ...
    
    TODO: Implement
    """
    # Load config if not provided
    if config is None:
        config = load_config()
    
    # Get paths
    if processed_dir is None:
        paths = get_data_paths(config)
        processed_dir = paths['processed']
    
    print("\n" + "=" * 70)
    print("📈 COMPUTING SUMMARY STATISTICS")
    print("=" * 70)
    
    all_summaries = []
    
    # Process each event
    for event_name in config['events'].keys():
        event_csv = processed_dir / f"event_{event_name}.csv"
        
        if not event_csv.exists():
            print(f"   ⚠️  Event CSV not found: {event_csv}")
            continue
        
        summary = compute_event_summary_stats(event_csv, event_name)
        
        if not summary.empty:
            all_summaries.append(summary)
    
    # Combine all events
    if all_summaries:
        combined = pd.concat(all_summaries, ignore_index=True)
        
        # Save
        output_path = processed_dir / "summary_table_all_events.csv"
        save_csv(combined, output_path)
        
        print("\n" + "=" * 70)
        print(f"✅ Summary table saved: {output_path}")
        print("=" * 70 + "\n")
        
        return combined
    else:
        print("\n❌ No event summaries computed")
        return pd.DataFrame()


def print_summary_table(summary_df: pd.DataFrame, event_filter: str = None) -> None:
    """
    Print formatted summary table to console.
    
    Args:
        summary_df: Summary DataFrame
        event_filter: Optional event name to filter
    
    Example:
        >>> print_summary_table(summary_df, 'cyprus_2013')
        
        ════════════════════════════════════════════════════
        Cyprus 2013 - Summary Statistics
        ════════════════════════════════════════════════════
        Metric              Pre-Mean  Crisis-Mean  Change
        ────────────────────────────────────────────────────
        median_sat_vb           45.2         68.7  +51.9%
        fees_per_block          0.12         0.18  +50.0%
        ...
    """
    if event_filter:
        df = summary_df[summary_df['event'] == event_filter]
        title = f"{event_filter.replace('_', ' ').title()} - Summary Statistics"
    else:
        df = summary_df
        title = "All Events - Summary Statistics"
    
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    
    # Format table
    print(f"{'Metric':<25} {'Pre-Mean':>12} {'Crisis-Mean':>12} {'Change':>10}")
    print("-" * 70)
    
    for _, row in df.iterrows():
        metric = row['metric'][:24]  # Truncate long names
        pre_mean = f"{row['pre_mean']:,.4f}"
        crisis_mean = f"{row['crisis_mean']:,.4f}"
        pct_chg = f"{row['percent_change']:+.1f}%" if pd.notna(row['percent_change']) else 'N/A'
        
        print(f"{metric:<25} {pre_mean:>12} {crisis_mean:>12} {pct_chg:>10}")
    
    print("=" * 70 + "\n")


def export_latex_table(summary_df: pd.DataFrame, output_path: Path) -> Path:
    """
    Export summary table to LaTeX format for paper.
    
    Args:
        summary_df: Summary DataFrame
        output_path: Where to save .tex file
    
    Returns:
        Path to saved LaTeX file
    
    Example:
        >>> export_latex_table(summary_df, Path('paper/tables/summary.tex'))
    
    TODO: Implement for paper preparation
    """
    print(f"\n📄 Exporting LaTeX table to {output_path}...")
    
    # TODO: Implement
    # 
    # # Convert DataFrame to LaTeX
    # latex_str = summary_df.to_latex(
    #     index=False,
    #     column_format='llrrrr',
    #     caption='Summary Statistics: Pre-Crisis vs. Crisis Periods',
    #     label='tab:summary_stats',
    #     escape=False
    # )
    # 
    # # Save
    # output_path.parent.mkdir(parents=True, exist_ok=True)
    # with open(output_path, 'w') as f:
    #     f.write(latex_str)
    # 
    # print(f"   ✓ LaTeX table saved")
    # return output_path
    
    print("   ⚠️  Not implemented yet\n")
    return None


# CLI interface
if __name__ == "__main__":
    print("Summary Statistics Pipeline")
    print("\n📝 This pipeline:")
    print("1. Loads event datasets from data/processed/")
    print("2. Computes pre vs. crisis statistics")
    print("3. Generates summary tables")
    print("4. Saves to CSV (and optionally LaTeX)")
    print("\n🚀 Run this after building event datasets")
    print("\n" + "=" * 70)
    
    # Run pipeline
    try:
        summary_df = compute_all_event_summaries()
        
        if not summary_df.empty:
            # Print all events
            print_summary_table(summary_df)
            
            # Print individual events
            config = load_config()
            for event_name in config['events'].keys():
                print_summary_table(summary_df, event_name)
            
            print("\n✅ Summary tables ready for your paper!")
            print("   Copy statistics from data/processed/summary_table_all_events.csv")
        else:
            print("\n⚠️  No summaries computed - check event datasets")
    
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")

