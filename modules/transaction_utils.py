from logging_config import logger


def apply_signature_to_transaction(tron_txn, signature):
    """
    Apply a signature to a Tron transaction.

    :param tron_txn: The Tron transaction to which the signature will be applied.
    :param signature: The signature to apply, expected to contain 'r', 's', and 'v' components.
    :return: The Tron transaction with the applied signature.
    :raises ValueError: If the signature is missing required components or if an error occurs while applying the signature.
    """
    try:
        if not all(k in signature for k in ('r', 's', 'v')):
            raise ValueError("Signature must contain 'r', 's', and 'v' components.")

        r = signature['r']
        s = signature['s']
        v = 27 + signature['v']  # Assuming v is 0 or 1 directly
        combined_signature = "0x" + r + s + hex(v)[2:]

        # Apply the signature to the transaction
        tron_txn.set_signature([combined_signature])

        logger.info(f"Signature applied to transaction: {tron_txn}")
        return tron_txn
    except Exception as e:
        logger.error(f"An error occurred while applying the signature to the transaction: {e}")
        raise
