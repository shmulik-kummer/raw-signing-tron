import json
from time import sleep
from fireblocks_sdk import VAULT_ACCOUNT, TRANSACTION_STATUS_COMPLETED, TRANSACTION_STATUS_FAILED, \
    TRANSACTION_STATUS_BLOCKED, RawMessage, UnsignedMessage, TransferPeerPath, FireblocksSDK
from config import ASSET_ID
from logging_config import logger


def sign_transaction(fireblocks_client: FireblocksSDK, vault_id: str, trx_transaction: dict,
                     bip44_address_index: int = 0):
    """
    Sign a Tron transaction using the Fireblocks API.

    :param fireblocks_client: An instance of the Fireblocks client.
    :param vault_id: The ID of the Fireblocks vault to use for signing.
    :param trx_transaction: The Tron transaction to be signed.
    :param bip44_address_index: The BIP44 address index to use for signing.
    :return: The signature and transaction ID if the transaction is completed successfully, otherwise None.
    """
    try:
        transaction_json = json.dumps(trx_transaction)
        tx_id = trx_transaction['txID']

        tx_response = create_raw_signin(
            fireblocks_client=fireblocks_client,
            asset_id=ASSET_ID,
            tx_id=tx_id,
            bip44_address_index=bip44_address_index,
            vault_account=VAULT_ACCOUNT,
            vault_id=vault_id,
            transaction_json=transaction_json
        )

        # Get the transaction's status and id
        tx_status = tx_response["status"]
        tx_id = tx_response["id"]

        tx_info = None

        # Wait for the transaction to complete or to fail
        while tx_status not in {TRANSACTION_STATUS_COMPLETED, TRANSACTION_STATUS_FAILED, TRANSACTION_STATUS_BLOCKED}:
            logger.info(f"Tx {tx_id} is not completed yet. Status: {tx_status}")
            tx_info = fireblocks_client.get_transaction_by_id(tx_id)
            tx_status = tx_info["status"]
            sleep(2)

        # If successfully completed - get the signature and return it
        if tx_status == TRANSACTION_STATUS_COMPLETED:
            sig = tx_info["signedMessages"][0]["signature"]
            logger.info(f"Signature obtained for transaction {tx_id}")
            return sig, tx_id  # Return the signature and the transaction hash

        logger.error("Transaction Failed")
        return None
    except Exception as e:
        logger.error(f"An error occurred while signing the transaction: {e}")
        raise


def create_raw_signin(fireblocks_client: FireblocksSDK, asset_id: str, tx_id: str, bip44_address_index: int,
                      vault_account: str, vault_id: str, transaction_json: str):
    """
    Create a raw transaction signing request using the Fireblocks API.

    :param fireblocks_client: An instance of the Fireblocks client.
    :param asset_id: The asset ID for the transaction.
    :param tx_id: The transaction ID.
    :param bip44_address_index: The BIP44 address index to use for signing.
    :param vault_account: The vault account to use for signing.
    :param vault_id: The ID of the Fireblocks vault to use for signing.
    :param transaction_json: The transaction details in JSON format.
    :return: The response from the Fireblocks API for the raw transaction signing request.
    """
    try:
        tx_response = fireblocks_client.create_raw_transaction(
            asset_id=asset_id,
            raw_message=RawMessage(
                [UnsignedMessage(content=tx_id, bip44addressIndex=bip44_address_index)]
            ),
            source=TransferPeerPath(vault_account, vault_id),
            note=f"TRX Transaction: {transaction_json}",
        )
        logger.info(f"Created raw signing request for transaction {tx_id}")
        return tx_response
    except Exception as e:
        logger.error(f"An error occurred while creating the raw signing request: {e}")
        raise
