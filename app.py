import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pressure Altitude Calculator", layout="centered")
st.title("🛬 Pressure Altitude Calculator")

# Load airport data from local CSV file
@st.cache_data
def load_airport_data():
    return pd.read_csv("airports.csv")

airport_data = load_airport_data()

# Get elevation and name based on ICAO
def get_airport_info(icao_code):
    result = airport_data[airport_data['ident'] == icao_code.upper()]
    if not result.empty:
        elevation = result.iloc[0]['elevation_ft']
        name = result.iloc[0]['name']
        if pd.notna(elevation):
            return float(elevation), name
    return None, None

# Pressure altitude formula
def calculate_pressure_altitude(elevation_ft, qnh_hpa):
    return elevation_ft + (1013.25 - qnh_hpa) * 30

# UI Inputs
icao = st.text_input("Enter ICAO Code (e.g., EDDF, KJFK)").upper()
qnh = st.number_input("Enter QNH (hPa)", min_value=800.0, max_value=1100.0, value=1013.25, step=0.01)

# Calculate button
if st.button("Calculate Pressure Altitude"):
    elevation, airport_name = get_airport_info(icao)
    if elevation is not None:
        pressure_altitude = calculate_pressure_altitude(elevation, qnh)
        st.success(
            f"📍 **{airport_name}** ({icao})\n\n"
            f"🗻 Elevation: {elevation:.0f} ft\n\n"
            f"🧮 Pressure Altitude: **{round(pressure_altitude)} ft**"
        )
    else:
        st.error("❌ Elevation not found for that ICAO code.")
