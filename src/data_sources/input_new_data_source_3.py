"""
Custom Data Source 3 - Template for adding new data sources.

Use this template to add a third data source to your research.

Suggested use cases:
- Layer 2 data (Lightning Network metrics)
- Geographic data (LocalBitcoins volume by country)
- On-chain analytics (UTXO age distribution, whale movements)
- News/event data (structured crisis timeline)
"""

from typing import Optional
from pathlib import Path
import pandas as pd

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.io import save_csv


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
    """
    print(f"\n📥 Custom Data Source 3: {start_date} to {end_date}")
    print("   🚧 Not implemented yet!\n")
    
    # TODO: Add implementation
    
    return None


if __name__ == "__main__":
    print("Custom Data Source 3 - Not yet implemented")

