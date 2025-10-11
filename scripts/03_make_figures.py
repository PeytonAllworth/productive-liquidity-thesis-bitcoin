#!/usr/bin/env python3
"""
Script 03: Make Figures

This script generates publication-quality figures for your paper:
- Event window plots with pre/crisis shading
- Multi-panel metric comparisons
- Summary bar charts
- Cross-event overlays

Figures are saved to data/figures/ as PNG (300 DPI).

Usage:
    python scripts/03_make_figures.py --event cyprus_2013
    python scripts/03_make_figures.py --event all
    python scripts/03_make_figures.py --event cyprus_2013 --days-before 60 --days-after 120
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.config import load_config, get_data_paths, get_event_date
from src.utils.date_windows import build_event_window
from src.plotting.plot_event_windows import (
    plot_single_metric,
    plot_multi_panel_event,
    plot_pre_vs_crisis_comparison
)
from src.pipelines.build_event_dataset import build_event_dataset, load_all_metrics, merge_metrics_on_date


def generate_event_figures(
    event_name: str,
    anchor_date: str,
    days_before: int,
    days_after: int,
    processed_dir: Path,
    figures_dir: Path
) -> list:
    """
    Generate all figures for a single event.
    
    Args:
        event_name: Event identifier
        anchor_date: Crisis anchor date
        days_before: Pre-crisis window size
        days_after: Crisis window size
        processed_dir: Path to processed metrics
        figures_dir: Path to save figures
    
    Returns:
        List of generated figure paths
    """
    print("\n" + "=" * 70)
    print(f"📊 GENERATING FIGURES FOR {event_name.upper()}")
    print("=" * 70)
    print(f"Anchor: {anchor_date}")
    print(f"Window: -{days_before} to +{days_after} days")
    
    # Build event window
    window = build_event_window(anchor_date, days_before, days_after)
    
    # Load metrics
    print("\n📂 Loading metrics...")
    metrics = load_all_metrics(processed_dir)
    
    if not metrics:
        print("❌ No metrics found - run 02_compute_metrics.py first!")
        return []
    
    # Merge metrics
    print("🔗 Merging metrics on date...")
    merged = merge_metrics_on_date(metrics)
    
    if merged.empty:
        print("❌ Failed to merge metrics")
        return []
    
    figure_paths = []
    
    # TODO: Generate actual plots once metrics are implemented
    # 
    # # Plot each metric individually
    # metric_columns = [col for col in merged.columns if col != 'date']
    # 
    # for metric_col in metric_columns:
    #     try:
    #         fig_path = plot_single_metric(
    #             merged,
    #             metric_col,
    #             event_name,
    #             anchor_date,
    #             window,
    #             figures_dir
    #         )
    #         figure_paths.append(fig_path)
    #     except Exception as e:
    #         print(f"   ⚠️  Failed to plot {metric_col}: {e}")
    # 
    # # Create multi-panel figure
    # try:
    #     metrics_dict = {
    #         'Fee Rate': (merged[['date', 'median_sat_vb']], 'sat/vB'),
    #         'Fees per Block': (merged[['date', 'fees_per_block_btc']], 'BTC'),
    #         'BDD': (merged[['date', 'bdd']], 'Bitcoin-Days'),
    #         'Transactions': (merged[['date', 'tx_per_day']], 'Tx/Day')
    #     }
    #     
    #     fig_path = plot_multi_panel_event(
    #         metrics_dict,
    #         event_name,
    #         anchor_date,
    #         window,
    #         figures_dir
    #     )
    #     figure_paths.append(fig_path)
    # except Exception as e:
    #     print(f"   ⚠️  Failed to create multi-panel: {e}")
    
    print("\n⚠️  Figure generation not fully implemented yet")
    print("   Complete metric computation first, then implement plotting")
    
    return figure_paths


def main():
    """Main entry point for figure generation script."""
    
    parser = argparse.ArgumentParser(
        description="Generate publication-quality figures for Bitcoin liquidity crisis research"
    )
    
    parser.add_argument(
        '--event',
        type=str,
        default='all',
        help='Event to plot (cyprus_2013, venezuela_2017, covid_cpi_peak_2022, or all)'
    )
    
    parser.add_argument(
        '--days-before',
        type=int,
        default=None,
        help='Pre-crisis window size (overrides config)'
    )
    
    parser.add_argument(
        '--days-after',
        type=int,
        default=None,
        help='Crisis window size (overrides config)'
    )
    
    parser.add_argument(
        '--output-format',
        type=str,
        default='png',
        choices=['png', 'svg', 'pdf'],
        help='Output format for figures'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = load_config()
        paths = get_data_paths(config)
        processed_dir = paths['processed']
        figures_dir = paths['figures']
    except FileNotFoundError:
        print("❌ Configuration file not found!")
        sys.exit(1)
    
    # Get window sizes
    days_before = args.days_before or config['windows']['days_before']
    days_after = args.days_after or config['windows']['days_after']
    
    # Determine which events to plot
    if args.event == 'all':
        events_to_plot = config['events'].items()
    else:
        if args.event not in config['events']:
            print(f"❌ Unknown event: {args.event}")
            print(f"   Available: {', '.join(config['events'].keys())}")
            sys.exit(1)
        events_to_plot = [(args.event, config['events'][args.event])]
    
    print("\n" + "=" * 70)
    print("🚀 BITCOIN LIQUIDITY CRISIS FIGURE GENERATOR")
    print("=" * 70)
    print(f"Events: {len(events_to_plot)}")
    print(f"Window: ±{days_before}/{days_after} days")
    print(f"Output: {figures_dir}")
    print(f"Format: {args.output_format}")
    print("=" * 70)
    
    all_figure_paths = []
    
    # Generate figures for each event
    for event_name, anchor_date in events_to_plot:
        try:
            fig_paths = generate_event_figures(
                event_name,
                anchor_date,
                days_before,
                days_after,
                processed_dir,
                figures_dir
            )
            all_figure_paths.extend(fig_paths)
        except Exception as e:
            print(f"\n❌ Error generating figures for {event_name}: {e}")
            continue
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ FIGURE GENERATION COMPLETE")
    print("=" * 70)
    print(f"Generated {len(all_figure_paths)} figures in {figures_dir}")
    
    if all_figure_paths:
        print("\nSample figures:")
        for path in all_figure_paths[:5]:
            print(f"  📊 {path}")
        if len(all_figure_paths) > 5:
            print(f"  ... and {len(all_figure_paths) - 5} more")
        
        print("\n💡 Ready to include in your paper!")
    else:
        print("\n⚠️  No figures generated")
        print("   Make sure metrics are computed: python scripts/02_compute_metrics.py")
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

