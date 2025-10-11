"""
Custom Data Source 1 - Template for adding new data sources.

This is a blank template you can use to integrate additional data sources
into your research pipeline.

Examples of what you might add here:
- Lightning Network statistics (e.g., channel capacity, routing volume)
- Mining pool data (e.g., hash rate distribution)
- Exchange data (e.g., on-chain flows to/from exchanges)
- Social sentiment data (e.g., Twitter mentions, Reddit activity)
- Macro indicators (e.g., gold prices, VIX, CPI data for correlation)

⚠️ REMEMBER: Stay BTC-native when possible!
   If using USD data, clearly label it and explain why it's needed.
"""

from typing import Optional
from pathlib import Path
import pandas as pd

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.io import save_csv, ensure_dir


def fetch_to_csv(
    start_date: str,
    end_date: str,
    output_dir: Path
) -> Optional[Path]:
    """
    Fetch data from [YOUR DATA SOURCE] and save to CSV.
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        output_dir: Directory to save CSV
    
    Returns:
        Path to saved CSV, or None if fetch fails
    
    TODO: Implement your data fetching logic here!
    
    Steps:
        1. Connect to API or load from file
        2. Filter data by date range
        3. Transform to tidy format with 'date' column
        4. Save to CSV in output_dir
        5. Return path
    
    Example:
        >>> from pathlib import Path
        >>> path = fetch_to_csv("2020-01-01", "2020-12-31", Path("data/raw"))
        >>> if path:
        ...     print(f"Data saved to {path}")
    """
    # TODO: Replace this placeholder with actual implementation
    
    print(f"\n📥 Fetching data from Custom Source 1...")
    print(f"   Date range: {start_date} to {end_date}")
    print("   ⚠️  This is a placeholder - implement fetch logic!")
    
    # Example structure:
    # 
    # # 1. Fetch data (replace with your API call)
    # response = requests.get("https://example.com/api/data", params={...})
    # data = response.json()
    # 
    # # 2. Parse to DataFrame
    # df = pd.DataFrame(data)
    # df['date'] = pd.to_datetime(df['timestamp']).dt.date
    # df = df[['date', 'your_metric_1', 'your_metric_2']]
    # 
    # # 3. Filter by date
    # df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    # 
    # # 4. Save
    # output_path = output_dir / "custom_source_1_data.csv"
    # save_csv(df, output_path)
    # 
    # return output_path
    
    print("   🚧 Not implemented yet!\n")
    return None


def process_data(csv_path: Path) -> pd.DataFrame:
    """
    Post-process fetched data (optional).
    
    Args:
        csv_path: Path to raw CSV from fetch_to_csv()
    
    Returns:
        Processed DataFrame
    
    TODO: Add any data cleaning, normalization, or derived metrics here.
    
    Example:
        - Remove outliers
        - Compute rolling averages
        - Merge with other datasets
    """
    df = pd.read_csv(csv_path, parse_dates=['date'])
    
    # TODO: Add processing logic
    # 
    # Example: Compute 7-day moving average
    # df['metric_7d_ma'] = df['your_metric'].rolling(7).mean()
    
    return df


# Notes for implementation:
"""
When implementing this module, consider:

1. Data Quality:
   - Check for missing values
   - Validate date formats
   - Handle API errors gracefully

2. Rate Limiting:
   - Add delays between API calls
   - Respect API usage limits
   - Cache responses when possible

3. Documentation:
   - Document data source URL
   - Explain what each metric means
   - Note any limitations or biases

4. BTC-Native Units:
   - Prefer BTC, sats, sat/vB over USD
   - If using USD, compute BTC equivalents
   - Document any currency conversions

5. Reproducibility:
   - Save raw API responses (JSON) before processing
   - Log data fetch timestamps
   - Version API endpoints in comments
"""

if __name__ == "__main__":
    print("Custom Data Source 1 - Not yet implemented")
    print("Edit this file to add your data source logic!")

