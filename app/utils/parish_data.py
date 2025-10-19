JAMAICA_PARISHES = {
    "kingston": {"lat": 17.9714, "lon": -76.7931},
    "st_andrew": {"lat": 18.0179, "lon": -76.8099},
    "st_thomas": {"lat": 17.9811, "lon": -76.3625},
    "portland": {"lat": 18.1080, "lon": -76.4598},
    "st_mary": {"lat": 18.3686, "lon": -76.9568},
    "st_ann": {"lat": 18.4386, "lon": -77.2006},
    "trelawny": {"lat": 18.3532, "lon": -77.6114},
    "st_james": {"lat": 18.4762, "lon": -77.9189},
    "hanover": {"lat": 18.4107, "lon": -78.1336},
    "westmoreland": {"lat": 18.2515, "lon": -78.1360},
    "st_elizabeth": {"lat": 17.9979, "lon": -77.7505},
    "manchester": {"lat": 18.0407, "lon": -77.5082},
    "clarendon": {"lat": 17.9590, "lon": -77.2386},
    "st_catherine": {"lat": 18.0027, "lon": -77.0000}
}

def get_parish_coordinates(parish_name: str):
    return JAMAICA_PARISHES.get(parish_name.lower().replace(" ", "_"))

def calculate_distance(lat1, lon1, lat2, lon2):
    from geopy.distance import geodesic
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers