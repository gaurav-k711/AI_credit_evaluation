def get_crop_yield_score(crop_type):
    """
    Agriculture stability indicator.
    """
    stable_crops = ["wheat", "rice", "cotton"]

    if crop_type.lower() in stable_crops:
        return 75
    return 55