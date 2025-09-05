import sys
import pandas as pd 

def summarize_airdrop(file_path, airdrop_name):
    # load
    data = pd.read_csv(file_path)

    # build summary
    summary = {
        "token_type": data["token_type"].iloc[0],
        "token_address": data["token_address"].iloc[0],
        "total_receivers": data["receiver"].nunique(),
        "total_tokens_airdropped": data["amount"].sum(),
        "min_tokens_airdropped": data["amount"].min(),
        "max_tokens_airdropped": data["amount"].max(),
        "average_tokens_per_receiver": data.groupby("receiver")["amount"].sum().mean(),
    }   

    # print
    print(f"\nAirdrop Summary: {airdrop_name}")
    print("-" * 30)
    for key, value in summary.items():
        clean_key = key.replace('_', ' ').title()
        if isinstance(value, float):
            print(f"{clean_key}: {value:,.3f}")
        else:            
            print(f"{clean_key}: {value}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <airdrop_file.csv>")
    else:
        airdrop_name = input("Enter the name of this airdrop: ")
        summarize_airdrop(sys.argv[1], airdrop_name)