import streamlit as st
import numpy as np
import math
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Diverter Valve Mixer", layout="wide")

# Title
st.title("Diverter Valve Mixer")
st.markdown("---")

# Input Panels
st.subheader("Inlet Conditions & Outlet Selection")
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        hotP = st.number_input('Hot Pressure (P1) (bar)', value=3.0, step=0.1)
        hotT = st.number_input('Hot Temperature (T1) (°C)', value=60.0, step=1.0)
    with col2:
        coldP = st.number_input('Cold Pressure (P2) (bar)', value=3.0, step=0.1)
        coldT = st.number_input('Cold Temperature (T2) (°C)', value=25.0, step=1.0)
    with col3:
        outletChoice = st.selectbox('Check Flow To:', ['Spout', 'Shower'])
        pipeLen = st.number_input('Pipe Length (m)', value=1.0, step=0.1)
        pipeDia = st.number_input('Pipe Diameter (mm)', value=18.4, step=0.1)

st.markdown("---")

# Lever, Gauge, and Image in a Single Line
st.subheader("Lever Control")

col_slider, col_gauge, col_image = st.columns([1, 1, 1])

with col_slider:
    theta = st.slider("Lever Angle (°)", min_value=-45, max_value=45, value=0, step=1)

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

st.markdown("---")

# Calculation Function
def calculate_outputs(hotP, coldP, hotT, coldT, theta, outletChoice, pipeLen, pipeDia):
    rho = 1000  # kg/m³
    g = 9.81    # m/s²
    D_throat = 0.007  # m
    D_outlet = 0.0127  # m
    A_throat = math.pi * (D_throat / 2) ** 2
    A_outlet = math.pi * (D_outlet / 2) ** 2

    K_inlet = 0.17
    K_cart = 0.67
    K_out_spout = 0.2
    K_out_shower = 0.2

    P_hot = hotP * 1e5  # Pa
    P_cold = coldP * 1e5  # Pa
    T_hot = hotT
    T_cold = coldT
    L_pipe = pipeLen
    D_pipe = pipeDia / 1000  # mm to meters

    lever = (theta + 45) / 90

    A_hot = (1 - lever) * A_throat
    A_cold = lever * A_throat

    Q_hot = A_hot * math.sqrt((2 * P_hot) / (rho * (K_inlet + K_cart)))
    Q_cold = A_cold * math.sqrt((2 * P_cold) / (rho * (K_inlet + K_cart)))
    Q_total = Q_hot + Q_cold

    P_mix = (Q_hot * P_hot + Q_cold * P_cold) / max(Q_total, 1e-6)
    T_mix = (Q_hot * T_hot + Q_cold * T_cold) / max(Q_total, 1e-6)

    if outletChoice.lower() == 'spout':
        K_out = K_out_spout
    else:
        K_out = K_out_shower

    K_total = K_cart + K_out
    Q_out = A_throat * math.sqrt((2 * P_mix) / (rho * K_total))

    v_out = Q_out / A_outlet
    DeltaP = 0.5 * rho * v_out**2
    P_out = P_mix - DeltaP

    # Pipe Pressure Drop
    A_pipe = math.pi * (D_pipe / 2) ** 2
    v_pipe = Q_out / A_pipe
    f = 0.009
    DeltaP_pipe = f * (L_pipe / D_pipe) * 0.5 * rho * v_pipe**2

    if outletChoice.lower() == 'shower':
        DeltaP_pipe += rho * g * L_pipe  # vertical lift only for shower
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

# Run calculations
results = calculate_outputs(hotP, coldP, hotT, coldT, theta, outletChoice, pipeLen, pipeDia)

# Output Panels
st.subheader("Results")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Valve Outlet Flow (LPM)", value=f"{results['Valve Outlet Flow (LPM)']:.2f}")
    st.metric(label="Final Pipe Flow (LPM)", value=f"{results['Final Pipe Flow (LPM)']:.2f}")
with col2:
    st.metric(label="Valve Outlet Pressure (bar)", value=f"{results['Valve Outlet Pressure (bar)']:.2f}")
    st.metric(label="Final Pipe Pressure (bar)", value=f"{results['Final Pipe Pressure (bar)']:.2f}")
with col3:
    st.metric(label="Mixed Water Temperature (°C)", value=f"{results['Mixed Water Temperature (°C)']:.1f}")
    st.metric(label="Final Pipe Temperature (°C)", value=f"{results['Final Pipe Temperature (°C)']:.1f}")

st.markdown("---")
