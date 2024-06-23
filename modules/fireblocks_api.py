import json
from time import sleep

from fireblocks_sdk import VAULT_ACCOUNT, TRANSACTION_STATUS_COMPLETED, TRANSACTION_STATUS_FAILED, \
    TRANSACTION_STATUS_BLOCKED, RawMessage, UnsignedMessage, TransferPeerPath, FireblocksSDK

from config import ASSET_ID, FIREBLOCKS_API_KEY, API_SECRET
from logging_config import logger

fireblocks_client = FireblocksSDK(private_key=API_SECRET, api_key=FIREBLOCKS_API_KEY)


def sign_transaction(vault_id: str, trx_transaction: dict, bip44_address_index: int = 0):
    transaction_json = json.dumps(trx_transaction)

    tx_id = trx_transaction['txID']

    tx_response = create_raw_signin(asset_id=ASSET_ID, tx_id=tx_id, bip44_address_index=bip44_address_index,
                                    vault_account=VAULT_ACCOUNT, vault_id=vault_id,
                                    transaction_json=transaction_json)

    # Get the transaction's status and id
    tx_status = tx_response["status"]
    tx_id = tx_response["id"]

    tx_info = None

    # Wait for the transaction to complete or to fail
    while (tx_status != TRANSACTION_STATUS_COMPLETED and tx_status != TRANSACTION_STATUS_FAILED
           and tx_status != TRANSACTION_STATUS_BLOCKED):
        logger.info(f"Tx {tx_id} is not completed yet. Status: {tx_status}")
        tx_info = fireblocks_client.get_transaction_by_id(tx_id)
        tx_status = tx_info["status"]
        sleep(2)

    # If successfully completed - get the signature and return it
    if tx_status == TRANSACTION_STATUS_COMPLETED:
        sig = tx_info["signedMessages"][0]["signature"]
        # pretty_signature = json.dumps(sig, indent=4)
        # logger.info(f"Signature: {pretty_signature}")
        return sig, tx_id  # Return the signature and the transaction hash

    logger.error("Transaction Failed")
    return None


def create_raw_signin(asset_id, tx_id, bip44_address_index, vault_account, vault_id,
                      transaction_json):
    tx_response = fireblocks_client.create_raw_transaction(
        asset_id=asset_id,
        raw_message=RawMessage(
            [UnsignedMessage(content=tx_id, bip44addressIndex=bip44_address_index)]
        ),
        source=TransferPeerPath(vault_account, vault_id),
        note=f"TRX Transaction: {transaction_json}",
    )
    return tx_response
