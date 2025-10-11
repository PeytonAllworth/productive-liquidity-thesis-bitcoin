"""
Plotting styles and configuration for consistent figures.

This module defines:
- Matplotlib style defaults
- Color schemes
- Figure dimensions
- Font sizes for publication quality

Usage:
    from src.plotting.styles import apply_plot_style, CRISIS_COLOR, PRE_COLOR
    
    apply_plot_style()
    plt.plot(..., color=CRISIS_COLOR)
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Tuple


# Color palette (professional, colorblind-friendly)
PRE_COLOR = '#2E86AB'        # Blue (calm, pre-crisis)
CRISIS_COLOR = '#A23B72'     # Purple-red (crisis period)
ACCENT_COLOR = '#F18F01'     # Orange (highlights, urgency)
GRAY = '#6C757D'             # Gray (neutral, reference lines)
DARK_GRAY = '#343A40'        # Dark gray (text, axes)

# Halving marker colors
HALVING_COLOR = '#FFC107'    # Amber (halving events)

# Default figure size (suitable for papers)
DEFAULT_FIGSIZE = (12, 6)    # Width x Height in inches

# DPI for saving (300 for publication quality)
DEFAULT_DPI = 300


def apply_plot_style() -> None:
    """
    Apply consistent matplotlib style settings.
    
    Call this at the start of any plotting script.
    
    Example:
        >>> from src.plotting.styles import apply_plot_style
        >>> apply_plot_style()
        >>> plt.plot([1, 2, 3], [1, 4, 9])
        >>> plt.show()
    """
    # Set style
    plt.style.use('default')  # Start with clean slate
    
    # Font sizes
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 11
    plt.rcParams['ytick.labelsize'] = 11
    plt.rcParams['legend.fontsize'] = 11
    
    # Font family (use system defaults, works everywhere)
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    
    # Figure settings
    plt.rcParams['figure.figsize'] = DEFAULT_FIGSIZE
    plt.rcParams['figure.dpi'] = 100  # Display DPI (save at higher DPI)
    plt.rcParams['figure.autolayout'] = True  # Tight layout by default
    
    # Axis settings
    plt.rcParams['axes.grid'] = True
    plt.rcParams['axes.axisbelow'] = True  # Grid behind data
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = '--'
    
    # Line widths
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['axes.linewidth'] = 1.2
    
    # Colors
    plt.rcParams['axes.prop_cycle'] = plt.cycler(
        color=[PRE_COLOR, CRISIS_COLOR, ACCENT_COLOR, GRAY]
    )


def format_date_axis(
    ax,
    date_format: str = '%Y-%m',
    major_locator_months: int = 3
) -> None:
    """
    Format x-axis for date plots.
    
    Args:
        ax: Matplotlib axis object
        date_format: strftime format string
        major_locator_months: Spacing for major ticks (in months)
    
    Example:
        >>> fig, ax = plt.subplots()
        >>> ax.plot(dates, values)
        >>> format_date_axis(ax, date_format='%Y-%m-%d')
    """
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=major_locator_months))
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def add_event_window_shading(
    ax,
    anchor_date: str,
    window_start: str,
    window_end: str,
    label: str = None
) -> None:
    """
    Add vertical shaded region for crisis window.
    
    Args:
        ax: Matplotlib axis
        anchor_date: Crisis anchor date (for vertical line)
        window_start: Start of crisis window
        window_end: End of crisis window
        label: Optional label for the shaded region
    
    Example:
        >>> fig, ax = plt.subplots()
        >>> add_event_window_shading(ax, '2013-03-16', '2012-12-16', '2013-06-14', 'Cyprus Crisis')
    """
    import pandas as pd
    
    # Convert to pandas Timestamp for plotting
    anchor = pd.Timestamp(anchor_date)
    start = pd.Timestamp(window_start)
    end = pd.Timestamp(window_end)
    
    # Shade pre-crisis period (lighter)
    ax.axvspan(start, anchor, alpha=0.15, color=PRE_COLOR, label='Pre-crisis')
    
    # Shade crisis period (slightly darker)
    ax.axvspan(anchor, end, alpha=0.25, color=CRISIS_COLOR, label='Crisis period')
    
    # Vertical line at anchor
    ax.axvline(anchor, color=DARK_GRAY, linestyle='--', linewidth=1.5, 
               label=f'Crisis anchor: {anchor_date}')
    
    if label:
        # Add text annotation
        ax.text(anchor, ax.get_ylim()[1] * 0.95, label,
                ha='center', va='top', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))


def add_halving_markers(
    ax,
    date_range: Tuple[str, str],
    halvings: dict = None
) -> None:
    """
    Add vertical lines for Bitcoin halving events.
    
    Args:
        ax: Matplotlib axis
        date_range: (start_date, end_date) to filter halvings
        halvings: Optional dict of {label: date}. If None, uses defaults.
    
    Default Halvings:
        - 2012-11-28: First halving (50 → 25 BTC)
        - 2016-07-09: Second halving (25 → 12.5 BTC)
        - 2020-05-11: Third halving (12.5 → 6.25 BTC)
        - 2024-04-20: Fourth halving (6.25 → 3.125 BTC)
    
    Example:
        >>> fig, ax = plt.subplots()
        >>> add_halving_markers(ax, ('2012-01-01', '2025-01-01'))
    """
    import pandas as pd
    
    # Default halving dates
    if halvings is None:
        halvings = {
            '1st Halving': '2012-11-28',
            '2nd Halving': '2016-07-09',
            '3rd Halving': '2020-05-11',
            '4th Halving': '2024-04-20'
        }
    
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])
    
    for label, date_str in halvings.items():
        date = pd.Timestamp(date_str)
        
        # Only plot if within date range
        if start_date <= date <= end_date:
            ax.axvline(date, color=HALVING_COLOR, linestyle=':', linewidth=1.5,
                      alpha=0.7, label=label)


def save_figure(
    fig,
    filename: str,
    output_dir,
    dpi: int = DEFAULT_DPI,
    bbox_inches: str = 'tight'
) -> str:
    """
    Save figure with consistent settings.
    
    Args:
        fig: Matplotlib figure object
        filename: Output filename (e.g., 'fig_cyprus_fees.png')
        output_dir: Directory to save (Path object or string)
        dpi: Resolution (default: 300 for publication)
        bbox_inches: Bounding box setting (default: 'tight')
    
    Returns:
        Full path to saved file
    
    Example:
        >>> from pathlib import Path
        >>> fig, ax = plt.subplots()
        >>> ax.plot([1, 2, 3])
        >>> save_figure(fig, 'my_plot.png', Path('data/figures'))
        'data/figures/my_plot.png'
    """
    from pathlib import Path
    
    output_path = Path(output_dir) / filename
    
    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save
    fig.savefig(output_path, dpi=dpi, bbox_inches=bbox_inches, 
                facecolor='white', edgecolor='none')
    
    print(f"   ✓ Saved figure: {output_path}")
    
    return str(output_path)


def create_comparison_legend(pre_label: str = "Pre-crisis", crisis_label: str = "Crisis") -> None:
    """
    Add a simple legend for pre vs. crisis comparisons.
    
    Args:
        pre_label: Label for pre-crisis data
        crisis_label: Label for crisis data
    
    Example:
        >>> plt.plot(dates, values)
        >>> create_comparison_legend()
    """
    from matplotlib.patches import Patch
    
    legend_elements = [
        Patch(facecolor=PRE_COLOR, alpha=0.15, label=pre_label),
        Patch(facecolor=CRISIS_COLOR, alpha=0.25, label=crisis_label)
    ]
    
    plt.legend(handles=legend_elements, loc='upper left')


# Quick test/demo
if __name__ == "__main__":
    print("Plotting Styles Module")
    print("\n📊 Available colors:")
    print(f"   PRE_COLOR: {PRE_COLOR}")
    print(f"   CRISIS_COLOR: {CRISIS_COLOR}")
    print(f"   ACCENT_COLOR: {ACCENT_COLOR}")
    print(f"   HALVING_COLOR: {HALVING_COLOR}")
    
    print("\n📐 Default figure size:", DEFAULT_FIGSIZE)
    print("📐 Default DPI:", DEFAULT_DPI)
    
    print("\n✅ Call apply_plot_style() at the start of plotting scripts")

