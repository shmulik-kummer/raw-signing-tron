import json

from main import unfreeze_balance_transaction, sign_transaction, apply_signature_to_transaction, \
    send_signed_transaction_to_tron
from config import RESOURCE,SOURCE_VAULT_ACCOUNT_ID,FROZEN_BALANCE,OWNER_ADDRESS

unfreeze_balance_txn = unfreeze_balance_transaction(OWNER_ADDRESS, FROZEN_BALANCE, RESOURCE)

# Convert the transaction to JSON for signing
tron_transaction_details = unfreeze_balance_txn.to_json()
print("Freeze Balance Transaction Details:", json.dumps(tron_transaction_details, indent=4))

# Sign the transaction using Fireblocks
signature, content = sign_transaction(SOURCE_VAULT_ACCOUNT_ID, tron_transaction_details)

if signature and content:
    # Apply the signature to the transaction
    signed_transaction = apply_signature_to_transaction(unfreeze_balance_txn, signature)
    print(signed_transaction.to_json())

    # Send the signed transaction to Tron
    response = send_signed_transaction_to_tron(signed_transaction)
    print("Response from Tron Network:\n\n", json.dumps(response, indent=4))
