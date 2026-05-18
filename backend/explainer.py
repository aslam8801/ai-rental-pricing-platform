def generate_explanation(property):

    explanations = []

    if property["school_score"] > 8:
        explanations.append(
            "High school quality increased rent."
        )

    if property["flood_risk"] > 7:
        explanations.append(
            "Flood-prone area reduced valuation."
        )

    if property["amenities_score"] > 50:
        explanations.append(
            "Strong nearby amenities improved pricing."
        )

    return explanations