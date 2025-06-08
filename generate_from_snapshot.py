import csv
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get folder paths from environment variables
SNAPSHOTS_FOLDER = os.getenv("SNAPSHOTS_FOLDER")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")

if not SNAPSHOTS_FOLDER or not OUTPUT_FOLDER:
    print("Error: SNAPSHOTS_FOLDER or OUTPUT_FOLDER not set in the .env file.")
    sys.exit(1)

# Prompt user for required input
file_name = input("Enter the Holder Data file name (excluding '.csv'): ").strip()
holder_csv_path = os.path.join(SNAPSHOTS_FOLDER, f"{file_name}.csv")

if not os.path.exists(holder_csv_path):
    print(f"Error: File '{holder_csv_path}' not found. Please check the filename and try again.")
    sys.exit(1)

token_type = input("Enter the token type (e.g., 'erc20'): ").strip()
token_address = input("Enter the token contract address: ").strip()
base_airdrop_amount = int(input("Enter the base airdrop amount: ").strip())
airdrop_type = input("Is the airdrop amount per asset held (Y/N)? ").strip().lower()

# Determine if airdrop is per asset held or per Holder
is_per_asset = airdrop_type == "y"

# Process snapshot data
airdrop_data = []
total_amount_to_airdrop = 0
total_holders = 0

with open(holder_csv_path, mode="r") as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        receiver = row["address"]
        quantity = int(row["quantity"])
        amount = base_airdrop_amount * quantity if is_per_asset else base_airdrop_amount # Calculate airdrop amount
        airdrop_data.append([token_type, token_address, receiver, amount])
        
        total_amount_to_airdrop += amount
        total_holders += 1

# Define the output file path
output_csv_path = os.path.join(OUTPUT_FOLDER, f"airdrop_{file_name}.csv")

# Write to output CSV
with open(output_csv_path, mode="w", newline="") as outfile:
    writer = csv.writer(outfile, lineterminator="\n")
    writer.writerow(["token_type", "token_address", "receiver", "amount"])  # Header
    #writer.writerows(airdrop_data)

    # Manually write rows to ensure no trailing newline
    for i, row in enumerate(airdrop_data):
        if i < len(airdrop_data) - 1:
            writer.writerow(row)
        else:
            outfile.write(",".join(map(str, row)))  # Write last row manually to avoid extra newline

print(f"Airdrop CSV '{output_csv_path}' generated successfully!")
print(f"Total Amount to Airdrop: {total_amount_to_airdrop} tokens across {total_holders} holders.")
