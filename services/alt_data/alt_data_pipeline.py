from services.alt_data.mobile_data import get_mobile_score
from services.alt_data.upi_data import get_upi_score
from services.alt_data.crop_data import get_crop_yield_score
from services.alt_data.satellite_data import get_satellite_health_score


def build_alt_data_profile(user_input):
    """
    Combines all alternative data sources into one structured output.
    This will later be used by:
    - risk engine
    - ML prediction
    - recommendation system

    CURRENT SYSTEM REMAINS UNCHANGED.
    """

    phone = user_input.get("phone")
    upi = user_input.get("upi_id")
    crop = user_input.get("crop_type")
    location = user_input.get("location")

    mobile_score = get_mobile_score(phone)
    upi_score = get_upi_score(upi)
    crop_score = get_crop_yield_score(crop)
    satellite_score = get_satellite_health_score(location)

    alt_profile = {
        "mobile_score": mobile_score,
        "upi_score": upi_score,
        "crop_score": crop_score,
        "satellite_score": satellite_score,
        "alt_data_confidence": (
            mobile_score + upi_score + crop_score + satellite_score
        ) / 4
    }

    return alt_profile