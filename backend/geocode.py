from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="rental-ai")

def get_coordinates(location):

    location_data = geolocator.geocode(location)

    if not location_data:
        return None

    return {
        "latitude": location_data.latitude,
        "longitude": location_data.longitude
    }


if __name__ == "__main__":

    result = get_coordinates("Mumbai Bandra")

    print(result)