
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Smart Bandage",
    page_icon="🩹",
    layout="wide",
)

# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------

st.markdown("""
<style>
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .sensor-card {
        padding: 1.25rem;
        border: 1px solid rgba(128,128,128,.25);
        border-radius: 16px;
        background: rgba(128,128,128,.06);
        min-height: 170px;
    }

    .sensor-name {
        font-size: 0.95rem;
        opacity: .75;
        margin-bottom: .35rem;
    }

    .sensor-value {
        font-size: 2.25rem;
        font-weight: 700;
        margin-bottom: .15rem;
    }

    .sensor-status {
        font-size: .9rem;
        opacity: .8;
    }

    .connection {
        padding: .65rem 1rem;
        border-radius: 12px;
        background: rgba(128,128,128,.08);
        border: 1px solid rgba(128,128,128,.25);
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

header_left, header_right = st.columns([3, 1])

with header_left:
    st.title("🩹 Smart Bandage")
    st.caption("Wound monitoring dashboard")

with header_right:
    st.markdown(
        """
        <div class="connection">
            ⚪ <b>Prototype</b><br>
            <span style="font-size:.85rem;opacity:.65;">
                Manual test data
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()


# ---------------------------------------------------------
# MANUAL SENSOR INPUT
#
# Replace these inputs with Arduino/Bluetooth data later.
# ---------------------------------------------------------

st.subheader("Test Sensor Data")

input1, input2, input3 = st.columns(3)

with input1:
    temperature = st.number_input(
        "Temperature (37°C)",
        min_value=0.0,
        max_value=50.0,
        value=36.8,
        step=0.1,
    )

with input2:
    moisture = st.number_input(
        "Moisture (20%)",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=1.0,
    )

with input3:
    ph = st.number_input(
        "pH",
        min_value=0.0,
        max_value=14.0,
        value=7.10,
        step=0.01,
    )


# ---------------------------------------------------------
# Status functions
# ---------------------------------------------------------

def temp_status(value):

    if value >= 38.0:
        return "Elevated"

    if value >= 37.5:
        return "Slightly elevated"

    return "Stable"


def moisture_status(value):

    if value >= 80:
        return "High moisture"

    if value <= 30:
        return "Low moisture"

    return "Moderate"


def ph_status(value):

    if value >= 8.0:
        return "Higher pH"

    if value <= 5.5:
        return "Lower pH"

    return "Within range"


# ---------------------------------------------------------
# Current readings
# ---------------------------------------------------------

st.subheader("Current Readings")

c1, c2, c3 = st.columns(3)


with c1:
    st.markdown(
        f"""
        <div class="sensor-card">

            <div class="sensor-name">
                🌡️ TEMPERATURE
            </div>

            <div class="sensor-value">
                {temperature:.1f} °C
            </div>

            <div class="sensor-status">
                {temp_status(temperature)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with c2:
    st.markdown(
        f"""
        <div class="sensor-card">

            <div class="sensor-name">
                💧 MOISTURE
            </div>

            <div class="sensor-value">
                {moisture:.0f} %
            </div>

            <div class="sensor-status">
                {moisture_status(moisture)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with c3:
    st.markdown(
        f"""
        <div class="sensor-card">

            <div class="sensor-name">
                🧪 pH
            </div>

            <div class="sensor-value">
                {ph:.2f}
            </div>

            <div class="sensor-status">
                {ph_status(ph)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )



