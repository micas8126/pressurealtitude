import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pressure Altitude Calculator", layout="centered")
st.title("🛬 Pressure Altitude Calculator")

@st.cache_data
def load_airport_data():
    return pd.read_csv("airports.csv")  # Reads from local file

airport_data = load_airport_data()

def get_elevation(icao_code):
    result = airport_data[airport_data['ident'] == icao_code.upper()]
    if not result.empty and pd.notna(result.iloc[0]['elevation_ft']):
        return float(result.iloc[0]['elevation_ft'])
    return None

def calculate_pressure_altitude(elevation_ft, qnh_hpa):
    return elevation_ft + (1013.25 - qnh_hpa) * 30

icao = st.text_input("Enter ICAO Code (e.g., EDDF, KJFK)").upper()
qnh = st.number_input("Enter QNH (hPa)", min_value=800.0, max_value=1100.0, value=1013.25, step=0.01)

if st.button("Calculate Pressure Altitude"):
    elevation = get_elevation(icao)
    if elevation is not None:
        pressure_altitude = calculate_pressure_altitude(elevation, qnh)
        st.success(f"📍 Airport Elevation: {elevation:.0f} ft\n\n🧮 Pressure Altitude at {icao}: **{round(pressure_altitude)} ft**")
    else:
        st.error("❌ Elevation not found for that ICAO code.")
