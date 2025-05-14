import requests

def fetch_metar(icao_code, api_key):
    url = f"https://avwx.rest/api/metar/{icao_code}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    qnh_hpa = float(data['altimeter']['value'])  # in hPa
    return qnh_hpa

def fetch_airfield_elevation(icao_code):
    # Example: Static lookup or via OurAirports CSV or another database/API
    airport_data = {
        "EGLL": 83,  # Elevation in feet
        "KJFK": 13,
        "EDDF": 364
    }
    return airport_data.get(icao_code.upper())

def calculate_pressure_altitude(elevation_ft, qnh_hpa):
    return elevation_ft + (1013.25 - qnh_hpa) * 30

# Example usage
icao = "EGLL"
api_key = "your_avwx_api_key"
elevation = fetch_airfield_elevation(icao)
qnh = fetch_metar(icao, api_key)
pressure_altitude = calculate_pressure_altitude(elevation, qnh)

print(f"Pressure altitude at {icao}: {round(pressure_altitude)} ft")
