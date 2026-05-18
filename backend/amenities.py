import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def nearby_amenities(lat, lon):

    query = f"""
    [out:json];
    (
      node(around:2000,{lat},{lon})["amenity"];
    );
    out;
    """

    response = requests.get(
        OVERPASS_URL,
        params={"data": query}
    )

    data = response.json()

    return len(data["elements"])


if __name__ == "__main__":

    print(
        nearby_amenities(19.0760, 72.8777)
    )