import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import plotly.graph_objects as go
import time
import base64

# ✅ SET PAGE FIRST
st.set_page_config(page_title="Kohler Performance", page_icon="💧", layout="centered")

# Load assets
def load_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

gif_b64 = load_base64("kohler_loading.gif")
mp3_b64 = load_base64("netflix_intro.mp3")
logo_b64 = load_base64("logo.png")

# 🌐 Add global styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    .center-container {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
    }

    .stButton > button {
        background-color: #0078D4;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 0.8em 2.5em;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 12px rgba(0, 120, 212, 0.25);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #005fa3;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if "start" not in st.session_state:
    st.session_state.start = False

if not st.session_state.start:
    st.markdown("<div class='center-container'>", unsafe_allow_html=True)
    if st.button("Click to Start"):
        st.session_state.start = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Splash screen with audio
st.markdown(f"""
    <style>
    #splash {{
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: black;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: fadeOut 1s ease-out 3.2s forwards;
    }}
    #splash-logo {{
        width: 300px;
        animation: grow 3s ease-in-out forwards;
    }}
    #splash-text {{
        color: white;
        margin-top: 20px;
        font-size: 20px;
    }}
    @keyframes grow {{
        0% {{ transform: scale(1.0); opacity: 0; }}
        50% {{ transform: scale(1.3); opacity: 0.8; }}
        100% {{ transform: scale(1.6); opacity: 1; }}
    }}
    @keyframes fadeOut {{
        to {{ opacity: 0; visibility: hidden; }}
    }}
    </style>

    <div id="splash">
        <img id="splash-logo" src="data:image/gif;base64,{gif_b64}">
        <div id="splash-text">Performance Model</div>
        <audio id="intro-audio" autoplay>
            <source src="data:audio/mp3;base64,{mp3_b64}" type="audio/mp3">
        </audio>
    </div>
""", unsafe_allow_html=True)

time.sleep(3.5)

# --- Sidebar Navigation or Button Logic ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- HOME PAGE ---
if st.session_state.page == 'home':
    if st.session_state.page == 'home':
        st.markdown("""
    <style>
    body {
        background: linear-gradient(to bottom, #ffffff, #f0fbff);
    }

    .home-title {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.6rem;
        margin-top: 0.5rem;
    }

    .home-title h1 {
        background: -webkit-linear-gradient(45deg, #0077b6, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6em;
        margin: 0;
    }

    .home-title .icon {
        font-size: 2.4rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .subtext-box {
        background-color: #f0faff;
        padding: 0.7em 1.3em;
        border-radius: 12px;
        border: 1px solid #d8f1fc;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin: 15px auto 25px;
        text-align: center;
        font-size: 16px;
        font-weight: 500;
        color: #023e8a;
        max-width: 700px;
    }

    div.stButton > button {
        background-color: #0077b6;
        color: white;
        font-weight: 600;
        font-size: 15px;
        padding: 0.9em 1.2em;
        border-radius: 12px;
        width: 100%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #005f87;
        transform: translateY(-2px);
    }

    .caption-footer {
        text-align: center;
        font-size: 13px;
        margin-top: 30px;
        color: #666;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="home-title">
        <div class="icon">💧</div>
        <h1>Kohler Performance Model</h1>
        <div class="icon">💧</div>
    </div>
    <div class="subtext-box">
        Welcome to the Performance Prediction Model.<br>
        This tool accurately computes outlet parameters based on your selected inlet conditions, you can choose from the available models to simulate system behavior accordingly.<br>
        All models have been rigorously tested and validated on the KIC test bench.<br>
        If you have any feedback or suggestions, please feel free to reach out. Thank you!
    </div>
    """, unsafe_allow_html=True)

    st.write("### Select a Model to Continue:")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🚿 Shower Model"):
            st.session_state.page = "shower"
            st.rerun()
    with col2:
        if st.button("🔧 Valve Model"):
            st.session_state.page = "valve"
            st.rerun()
    with col3:
        if st.button("🚰 Faucet Model"):
            st.session_state.page = "faucet"
            st.rerun()
    with col4:
        if st.button("📉 PRV Placement"):
            st.session_state.page = "prv"
            st.rerun()

    st.markdown("""
        <div class="caption-footer">
            Made by <strong>Vigyan Lal</strong><br>
            KOCF372<br>
            Graduate Engineer Trainee – Faucets and Showering Engineering
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <style>
        .bottom-right-logo {{
            position: fixed;
            right: 20px;
            bottom: 20px;
            z-index: 1000;
            opacity: 0.9;
            border-radius: 10px;
        }}
        </style>
        <div class="bottom-right-logo">
            <img src="data:image/png;base64,{logo_b64}" width="120">
        </div>
    """, unsafe_allow_html=True)

        
# === FAUCET MODEL PAGE ===
elif st.session_state.page == 'faucet':
    st.title("🚰 Faucet Modelling")

    model_choice = st.selectbox("Choose Cartridge Size:", ["26mm", "28mm", "35mm"], index=0)

    if model_choice == "26mm":
        st.title("🚰 26mm")
        # Inputs
        col1, col2 = st.columns(2)
        with col1:
            hot_temp = st.slider('Hot Water Temp (°C)', 0, 100, 60)
            hot_pressure = st.slider('Hot Pressure (bar)', 0.0, 10.0, 1.5, 0.05)
        with col2:
            cold_temp = st.slider('Cold Water Temp (°C)', 0, 100, 20)
            cold_pressure = st.slider('Cold Pressure (bar)', 0.0, 10.0, 2.95, 0.05)

        col_lever, col_img = st.columns([2, 1])
        with col_lever:
            lever_angle = st.slider("Lever Angle (°)", -45, 45, 0)
            if lever_angle < -30:
                st.info("🔴 Mostly Hot")
            elif lever_angle > 30:
                st.info("🔵 Mostly Cold")
            else:
                st.info("🟢 Mixed")

        with col_img:
            st.image("L.png", width=100, caption="Lever Reference")

        # Calculations
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

        col3, col4 = st.columns(2)
        col3.metric("🌡️ Outlet Temp", f"{T_mixed:.1f} °C")
        col4.metric("🚿 Flow Rate", f"{flow_LPM:.2f} LPM")

        # Aerator Selection Section
        st.markdown("### 💦 Select Aerator Type")

# Aerator specs (mid-range flow at 3 bar)
        aerator_specs = {
        "Aerated - Light Green (Z) - 7.5-9 LPM": {"flow": 8.25, "wetted_area": 4806},  # Mid of 7.5 and 9
        "Aerated - Light Blue (A) - 13.5-15 LPM": {"flow": 14.25, "wetted_area": 4716},  # Mid of 13.5 and 15
        "Aerated - Light Grey (B) - 22.8-25.2 LPM": {"flow": 24, "wetted_area": 4840},
        "Aerated - Dark Grey (C) - 27-30 LPM": {"flow": 28.5, "wetted_area": 4823},
        "Aerated - Blue (V) - 22.8-25.2 LPM": {"wetted_area": 4033},
        "Aerated - Orange - 5 LPM": {"flow": 5, "wetted_area": 4596},
        "Aerated - White - 8 LPM": {"flow": 8, "wetted_area": 4596},
}
        aerator_choice = st.selectbox("Choose Aerator Type", list(aerator_specs.keys()))
        aerator_flow_rate = aerator_specs[aerator_choice]["flow"]
        wetted_area = aerator_specs[aerator_choice]["wetted_area"]

# Logic to compare calculated flow vs aerator rated flow
        st.markdown("#### ✅ With respect to Aerator:")

        if flow_LPM <= aerator_flow_rate:
                st.success(f"Flow will be **{flow_LPM:.2f} LPM** (within aerator limit of {aerator_flow_rate} LPM), with wetted area less than ~4806mm2")
        else:
                st.warning(f"⚠️ Aerator will restrict flow to **{aerator_flow_rate} LPM** (your calculated flow is {flow_LPM:.2f} LPM), with wetted area ~4806mm2 ")

            # Compact bar + graph
        def get_temp_color(temp):
            T = np.clip(temp, 0, 100)
            if T <= 25:
                return (0, T/25, 1)
            elif T <= 50:
                frac = (T-25) / 25
                return (frac, 1, 1 - frac)
            elif T <= 75:
                frac = (T-50)/25
                return (1, 1 - frac, 0)
            else:
                frac = (T-75)/25
                return (1, 0, 0)

        angles = np.linspace(-45, 45, 50)
        flows = []
        for angle in angles:
            lever_local = (45 - angle) / 90
            A_hot_local = lever_local * A_max
            A_cold_local = (1 - lever_local) * A_max
            m_hot = C_d * A_hot_local * np.sqrt(2 * rho * deltaP_hot)
            m_cold = C_d * A_cold_local * np.sqrt(2 * rho * deltaP_cold)
            m_total = m_hot + m_cold
            flows.append((m_total / rho) * 60)

        st.markdown("#### 📊 Visual Output")
        col_plot1, col_plot2 = st.columns([1, 2])

        with col_plot1:
            fig, ax = plt.subplots(figsize=(1.1, 2))
            ax.bar(1, T_mixed, width=0.3, color=get_temp_color(T_mixed))
            ax.set_ylim(0, 100)
            ax.set_xticks([]); ax.set_yticks([0, 50, 100])
            ax.set_title('Temp', fontsize=7)
            ax.set_ylabel('°C', fontsize=7)
            ax.tick_params(labelsize=6)
            st.pyplot(fig, use_container_width=False)

        with col_plot2:
            fig2, ax2 = plt.subplots(figsize=(3, 1.8))
            ax2.plot(angles, flows, 'b-o', linewidth=1.4, markersize=3)
            ax2.set_xlabel('Angle (°)', fontsize=7)
            ax2.set_ylabel('Flow (LPM)', fontsize=7)
            ax2.set_title('Flow Curve', fontsize=8)
            ax2.tick_params(labelsize=6)
            ax2.set_xlim([-50, 50]); ax2.set_ylim([0, max(flows)*1.1])
            ax2.grid(True, linewidth=0.4)
            st.pyplot(fig2, use_container_width=False)

        st.markdown("---")

    elif model_choice == "28mm":
        st.title("🚰 28mm")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            hot_temp = st.slider('🔥 Hot Water Temperature (°C)', 0, 100, 60)
            hot_pressure = st.slider('🔥 Hot Water Pressure (bar)', 0.0, 10.0, 1.5, 0.05)
        with col2:
            cold_temp = st.slider('❄️ Cold Water Temperature (°C)', 0, 100, 20)
            cold_pressure = st.slider('❄️ Cold Water Pressure (bar)', 0.0, 10.0, 2.95, 0.05)

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

        rho = 980
        A_max = 8.5e-3
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

        st.markdown("---")
        col3, col4 = st.columns(2)
        col3.metric("🌡️ Outlet Temp", f"{T_mixed:.1f} °C")
        col4.metric("🚿 Flow Rate", f"{flow_LPM:.2f} LPM")

        st.markdown("### 💦 Select Aerator Type")

# Aerator specs (mid-range flow at 3 bar)
        aerator_specs = {
        "Aerated - Light Green (Z) - 7.5-9 LPM": {"flow": 8.25, "wetted_area": 4806},  # Mid of 7.5 and 9
        "Aerated - Light Blue (A) - 13.5-15 LPM": {"flow": 14.25, "wetted_area": 4716},  # Mid of 13.5 and 15
        "Aerated - Light Grey (B) - 22.8-25.2 LPM": {"flow": 24, "wetted_area": 4840},
        "Aerated - Dark Grey (C) - 27-30 LPM": {"flow": 28.5, "wetted_area": 4823},
        "Aerated - Blue (V) - 22.8-25.2 LPM": {"wetted_area": 4033},
        "Aerated - Orange - 5 LPM": {"flow": 5, "wetted_area": 4596},
        "Aerated - White - 8 LPM": {"flow": 8, "wetted_area": 4596},
}
        aerator_choice = st.selectbox("Choose Aerator Type", list(aerator_specs.keys()))
        aerator_flow_rate = aerator_specs[aerator_choice]["flow"]
        wetted_area = aerator_specs[aerator_choice]["wetted_area"]

# Logic to compare calculated flow vs aerator rated flow
        st.markdown("#### ✅ With respect to Aerator:")

        if flow_LPM <= aerator_flow_rate:
            st.success(f"Flow will be **{flow_LPM:.2f} LPM** (within aerator limit of {aerator_flow_rate} LPM), with wetted area less than ~4806mm2")
        else:
            st.warning(f"⚠️ Aerator will restrict flow to **{aerator_flow_rate} LPM** (your calculated flow is {flow_LPM:.2f} LPM), with wetted area ~4806mm2 ")

        def get_temp_color(temp):
            T = np.clip(temp, 0, 100)
            if T <= 25:
                return (0, T/25, 1)
            elif T <= 50:
                frac = (T-25) / 25
                return (frac, 1, 1 - frac)
            elif T <= 75:
                frac = (T-50)/25
                return (1, 1 - frac, 0)
            else:
                frac = (T-75)/25
                return (1, 0, 0)

        angles = np.linspace(-45, 45, 50)
        flows = []
        for angle in angles:
            lever_local = (45 - angle) / 90
            A_hot_local = lever_local * A_max
            A_cold_local = (1 - lever_local) * A_max
            m_hot = C_d * A_hot_local * np.sqrt(2 * rho * deltaP_hot)
            m_cold = C_d * A_cold_local * np.sqrt(2 * rho * deltaP_cold)
            flows.append((m_hot + m_cold) / rho * 60)

        st.markdown("#### 📊 Visual Output")
        col_plot1, col_plot2 = st.columns([1, 2])
        with col_plot1:
            fig, ax = plt.subplots(figsize=(1.1, 2))
            ax.bar(1, T_mixed, width=0.3, color=get_temp_color(T_mixed))
            ax.set_ylim(0, 100)
            ax.set_xticks([]); ax.set_yticks([0, 50, 100])
            ax.set_title('Temp', fontsize=7)
            ax.set_ylabel('°C', fontsize=7)
            ax.tick_params(labelsize=6)
            st.pyplot(fig, use_container_width=False)

        with col_plot2:
            fig2, ax2 = plt.subplots(figsize=(3, 1.8))
            ax2.plot(angles, flows, 'b-o', linewidth=1.4, markersize=3)
            ax2.set_xlabel('Angle (°)', fontsize=7)
            ax2.set_ylabel('Flow (LPM)', fontsize=7)
            ax2.set_title('Flow Curve', fontsize=8)
            ax2.tick_params(labelsize=6)
            ax2.set_xlim([-50, 50])
            ax2.set_ylim([0, max(flows)*1.1])
            ax2.grid(True, linewidth=0.4)
            st.pyplot(fig2, use_container_width=False)

        st.markdown("---")
        st.caption("Created by Vigyan Lal💧")

    elif model_choice == "35mm":
        st.title("🚰35mm")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            hot_temp = st.slider('🔥 Hot Water Temperature (°C)', 0, 100, 60)
            hot_pressure = st.slider('🔥 Hot Water Pressure (bar)', 0.0, 10.0, 1.5, 0.05)
        with col2:
            cold_temp = st.slider('❄️ Cold Water Temperature (°C)', 0, 100, 20)
            cold_pressure = st.slider('❄️ Cold Water Pressure (bar)', 0.0, 10.0, 2.95, 0.05)

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

        rho = 980
        A_max = 15.75e-3
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

        st.markdown("---")
        col3, col4 = st.columns(2)
        col3.metric("🌡️ Outlet Temp", f"{T_mixed:.1f} °C")
        col4.metric("🚿 Flow Rate", f"{flow_LPM:.2f} LPM")

        st.markdown("### 💦 Select Aerator Type")

# Aerator specs (mid-range flow at 3 bar)
        aerator_specs = {
        "Aerated - Light Green (Z) - 7.5-9 LPM": {"flow": 8.25, "wetted_area": 4806},  # Mid of 7.5 and 9
        "Aerated - Light Blue (A) - 13.5-15 LPM": {"flow": 14.25, "wetted_area": 4716},  # Mid of 13.5 and 15
        "Aerated - Light Grey (B) - 22.8-25.2 LPM": {"flow": 24, "wetted_area": 4840},
        "Aerated - Dark Grey (C) - 27-30 LPM": {"flow": 28.5, "wetted_area": 4823},
        "Aerated - Blue (V) - 22.8-25.2 LPM": {"wetted_area": 4033},
        "Aerated - Orange - 5 LPM": {"flow": 5, "wetted_area": 4596},
        "Aerated - White - 8 LPM": {"flow": 8, "wetted_area": 4596},
}
        aerator_choice = st.selectbox("Choose Aerator Type", list(aerator_specs.keys()))
        aerator_flow_rate = aerator_specs[aerator_choice]["flow"]
        wetted_area = aerator_specs[aerator_choice]["wetted_area"]

# Logic to compare calculated flow vs aerator rated flow
        st.markdown("#### ✅ With Respect to Aerator:")

        if flow_LPM <= aerator_flow_rate:
            st.success(f"Flow will be **{flow_LPM:.2f} LPM** (within aerator limit of {aerator_flow_rate} LPM), with wetted area less than ~4806mm2")
        else:
            st.warning(f"⚠️ Aerator will restrict flow to **{aerator_flow_rate} LPM** (your calculated flow is {flow_LPM:.2f} LPM), with wetted area ~4806mm2 ")

        def get_temp_color(temp):
            T = np.clip(temp, 0, 100)
            if T <= 25:
                return (0, T/25, 1)
            elif T <= 50:
                frac = (T-25) / 25
                return (frac, 1, 1 - frac)
            elif T <= 75:
                frac = (T-50)/25
                return (1, 1 - frac, 0)
            else:
                frac = (T-75)/25
                return (1, 0, 0)

        angles = np.linspace(-45, 45, 50)
        flows = []
        for angle in angles:
            lever_local = (45 - angle) / 90
            A_hot_local = lever_local * A_max
            A_cold_local = (1 - lever_local) * A_max
            m_hot = C_d * A_hot_local * np.sqrt(2 * rho * deltaP_hot)
            m_cold = C_d * A_cold_local * np.sqrt(2 * rho * deltaP_cold)
            flows.append((m_hot + m_cold) / rho * 60)

        st.markdown("#### 📊 Visual Output")
        col_plot1, col_plot2 = st.columns([1, 2])
        with col_plot1:
            fig, ax = plt.subplots(figsize=(1.1, 2))
            ax.bar(1, T_mixed, width=0.3, color=get_temp_color(T_mixed))
            ax.set_ylim(0, 100)
            ax.set_xticks([]); ax.set_yticks([0, 50, 100])
            ax.set_title('Temp', fontsize=7)
            ax.set_ylabel('°C', fontsize=7)
            ax.tick_params(labelsize=6)
            st.pyplot(fig, use_container_width=False)

        with col_plot2:
            fig2, ax2 = plt.subplots(figsize=(3, 1.8))
            ax2.plot(angles, flows, 'b-o', linewidth=1.4, markersize=3)
            ax2.set_xlabel('Angle (°)', fontsize=7)
            ax2.set_ylabel('Flow (LPM)', fontsize=7)
            ax2.set_title('Flow Curve', fontsize=8)
            ax2.tick_params(labelsize=6)
            ax2.set_xlim([-50, 50])
            ax2.set_ylim([0, max(flows)*1.1])
            ax2.grid(True, linewidth=0.4)
            st.pyplot(fig2, use_container_width=False)

        st.markdown("---")
        st.caption("Created by Vigyan Lal💧")

    if st.button("🔙 Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

# === VALVE MODEL PAGE ===
elif st.session_state.page == 'valve':
    st.title("🚰 Valve Model")

    model_choice = st.selectbox("Choose Valve:", ["AT235", "AT360", "Thermostatic"], index=0)

    if model_choice == "AT360":
        st.title("🚰 AQUA TURBO 360")
        st.subheader("Inlet Conditions & Outlet Selection")
        with st.container():
            col1, col2, col3 = st.columns(3)
        with col1:
            hotP = st.number_input('Hot Pressure (P1) (bar)', value=3.0, step=0.1, key="hotP_valve")
            hotT = st.number_input('Hot Temperature (T1) (°C)', value=60.0, step=1.0, key="hotT_valve")
        with col2:
            coldP = st.number_input('Cold Pressure (P2) (bar)', value=3.0, step=0.1, key="coldP_valve")
            coldT = st.number_input('Cold Temperature (T2) (°C)', value=25.0, step=1.0, key="coldT_valve")
        with col3:
            outletChoice = st.selectbox('Check Flow To:', ['Spout', 'Shower'], key="outletChoice_valve")
            pipeLen = st.number_input('Pipe Length L in m', value=1.0, step=0.1, key="pipeLen_valve")
            pipeDia = st.number_input('Pipe Diameter (mm)', value=18.4, step=0.1, key="pipeDia_valve")

        st.subheader("Lever Control")

        col_slider, col_gauge, col_image, col_image2 = st.columns([1.2, 1, 1, 1])

        with col_slider:
            st.markdown("##### Lever Angle (°)")
            st.markdown("<div style='padding-top: 35px;'>", unsafe_allow_html=True)
            theta = st.slider("", min_value=-45, max_value=45, value=0, step=1, key="theta_valve_slider")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_gauge:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=theta,
                title={'text': ""},
                gauge={
                    'axis': {'range': [-45, 45]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [-45, 0], 'color': "indianred"},
                        {'range': [0, 45], 'color': "lightblue"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 2},
                        'thickness': 0.75,
                        'value': theta
                    }
                }
            ))
            fig.update_layout(height=200, width=200, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=False)

        with col_image:
            st.markdown("<div style='text-align:center; padding-top: 35px;'>", unsafe_allow_html=True)
            st.image("AT360.png", width=130, caption="Valve Image")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_image2:        
            st.markdown("<div style='text-align:center; padding-top: 35px;'>", unsafe_allow_html=True)
            st.image("Valve_Shower.png", width=130, caption="Length of Pipe from Valve to Shower")
            st.markdown("</div>", unsafe_allow_html=True)

    # Calculation inside Valve
        def calculate_valve(hotP, coldP, hotT, coldT, theta, outletChoice, pipeLen, pipeDia):
            rho = 1000
            g = 9.81
            D_throat = 0.007
            D_outlet = 0.0127
            A_throat = math.pi * (D_throat/2)**2
            A_outlet = math.pi * (D_outlet/2)**2

            lever = (theta + 45) / 90
            P_hot = hotP * 1e5
            P_cold = coldP * 1e5
            L_pipe = pipeLen
            D_pipe = pipeDia / 1000

            A_hot = (1 - lever) * A_throat
            A_cold = lever * A_throat
            K_inlet = 0.17
            K_cart = 0.67
            K_out = 0.2

            Q_hot = A_hot * math.sqrt((2 * P_hot) / (rho * (K_inlet + K_cart)))
            Q_cold = A_cold * math.sqrt((2 * P_cold) / (rho * (K_inlet + K_cart)))
            Q_total = Q_hot + Q_cold

            P_mix = (Q_hot * P_hot + Q_cold * P_cold) / max(Q_total, 1e-6)
            T_mix = (Q_hot * hotT + Q_cold * coldT) / max(Q_total, 1e-6)

            if outletChoice == 'Shower':
                K_total = K_cart + K_out
            else:
                K_total = K_cart + K_out

            Q_out = A_throat * math.sqrt((2 * P_mix) / (rho * K_total))

            v_out = Q_out / A_outlet
            DeltaP = 0.5 * rho * v_out**2
            P_out = P_mix - DeltaP

            A_pipe = math.pi * (D_pipe/2)**2
            v_pipe = Q_out / A_pipe
            f = 0.009
            DeltaP_pipe = f * (L_pipe / D_pipe) * 0.5 * rho * v_pipe**2

            if outletChoice == 'Shower':
                DeltaP_pipe += rho * g * L_pipe
            else:
                DeltaP_pipe *= 0.05

            P_pipe_out = max(P_out - DeltaP_pipe, 0)
            T_pipe_out = T_mix - 0.2 * L_pipe

            results = {
                "Valve Outlet Flow (LPM)": Q_out * 1000 * 60,
                "Valve Outlet Pressure (bar)": P_out / 1e5,
                "Mixed Water Temperature (°C)": T_mix,
                "Final Pipe Flow (LPM)": Q_out * 1000 * 60,
                "Final Pipe Pressure (bar)": P_pipe_out / 1e5,
                "Final Pipe Temperature (°C)": T_pipe_out
            }
            return results

        with st.spinner("🔄 Calculating output... Please wait"):
            results = calculate_valve(hotP, coldP, hotT, coldT, theta, outletChoice, pipeLen, pipeDia)

        st.subheader("Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Valve Outlet Flow (LPM)", f"{results['Valve Outlet Flow (LPM)']:.2f}")
            st.metric("Final Pipe Flow (LPM)", f"{results['Final Pipe Flow (LPM)']:.2f}")
        with col2:
            st.metric("Valve Outlet Pressure (bar)", f"{results['Valve Outlet Pressure (bar)']:.2f}")
            st.metric("Final Pipe Pressure (bar)", f"{results['Final Pipe Pressure (bar)']:.2f}")
        with col3:
            st.metric("Mixed Water Temperature (°C)", f"{results['Mixed Water Temperature (°C)']:.1f}")
            st.metric("Final Pipe Temperature (°C)", f"{results['Final Pipe Temperature (°C)']:.1f}")



    elif model_choice == "AT235":
        st.title("🚰 AQUA TURBO 235")
        st.subheader("Inlet Conditions & Outlet Selection")
        with st.container():
            col1, col2, col3 = st.columns(3)
        with col1:
            hotP = st.number_input('Hot Pressure (P1) (bar)', value=3.0, step=0.1, key="hotP_valve")
            hotT = st.number_input('Hot Temperature (T1) (°C)', value=60.0, step=1.0, key="hotT_valve")
        with col2:
            coldP = st.number_input('Cold Pressure (P2) (bar)', value=3.0, step=0.1, key="coldP_valve")
            coldT = st.number_input('Cold Temperature (T2) (°C)', value=25.0, step=1.0, key="coldT_valve")
        with col3:
            outletChoice = st.selectbox('Check Flow To:', ['Spout', 'Shower'], key="outletChoice_valve")
            pipeLen = st.number_input('Pipe Length (L) in m', value=1.0, step=0.1, key="pipeLen_valve")
            pipeDia = st.number_input('Pipe Diameter (mm)', value=18.4, step=0.1, key="pipeDia_valve")

        st.subheader("Lever Control")

        col_slider, col_gauge, col_image, col_image2 = st.columns([1.2, 1, 1, 1])

        with col_slider:
            st.markdown("##### Lever Angle (°)")
            st.markdown("<div style='padding-top: 35px;'>", unsafe_allow_html=True)
            theta = st.slider("", min_value=-45, max_value=45, value=0, step=1, key="theta_valve_slider")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_gauge:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=theta,
                title={'text': ""},
                gauge={
                    'axis': {'range': [-45, 45]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [-45, 0], 'color': "indianred"},
                        {'range': [0, 45], 'color': "lightblue"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 2},
                        'thickness': 0.75,
                        'value': theta
                    }
                }
            ))
            fig.update_layout(height=200, width=200, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=False)

        with col_image:
            st.markdown("<div style='text-align:center; padding-top: 35px;'>", unsafe_allow_html=True)
            st.image("882IN.png", width=130, caption="Valve Image")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_image2:
            st.markdown("<div style='text-align:center; padding-top: 35px;'>", unsafe_allow_html=True)
            st.image("Valve_Shower.png", width=130, caption="Length of Pipe from Valve to Shower")
            st.markdown("</div>", unsafe_allow_html=True)

    # Calculation inside Valve
        def calculate_valve(hotP, coldP, hotT, coldT, theta, outletChoice, pipeLen, pipeDia):
            rho = 1000
            g = 9.81
            D_throat = 0.0051
            D_outlet = 0.0127
            A_throat = math.pi * (D_throat/2)**2
            A_outlet = math.pi * (D_outlet/2)**2

            lever = (theta + 45) / 90
            P_hot = hotP * 1e5
            P_cold = coldP * 1e5
            L_pipe = pipeLen
            D_pipe = pipeDia / 1000

            A_hot = (1 - lever) * A_throat
            A_cold = lever * A_throat
            K_inlet = 0.17
            K_cart = 0.65
            K_out = 0.2

            Q_hot = A_hot * math.sqrt((2 * P_hot) / (rho * (K_inlet + K_cart)))
            Q_cold = A_cold * math.sqrt((2 * P_cold) / (rho * (K_inlet + K_cart)))
            Q_total = Q_hot + Q_cold

            P_mix = (Q_hot * P_hot + Q_cold * P_cold) / max(Q_total, 1e-6)
            T_mix = (Q_hot * hotT + Q_cold * coldT) / max(Q_total, 1e-6)

            if outletChoice == 'Shower':
                K_total = K_cart + K_out
            else:
                K_total = K_cart + K_out

            Q_out = A_throat * math.sqrt((2 * P_mix) / (rho * K_total))

            v_out = Q_out / A_outlet
            DeltaP = 0.5 * rho * v_out**2
            P_out = P_mix - DeltaP

            A_pipe = math.pi * (D_pipe/2)**2
            v_pipe = Q_out / A_pipe
            f = 0.009
            DeltaP_pipe = f * (L_pipe / D_pipe) * 0.5 * rho * v_pipe**2

            if outletChoice == 'Shower':
                DeltaP_pipe += rho * g * L_pipe
            else:
                DeltaP_pipe *= 0.05

            P_pipe_out = max(P_out - DeltaP_pipe, 0)
            T_pipe_out = T_mix - 0.2 * L_pipe

            results = {
                "Valve Outlet Flow (LPM)": Q_out * 1000 * 60,
                "Valve Outlet Pressure (bar)": P_out / 1e5,
                "Mixed Water Temperature (°C)": T_mix,
                "Final Pipe Flow (LPM)": Q_out * 1000 * 60,
                "Final Pipe Pressure (bar)": P_pipe_out / 1e5,
                "Final Pipe Temperature (°C)": T_pipe_out
            }
            return results

        with st.spinner("🔄 Calculating output... Please wait"):
            results = calculate_valve(hotP, coldP, hotT, coldT, theta, outletChoice, pipeLen, pipeDia)

        st.subheader("Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Valve Outlet Flow (LPM)", f"{results['Valve Outlet Flow (LPM)']:.2f}")
            st.metric("Final Pipe Flow (LPM)", f"{results['Final Pipe Flow (LPM)']:.2f}")
        with col2:
            st.metric("Valve Outlet Pressure (bar)", f"{results['Valve Outlet Pressure (bar)']:.2f}")
            st.metric("Final Pipe Pressure (bar)", f"{results['Final Pipe Pressure (bar)']:.2f}")
        with col3:
            st.metric("Mixed Water Temperature (°C)", f"{results['Mixed Water Temperature (°C)']:.1f}")
            st.metric("Final Pipe Temperature (°C)", f"{results['Final Pipe Temperature (°C)']:.1f}")

        # if st.button("🔙 Back to Home"):
        #     st.session_state.page = 'home'
        #     st.rerun()

    elif model_choice == "Thermostatic":
        st.title("🌡️ Anthem: Select no. of outlets")

        col1, col2, col3 = st.columns(3)
        with col1:
            T_hot = st.number_input("Hot Water Temp (°C):", value=60.9, step=0.1)
            mix_setting = 'A (Mixing)'
            product_attached = st.toggle("Product Attached", value=True)

        with col2:
            T_cold = st.number_input("Cold Water Temp (°C):", value=20.8, step=0.1)
            mix_ratio = st.slider("Mixing Ratio (0 = Cold, 1 = Hot):", 0.0, 1.0, 0.5, step=0.01)

        with col3:
            num_outlets = st.selectbox("No. of Outlets:", ['3','4','5','6','7'], index=3)
            num = int(num_outlets)

        outlet_types = ['Spout', 'Handshower', 'Showerhead', 'Rain Panel', 'Body Jet -1', 'Body Jet -2']
        outlet_data = []

        outlet_cols = st.columns([3, 1])
        with outlet_cols[0]:
            outlet_data = []
            for i in range(num):
                st.markdown(f"**Outlet {i+1}**")
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    outlet_type = st.selectbox(f"Type {i+1}", outlet_types, key=f"type_{i}")
                with col_b:
                    length_ft = st.slider(f"Pipe Length (ft) {i+1}", 1, 6, 2, key=f"len_{i}")
                outlet_data.append((outlet_type, length_ft))

        with outlet_cols[1]:
            st.image("3 port.png", width=160, caption="3 Outlet Anthem")
            st.image("4 port.png", width=160, caption="4 Outlet Anthem")
            st.image("5 port.png", width=160, caption="5 Outlet Anthem")
            st.image("6 port.png", width=160, caption="6 Outlet Anthem")

        def get_temp_drop(outlet, len_ft, setting, is_attached):
            if setting == "A (Mixing)":
                if outlet == 'Handshower':
                    deltaT = min(2, 1 * (len_ft / 2))
                elif outlet == 'Showerhead':
                    deltaT = np.interp(len_ft, [0, 2, 4, 6], [1, 1.2, 1.9, 3.1])
                elif outlet == 'Rain Panel':
                    deltaT = 0.08 * len_ft
                elif outlet == 'Body Jet -1' or outlet == 'Body Jet -2':
                    deltaT = 0.5 * len_ft
                elif outlet == 'Spout':
                    deltaT = 0.3 * len_ft
                else:
                    deltaT = 0.5 * len_ft
            else:
                if outlet == 'Handshower':
                    deltaT = np.interp(len_ft, [0, 2, 4], [0, 2.7, 3.5])
                elif outlet == 'Showerhead':
                    deltaT = np.interp(len_ft, [0, 2, 4, 6], [1, 1.2, 1.9, 3.1])
                elif outlet == 'Rain Panel':
                    deltaT = np.interp(len_ft, [0, 2], [0, 1.3])
                elif outlet == 'Body Jet -1' or outlet == 'Body Jet -2':
                    deltaT = 0.6 * len_ft
                elif outlet == 'Spout':
                    deltaT = 0.3 * len_ft
                else:
                    deltaT = 0.6 * len_ft
            return deltaT + 0.8 if is_attached else deltaT

        if True:
            mix_ratio_val = mix_ratio

            T_mix = mix_ratio_val * T_hot + (1 - mix_ratio_val) * T_cold
            st.success(f"🔁 Valve Output Temperature: **{T_mix:.2f} °C**")

            cols = st.columns(num)
            for i, (outlet, length) in enumerate(outlet_data):
                delta_T = get_temp_drop(outlet, length, mix_setting, product_attached)
                outlet_temp = T_mix - delta_T
                with cols[i]:
                    st.metric(label=f"Outlet {i+1} ({outlet})", value=f"{outlet_temp:.1f} °C")

    if st.button("🔙 Back to Home", key = "back_home_thermo"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'shower':
    st.title("🚿 Shower Performance Model")
    st.markdown("---")

    st.subheader("Enter Parameters:")
    temp = st.number_input("Water Temperature (°C)", value=40.0, step=1.0, format="%.1f")
    pressure = st.number_input("Water Pressure (bar)", value=3.0, step=0.1, format="%.1f")
    nozzle_dia = st.number_input("Nozzle Diameter (mm)", value=1.2, step=0.1, format="%.2f")
    num_nozzles = st.number_input("Number of Nozzles", value=50, step=1)
    air_temp = st.number_input("Ambient Air Temperature (°C)", value=25.0, step=0.1, format="%.1f")

    if st.button("💧 Calculate Final Outlet Temperature"):
        rho = 997
        h_fg = 2257000
        sigma = 5.67e-8
        emissivity = 0.95
        Cp_water = 4182
        rel_humidity = 0.5

        P = pressure * 1e5
        d_nozzle = nozzle_dia / 1000
        T_w = temp
        T_air = air_temp

        v = np.sqrt(2 * P / rho)
        A_nozzle = np.pi * (d_nozzle / 2)**2
        Q_single = A_nozzle * v
        Q_total = Q_single * num_nozzles
        Q_total_LPM = Q_total * 60000

        if Q_total_LPM > 12:
            Q_total_LPM = 12
            Q_total = Q_total_LPM / 60000

        m_dot = rho * Q_total
        d_droplet = d_nozzle
        A_surface_total = np.pi * d_droplet**2 * num_nozzles

        h_air = 60
        q_conv = h_air * A_surface_total * (T_w - T_air)
        evap_fraction = 0.01 * rel_humidity
        m_evap = evap_fraction * m_dot
        q_evap = m_evap * h_fg
        q_rad = emissivity * sigma * A_surface_total * ((T_w + 273.15)**4 - (T_air + 273.15)**4)
        q_surface = 0.015 * m_dot * Cp_water * (T_w - T_air)

        deltaT_total = (q_conv + q_evap + q_rad + q_surface) / (m_dot * Cp_water)
        T_final = T_w - deltaT_total

        st.success(f"🌡️ Final Outlet Temperature: **{T_final:.2f} °C**")

    if st.button("🔙 Back to Home", key = "back_home_shower"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'prv':
    st.title("🔧 PRV Placement Calculator")

    with st.form("prv_form"):
        st.subheader("Enter Pipeline Parameters")

        # Layout: Inputs on left, image on right
        col_form, col_img = st.columns([2, 1.2])
        with col_form:
            col1, col2 = st.columns(2)
            with col1:
                total_length = st.number_input("Total Pipeline Length (m)", min_value=0.0, value=0.0, step=0.1)
                target_pressure_bar = st.number_input("Target Outlet Pressure (bar)", min_value=0.0, value=0.0, step=0.1)
            with col2:
                elevation_drop = st.number_input("Total Elevation Drop (m)", min_value=0.0, value=0.0, step=0.1)
                pipe_dia_mm = st.number_input("Pipe Inner Diameter (mm)", min_value=0.0, value=0.0, step=0.1)

            col_calc, col_reset = st.columns([1, 1])
            with col_calc:
                submitted = st.form_submit_button("Calculate PRV Location")
            with col_reset:
                reset = st.form_submit_button("Reset")

        with col_img:
            st.image("PRV_Location.jpg", caption="📈 PRV Placement Thoery", use_container_width=True)

    # After form is submitted
    if submitted:
        if total_length == 0 or elevation_drop == 0 or target_pressure_bar == 0:
            st.error("Please fill all fields with non-zero values.")
        else:
            rho = 1000  # kg/m³
            g = 9.81    # m/s²
            pipe_dia_m = pipe_dia_mm / 1000  # in meters
            P_target_Pa = target_pressure_bar * 1e5  # in Pascal

            required_height = P_target_Pa / (rho * g)
            elevation_fraction = required_height / elevation_drop
            L2 = elevation_fraction * total_length
            L1 = total_length - L2

            st.success(f"""✅ To ensure outlet pressure = **{target_pressure_bar:.2f} bar**:
- Place the PRV **{L1:.2f} meters** from the inlet  
- (i.e., **{L2:.2f} meters** from the outlet)""")

    elif reset:
        st.experimental_rerun()

    st.markdown("---")
    if st.button("🔙 Back to Home", key="back_home_prv"):
        st.session_state.page = 'home'
        st.rerun()
