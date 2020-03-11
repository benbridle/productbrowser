"""
Utility functions for validating that data conforms to a given type.
"""


def is_barcode(barcode):
    """
    Determine if the given value is a valid barcode.
    """
    if not isinstance(barcode, int):
        return False
    if barcode < 10000:
        return False
    return True


def is_sku(sku):
    if not isinstance(sku, int):
        return False
    if sku < 0:
        return False
    return True

def is_branch_id(branch_id):
    if not isinstance(branch_id, int):
        return False
    if branch_id < 1:
        return False
    return True