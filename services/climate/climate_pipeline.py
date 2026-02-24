from services.climate.rainfall import get_rainfall_score
from services.climate.drought import get_drought_risk
from services.climate.soil import get_soil_health_score


def build_climate_profile(user_input):
    """
    Combines climate indicators into one score.
    Add‑on only — does NOT affect current system.
    """

    location = user_input.get("location")

    rainfall = get_rainfall_score(location)
    drought = get_drought_risk(location)
    soil = get_soil_health_score(location)

    climate_score = {
        "rainfall_score": rainfall,
        "drought_risk": drought,
        "soil_score": soil,
        "overall_climate_risk": (rainfall + soil - drought) / 2
    }

    return climate_score