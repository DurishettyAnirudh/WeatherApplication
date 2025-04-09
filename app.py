import streamlit as st
from utils.weather_api import get_coordinates, get_current_weather, get_forecast
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide", page_title="🌍 Weather Dashboard")
# Custom CSS for reducing font sizes
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 14px !important;
    }
    h2, h3, h4, h5, h6 {
        font-size: 16px !important;
    }
    .stTextInput > div > input {
        font-size: 14px !important;
    }
    .stMetric {
        font-size: 14px !important;
    }
    .stButton button {
        font-size: 14px !important;
    }
    .css-1r6slb0 {
        font-size: 13px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌦️ Feature-Rich Weather Dashboard")

# Create main columns
col2, col1 = st.columns([1, 2])

# ====================== RIGHT COLUMN ==========================
with col2:
    st.subheader("🔎 Search Location")

    with st.form("location_form"):
        location = st.text_input("Enter location (city, state, or country)", "Hyderabad")
        fetch = st.form_submit_button("Fetch Weather Data")

# Only fetch when button clicked
if fetch:
    try:
        lat, lon = get_coordinates(location)
        city = location.title()

        # Fetch data
        forecast = get_forecast(lat, lon, city)
        current = get_current_weather(lat, lon, city)

        # Parse forecast into DataFrame
        df = pd.DataFrame(forecast["list"])
        df["temp"] = df["main"].apply(lambda x: x["temp"] - 273.15)
        df["feels_like"] = df["main"].apply(lambda x: x["feels_like"] - 273.15)
        df["temp_min"] = df["main"].apply(lambda x: x["temp_min"] - 273.15)
        df["temp_max"] = df["main"].apply(lambda x: x["temp_max"] - 273.15)
        df["humidity"] = df["main"].apply(lambda x: x["humidity"])
        df["pressure"] = df["main"].apply(lambda x: x["pressure"])
        df["wind_speed"] = df["wind"].apply(lambda x: x["speed"])
        df["wind_deg"] = df["wind"].apply(lambda x: x["deg"])
        df["dt_txt"] = pd.to_datetime(df["dt_txt"])

        # ============ LEFT COLUMN: CHARTS =============
        with col1:
            # ========= CHART GRID (2x2 Layout) =========
            st.subheader(f"📊 5-Day Forecast Overview: {city}")

            row1_col1, row1_col2 = st.columns(2)
            row2_col1, row2_col2 = st.columns(2)

            # --- Temperature Chart ---
            with row1_col1:
                st.markdown("### 🌡️ Temperature Forecast")
                fig_temp = go.Figure()
                fig_temp.add_trace(go.Scatter(x=df["dt_txt"], y=df["temp"], mode="lines+markers", name="Temp"))
                fig_temp.add_trace(go.Scatter(x=df["dt_txt"], y=df["temp_min"], mode="lines", name="Min Temp"))
                fig_temp.add_trace(go.Scatter(x=df["dt_txt"], y=df["temp_max"], mode="lines", name="Max Temp"))
                fig_temp.update_layout(xaxis_title="Date", yaxis_title="Temperature (°C)", height=300)
                st.plotly_chart(fig_temp, use_container_width=True)

            # --- Humidity Chart ---
            with row1_col2:
                st.markdown("### 💧 Humidity Over Time")
                fig_humidity = go.Figure()
                fig_humidity.add_trace(go.Bar(x=df["dt_txt"], y=df["humidity"], name="Humidity", marker_color="skyblue"))
                fig_humidity.update_layout(xaxis_title="Date", yaxis_title="Humidity (%)", height=300)
                st.plotly_chart(fig_humidity, use_container_width=True)

            # --- Pressure Chart ---
            with row2_col1:
                st.markdown("### 📈 Pressure Over Time")
                fig_pressure = go.Figure()
                fig_pressure.add_trace(go.Scatter(x=df["dt_txt"], y=df["pressure"], mode="lines+markers", name="Pressure", line_color="orange"))
                fig_pressure.update_layout(xaxis_title="Date", yaxis_title="Pressure (hPa)", height=300)
                st.plotly_chart(fig_pressure, use_container_width=True)

            # --- Wind Speed Chart ---
            with row2_col2:
                st.markdown("### 🌬️ Wind Speed Over Time")
                fig_wind = go.Figure()
                fig_wind.add_trace(go.Scatter(x=df["dt_txt"], y=df["wind_speed"], mode="lines+markers", name="Wind Speed", line_color="green"))
                fig_wind.update_layout(xaxis_title="Date", yaxis_title="Speed (m/s)", height=300)
                st.plotly_chart(fig_wind, use_container_width=True)

        # ============ RIGHT COLUMN: METRICS ============
        with col2:
            st.subheader(f"🌤️ Current Weather in {city}")
            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("🌡️ Temp", f"{current['main']['temp'] - 273.15:.1f} °C")
            metric_col2.metric("🤔 Feels Like", f"{current['main']['feels_like'] - 273.15:.1f} °C")

            metric_col3, metric_col4 = st.columns(2)
            metric_col3.metric("💧 Humidity", f"{current['main']['humidity']} %")
            metric_col4.metric("🔽 Pressure", f"{current['main']['pressure']} hPa")

            metric_col5, metric_col6 = st.columns(2)
            metric_col5.metric("🌬️ Wind Speed", f"{current['wind']['speed']} m/s")
            metric_col6.metric("☁️ Cloudiness", f"{current['clouds']['all']} %")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
else:
    st.info("📍 Use the search box on the right to begin.")
