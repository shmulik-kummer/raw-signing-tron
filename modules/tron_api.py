from tronpy import Tron
from tronpy.exceptions import AddressNotFound, UnknownError
from tronpy.keys import to_hex_address
from tronpy.tron import Transaction
from typing import List, Tuple
from logging_config import logger


def broadcast_transaction(tron_client: Tron, signed_transaction):
    """
    Broadcast a signed transaction to the Tron network.

    :param tron_client: An instance of the Tron client.
    :param signed_transaction: The signed transaction to broadcast.
    :return: The result of the broadcast operation or an error message.
    """
    try:
        result = tron_client.broadcast(signed_transaction)
        logger.info(f"Tron Broadcast transaction result: {result}")
        return result
    except UnknownError as e:
        error_message, error_code = e.args
        logger.error(f"Error broadcasting transaction: {error_message} (Code: {error_code})")
        return {
            "status": "error",
            "message": error_message,
            "code": error_code
        }
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {
            "status": "error",
            "message": str(e),
            "code": "UNKNOWN_ERROR"
        }


def unfreeze_balance_transaction(tron_client: Tron, owner_address: str, frozen_balance: int,
                                 resource: str) -> Transaction:
    """
    Create an unfreeze balance transaction.

    :param tron_client: An instance of the Tron client.
    :param owner_address: The address of the owner.
    :param frozen_balance: The amount of balance to unfreeze.
    :param resource: The type of resource (e.g., "BANDWIDTH", "ENERGY").
    :return: The built unfreeze balance transaction.
    :raises Exception: If an error occurs during the transaction creation.
    """
    try:
        unfreeze_balance_txn = tron_client.trx.unfreeze_balance(
            owner=owner_address,
            unfreeze_balance=frozen_balance,
            resource=resource,
        ).build()
        logger.info(f"Unfreeze balance transaction: {unfreeze_balance_txn}")
        return unfreeze_balance_txn
    except Exception as e:
        logger.error(f"Failed to create unfreeze balance transaction: {e}")
        raise


def freeze_balance_transaction(tron_client: Tron, owner_address: str, frozen_balance: int,
                               resource: str) -> Transaction:
    """
    Create a freeze balance transaction.

    :param tron_client: An instance of the Tron client.
    :param owner_address: The address of the owner.
    :param frozen_balance: The amount of balance to freeze.
    :param resource: The type of resource (e.g., "BANDWIDTH", "ENERGY").
    :return: The built freeze balance transaction.
    :raises Exception: If an error occurs during the transaction creation.
    """
    try:
        freeze_balance_txn = tron_client.trx.freeze_balance(
            owner=owner_address,
            amount=frozen_balance,
            resource=resource,
        ).build()
        logger.info(f"Freeze balance transaction: {freeze_balance_txn}")
        return freeze_balance_txn
    except Exception as e:
        logger.error(f"Failed to create freeze balance transaction: {e}")
        raise


def vote_for_witnesses(tron_client: Tron, owner_address: str, votes: List[Tuple[str, int]]) -> Transaction:
    """
    Create a vote for witnesses transaction.

    :param tron_client: An instance of the Tron client.
    :param owner_address: The address of the voter (also the owner address).
    :param votes: A list of tuples containing the witness address and the vote count.
    :return: The built vote for witnesses transaction.
    :raises Exception: If an error occurs during the transaction creation.
    """
    try:
        formatted_votes = [(to_hex_address(addr), count) for addr, count in votes]
        transaction_builder = tron_client.trx.vote_witness(owner_address, *formatted_votes)
        transaction = transaction_builder.build()
        logger.info(f"Vote for witnesses transaction: {transaction}")
        return transaction
    except Exception as e:
        logger.error(f"Failed to create vote for witnesses transaction: {e}")
        raise


import json


def get_account_details(tron_client: Tron, address: str) -> dict:
    """
    Get account details from the Tron blockchain.

    :param tron_client: An instance of the Tron client.
    :param address: The address of the account.
    :return: The account details as a dictionary.
    :raises AddressNotFound: If the address is not found on the Tron blockchain.
    :raises Exception: If an error occurs during the account retrieval.
    """
    try:
        account_info = tron_client.get_account(address)
        pretty_account_info = json.dumps(account_info, indent=4)
        logger.info(f"Account details for {address}:\n{pretty_account_info}")
        return account_info
    except AddressNotFound:
        logger.error("Address not found")
        return {"error": "Address not found"}
    except Exception as e:
        logger.error(f"Failed to get account details: {e}")
        raise


def withdraw_balance(tron_client: Tron, owner_address: str) -> Transaction:
    """
    Create a withdraw balance transaction to withdraw rewards from the Tron network.

    :param tron_client: An instance of the Tron client.
    :param owner_address: The address of the owner.
    :return: The built withdraw balance transaction.
    :raises Exception: If an error occurs during the transaction creation.
    """
    try:
        txn = tron_client.trx.withdraw_rewards(owner_address).build()
        logger.info(f"Withdraw balance transaction: {txn}")
        return txn
    except Exception as e:
        logger.error(f"Failed to create withdraw balance transaction: {e}")
        raise
