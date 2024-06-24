from logging_config import logger


def manipulate_signature(signature):
    """
    Manipulate the signature to combine its components into a single string.

    :param signature: The signature to manipulate, expected to contain 'r', 's', and 'v' components.
    :return: The combined signature string.
    :raises ValueError: If the signature is missing required components.
    """
    if not all(k in signature for k in ('r', 's', 'v')):
        raise ValueError("Signature must contain 'r', 's', and 'v' components.")

    r = signature['r']
    s = signature['s']
    v = 27 + signature['v']  # Assuming v is 0 or 1 directly
    combined_signature = "0x" + r + s + hex(v)[2:]

    return combined_signature


def apply_signature_to_transaction(tron_txn, signature):
    """
    Apply a manipulated signature to a Tron transaction object.

    :param tron_txn: The Tron transaction to which the signature will be applied.
    :param signature: The signature to apply, expected to contain 'r', 's', and 'v' components.
    :return: The Tron transaction with the applied signature.
    :raises ValueError: If an error occurs while applying the signature.
    """
    try:
        combined_signature = manipulate_signature(signature)
        tron_txn.set_signature([combined_signature])

        logger.info(f"Signature applied to transaction successfully")
        return tron_txn
    except Exception as e:
        logger.error(f"An error occurred while applying the signature to the transaction: {e}")
        raise
