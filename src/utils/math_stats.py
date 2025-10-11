"""
Mathematical and statistical utilities for analysis.

This module provides:
- Percent change calculations
- Percentile computations
- Rolling averages
- Basic descriptive statistics

All calculations use BTC-native units (no USD conversions).
"""

from typing import Union
import pandas as pd
import numpy as np


def percent_change(
    value_new: float,
    value_old: float,
    round_decimals: int = 2
) -> float:
    """
    Calculate percent change from old to new value.
    
    Formula: ((new - old) / old) * 100
    
    Args:
        value_new: New value (crisis period)
        value_old: Old value (pre-period)
        round_decimals: Decimal places to round result
    
    Returns:
        Percent change (positive = increase, negative = decrease)
    
    Example:
        >>> percent_change(150, 100)
        50.0
        >>> percent_change(75, 100)
        -25.0
    
    Notes:
        - Returns NaN if value_old is 0 (undefined)
    """
    if value_old == 0:
        return np.nan
    
    pct = ((value_new - value_old) / value_old) * 100
    return round(pct, round_decimals)


def pp_change(
    share_new: float,
    share_old: float,
    round_decimals: int = 2
) -> float:
    """
    Calculate percentage point (pp) change for ratios/shares.
    
    Formula: new - old (simple difference for shares)
    
    Args:
        share_new: New ratio (e.g., 0.15 for 15%)
        share_old: Old ratio (e.g., 0.10 for 10%)
        round_decimals: Decimal places
    
    Returns:
        Percentage point change
    
    Example:
        >>> pp_change(0.15, 0.10)
        0.05
        # Interpretation: Fee-to-Subsidy increased by 5 percentage points
    
    Use Case:
        - Fee-to-Subsidy ratio: 10% → 15% is a 5pp increase (NOT 50%)
        - Percentage points preserve absolute scale for ratios
    """
    pp = share_new - share_old
    return round(pp, round_decimals)


def rolling_mean(
    series: pd.Series,
    window: int = 30,
    min_periods: int = 1
) -> pd.Series:
    """
    Calculate rolling (moving) average.
    
    Args:
        series: Pandas Series to smooth
        window: Window size in periods (default: 30 days)
        min_periods: Minimum observations needed (default: 1)
    
    Returns:
        Series with rolling mean values
    
    Example:
        >>> s = pd.Series([1, 2, 3, 4, 5])
        >>> rolling_mean(s, window=3)
        0    1.0
        1    1.5
        2    2.0
        3    3.0
        4    4.0
        dtype: float64
    
    Use Case:
        - Smooth noisy daily metrics (fees, tx counts)
        - 30-day MA is common for Bitcoin analysis
    """
    return series.rolling(window=window, min_periods=min_periods).mean()


def compute_percentiles(
    series: pd.Series,
    percentiles: list = [50, 90]
) -> dict:
    """
    Compute multiple percentiles from a series.
    
    Args:
        series: Pandas Series of values
        percentiles: List of percentiles to compute (e.g., [50, 90])
    
    Returns:
        Dictionary {50: median_value, 90: p90_value, ...}
    
    Example:
        >>> s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        >>> compute_percentiles(s, [50, 90])
        {50: 5.5, 90: 9.1}
    
    Use Case:
        - Median fee rate (p50)
        - Urgency fee rate (p90)
        - Spread = p90 - p50
    """
    return {p: series.quantile(p / 100) for p in percentiles}


def urgency_spread(p90: float, p50: float) -> float:
    """
    Calculate urgency spread (p90 - p50 fee rate).
    
    Args:
        p90: 90th percentile fee rate (sat/vB)
        p50: 50th percentile (median) fee rate (sat/vB)
    
    Returns:
        Spread in sat/vB
    
    Example:
        >>> urgency_spread(150, 50)
        100.0
        # Users willing to pay 100 sat/vB more for urgency
    
    Interpretation:
        - Higher spread = more urgency / fee-rate diversity
        - During crises, expect spread to increase as some users
          are willing to pay premium for fast confirmation
    """
    return p90 - p50


def summary_stats(series: pd.Series) -> dict:
    """
    Compute basic summary statistics for a series.
    
    Args:
        series: Pandas Series of values
    
    Returns:
        Dictionary with mean, median, std, min, max
    
    Example:
        >>> s = pd.Series([1, 2, 3, 4, 5])
        >>> stats = summary_stats(s)
        >>> print(stats['mean'])
        3.0
    """
    return {
        'mean': series.mean(),
        'median': series.median(),
        'std': series.std(),
        'min': series.min(),
        'max': series.max(),
        'count': len(series)
    }


def compare_periods(
    pre_series: pd.Series,
    crisis_series: pd.Series,
    metric_name: str = "metric"
) -> dict:
    """
    Compare statistics between pre and crisis periods.
    
    Args:
        pre_series: Series of values from pre-period
        crisis_series: Series of values from crisis period
        metric_name: Name for labeling output
    
    Returns:
        Dictionary with pre/crisis means and percent change
    
    Example:
        >>> pre = pd.Series([50, 55, 60])
        >>> crisis = pd.Series([80, 85, 90])
        >>> result = compare_periods(pre, crisis, "median_sat_vb")
        >>> print(result)
        {
            'metric': 'median_sat_vb',
            'pre_mean': 55.0,
            'crisis_mean': 85.0,
            'percent_change': 54.55
        }
    """
    pre_mean = pre_series.mean()
    crisis_mean = crisis_series.mean()
    pct_chg = percent_change(crisis_mean, pre_mean)
    
    return {
        'metric': metric_name,
        'pre_mean': round(pre_mean, 4),
        'crisis_mean': round(crisis_mean, 4),
        'percent_change': pct_chg
    }

