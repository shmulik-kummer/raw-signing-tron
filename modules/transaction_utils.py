def apply_signature_to_transaction(tron_txn, signature):
    r = signature['r']
    s = signature['s']
    v = 27 + signature['v']  # Assuming v is 0 or 1 directly
    combined_signature = "0x" + r + s + hex(v)[2:]

    # Apply the signature to the transaction
    tron_txn.set_signature([combined_signature])

    return tron_txn
