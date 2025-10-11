"""
Input/output utilities for saving and loading data files.

This module provides helpers for:
- Saving DataFrames to CSV with consistent formatting
- Loading CSV files with date parsing
- Creating timestamped backups (optional)
- Ensuring output directories exist

All data should flow through these helpers for consistency.
"""

from pathlib import Path
from typing import Optional
from datetime import datetime
import pandas as pd


def ensure_dir(path: Path) -> None:
    """
    Create directory if it doesn't exist.
    
    Args:
        path: Path object or string to directory
    
    Example:
        >>> ensure_dir(Path("data/raw"))
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def save_csv(
    df: pd.DataFrame,
    file_path: Path,
    timestamp_backup: bool = False
) -> Path:
    """
    Save DataFrame to CSV with consistent formatting.
    
    Args:
        df: DataFrame to save
        file_path: Output path (Path object or string)
        timestamp_backup: If True, also save a timestamped backup
    
    Returns:
        Path to saved file
    
    Example:
        >>> df = pd.DataFrame({'date': ['2013-01-01'], 'value': [100]})
        >>> save_csv(df, Path("data/raw/test.csv"))
        PosixPath('data/raw/test.csv')
    
    Notes:
        - Creates parent directories if they don't exist
        - Saves with index=False (cleaner CSVs)
        - Uses UTF-8 encoding
    """
    file_path = Path(file_path)
    
    # Ensure output directory exists
    ensure_dir(file_path.parent)
    
    # Save main file
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"✓ Saved {len(df)} rows to {file_path}")
    
    # Optional: Save timestamped backup
    if timestamp_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = file_path.parent / backup_name
        df.to_csv(backup_path, index=False, encoding='utf-8')
        print(f"  ↳ Backup saved: {backup_path.name}")
    
    return file_path


def load_csv(
    file_path: Path,
    parse_dates: Optional[list] = None,
    date_column: str = 'date'
) -> pd.DataFrame:
    """
    Load CSV file into DataFrame with date parsing.
    
    Args:
        file_path: Path to CSV file
        parse_dates: List of column names to parse as dates
                    If None and date_column exists, parses date_column
        date_column: Default date column name
    
    Returns:
        DataFrame with parsed dates
    
    Example:
        >>> df = load_csv(Path("data/raw/fees.csv"))
        >>> print(df['date'].dtype)
        datetime64[ns]
    
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"CSV not found: {file_path}")
    
    # Auto-detect date columns if not specified
    if parse_dates is None:
        parse_dates = [date_column]
    
    df = pd.read_csv(file_path, parse_dates=parse_dates, encoding='utf-8')
    print(f"✓ Loaded {len(df)} rows from {file_path}")
    
    return df


def save_json(data: dict, file_path: Path) -> Path:
    """
    Save dictionary to JSON file (for raw API responses).
    
    Args:
        data: Dictionary to save
        file_path: Output path
    
    Returns:
        Path to saved file
    
    Example:
        >>> data = {'blocks': [{'height': 100000, 'fees': 0.5}]}
        >>> save_json(data, Path("data/raw/blocks.json"))
    """
    import json
    
    file_path = Path(file_path)
    ensure_dir(file_path.parent)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved JSON to {file_path}")
    return file_path


def load_json(file_path: Path) -> dict:
    """
    Load JSON file into dictionary.
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        Dictionary
    
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    import json
    
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"JSON not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✓ Loaded JSON from {file_path}")
    return data


def get_latest_file(directory: Path, pattern: str = "*.csv") -> Optional[Path]:
    """
    Get the most recently modified file matching a pattern.
    
    Args:
        directory: Directory to search
        pattern: Glob pattern (default: *.csv)
    
    Returns:
        Path to latest file, or None if no matches
    
    Example:
        >>> latest = get_latest_file(Path("data/raw"), "fees_*.csv")
        >>> if latest:
        ...     print(f"Latest: {latest.name}")
    """
    directory = Path(directory)
    
    if not directory.exists():
        return None
    
    files = list(directory.glob(pattern))
    
    if not files:
        return None
    
    # Sort by modification time, return most recent
    latest = max(files, key=lambda p: p.stat().st_mtime)
    return latest

