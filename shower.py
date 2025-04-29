import streamlit as st
import numpy as np

# Page Setup
st.set_page_config(page_title="Shower Model", layout="centered")
st.title("🚿 Shower Performance Model")
st.markdown("---")

# Input Fields
st.subheader("Enter Parameters:")
temp = st.number_input("Water Temperature (°C)", value=40.0, format="%.1f")
pressure = st.number_input("Water Pressure (bar)", value=3.0, format="%.1f")
nozzle_dia = st.number_input("Nozzle Diameter (mm)", value=1.2, format="%.2f")
num_nozzles = st.number_input("Number of Nozzles", value=50, step=1)
air_temp = st.number_input("Ambient Air Temperature (°C)", value=25.0, format="%.1f")

# Button
if st.button("💧 Calculate Final Outlet Temperature"):

    # Constants
    rho = 997  # kg/m³
    h_fg = 2257000  # J/kg
    sigma = 5.67e-8  # W/m²K⁴
    emissivity = 0.95
    Cp_water = 4182  # J/kg·K
    rel_humidity = 0.5  # Moderate humidity

    # Unit Conversions
    P = pressure * 1e5  # bar to Pa
    d_nozzle = nozzle_dia / 1000  # mm to m
    T_w = temp
    T_air = air_temp

    # Flow Rate
    v = np.sqrt(2 * P / rho)
    A_nozzle = np.pi * (d_nozzle / 2)**2
    Q_single = A_nozzle * v  # m³/s
    Q_total = Q_single * num_nozzles
    Q_total_LPM = Q_total * 60000  # L/min

    # Restrict flow rate to max 12 LPM
    if Q_total_LPM > 12:
        Q_total_LPM = 12
        Q_total = Q_total_LPM / 60000

    m_dot = rho * Q_total
    d_droplet = d_nozzle
    A_surface_total = np.pi * d_droplet**2 * num_nozzles

    # Heat Losses
    h_air = 60  # W/m²K
    q_conv = h_air * A_surface_total * (T_w - T_air)

    evap_fraction = 0.01 * rel_humidity
    m_evap = evap_fraction * m_dot
    q_evap = m_evap * h_fg

    q_rad = emissivity * sigma * A_surface_total * ((T_w + 273.15)**4 - (T_air + 273.15)**4)

    q_surface = 0.015 * m_dot * Cp_water * (T_w - T_air)

    deltaT_total = (q_conv + q_evap + q_rad + q_surface) / (m_dot * Cp_water)
    T_final = T_w - deltaT_total

    # Output
    st.success(f"🌡️ Final Outlet Temperature: **{T_final:.2f} °C**")
