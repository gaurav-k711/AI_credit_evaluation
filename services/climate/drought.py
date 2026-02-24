def get_drought_risk(location):
    """
    Higher value = higher drought risk.
    """
    drought_prone = ["Rajasthan", "Vidarbha"]

    if location in drought_prone:
        return 80
    return 40