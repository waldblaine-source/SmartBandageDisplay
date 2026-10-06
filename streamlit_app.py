import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(
    page_title="Smart Bandage",
    page_icon="🩹",
    layout="wide",
    initial_sidebar_state="collapsed",
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
        background: rgba(46, 160, 67, .12);
        border: 1px solid rgba(46, 160, 67, .3);
    }

    .small-muted {
        font-size: .85rem;
        opacity: .65;
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
            🟢 <b>Bandage connected</b><br>
            <span class="small-muted">
                Prototype / simulated data
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()


# ---------------------------------------------------------
# Prototype controls
# ---------------------------------------------------------

with st.sidebar:
    st.header("Prototype Controls")

    simulate = st.toggle(
        "Simulate live data",
        value=True
    )

    sample_rate = st.slider(
        "Sample interval (seconds)",
        1,
        10,
        3
    )

    history_minutes = st.slider(
        "History shown (minutes)",
        5,
        60,
        20
    )


# ---------------------------------------------------------
# Initialize simulated history
# ---------------------------------------------------------

if "history" not in st.session_state:

    now = pd.Timestamp.now()

    times = pd.date_range(
        end=now,
        periods=60,
        freq="30s"
    )

    rng = np.random.default_rng(7)

    st.session_state.history = pd.DataFrame({
        "Time": times,

        "Temperature":
            36.7 + rng.normal(0, 0.08, 60),

        "Moisture":
            60 + rng.normal(0, 2.0, 60),

        "pH":
            7.1 + rng.normal(0, 0.04, 60),
    })


# ---------------------------------------------------------
# Simulated sensor reading
# ---------------------------------------------------------

def add_simulated_reading():

    history = st.session_state.history

    last = history.iloc[-1]

    rng = np.random.default_rng()

    new_row = {
        "Time": pd.Timestamp.now(),

        "Temperature":
            float(
                last["Temperature"]
                + rng.normal(0, 0.04)
            ),

        "Moisture":
            float(
                np.clip(
                    last["Moisture"]
                    + rng.normal(0, 0.8),
                    0,
                    100
                )
            ),

        "pH":
            float(
                np.clip(
                    last["pH"]
                    + rng.normal(0, 0.025),
                    4.5,
                    9.0
                )
            ),
    }

    st.session_state.history = pd.concat(
        [
            history,
            pd.DataFrame([new_row])
        ],
        ignore_index=True
    )


if simulate:
    add_simulated_reading()


# ---------------------------------------------------------
# Select displayed history
# ---------------------------------------------------------

data = st.session_state.history.copy()

cutoff = (
    pd.Timestamp.now()
    - pd.Timedelta(minutes=history_minutes)
)

data = data[
    data["Time"] >= cutoff
].copy()

latest = data.iloc[-1]


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

st.subheader("Current readings")

c1, c2, c3 = st.columns(3)


# Temperature
with c1:

    st.markdown(
        f"""
        <div class="sensor-card">

            <div class="sensor-name">
                🌡️ TEMPERATURE
            </div>

            <div class="sensor-value">
                {latest["Temperature"]:.1f} °C
            </div>

            <div class="sensor-status">
                {temp_status(latest["Temperature"])}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# Moisture
with c2:

    st.markdown(
        f"""
        <div class="sensor-card">

            <div class="sensor-name">
                💧 MOISTURE
            </div>

            <div class="sensor-value">
                {latest["Moisture"]:.0f} %
            </div>

            <div class="sensor-status">
                {moisture_status(latest["Moisture"])}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# pH
with c3:

    st.markdown(
        f"""
        <div class="sensor-card">

            <div class="sensor-name">
                🧪 pH
            </div>

            <div class="sensor-value">
                {latest["pH"]:.2f}
            </div>

            <div class="sensor-status">
                {ph_status(latest["pH"])}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# Sensor trends
# ---------------------------------------------------------

st.write("")

st.subheader("Sensor trends")

tab1, tab2, tab3 = st.tabs([
    "Temperature",
    "Moisture",
    "pH"
])


with tab1:

    chart_data = data.set_index("Time")[[
        "Temperature"
    ]]

    st.line_chart(
        chart_data,
        height=300
    )

    st.caption(
        "Temperature trend from the bandage sensor."
    )


with tab2:

    chart_data = data.set_index("Time")[[
        "Moisture"
    ]]

    st.line_chart(
        chart_data,
        height=300
    )

    st.caption(
        "Moisture trend from the nylon-tape sensor."
    )


with tab3:

    chart_data = data.set_index("Time")[[
        "pH"
    ]]

    st.line_chart(
        chart_data,
        height=300
    )

    st.caption(
        "PANI/SPCE pH measurement after calibration."
    )


# ---------------------------------------------------------
# System information
# ---------------------------------------------------------

st.divider()

info1, info2, info3 = st.columns(3)


with info1:

    st.metric(
        "Last update",
        latest["Time"].strftime("%H:%M:%S")
    )


with info2:

    st.metric(
        "Samples",
        len(data)
    )


with info3:

    st.metric(
        "Connection",
        "BLE prototype"
        if not simulate
        else "Simulation"
    )


st.caption(
    "Prototype interface only. Simulated values are "
    "not clinical measurements."
)


# ---------------------------------------------------------
# Live refresh
# ---------------------------------------------------------

if simulate:

    time.sleep(sample_rate)

    st.rerun()
