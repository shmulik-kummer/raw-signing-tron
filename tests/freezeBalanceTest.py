from fireblocks_sdk import FireblocksSDK
from tronpy import Tron

import config
from config import RESOURCE, SOURCE_VAULT_ACCOUNT_ID, FROZEN_BALANCE, OWNER_ADDRESS
from modules import tron_api
from modules.fireblocks_api import sign_transaction
from modules.transaction_utils import apply_signature_to_transaction
from modules.tron_api import broadcast_transaction

tron_client = Tron(network=config.TRON_NETWORK)
fireblocks_client = FireblocksSDK(private_key=config.API_SECRET, api_key=config.FIREBLOCKS_API_KEY)

freeze_balance_txn = tron_api.freeze_balance_transaction(tron_client, OWNER_ADDRESS, FROZEN_BALANCE, RESOURCE)

# Convert the transaction to JSON for signing
tron_transaction_details = freeze_balance_txn.to_json()
# print("Freeze Balance Transaction Details:", json.dumps(tron_transaction_details, indent=4))

# Sign the transaction using Fireblocks
signature, content = sign_transaction(fireblocks_client, SOURCE_VAULT_ACCOUNT_ID, tron_transaction_details)

if signature and content:
    # Apply the signature to the transaction
    signed_transaction = apply_signature_to_transaction(freeze_balance_txn, signature)
    # print("Signed transaction from Fireblocks:\n\n", signed_transaction)

    # Send the signed transaction to Tron
    response = broadcast_transaction(tron_client, signed_transaction)
    # print("Response from Tron Network:\n", json.dumps(response, indent=4))
