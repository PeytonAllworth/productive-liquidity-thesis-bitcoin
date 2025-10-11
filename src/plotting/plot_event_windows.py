"""
Event window plotting functions.

This module creates visualizations for crisis event analysis:
- Time series with shaded event windows
- Multi-panel comparisons
- Pre vs. crisis comparison charts
- Export to PNG/SVG for paper

All plots use consistent styling from styles.py.
"""

from pathlib import Path
from typing import Optional, Tuple, List
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.plotting.styles import (
    apply_plot_style, format_date_axis, add_event_window_shading,
    add_halving_markers, save_figure, PRE_COLOR, CRISIS_COLOR
)
from src.utils.date_windows import build_event_window


def plot_single_metric(
    df: pd.DataFrame,
    metric_column: str,
    event_name: str,
    anchor_date: str,
    window_dict: dict,
    output_dir: Path,
    title: str = None,
    ylabel: str = None,
    include_halvings: bool = True
) -> Path:
    """
    Plot a single metric with event window shading.
    
    Args:
        df: DataFrame with columns [date, <metric_column>]
        metric_column: Name of metric to plot
        event_name: Event identifier (e.g., 'cyprus_2013')
        anchor_date: Crisis anchor date (YYYY-MM-DD)
        window_dict: Dict from build_event_window() with 'pre' and 'crisis' keys
        output_dir: Where to save figure
        title: Chart title (if None, auto-generates)
        ylabel: Y-axis label (if None, uses metric_column)
        include_halvings: Whether to show halving markers
    
    Returns:
        Path to saved figure
    
    Example:
        >>> from src.utils.date_windows import build_event_window
        >>> window = build_event_window('2013-03-16', 90, 90)
        >>> plot_single_metric(df, 'median_sat_vb', 'cyprus_2013', 
        ...                    '2013-03-16', window, Path('data/figures'))
    """
    apply_plot_style()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Plot metric
    ax.plot(df['date'], df[metric_column], 
            color=CRISIS_COLOR, linewidth=2, label=metric_column)
    
    # Add event window shading
    add_event_window_shading(
        ax,
        anchor_date,
        window_dict['pre'][0],
        window_dict['crisis'][1],
        label=event_name.replace('_', ' ').title()
    )
    
    # Add halving markers (if applicable)
    if include_halvings:
        date_range = (df['date'].min(), df['date'].max())
        add_halving_markers(ax, date_range)
    
    # Labels and title
    if title is None:
        title = f"{metric_column.replace('_', ' ').title()} - {event_name.replace('_', ' ').title()}"
    ax.set_title(title, fontsize=16, fontweight='bold')
    
    if ylabel is None:
        ylabel = metric_column.replace('_', ' ').title()
    ax.set_ylabel(ylabel, fontsize=13)
    
    ax.set_xlabel('Date', fontsize=13)
    
    # Format x-axis
    format_date_axis(ax, date_format='%Y-%m', major_locator_months=3)
    
    # Legend
    ax.legend(loc='best', framealpha=0.9)
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Save
    filename = f"fig_{event_name}_{metric_column}.png"
    save_path = save_figure(fig, filename, output_dir)
    
    plt.close(fig)
    
    return Path(save_path)


def plot_multi_panel_event(
    metrics_dict: dict,
    event_name: str,
    anchor_date: str,
    window_dict: dict,
    output_dir: Path,
    include_halvings: bool = False
) -> Path:
    """
    Create multi-panel figure showing multiple metrics for one event.
    
    Args:
        metrics_dict: {metric_name: (df, ylabel)} where df has [date, value] columns
        event_name: Event identifier
        anchor_date: Crisis anchor date
        window_dict: Event window from build_event_window()
        output_dir: Where to save
        include_halvings: Show halving markers
    
    Returns:
        Path to saved figure
    
    Example:
        >>> metrics = {
        ...     'Median Fee Rate': (fee_df[['date', 'median_sat_vb']], 'sat/vB'),
        ...     'Fees per Block': (fees_df[['date', 'fees_per_block_btc']], 'BTC'),
        ...     'BDD': (bdd_df[['date', 'bdd']], 'Bitcoin-Days'),
        ...     'Tx per Day': (tx_df[['date', 'tx_per_day']], 'Transactions')
        ... }
        >>> plot_multi_panel_event(metrics, 'cyprus_2013', '2013-03-16', window, Path('data/figures'))
    
    TODO: Implement after collecting all metrics
    """
    apply_plot_style()
    
    n_metrics = len(metrics_dict)
    fig, axes = plt.subplots(n_metrics, 1, figsize=(14, 4 * n_metrics), sharex=True)
    
    # Ensure axes is iterable
    if n_metrics == 1:
        axes = [axes]
    
    # Plot each metric in its own panel
    for ax, (metric_name, (df, ylabel)) in zip(axes, metrics_dict.items()):
        # Plot data
        value_col = df.columns[1]  # Second column (first is 'date')
        ax.plot(df['date'], df[value_col], color=CRISIS_COLOR, linewidth=2)
        
        # Add shading
        add_event_window_shading(
            ax,
            anchor_date,
            window_dict['pre'][0],
            window_dict['crisis'][1]
        )
        
        # Labels
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(metric_name, fontsize=13, fontweight='bold', loc='left')
        ax.grid(True, alpha=0.3)
        
        # Halvings (only on first panel to avoid clutter)
        if include_halvings and ax == axes[0]:
            date_range = (df['date'].min(), df['date'].max())
            add_halving_markers(ax, date_range)
    
    # Common x-axis label
    axes[-1].set_xlabel('Date', fontsize=13)
    format_date_axis(axes[-1], date_format='%Y-%m', major_locator_months=3)
    
    # Overall title
    fig.suptitle(f"{event_name.replace('_', ' ').title()} - Multi-Metric Analysis",
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    
    # Save
    filename = f"fig_{event_name}_multi_panel.png"
    save_path = save_figure(fig, filename, output_dir)
    
    plt.close(fig)
    
    return Path(save_path)


def plot_pre_vs_crisis_comparison(
    df: pd.DataFrame,
    metric_column: str,
    event_name: str,
    anchor_date: str,
    output_dir: Path,
    ylabel: str = None
) -> Path:
    """
    Create bar chart comparing pre-crisis vs. crisis mean values.
    
    Args:
        df: DataFrame with [date, period, <metric_column>]
                where period is 'pre' or 'crisis'
        metric_column: Metric to compare
        event_name: Event identifier
        output_dir: Where to save
        ylabel: Y-axis label
    
    Returns:
        Path to saved figure
    
    Example:
        >>> # Assume df has 'period' column labeled pre/crisis
        >>> plot_pre_vs_crisis_comparison(df, 'median_sat_vb', 'cyprus_2013',
        ...                               '2013-03-16', Path('data/figures'))
    
    TODO: Implement for summary statistics visualization
    """
    apply_plot_style()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Compute means
    pre_mean = df[df['period'] == 'pre'][metric_column].mean()
    crisis_mean = df[df['period'] == 'crisis'][metric_column].mean()
    
    # Create bar chart
    periods = ['Pre-crisis', 'Crisis']
    means = [pre_mean, crisis_mean]
    colors = [PRE_COLOR, CRISIS_COLOR]
    
    bars = ax.bar(periods, means, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar, value in zip(bars, means):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height,
                f'{value:.2f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Calculate percent change
    pct_change = ((crisis_mean - pre_mean) / pre_mean) * 100
    
    # Add percent change annotation
    ax.text(0.5, max(means) * 0.9, 
            f'Change: {pct_change:+.1f}%',
            transform=ax.transData,
            ha='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # Labels
    title = f"{metric_column.replace('_', ' ').title()} - {event_name.replace('_', ' ').title()}"
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    else:
        ax.set_ylabel(metric_column.replace('_', ' ').title(), fontsize=12)
    
    ax.grid(True, axis='y', alpha=0.3)
    
    # Save
    filename = f"fig_{event_name}_{metric_column}_comparison.png"
    save_path = save_figure(fig, filename, output_dir)
    
    plt.close(fig)
    
    return Path(save_path)


def plot_all_events_overlay(
    dfs_dict: dict,
    metric_column: str,
    output_dir: Path,
    normalize: bool = False,
    title: str = None,
    ylabel: str = None
) -> Path:
    """
    Overlay multiple crisis events on one chart for comparison.
    
    Args:
        dfs_dict: {event_name: df} where each df has [days_from_anchor, metric]
        metric_column: Metric to plot
        output_dir: Where to save
        normalize: If True, normalize each series to anchor date = 100
        title: Chart title
        ylabel: Y-axis label
    
    Returns:
        Path to saved figure
    
    Use Case:
        Compare how quickly different crises affected metrics.
        E.g., Cyprus vs. Venezuela vs. COVID fee rate response.
    
    TODO: Implement for cross-event analysis
    """
    apply_plot_style()
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot each event
    for event_name, df in dfs_dict.items():
        if normalize:
            # Normalize to anchor date (day 0) = 100
            anchor_value = df[df['days_from_anchor'] == 0][metric_column].iloc[0]
            df['normalized'] = (df[metric_column] / anchor_value) * 100
            plot_col = 'normalized'
        else:
            plot_col = metric_column
        
        ax.plot(df['days_from_anchor'], df[plot_col], 
                linewidth=2, label=event_name.replace('_', ' ').title())
    
    # Add vertical line at anchor (day 0)
    ax.axvline(0, color='black', linestyle='--', linewidth=1.5, label='Crisis Anchor')
    
    # Labels
    if title is None:
        title = f"{metric_column.replace('_', ' ').title()} - All Events Comparison"
    ax.set_title(title, fontsize=16, fontweight='bold')
    
    ax.set_xlabel('Days from Crisis Anchor', fontsize=13)
    
    if ylabel is None:
        ylabel = 'Normalized (Anchor = 100)' if normalize else metric_column.replace('_', ' ').title()
    ax.set_ylabel(ylabel, fontsize=13)
    
    # Legend
    ax.legend(loc='best', framealpha=0.9)
    
    ax.grid(True, alpha=0.3)
    
    # Save
    filename = f"fig_all_events_{metric_column}.png"
    save_path = save_figure(fig, filename, output_dir)
    
    plt.close(fig)
    
    return Path(save_path)


# Example/test
if __name__ == "__main__":
    print("Event Window Plotting Module")
    print("\n📊 Available plot functions:")
    print("1. plot_single_metric() - Single metric with event shading")
    print("2. plot_multi_panel_event() - 4-panel view of all metrics")
    print("3. plot_pre_vs_crisis_comparison() - Bar chart comparison")
    print("4. plot_all_events_overlay() - Compare multiple crises")
    print("\n💡 All plots use consistent styling from styles.py")
    print("   Call apply_plot_style() at the start of scripts")

