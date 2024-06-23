import json
import main
import modules.fireblocks_api
import modules.transaction_utils
import modules.tron_api
from config import OWNER_ADDRESS, SOURCE_VAULT_ACCOUNT_ID

# Convert the transaction to JSON for signing
withdraw_balance = main.withdraw_balance(OWNER_ADDRESS)
withdraw_balance_json = withdraw_balance.to_json()
print("Freeze Balance Transaction Details:\n", json.dumps(withdraw_balance_json, indent=4))

# Sign the transaction using Fireblocks
signature, content = modules.fireblocks_api.sign_transaction(SOURCE_VAULT_ACCOUNT_ID, withdraw_balance_json)

if signature and content:
    # Apply the signature to the transaction
    signed_transaction = modules.transaction_utils.apply_signature_to_transaction(withdraw_balance, signature)
    print(signed_transaction)

    # Send the signed transaction to Tron
    response = modules.tron_api.broadcast_transaction_to_tron(signed_transaction)
    print("Response from Tron Network:\n\n", json.dumps(response, indent=4))
