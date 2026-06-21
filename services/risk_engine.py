def calculate_risk_level(probability):
    """
    Convert probability (0-100)
    into risk categories.
    """

    if probability < 20:
        return "SAFE"

    elif probability < 50:
        return "SUSPICIOUS"

    elif probability < 80:
        return "HIGH RISK"

    else:
        return "CRITICAL"


def get_recommendation(risk_level):
    """
    Return recommendation text
    """

    recommendations = {
        "SAFE": "Transaction appears normal.",
        "SUSPICIOUS": "Monitor transaction activity.",
        "HIGH RISK": "Manual verification recommended.",
        "CRITICAL": "Immediate fraud investigation required."
    }

    return recommendations.get(
        risk_level,
        "No recommendation available."
    )