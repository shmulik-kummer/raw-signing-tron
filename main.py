import json
from time import sleep
from typing import List, Tuple
from fireblocks_sdk import TransferPeerPath, FireblocksSDK, RawMessage, UnsignedMessage, VAULT_ACCOUNT, \
    TRANSACTION_STATUS_COMPLETED, TRANSACTION_STATUS_FAILED, TRANSACTION_STATUS_BLOCKED
from tronpy import Tron
from tronpy.exceptions import AddressNotFound, UnknownError
from tronpy.keys import to_hex_address
from tronpy.tron import Transaction
import config_template
from config_template import ASSET_ID, API_SECRET, FIREBLOCKS_API_KEY

client = Tron(network=config_template.TRON_NETWORK)

# Initialize Fireblocks SDK
fireblocks = FireblocksSDK(private_key=API_SECRET, api_key=FIREBLOCKS_API_KEY)


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
        print(f"Tx {tx_id} is not completed yet. Status: {tx_status}")
        tx_info = fireblocks.get_transaction_by_id(tx_id)
        tx_status = tx_info["status"]
        sleep(2)

    # If successfully completed - get the signature and return it
    if tx_status == TRANSACTION_STATUS_COMPLETED:
        sig = tx_info["signedMessages"][0]["signature"]
        pretty_signature = json.dumps(sig, indent=4)
        # print(f"Signature: {pretty_signature}")
        return sig, tx_id  # Return the signature and the transaction hash

    # Else - failed
    print("Transaction Failed")
    return None


def send_signed_transaction_to_tron(signed_transaction):
    try:
        # Broadcast the transaction using the tronpy client
        result = client.broadcast(signed_transaction)
        return result
    except UnknownError as e:
        error_message, error_code = e.args
        if error_code == 'BANDWITH_ERROR':
            return {
                "status": "error",
                "message": error_message,
                "code": error_code
            }
        else:
            raise e


def apply_signature_to_transaction(tron_txn, signature):
    r = signature['r']
    s = signature['s']
    v = 27 + signature['v']  # Assuming v is 0 or 1 directly
    combined_signature = "0x" + r + s + hex(v)[2:]

    # Apply the signature to the transaction
    tron_txn.set_signature([combined_signature])

    return tron_txn


def unfreeze_balance_transaction(owner_address, frozen_balance, resource):
    unfreeze_balance_txn = client.trx.unfreeze_balance(
        owner=owner_address,
        unfreeze_balance=frozen_balance,
        resource=resource,
    ).build()
    return unfreeze_balance_txn


def freeze_balance_transaction(owner_address, frozen_balance, resource):
    freeze_balance_txn = client.trx.freeze_balance(
        owner=owner_address,
        amount=frozen_balance,
        resource=resource,
    ).build()
    return freeze_balance_txn


def create_raw_signin(asset_id, tx_id, bip44_address_index, vault_account, vault_id,
                      transaction_json):
    tx_response = fireblocks.create_raw_transaction(
        asset_id=asset_id,
        raw_message=RawMessage(
            [UnsignedMessage(content=tx_id, bip44addressIndex=bip44_address_index)]
        ),
        source=TransferPeerPath(vault_account, vault_id),
        note=f"TRX Transaction: {transaction_json}",
    )
    return tx_response


def vote_for_witnesses(owner_address: str, votes: List[Tuple[str, int]]) -> Transaction:
    """
    Wrapper function to vote for witnesses.

    :param owner_address: The voter address (also the owner address)
    :param votes: A list of tuples containing the witness address and the vote count
    :return: The transaction details as a dictionary
    """
    # Convert votes to the required format
    formatted_votes = [(to_hex_address(addr), count) for addr, count in votes]

    # Create the transaction
    transaction_builder = client.trx.vote_witness(owner_address, *formatted_votes)

    # Build the transaction
    transaction = transaction_builder.build()

    print(f"Vote details: {transaction}")

    # Return the transaction details
    return transaction


def get_account_details(address: str) -> dict:
    """
    Get account details from the Tron blockchain.

    :param address: The address of the account    :return:  details as a dictionary
    """
    try:
        # Get account details
        account_info = client.get_account(address)
        return account_info
    except AddressNotFound:
        return {"error": "Address not found"}


def withdraw_balance(owner_address: str) -> Transaction:
    """
    Withdraw balance (rewards) from the Tron network.

    :param owner_address:
    :return: The transaction result as a dictionary
    """

    # Create the withdrawal transaction
    txn = client.trx.withdraw_rewards(owner_address).build()

    return txn
