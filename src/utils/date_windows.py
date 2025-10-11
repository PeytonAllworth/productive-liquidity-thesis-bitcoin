"""
Date window utilities for event study analysis.

This module provides functions to:
- Parse ISO date strings
- Build event windows (±N days around an anchor)
- Label periods as "pre" vs "crisis"
- Slice time-series data by date ranges

Key Concept: Event Windows
---------------------------
An "event window" is a time period centered on a crisis anchor date.

Example:
    Anchor = 2013-03-16 (Cyprus crisis)
    days_before = 90
    days_after = 90
    
    Pre-period:   2012-12-16 to 2013-03-15 (90 days)
    Crisis period: 2013-03-16 to 2013-06-14 (91 days, inclusive of anchor)

This allows us to compare on-chain behavior before vs. during crises.
"""

from datetime import datetime, timedelta
from typing import Tuple, Dict
import pandas as pd


def parse_date(date_str: str) -> datetime:
    """
    Parse an ISO date string (YYYY-MM-DD) to datetime object.
    
    Args:
        date_str: Date in YYYY-MM-DD format
    
    Returns:
        datetime object
    
    Example:
        >>> dt = parse_date("2013-03-16")
        >>> print(dt)
        2013-03-16 00:00:00
    """
    return datetime.strptime(date_str, "%Y-%m-%d")


def build_event_window(
    anchor_date: str,
    days_before: int = 90,
    days_after: int = 90
) -> Dict[str, Tuple[str, str]]:
    """
    Build pre-crisis and crisis date ranges around an anchor date.
    
    Args:
        anchor_date: Crisis anchor in YYYY-MM-DD format
        days_before: Number of days before anchor (pre-period)
        days_after: Number of days after anchor (crisis period, inclusive)
    
    Returns:
        Dictionary with keys 'pre' and 'crisis', each containing
        (start_date, end_date) tuples as strings
    
    Example:
        >>> window = build_event_window("2013-03-16", 90, 90)
        >>> print(window['pre'])
        ('2012-12-16', '2013-03-15')
        >>> print(window['crisis'])
        ('2013-03-16', '2013-06-14')
    """
    anchor = parse_date(anchor_date)
    
    # Pre-period: [anchor - days_before, anchor - 1 day]
    pre_start = anchor - timedelta(days=days_before)
    pre_end = anchor - timedelta(days=1)
    
    # Crisis period: [anchor, anchor + days_after]
    crisis_start = anchor
    crisis_end = anchor + timedelta(days=days_after)
    
    return {
        'pre': (
            pre_start.strftime("%Y-%m-%d"),
            pre_end.strftime("%Y-%m-%d")
        ),
        'crisis': (
            crisis_start.strftime("%Y-%m-%d"),
            crisis_end.strftime("%Y-%m-%d")
        )
    }


def label_period(date: pd.Timestamp, anchor_date: str) -> str:
    """
    Label a date as 'pre' or 'crisis' relative to anchor.
    
    Args:
        date: Pandas Timestamp to label
        anchor_date: Crisis anchor in YYYY-MM-DD format
    
    Returns:
        'pre' if date < anchor, 'crisis' if date >= anchor
    
    Example:
        >>> import pandas as pd
        >>> dt = pd.Timestamp("2013-03-10")
        >>> label = label_period(dt, "2013-03-16")
        >>> print(label)
        'pre'
    """
    anchor = pd.Timestamp(anchor_date)
    return 'pre' if date < anchor else 'crisis'


def slice_dataframe_by_window(
    df: pd.DataFrame,
    start_date: str,
    end_date: str,
    date_column: str = 'date'
) -> pd.DataFrame:
    """
    Slice a DataFrame to include only rows within [start_date, end_date].
    
    Args:
        df: DataFrame with a date column
        start_date: Start date (YYYY-MM-DD), inclusive
        end_date: End date (YYYY-MM-DD), inclusive
        date_column: Name of the date column (default: 'date')
    
    Returns:
        Filtered DataFrame
    
    Example:
        >>> df = pd.DataFrame({
        ...     'date': pd.date_range('2013-01-01', periods=365),
        ...     'value': range(365)
        ... })
        >>> sliced = slice_dataframe_by_window(df, "2013-03-01", "2013-03-31")
        >>> print(len(sliced))
        31
    
    Note:
        - Assumes date_column is already a datetime type or can be converted
        - Bounds are inclusive: [start_date, end_date]
    """
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df = df.copy()
        df[date_column] = pd.to_datetime(df[date_column])
    
    # Filter by date range (inclusive)
    mask = (df[date_column] >= start_date) & (df[date_column] <= end_date)
    return df[mask].copy()


def add_period_labels(
    df: pd.DataFrame,
    anchor_date: str,
    date_column: str = 'date'
) -> pd.DataFrame:
    """
    Add a 'period' column labeling each row as 'pre' or 'crisis'.
    
    Args:
        df: DataFrame with date column
        anchor_date: Crisis anchor date (YYYY-MM-DD)
        date_column: Name of date column
    
    Returns:
        DataFrame with new 'period' column
    
    Example:
        >>> df = pd.DataFrame({
        ...     'date': ['2013-03-10', '2013-03-20'],
        ...     'value': [100, 150]
        ... })
        >>> df['date'] = pd.to_datetime(df['date'])
        >>> labeled = add_period_labels(df, "2013-03-16")
        >>> print(labeled['period'].tolist())
        ['pre', 'crisis']
    """
    df = df.copy()
    
    # Ensure datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])
    
    # Apply label function
    df['period'] = df[date_column].apply(lambda d: label_period(d, anchor_date))
    
    return df


def get_all_event_windows(
    events_dict: Dict[str, str],
    days_before: int = 90,
    days_after: int = 90
) -> Dict[str, Dict[str, Tuple[str, str]]]:
    """
    Build event windows for multiple crises at once.
    
    Args:
        events_dict: {event_name: anchor_date} from config
        days_before: Pre-period length
        days_after: Crisis period length
    
    Returns:
        Nested dict: {event_name: {pre: (start, end), crisis: (start, end)}}
    
    Example:
        >>> events = {
        ...     'cyprus_2013': '2013-03-16',
        ...     'covid_cpi_peak_2022': '2022-06-01'
        ... }
        >>> windows = get_all_event_windows(events, 90, 90)
        >>> print(windows['cyprus_2013']['crisis'])
        ('2013-03-16', '2013-06-14')
    """
    return {
        event_name: build_event_window(anchor, days_before, days_after)
        for event_name, anchor in events_dict.items()
    }

