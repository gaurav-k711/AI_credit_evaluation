def get_rainfall_score(location):
    """
    Dummy rainfall stability score.
    Later can connect to weather API.
    """
    if not location:
        return 50
    return 70