#!/usr/bin/env python3
"""
Generate individual crisis figures with all data points clearly visible.

This script creates individual figures for each crisis showing:
- All data points with markers for visibility
- Clear pre-crisis vs crisis period shading
- Data point counts for transparency
- 2x2 subplot layout for all 4 metrics
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import load_config
from src.pipelines.build_event_dataset import load_all_metrics, merge_metrics_on_date
from src.plotting.plot_event_windows import plot_individual_crisis


def generate_individual_crisis_figures(
    processed_dir: Path,
    figures_dir: Path,
    event_name: str = None
) -> list:
    """
    Generate individual crisis figures with all data points visible.
    
    Args:
        processed_dir: Path to processed data directory
        figures_dir: Path to figures output directory
        event_name: Specific event to generate (if None, generates all)
    
    Returns:
        List of generated figure paths
    """
    # Load configuration
    config = load_config()
    events = config['events']
    windows = config['windows']
    
    # Load all metrics
    print("📊 Loading all processed metrics...")
    metrics = load_all_metrics(processed_dir)
    merged_df = merge_metrics_on_date(metrics)
    
    print(f"   ✓ Loaded {len(merged_df)} data points")
    print(f"   ✓ Date range: {merged_df['date'].min()} to {merged_df['date'].max()}")
    
    figure_paths = []
    
    # Generate figures for each event
    for event_key, anchor_date in events.items():
        if event_name and event_key != event_name:
            continue
            
        print(f"\n📈 Generating individual figure for {event_key}...")
        print(f"   Anchor date: {anchor_date}")
        
        # Generate for both window configurations
        window_configs = [
            (windows['standard']['days_before'], windows['standard']['days_after'], "90/90"),
            (windows['extended']['days_before'], windows['extended']['days_after'], "180/45")
        ]
        
        for days_before, days_after, window_name in window_configs:
            print(f"   Creating {window_name} day window figure...")
            
            # Create individual crisis figure
            fig_path = plot_individual_crisis(
                df=merged_df,
                event_name=f"{event_key}_{window_name.replace('/', '_')}",
                anchor_date=anchor_date,
                days_before=days_before,
                days_after=days_after,
                output_dir=figures_dir,
                title=f"{event_key.replace('_', ' ').title()} Crisis Analysis ({window_name} window)"
            )
            
            if fig_path:
                figure_paths.append(fig_path)
                print(f"   ✓ Saved: {fig_path.name}")
            else:
                print(f"   ❌ Failed to create figure for {event_key} {window_name}")
    
    return figure_paths


def main():
    """Main function to generate individual crisis figures."""
    parser = argparse.ArgumentParser(description="Generate individual crisis figures")
    parser.add_argument(
        "--event", 
        choices=["cyprus_2013", "venezuela_2016", "covid_cpi_peak_2022", "all"],
        default="all",
        help="Which event to generate figures for"
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("data/processed"),
        help="Path to processed data directory"
    )
    parser.add_argument(
        "--figures-dir", 
        type=Path,
        default=Path("data/figures"),
        help="Path to figures output directory"
    )
    
    args = parser.parse_args()
    
    # Ensure directories exist
    args.processed_dir.mkdir(parents=True, exist_ok=True)
    args.figures_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("🎯 INDIVIDUAL CRISIS FIGURE GENERATION")
    print("=" * 80)
    print(f"Event: {args.event}")
    print(f"Processed data: {args.processed_dir}")
    print(f"Output: {args.figures_dir}")
    print()
    
    # Generate figures
    try:
        figure_paths = generate_individual_crisis_figures(
            processed_dir=args.processed_dir,
            figures_dir=args.figures_dir,
            event_name=args.event if args.event != "all" else None
        )
        
        print("\n" + "=" * 80)
        print("✅ INDIVIDUAL FIGURE GENERATION COMPLETE")
        print("=" * 80)
        print(f"Generated {len(figure_paths)} individual figures in {args.figures_dir}")
        print()
        
        if figure_paths:
            print("Sample figures:")
            for fig_path in figure_paths[:6]:  # Show first 6
                print(f"  📊 {fig_path}")
            if len(figure_paths) > 6:
                print(f"  ... and {len(figure_paths) - 6} more")
        
        print("\n💡 These figures show all data points clearly visible!")
        print("   Each crisis has both 90/90 and 180/45 day window versions")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error generating individual figures: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
