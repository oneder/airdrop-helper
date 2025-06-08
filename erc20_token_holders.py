import csv
import requests
import time
import os
import sys
import math
import traceback

from web3 import Web3
from collections import defaultdict
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HEADERS = {"Content-Type": "application/json"}
INFURA_API_KEY = os.environ["INFURA_API_KEY"]
POLYGON_RPC_URL = f"https://polygon-mainnet.infura.io/v3/{INFURA_API_KEY}"

# Get folder path from environment variables
SNAPSHOTS_FOLDER = os.getenv("SNAPSHOTS_FOLDER")

if not SNAPSHOTS_FOLDER:
    print("Error: SNAPSHOTS_FOLDER not set in the .env file.")
    sys.exit(1)

w3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))
if not w3.is_connected():
    raise Exception("Could not connect to Polygon RPC.")
print(f"Connected to Polygon. Latest block: {w3.eth.block_number}")

EXCLUDED_ADDRESSES = [
    w3.to_checksum_address("0x0000000000000000000000000000000000000000"),
    w3.to_checksum_address("0x000000000000000000000000000000000000DEAD")
]

TRANSFER_EVENT_SIG = Web3.to_hex(Web3.keccak(text="Transfer(address,address,uint256)"))
START_BLOCK = 0

# Prompt user for required input
raw_token_contract = input("Enter the token contract of the token holders need to receive the airdrop: ").strip()
token_contract = Web3.to_checksum_address(raw_token_contract)
print(f"\tToken Contract: {token_contract}")

minimum_amount = int(input("Enter the minimum amount required: ").strip())

def fetch_token_transfers(token_contract, from_block, to_block, step=1000):
    print(f"Fetching all token transfer recipients for '{token_contract}' starting from block 0...")
    transfers = []
    for start in range(from_block, to_block + 1, step):
        end = min(start + step - 1, to_block)
        print(f"\tFetching blocks {start} to {end}...")

        try:
            result = w3.eth.get_logs({
                "fromBlock": start,
                "toBlock": end,
                "address": token_contract,
                "topics": [TRANSFER_EVENT_SIG, None, None]
            })
            transfers.extend(result)
            time.sleep(0.5)
        except Exception as e:
            print(f"Error fetching blocks {start}-{end}: {e}")
            traceback.print_exc()

    print(f"Fetched {len(transfers)} transfer events.")
    return transfers

def build_balances(transfers, min_amount):
    balances = defaultdict(int)

    for transfer in transfers:
        try:
            from_address = Web3.to_checksum_address("0x" + transfer['topics'][1].hex()[-40:])
            to_address = Web3.to_checksum_address("0x" + transfer['topics'][2].hex()[-40:])

            data_field = transfer['data']
            if isinstance(data_field, bytes):
                value = int(data_field.hex(), 16)
            else:
                value = int(data_field, 16)

            if value > 0:
                if from_address not in EXCLUDED_ADDRESSES:
                    balances[from_address] -= value
                if to_address not in EXCLUDED_ADDRESSES:
                    balances[to_address] += value
        except Exception as e:
            print(f"Error parsing transfer log: {e}")

    # Filter zero balances
    return {addr: bal for addr, bal in balances.items() if bal >= min_amount}

def save_to_csv(snapshot, decimals=18):
    # Define the output file path
    filename = f"erc20_snapshot_{token_contract}_{datetime.now().strftime('%Y%m%d')}.csv"
    output_csv_path = os.path.join(SNAPSHOTS_FOLDER, filename)

    with open(output_csv_path, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["address", "quantity"])

        for addr, raw_bal in snapshot.items():
            formatted = raw_bal / (10 ** decimals)
            writer.writerow([addr, f"{formatted:.6f}"])

    print(f"Snapshot saved to '{filename}' in {SNAPSHOTS_FOLDER} folder.")

def main():
    latest_block = w3.eth.block_number
    transfers = fetch_token_transfers(token_contract, START_BLOCK, latest_block)
    balances = build_balances(transfers=transfers, min_amount=minimum_amount)
    print(f"Found {len(balances)} holders of '{token_contract}' with non-zero balance.")
    save_to_csv(balances)

if __name__ == "__main__":
    main()