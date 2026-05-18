def calculate_final_rent(comparables):

    if not comparables:
        return 0

    rents = [p["rent"] for p in comparables]

    avg_rent = sum(rents) / len(rents)

    return round(avg_rent, 2)