```python
import streamlit as st

st.set_page_config(
    page_title="Smart Bandage",
    page_icon="🩹",
    layout="wide"
)

# -----------------------------
# Page title
# -----------------------------

st.title("🩹 Smart Bandage")
st.caption("Wound monitoring system")

st.divider()

# -----------------------------
# Sensor inputs
# -----------------------------

st.subheader("Sensor Input")

col1, col2, col3 = st.columns(3)

with col1:
    temperature = st.number_input(
        "Temperature (°C)",
        value=36.8,
        step=0.1
    )

with col2:
    moisture = st.number_input(
        "Moisture (%)",
        value=60.0,
        step=1.0
    )

with col3:
    ph = st.number_input(
        "pH",
        value=7.0,
        step=0.1
    )

st.divider()

# -----------------------------
# Current readings
# -----------------------------

st.subheader("Current Readings")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Temperature",
        f"{temperature:.1f} °C"
    )

with col2:
    st.metric(
        "Moisture",
        f"{moisture:.0f} %"
    )

with col3:
    st.metric(
        "pH",
        f"{ph:.1f}"
    )

st.divider()

# -----------------------------
# Connection status
# -----------------------------

st.caption("● Sensor connection: Prototype / Manual Input")
```
