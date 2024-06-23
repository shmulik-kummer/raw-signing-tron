from typing import List, Tuple
from tronpy.exceptions import AddressNotFound, UnknownError
from tronpy.keys import to_hex_address
from tronpy.tron import Transaction, Tron

from config import TRON_NETWORK
from logging_config import logger

tron_client = Tron(network=TRON_NETWORK)


def unfreeze_balance_transaction(owner_address, frozen_balance, resource):
    unfreeze_balance_txn = tron_client.trx.unfreeze_balance(
        owner=owner_address,
        unfreeze_balance=frozen_balance,
        resource=resource,
    ).build()
    return unfreeze_balance_txn


def freeze_balance_transaction(owner_address, frozen_balance, resource):
    freeze_balance_txn = tron_client.trx.freeze_balance(
        owner=owner_address,
        amount=frozen_balance,
        resource=resource,
    ).build()
    return freeze_balance_txn


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
    transaction_builder = tron_client.trx.vote_witness(owner_address, *formatted_votes)

    # Build the transaction
    transaction = transaction_builder.build()

    logger.info(f"Vote details: {transaction}")

    # Return the transaction details
    return transaction


def get_account_details(address: str) -> dict:
    """
    Get account details from the Tron blockchain.

    :param address: The address of the account    :return:  details as a dictionary
    """
    try:
        # Get account details
        account_info = tron_client.get_account(address)
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
    txn = tron_client.trx.withdraw_rewards(owner_address).build()

    return txn


def broadcast_transaction_to_tron(signed_transaction):
    try:
        # Broadcast the transaction using the tronpy client
        result = tron_client.broadcast(signed_transaction)
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
