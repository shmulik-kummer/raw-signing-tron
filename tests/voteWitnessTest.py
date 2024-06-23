# Create vote witness
from fireblocks_sdk import FireblocksSDK
from tronpy import Tron

import config
from config import OWNER_ADDRESS, SR_ADDRESS, SOURCE_VAULT_ACCOUNT_ID, FIREBLOCKS_API_KEY, API_SECRET
from modules.tron_api import vote_for_witnesses
from modules.transaction_utils import apply_signature_to_transaction
from modules.tron_api import broadcast_transaction
from modules.fireblocks_api import sign_transaction

fireblocks_client = FireblocksSDK(private_key=API_SECRET, api_key=FIREBLOCKS_API_KEY)
tron_client = Tron(network=config.TRON_NETWORK)

owner_address = OWNER_ADDRESS
votes = [(SR_ADDRESS, 10)]
vote_transaction = vote_for_witnesses(tron_client, OWNER_ADDRESS, votes)
vote_transaction_json = vote_transaction.to_json()

signature, content = sign_transaction(fireblocks_client,SOURCE_VAULT_ACCOUNT_ID, vote_transaction_json)
if signature and content:
    # # Apply the signature to the transaction
    signed_transaction = apply_signature_to_transaction(vote_transaction, signature)
    print(signed_transaction.to_json())

    # Send the signed transaction to Tron
    response = broadcast_transaction(tron_client, signed_transaction)
    print("Response from Tron Network:", response)
