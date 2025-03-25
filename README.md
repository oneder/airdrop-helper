# Airdrop Helper

This program can be used to streamline the process of generating token airdrop data needed for executing airdrops to asset holders through SafeWallet's CSV Airdrop app. The user will provide a CSV file containing a snapshot of asset holders' data (holder addresses and quantity of the asset held) into the configured 'Snapshots' folder.

When running the program, it will prompt the user for the required information needed to output a valid asset tranfer CSV file, and then generate the file into the configured 'Output' folder. Once the airdrop CSV file has been created, the user can then import that into SafeWallet's CSV Airdrop app and submit the airdrop transaction.

Currently, this program supports generating data for airdropping a single asset to a list of holders, holding a valid, qualifying asset.

# CSV Formatting

A given airdrop cares about two CSV files:

* Snapshot (live in the /Snapshots folder)
* Airdrop (live in the /Output folder)

**Snapshot CSV**

This is the "input" data. This file contains the addresses holding an asset that qualifies for a given airdrop, and the respective quantity of the asset the wallets are holding.

Use a tool such as SignorCrypto's [NFT Snapshot Tool](https://www.signorcrypto.com/toolkit/snapshot) to export a CSV of holder address in a valid format - just provide the network and contract address for the asset that qualifies for the airdrop.

Format of a snapshot CSV file:
```
address,quantity
0xeD6Ea230d9DAaa02F6D7F16A78C5e5c5B37CbBb4,37
0x409BB0a45Bd756F409D4ea774C918f8eEAa9b25f,15
0xddeF3dca5B27622e53Bad51569db8f3F72EDd1F8,9
0x9C12F7B02D9e9EC8dCD8Fb3A015A57446d7Af3a7,4
0xED1a47989427e22dBaB7b2ec06A769D49168d21F,3
0xdaB60eE75171B84F71Bf2Fb9B2D2E77aED814616,2
0x03ed7584E01d7e9014F0b6C9f241d89761eAC19A,1
0x069C5BB4dA9eAD8f823852d2F5df3F057a86e359,1
```

**Airdrop CSV**

This is the "output" data. This file contains the data pertaining to the airdrop, itself, and will be output in a format that is compatible with [SafeWallet](https://app.safe.global/welcome)'s CSV Airdrop app. This file will be generated based on user input information and contents of the specified snapshot CSV file associated with the airdrop.

Format of an airdrop CSV file:
```
token_type,token_address,receiver,amount
erc20,0xB631937b9E75A66291E7570E8Ed3Db10Eb43A888,0xeD6Ea230d9DAaa02F6D7F16A78C5e5c5B37CbBb4,1000
erc20,0xB631937b9E75A66291E7570E8Ed3Db10Eb43A888,0x409BB0a45Bd756F409D4ea774C918f8eEAa9b25f,1000
erc20,0xB631937b9E75A66291E7570E8Ed3Db10Eb43A888,0xddeF3dca5B27622e53Bad51569db8f3F72EDd1F8,1000
erc20,0xB631937b9E75A66291E7570E8Ed3Db10Eb43A888,0x9C12F7B02D9e9EC8dCD8Fb3A015A57446d7Af3a7,1000
erc20,0xB631937b9E75A66291E7570E8Ed3Db10Eb43A888,0xED1a47989427e22dBaB7b2ec06A769D49168d21F,1000
erc20,0xB631937b9E75A66291E7570E8Ed3Db10Eb43A888,0xdaB60eE75171B84F71Bf2Fb9B2D2E77aED814616,1000
erc20,0xB631937b9E75A66291E7570E8Ed3Db10Eb43A888,0x03ed7584E01d7e9014F0b6C9f241d89761eAC19A,1000
erc20,0xB631937b9E75A66291E7570E8Ed3Db10Eb43A888,0x069C5BB4dA9eAD8f823852d2F5df3F057a86e359,1000
```

# Running the Program

Follow these steps to set up and run the program on your local machine:

### **1. Verify Python is Installed**
Ensure you have **Python 3.8+** installed. You can check by running:

```sh
python --version
```

If you don’t have Python installed, [download it here](https://www.python.org/downloads/) and install it before proceeding.

### **2. Clone the Repository**

If you haven’t already cloned the repository, run:

```
git clone https://github.com/oneder/airdrop-helper
cd YOUR-REPO-NAME
```

### **3. Set Up a Virtual Environment**

Create and activate a virtual environment using [venv](https://docs.python.org/3/library/venv.html):

```
python -m venv \path\to\new\virtual\environment

# Windows Command Prompt
\path\to\new\virtual\environment\Scripts\activate.bat 

# Windows Powershell
\path\to\new\virtual\environment\Scripts\Activate.ps1

# Mac/Linux
source \path\to\new\virtual\environment\bin\activate
```

### **4. Install Dependencies**

Run the following command to install all required dependencies:

```
pip install -r requirements.txt
```

### **5. Set Up Environment Variables**

Create a .env file in the root project directory and add the required configuration (see env.example):

```
SNAPSHOTS_FOLDER= # path to folder containing snapshot .csv files
OUTPUT_FOLDER= # path for where to generate the SafeWallet airdrop .csv files
```

### **6. Add Snapshot CSV File to Snapshots Folder**

Add a CSV file containing the holder data to the *Snapshots* folder (see **`CSV Formating`** section above).

### **7. Run the Program**

Run the Python script:
```
python generate_from_snapshot.py
```

Once the program is running, the user will provide the name of a snapshot CSV of qualifying asset holders, type of ERC token holders will receive from the airdrop, the token address of the asset being airdropped, the base amount of tokens for the airdrop, and whether or not the airdrop amount if *per NFT* or *per holder*.

The program will then output an airdrop CSV file to the *Output* folder, which can be imported into SafeWallet's CSV Airdrop app and used to execute the airdrop.
