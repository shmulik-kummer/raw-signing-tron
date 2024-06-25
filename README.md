# Raw Signing for Tron Transactions

This repository provides a library for raw signing of Tron transactions using the Fireblocks SDK. It includes functionality to create and sign transactions, as well as to apply signatures to transactions on the Tron network.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Initializing the Clients](#initializing-the-clients)
  - [Signing a Transaction](#signing-a-transaction)
  - [Broadcasting a Transaction](#broadcasting-a-transaction)
  - [Freezing Balance](#freezing-balance)
  - [Unfreezing Balance](#unfreezing-balance)
  - [Voting for Witnesses](#voting-for-witnesses)
  - [Getting Account Details](#getting-account-details)
  - [Withdrawing Balance](#withdrawing-balance)
  - [Applying a Signature to a Transaction](#applying-a-signature-to-a-transaction)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use this library, you need to have Python installed. You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Folder Structure

```
├── modules
│   ├── fireblocks_api.py
│   ├── tron_api.py
│   ├── transaction_utils.py
├── .gitignore
├── README.md
├── config_template.py
├── logging_config.py

```
* **modules**: Contains the core functionality for interacting with the Fireblocks and Tron APIs.
  * **Fireblocks_api.py**: Functions for creating and signing transactions using the Fireblocks API.
  * **tron_api.py**: Functions for interacting with the Tron network.
  * **transaction_utils.py****: Utility functions for handling transactions.	
* **config_template.py**: Template configuration file for setting up your API keys and network details.
* **logging_config.py**: Configuration for logging.

## Configuration
You can Create a configuration file named config.py based on the config_template.py provided in the repository. Fill in your Fireblocks API credentials and Tron network details.
Rename the file to config.py (as required in the code)

```
ASSET_ID = 'TRX asset id' (TRX / TRX_TEST)
FIREBLOCKS_API_KEY = 'your_fireblocks_api_key'
API_SECRET = 'your_api_secret'
TRON_NETWORK = 'mainnet' / 'nile' /'shasta'
```

## Usage
1. **Client initialization** - Initialize the Tron and fireblocks clients
* **Tron** - Tronpy python module
* **Fireblocks** - official Fireblocks python SDK

```
from fireblocks_sdk import FireblocksSDK
from tronpy import Tron
from config import FIREBLOCKS_API_KEY, API_SECRET, TRON_NETWORK

# Initialize Fireblocks client
fireblocks_client = FireblocksSDK(private_key=API_SECRET, api_key=FIREBLOCKS_API_KEY)

# Initialize Tron client
tron_client = Tron(network=TRON_NETWORK)

```
1. Tron API wrapper functions
   * freeze_balance_transaction 
   * unfreeze_balance_transaction 
   * vote_for_witnesses 
   * get_account_details 
   * withdraw_balance
   

2. **Raw sign a transaction** - to sign a Tron transaction using the Fireblocks API, you can use the _sign_transaction_ function. 
    the function will return the signature from Fireblocks.


3. **Apply a signature to tron transaction** - Before broadcasting the transaction to Tron, the signature needs to be added to Tron transaction object.
  use the _apply_signature_to_transaction_ for this purpose.


4. **Broadcast a signed transaction** - use the broadcast_transaction function






