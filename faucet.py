import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Page setup ---
st.set_page_config(page_title="Faucet Model", page_icon="🚰", layout="centered")

st.title("🚰 Faucet Performance Model")
st.markdown("---")

# --- Input layout ---
col1, col2 = st.columns(2)

with col1:
    hot_temp = st.slider('🔥 Hot Water Temperature (°C)', 0, 100, 60)
    hot_pressure = st.slider('🔥 Hot Water Pressure (bar)', 0.0, 10.0, 1.5, 0.05)

with col2:
    cold_temp = st.slider('❄️ Cold Water Temperature (°C)', 0, 100, 20)
    cold_pressure = st.slider('❄️ Cold Water Pressure (bar)', 0.0, 10.0, 2.95, 0.05)

# --- Lever angle ---
st.markdown("### 🛠️ Lever Control")

col_lever, col_img = st.columns([2, 1])

with col_lever:
    lever_angle = st.slider("Rotate Lever (°)", min_value=-45, max_value=45, value=0, step=1, format="%d°")
    if lever_angle < -30:
        st.info("🔴 Mostly Hot Water")
    elif lever_angle > 30:
        st.info("🔵 Mostly Cold Water")
    else:
        st.info("🟢 Mixed Water")

with col_img:
    st.image("L.png", width=100, caption="Faucet for Lever Reference")

# --- Physics calculation ---
rho = 980
A_max = 7e-3
C_d = 1.0
lever = (45 - lever_angle) / 90

A_hot = lever * A_max
A_cold = (1 - lever) * A_max

P_hot = hot_pressure * 1e5
P_cold = cold_pressure * 1e5

deltaP_hot = max(P_hot, 1e4)
deltaP_cold = max(P_cold, 1e4)

m_dot_hot = C_d * A_hot * np.sqrt(2 * rho * deltaP_hot)
m_dot_cold = C_d * A_cold * np.sqrt(2 * rho * deltaP_cold)
m_dot_total = m_dot_hot + m_dot_cold

if m_dot_total < 1e-6:
    T_mixed = (hot_temp + cold_temp) / 2
    flow_LPM = 0
else:
    T_mixed = (m_dot_hot * hot_temp + m_dot_cold * cold_temp) / m_dot_total
    flow_LPM = (m_dot_total / rho) * 60

# --- Output metrics ---
st.markdown("---")
col3, col4 = st.columns(2)
col3.metric("🌡️ Outlet Temp", f"{T_mixed:.1f} °C")
col4.metric("🚿 Flow Rate", f"{flow_LPM:.2f} LPM")

# --- Define color gradient for temp bar ---
def get_temp_color(temp):
    T = np.clip(temp, 0, 100)
    if T <= 25:
        frac = T / 25
        return (0, frac, 1)
    elif T <= 50:
        frac = (T - 25) / 25
        return (0, 1, 1 - frac)
    elif T <= 75:
        frac = (T - 50) / 25
        return (frac, 1 - 0.5 * frac, 0)
    else:
        frac = (T - 75) / 25
        return (1, 0.5 - 0.5 * frac, 0)

# --- Flow curve ---
angles = np.linspace(-45, 45, 50)
flows = []
for angle in angles:
    lever_local = (45 - angle) / 90
    A_hot_local = lever_local * A_max
    A_cold_local = (1 - lever_local) * A_max

    m_dot_hot_local = C_d * A_hot_local * np.sqrt(2 * rho * deltaP_hot)
    m_dot_cold_local = C_d * A_cold_local * np.sqrt(2 * rho * deltaP_cold)
    m_dot_total_local = m_dot_hot_local + m_dot_cold_local
    flow_local = (m_dot_total_local / rho) * 60
    flows.append(flow_local)

# --- Compact side-by-side plots ---
st.markdown("#### 📊 Visual Output")

col_plot1, col_plot2 = st.columns([1, 2])

# --- Thermocolor Bar
with col_plot1:
    fig, ax = plt.subplots(figsize=(1.1, 2))
    ax.bar(1, T_mixed, width=0.3, color=get_temp_color(T_mixed))
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_yticks([0, 50, 100])
    ax.set_title('Temp', fontsize=7)
    ax.set_ylabel('°C', fontsize=7)
    ax.tick_params(labelsize=6)
    st.pyplot(fig, use_container_width=False)

# --- Flow vs Lever Plot
with col_plot2:
    fig2, ax2 = plt.subplots(figsize=(3, 1.8))
    ax2.plot(angles, flows, 'b-o', linewidth=1.4, markersize=3)
    ax2.set_xlabel('Angle (°)', fontsize=7)
    ax2.set_ylabel('Flow (LPM)', fontsize=7)
    ax2.set_title('Flow Curve', fontsize=8)
    ax2.tick_params(labelsize=6)
    ax2.set_xlim([-50, 50])
    ax2.set_ylim([0, max(flows) * 1.1])
    ax2.grid(True, linewidth=0.4)
    st.pyplot(fig2, use_container_width=False)

st.markdown("---")
st.caption("Created by Vigyan Lal💧")
