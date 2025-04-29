import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import plotly.graph_objects as go

# --- Page Setup ---
st.set_page_config(page_title="Water Systems Home", page_icon="💧", layout="centered")

# --- Sidebar Navigation or Button Logic ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- HOME PAGE ---
if st.session_state.page == 'home':
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #d1f3f9;
            color: #0077b6;
            border: 1px solid #90e0ef;
            padding: 0.6em 1em;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            background-color: #b2ebf2;
            color: #000000;
            transform: scale(1.03);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("💧 Kohler Performance Model 💧")
    st.subheader("This is a Perfomace Prediction Model that gives the Outlet Parameters.")
    st.markdown("---")
    st.write("### Select a Model to Continue:")

    col1, col2, col3 = st.columns(3)

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

    st.markdown("---")
    st.caption("Made by Vigyan Lal")

# === FAUCET MODEL PAGE ===
elif st.session_state.page == 'faucet':
    st.title("🚰 Faucet Modelling")

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

    # Compact bar + graph
    def get_temp_color(temp):
        T = np.clip(temp, 0, 100)
        if T <= 25:
            return (0, T/25, 1)
        elif T <= 50:
            return (0, 1, 1 - (T - 25)/25)
        elif T <= 75:
            return ((T - 50)/25, 1 - 0.5*(T - 50)/25, 0)
        else:
            return (1, 0.5 - 0.5*(T - 75)/25, 0)

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

    if st.button("🔙 Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

# === VALVE MODEL PAGE ===
elif st.session_state.page == 'valve':
    st.title("🔧 Diverter Valve Modelling")

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
            pipeLen = st.number_input('Pipe Length (m)', value=1.0, step=0.1, key="pipeLen_valve")
            pipeDia = st.number_input('Pipe Diameter (mm)', value=18.4, step=0.1, key="pipeDia_valve")

    st.subheader("Lever Control")

    col_slider, col_gauge, col_image = st.columns([1, 1, 1])

    with col_slider:
        theta = st.slider("Lever Angle (°)", min_value=-45, max_value=45, value=0, step=1, key="theta_valve")

    with col_gauge:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=theta,
            title={'text': "Lever Angle", 'font': {'size': 16}},
            gauge={
                'axis': {'range': [-45, 45]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [-45, 0], 'color': "lightblue"},
                    {'range': [0, 45], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 2},
                    'thickness': 0.75,
                    'value': theta
                }
            }
        ))
        fig.update_layout(height=220, width=220, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig)

    with col_image:
        st.image('882IN.png', width=150, caption="Valve Image (Small)")

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

    if st.button("🔙 Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

# === SHOWER MODEL PAGE ===
# === SHOWER MODEL PAGE ===
elif st.session_state.page == 'shower':
    st.title("🚿 Shower Performance Model")
    st.markdown("---")

    st.subheader("Enter Parameters:")
    temp = st.number_input("Water Temperature (°C)", value=40.0, format="%.1f")
    pressure = st.number_input("Water Pressure (bar)", value=3.0, format="%.1f")
    nozzle_dia = st.number_input("Nozzle Diameter (mm)", value=1.2, format="%.2f")
    num_nozzles = st.number_input("Number of Nozzles", value=50, step=1)
    air_temp = st.number_input("Ambient Air Temperature (°C)", value=25.0, format="%.1f")

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

    if st.button("🔙 Back to Home"):
        st.session_state.page = 'home'
        st.rerun()