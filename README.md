# 🌦️ AI-Powered Weather Dashboard

This is a feature-rich weather application built as part of the **AI Engineer Intern - Technical Assessment** for **PM Accelerator**.

---

## 📌 Overview

This Streamlit-based weather dashboard lets users search for any location using a natural input (zip code, town, GPS coordinates, landmarks, etc.) and view real-time weather and 5-day forecasts using the OpenWeatherMap API. The app also supports full CRUD operations using MongoDB for persistent storage.

---

## ✅ Features Implemented

### Tech Assessment 1 – Core Weather App

| Feature                                           | Status           |
|--------------------------------------------------|------------------|
| User input for location                          | ✅ Implemented   |
| Real-time weather info                           | ✅ Implemented   |
| Detailed weather cards (temp, wind, humidity…)   | ✅ Implemented   |
| 5-day forecast with interactive charts           | ✅ Implemented   |
| Flexible input (City, Landmark, etc.)       | ✅ Implemented   |
| API-based live weather data                      | ✅ Implemented   |
| emojis for visual context                        | ✅ Implemented   |
| Simple, effective UI (Streamlit layout)          | ✅ Implemented   |

---

### Tech Assessment 2 – Advanced App with Persistence

| Feature                                           | Status           |
|--------------------------------------------------|------------------|
| Database Persistence                             | ✅ MongoDB       |
| CRUD functionality (Create, Read, Update, Delete)| ✅ Full Support  |
| Location validation                              | ✅ Via geopy     |
| Display past requested data                      | ✅ Implemented   |
| Update or delete any stored data                 | ✅ Included      |
| Error handling for API & inputs                  | ✅ Implemented   |
| Modular code architecture                        | ✅ utils/weather_api.py |
| `.env` for secure API key handling               | ✅ Included      |

---

## 🧠 Stack Used

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:** Python, OpenWeatherMap API, Geopy
- **Database:** MongoDB (via pymongo)
- **Data Viz:** Plotly for interactive charts

---

## 📂 Project Structure

     ```bash
     📁 weather_dashboard/
     ├── app.py      ← Streamlit  frontend
     ├── utils/
     │   └── weather_api.py   ← AllMongoDB logic
     ├── .env                  ← Secure API keys
     ├── requirements.txt      ← All dependencies



---

## 🛠️ How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/weather-dashboard.git
   cd weather-dashboard

2. Install dependencies:
     ```bash
    pip install -r requirements.txt

3. Set up .env file:
    ```bash
    MONGO_URI=your_mongodb_connection_string
    OPENWEATHER_API_KEY=your_openweathermap_key

4. Run the app:

    ```bash
    streamlit run app.py