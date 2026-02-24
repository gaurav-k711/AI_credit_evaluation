def get_upi_score(upi_id):
    """
    Dummy financial behavior score from UPI usage.
    """
    if not upi_id:
        return 0

    return 70