"""
Bitcoin Core RPC data source adapter.

This module connects to a local or remote Bitcoin Core node via RPC to fetch:
- Block-level data (fees, subsidy, transactions)
- Transaction-level data (fee rates in sat/vB)
- Historical on-chain metrics with full granularity

⚠️ REQUIREMENTS:
   - Bitcoin Core installed and synced
   - bitcoin.conf configured with:
       txindex=1  (for full transaction access)
       server=1
       rpcuser=YOUR_USER
       rpcpassword=YOUR_PASSWORD
   - python-bitcoinrpc package installed

WHY USE A NODE?
   - Complete historical data back to genesis block
   - Per-transaction granularity (exact fee rates)
   - No API rate limits or data gaps
   - Full control and reproducibility

SETUP GUIDE:
   1. Install Bitcoin Core: https://bitcoin.org/en/download
   2. Edit bitcoin.conf (location varies by OS):
      macOS: ~/Library/Application Support/Bitcoin/bitcoin.conf
      Linux: ~/.bitcoin/bitcoin.conf
      Windows: %APPDATA%\\Bitcoin\\bitcoin.conf
   
   3. Add these lines:
      txindex=1
      server=1
      rpcuser=bitcoinrpc
      rpcpassword=YOUR_SECURE_PASSWORD_HERE
   
   4. Restart Bitcoin Core and wait for txindex to build (takes hours)
   5. Update config/settings.yaml with your RPC credentials

ALTERNATIVES IF NO NODE:
   - Use Blockchain.com API (limited granularity, see blockchain_com.py)
   - Import pre-computed CSV files from community sources
"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import pandas as pd

# Bitcoin RPC library (optional dependency)
try:
    from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
    HAS_RPC = True
except ImportError:
    HAS_RPC = False
    print("⚠️  python-bitcoinrpc not installed. Install with: pip install python-bitcoinrpc")

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.io import save_csv


def connect_to_node(
    rpc_user: str,
    rpc_password: str,
    rpc_host: str = "127.0.0.1",
    rpc_port: int = 8332
) -> Optional['AuthServiceProxy']:
    """
    Connect to Bitcoin Core RPC interface.
    
    Args:
        rpc_user: RPC username from bitcoin.conf
        rpc_password: RPC password from bitcoin.conf
        rpc_host: Node IP address
        rpc_port: RPC port (default: 8332 for mainnet)
    
    Returns:
        RPC connection object, or None if connection fails
    
    Example:
        >>> rpc = connect_to_node("bitcoinrpc", "mypassword")
        >>> if rpc:
        ...     info = rpc.getblockchaininfo()
        ...     print(f"Current height: {info['blocks']}")
    """
    if not HAS_RPC:
        print("Cannot connect: python-bitcoinrpc not installed")
        return None
    
    try:
        rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
        rpc = AuthServiceProxy(rpc_url, timeout=300)
        
        # Test connection
        info = rpc.getblockchaininfo()
        print(f"✓ Connected to Bitcoin Core node")
        print(f"  Height: {info['blocks']}")
        print(f"  Chain: {info['chain']}")
        
        return rpc
    
    except Exception as e:
        print(f"❌ Failed to connect to node: {e}")
        print("   Check that:")
        print("   1. Bitcoin Core is running")
        print("   2. RPC credentials in config/settings.yaml are correct")
        print("   3. bitcoin.conf has server=1")
        return None


def get_block_subsidy(height: int) -> float:
    """
    Calculate block subsidy (coinbase reward) at a given height.
    
    Args:
        height: Block height
    
    Returns:
        Subsidy in BTC
    
    Formula:
        - Genesis to 209,999: 50 BTC
        - 210,000 to 419,999: 25 BTC  (first halving)
        - 420,000 to 629,999: 12.5 BTC
        - 630,000 to 839,999: 6.25 BTC
        - 840,000 to 1,049,999: 3.125 BTC
        - Halves every 210,000 blocks (~4 years)
    
    Example:
        >>> get_block_subsidy(100000)
        50.0
        >>> get_block_subsidy(700000)
        6.25
    """
    # Initial subsidy: 50 BTC
    subsidy = 50.0
    
    # Number of halvings that have occurred
    halvings = height // 210000
    
    # Divide by 2 for each halving
    subsidy = subsidy / (2 ** halvings)
    
    return subsidy


def extract_block_fees(rpc: 'AuthServiceProxy', block_hash: str) -> Dict:
    """
    Extract fee data from a single block.
    
    Args:
        rpc: Bitcoin Core RPC connection
        block_hash: Block hash (hex string)
    
    Returns:
        Dictionary with:
            - height: Block height
            - time: Block timestamp
            - fees_btc: Total fees in block (BTC)
            - tx_count: Number of transactions
            - subsidy_btc: Block subsidy
            - fee_to_subsidy: Fees / (Fees + Subsidy)
    
    Pseudocode:
        1. Get block data (height, timestamp, tx list)
        2. Calculate subsidy from height
        3. Sum all transaction fees:
           - Method A: Coinbase output - subsidy = fees
           - Method B: Sum(inputs) - Sum(outputs) for each tx
        4. Return aggregated metrics
    
    TODO: Implement actual fee extraction logic!
    """
    # TODO: Implement this function
    # 
    # block = rpc.getblock(block_hash, 2)  # verbosity=2 includes tx details
    # height = block['height']
    # timestamp = block['time']
    # 
    # # Get subsidy
    # subsidy = get_block_subsidy(height)
    # 
    # # Extract coinbase tx (first tx in block)
    # coinbase_tx = block['tx'][0]
    # coinbase_output_sum = sum(vout['value'] for vout in coinbase_tx['vout'])
    # fees = coinbase_output_sum - subsidy
    # 
    # # Transaction count (exclude coinbase)
    # tx_count = len(block['tx']) - 1
    # 
    # # Fee-to-subsidy ratio
    # total_reward = fees + subsidy
    # fee_to_subsidy = fees / total_reward if total_reward > 0 else 0
    # 
    # return {
    #     'height': height,
    #     'time': timestamp,
    #     'fees_btc': fees,
    #     'tx_count': tx_count,
    #     'subsidy_btc': subsidy,
    #     'fee_to_subsidy': fee_to_subsidy
    # }
    
    raise NotImplementedError("TODO: Implement block fee extraction")


def extract_transaction_fee_rates(
    rpc: 'AuthServiceProxy',
    block_hash: str
) -> List[float]:
    """
    Extract fee rates (sat/vB) for all transactions in a block.
    
    Args:
        rpc: RPC connection
        block_hash: Block hash
    
    Returns:
        List of fee rates in sat/vB (one per transaction, excluding coinbase)
    
    Pseudocode:
        1. Get block with full transaction details
        2. For each non-coinbase transaction:
           a. Calculate fee = sum(inputs) - sum(outputs)
           b. Get vsize (virtual size in vbytes)
           c. fee_rate = (fee * 1e8) / vsize  # Convert BTC to sats
        3. Return list of fee rates
    
    TODO: Implement this function!
    
    Note:
        - Requires txindex=1 to look up input values
        - vsize accounts for SegWit weight units
    """
    # TODO: Implement
    # 
    # block = rpc.getblock(block_hash, 2)
    # fee_rates = []
    # 
    # for tx in block['tx'][1:]:  # Skip coinbase
    #     # Get inputs (need to fetch previous txs for amounts)
    #     input_sum = 0
    #     for vin in tx['vin']:
    #         prev_tx = rpc.getrawtransaction(vin['txid'], True)
    #         input_sum += prev_tx['vout'][vin['vout']]['value']
    #     
    #     # Get outputs
    #     output_sum = sum(vout['value'] for vout in tx['vout'])
    #     
    #     # Fee in BTC
    #     fee = input_sum - output_sum
    #     
    #     # Fee rate in sat/vB
    #     vsize = tx['vsize']
    #     fee_rate = (fee * 1e8) / vsize
    #     
    #     fee_rates.append(fee_rate)
    # 
    # return fee_rates
    
    raise NotImplementedError("TODO: Implement transaction fee rate extraction")


def fetch_blocks_in_date_range(
    rpc: 'AuthServiceProxy',
    start_date: str,
    end_date: str,
    output_dir: Path
) -> Path:
    """
    Fetch block-level data for all blocks in a date range.
    
    Args:
        rpc: RPC connection
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
        output_dir: Where to save CSV
    
    Returns:
        Path to saved CSV
    
    Output CSV columns:
        - date: YYYY-MM-DD
        - height: Block height
        - fees_btc: Total fees in block
        - subsidy_btc: Block subsidy
        - tx_count: Number of transactions
        - fee_to_subsidy: Fees / Total reward
        - median_sat_vb: Median fee rate in block
        - p90_sat_vb: 90th percentile fee rate
    
    Pseudocode:
        1. Convert dates to timestamps
        2. Find first and last block heights in range
        3. For each block:
           a. Extract fees and subsidy
           b. Extract transaction fee rates
           c. Compute median and p90
        4. Save to CSV
    
    TODO: Implement this function!
    
    Note: This can take hours for large date ranges!
          Consider parallelization or caching.
    """
    # TODO: Implement
    # 
    # start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    # end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    # 
    # # Binary search or linear scan to find block heights
    # # (Use getblockhash + getblockheader to map time to height)
    # 
    # blocks_data = []
    # for height in range(start_height, end_height + 1):
    #     block_hash = rpc.getblockhash(height)
    #     
    #     # Extract fees
    #     block_fees = extract_block_fees(rpc, block_hash)
    #     
    #     # Extract fee rates
    #     fee_rates = extract_transaction_fee_rates(rpc, block_hash)
    #     
    #     # Compute percentiles
    #     if fee_rates:
    #         median_sat_vb = np.median(fee_rates)
    #         p90_sat_vb = np.percentile(fee_rates, 90)
    #     else:
    #         median_sat_vb = 0
    #         p90_sat_vb = 0
    #     
    #     blocks_data.append({
    #         'date': datetime.fromtimestamp(block_fees['time']).date(),
    #         'height': height,
    #         'fees_btc': block_fees['fees_btc'],
    #         'subsidy_btc': block_fees['subsidy_btc'],
    #         'tx_count': block_fees['tx_count'],
    #         'fee_to_subsidy': block_fees['fee_to_subsidy'],
    #         'median_sat_vb': median_sat_vb,
    #         'p90_sat_vb': p90_sat_vb
    #     })
    # 
    # df = pd.DataFrame(blocks_data)
    # output_path = output_dir / f"node_rpc_blocks_{start_date}_to_{end_date}.csv"
    # save_csv(df, output_path)
    # return output_path
    
    raise NotImplementedError("TODO: Implement date range block fetching")


# Example usage
if __name__ == "__main__":
    print("⚠️  This module requires a Bitcoin Core node with RPC access.")
    print("   See docstring for setup instructions.")
    print("\n   Once configured, you can:")
    print("   1. Connect to node: rpc = connect_to_node('user', 'pass')")
    print("   2. Fetch blocks: fetch_blocks_in_date_range(rpc, '2013-01-01', '2013-12-31', Path('data/raw'))")
    print("\n   For now, use blockchain_com.py for quick data access!")

