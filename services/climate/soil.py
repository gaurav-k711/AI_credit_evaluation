def get_soil_health_score(location):
    """
    Soil productivity indicator.
    """
    if not location:
        return 60
    return 72