"""
Blockchain.com API data source adapter.

This module fetches Bitcoin network statistics from Blockchain.com's free API.
No authentication required!

Available metrics:
- Total transaction fees per day (BTC)
- Total confirmed transactions per day
- Blocks mined per day
- Bitcoin Days Destroyed (BDD) - dormancy proxy

API Documentation: https://www.blockchain.com/api/charts_api

Key endpoints:
- https://api.blockchain.info/charts/transaction-fees?timespan=all&format=json
- https://api.blockchain.info/charts/n-transactions?timespan=all&format=json
- https://api.blockchain.info/charts/n-blocks?timespan=all&format=json
- https://api.blockchain.info/charts/bdd?timespan=all&format=json
"""

import time
from typing import Optional
from pathlib import Path
import pandas as pd
import requests

# Import project utilities
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.io import save_csv, ensure_dir


def fetch_chart_data(
    chart_name: str,
    timespan: str = "all",
    base_url: str = "https://api.blockchain.info"
) -> dict:
    """
    Fetch data from Blockchain.com Charts API.
    
    Args:
        chart_name: Chart identifier (e.g., 'transaction-fees', 'n-transactions')
        timespan: Time span ('all', '1year', '30days', etc.)
        base_url: API base URL
    
    Returns:
        Dictionary with 'values' list: [{'x': timestamp, 'y': value}, ...]
    
    Raises:
        requests.RequestException: If API call fails
    
    Example:
        >>> data = fetch_chart_data('transaction-fees', timespan='1year')
        >>> print(data['name'])
        'Transaction Fees'
    """
    url = f"{base_url}/charts/{chart_name}"
    params = {
        'timespan': timespan,
        'format': 'json'
    }
    
    print(f"Fetching {chart_name} from Blockchain.com API...")
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()  # Raise exception for 4xx/5xx errors
    
    data = response.json()
    print(f"  ✓ Fetched {len(data.get('values', []))} data points")
    
    return data


def parse_chart_to_dataframe(chart_data: dict, value_column: str) -> pd.DataFrame:
    """
    Convert Blockchain.com chart data to a tidy DataFrame.
    
    Args:
        chart_data: JSON response from API
        value_column: Name for the value column
    
    Returns:
        DataFrame with columns: date, <value_column>
    
    Example:
        >>> data = {'values': [{'x': 1609459200, 'y': 12.5}]}
        >>> df = parse_chart_to_dataframe(data, 'fees_btc_day')
        >>> print(df.columns)
        Index(['date', 'fees_btc_day'], dtype='object')
    """
    values = chart_data.get('values', [])
    
    # Extract x (timestamp) and y (value)
    df = pd.DataFrame(values)
    
    # Convert Unix timestamp to date
    df['date'] = pd.to_datetime(df['x'], unit='s').dt.date
    df['date'] = pd.to_datetime(df['date'])  # Convert back to datetime
    
    # Rename 'y' to meaningful column name
    df = df.rename(columns={'y': value_column})
    
    # Keep only date and value
    df = df[['date', value_column]]
    
    return df


def fetch_transaction_fees(
    output_dir: Path,
    timespan: str = "all"
) -> Path:
    """
    Fetch total transaction fees per day (BTC).
    
    Args:
        output_dir: Directory to save CSV
        timespan: Time span to fetch
    
    Returns:
        Path to saved CSV file
    
    Output CSV columns:
        - date: YYYY-MM-DD
        - fees_btc_day: Total fees in BTC for that day
    
    Example:
        >>> from pathlib import Path
        >>> csv_path = fetch_transaction_fees(Path("data/raw"))
        >>> print(csv_path)
        data/raw/blockchain_com_fees_btc_day.csv
    """
    chart_data = fetch_chart_data('transaction-fees', timespan)
    df = parse_chart_to_dataframe(chart_data, 'fees_btc_day')
    
    # Save to CSV
    output_path = Path(output_dir) / "blockchain_com_fees_btc_day.csv"
    save_csv(df, output_path)
    
    return output_path


def fetch_transactions_per_day(
    output_dir: Path,
    timespan: str = "all"
) -> Path:
    """
    Fetch total confirmed transactions per day.
    
    Args:
        output_dir: Directory to save CSV
        timespan: Time span to fetch
    
    Returns:
        Path to saved CSV file
    
    Output CSV columns:
        - date: YYYY-MM-DD
        - tx_per_day: Number of confirmed transactions
    """
    chart_data = fetch_chart_data('n-transactions', timespan)
    df = parse_chart_to_dataframe(chart_data, 'tx_per_day')
    
    output_path = Path(output_dir) / "blockchain_com_tx_per_day.csv"
    save_csv(df, output_path)
    
    return output_path


def fetch_blocks_per_day(
    output_dir: Path,
    timespan: str = "all"
) -> Path:
    """
    Fetch number of blocks mined per day.
    
    Args:
        output_dir: Directory to save CSV
        timespan: Time span to fetch
    
    Returns:
        Path to saved CSV file
    
    Output CSV columns:
        - date: YYYY-MM-DD
        - blocks_per_day: Number of blocks mined
    
    Note:
        - Expected value: ~144 blocks/day (10 min avg)
        - Actual varies due to difficulty adjustments
    """
    chart_data = fetch_chart_data('n-blocks', timespan)
    df = parse_chart_to_dataframe(chart_data, 'blocks_per_day')
    
    output_path = Path(output_dir) / "blockchain_com_blocks_per_day.csv"
    save_csv(df, output_path)
    
    return output_path


def fetch_bitcoin_days_destroyed(
    output_dir: Path,
    timespan: str = "all"
) -> Path:
    """
    Fetch Bitcoin Days Destroyed (BDD) - dormancy indicator.
    
    Args:
        output_dir: Directory to save CSV
        timespan: Time span to fetch
    
    Returns:
        Path to saved CSV file
    
    Output CSV columns:
        - date: YYYY-MM-DD
        - bdd: Bitcoin Days Destroyed
    
    What is BDD?
        - BDD = sum of (bitcoin_amount * age_in_days) for all spent outputs
        - High BDD = old coins moving (HODLers breaking dormancy)
        - During crises, liquidity preference → old coins wake up → BDD spikes
    
    Limitation:
        - Affected by on-chain activity unrelated to crises (e.g., exchanges)
        - Consider normalizing or using moving averages
    """
    chart_data = fetch_chart_data('bdd', timespan)
    df = parse_chart_to_dataframe(chart_data, 'bdd')
    
    output_path = Path(output_dir) / "blockchain_com_bdd.csv"
    save_csv(df, output_path)
    
    return output_path


def fetch_all_metrics(
    output_dir: Path,
    timespan: str = "all",
    delay_seconds: float = 1.0
) -> dict:
    """
    Fetch all available metrics from Blockchain.com API.
    
    Args:
        output_dir: Directory to save CSVs
        timespan: Time span for all requests
        delay_seconds: Delay between API calls (be polite!)
    
    Returns:
        Dictionary mapping metric name to CSV path
    
    Example:
        >>> from pathlib import Path
        >>> paths = fetch_all_metrics(Path("data/raw"))
        >>> print(paths.keys())
        dict_keys(['fees', 'transactions', 'blocks', 'bdd'])
    
    Note:
        - Adds delays between requests to avoid rate limiting
        - Be respectful of free APIs!
    """
    ensure_dir(output_dir)
    
    paths = {}
    
    print("\n📊 Fetching Blockchain.com data...")
    print("=" * 60)
    
    # Transaction fees
    paths['fees'] = fetch_transaction_fees(output_dir, timespan)
    time.sleep(delay_seconds)
    
    # Transactions per day
    paths['transactions'] = fetch_transactions_per_day(output_dir, timespan)
    time.sleep(delay_seconds)
    
    # Blocks per day
    paths['blocks'] = fetch_blocks_per_day(output_dir, timespan)
    time.sleep(delay_seconds)
    
    # Bitcoin Days Destroyed (dormancy proxy)
    paths['bdd'] = fetch_bitcoin_days_destroyed(output_dir, timespan)
    
    print("=" * 60)
    print("✓ All Blockchain.com metrics fetched successfully!\n")
    
    return paths


def compute_fees_per_block(
    fees_csv: Path,
    blocks_csv: Path,
    output_dir: Path
) -> Path:
    """
    Compute fees per block (BTC) from daily totals.
    
    Args:
        fees_csv: Path to fees_btc_day CSV
        blocks_csv: Path to blocks_per_day CSV
        output_dir: Directory to save result
    
    Returns:
        Path to computed CSV
    
    Output CSV columns:
        - date
        - fees_btc_day
        - blocks_per_day
        - fees_per_block_btc: fees_btc_day / blocks_per_day
    
    Formula:
        fees_per_block = (total_fees_that_day) / (blocks_mined_that_day)
    
    Use Case:
        - Normalizes daily fee revenue by block count
        - More stable than raw daily fees (which vary with block luck)
    """
    # Load data
    fees_df = pd.read_csv(fees_csv, parse_dates=['date'])
    blocks_df = pd.read_csv(blocks_csv, parse_dates=['date'])
    
    # Merge on date
    df = fees_df.merge(blocks_df, on='date', how='inner')
    
    # Compute fees per block
    df['fees_per_block_btc'] = df['fees_btc_day'] / df['blocks_per_day']
    
    # Save
    output_path = Path(output_dir) / "blockchain_com_fees_per_block_btc.csv"
    save_csv(df, output_path)
    
    return output_path


# Example usage (if run as script):
if __name__ == "__main__":
    from pathlib import Path
    
    # Define output directory
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw"
    
    # Fetch all metrics
    paths = fetch_all_metrics(output_dir, timespan="all")
    
    # Compute derived metric
    fees_per_block_path = compute_fees_per_block(
        paths['fees'],
        paths['blocks'],
        output_dir
    )
    
    print(f"\n✅ Done! Check {output_dir} for CSV files.")

