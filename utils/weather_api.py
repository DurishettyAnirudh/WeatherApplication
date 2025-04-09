import requests
from geopy.geocoders import Nominatim
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Load API and MongoDB credentials
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
MONGO_URI = os.getenv("MONGODB_URI")

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["weather_dashboard"]
current_collection = db["current_weather"]
forecast_collection = db["forecast_data"]

# Geolocation
def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="geo_api")
    location = geolocator.geocode(location_name)
    if not location:
        raise ValueError("Location not found.")
    return round(location.latitude, 2), round(location.longitude, 2)

# Current weather
def get_current_weather(lat, lon, city):
    cached = current_collection.find_one({"city": city})
    if cached and (datetime.utcnow().timestamp() - cached["timestamp"] < 600):
        return cached["data"]
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    current_collection.update_one(
        {"city": city},
        {"$set": {"data": response, "timestamp": datetime.utcnow().timestamp()}},
        upsert=True
    )
    return response

# Forecast
def get_forecast(lat, lon, city):
    cached = forecast_collection.find_one({"city": city})
    if cached and (datetime.utcnow().timestamp() - cached["timestamp"] < 1800):
        return cached["data"]
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    forecast_collection.update_one(
        {"city": city},
        {"$set": {"data": response, "timestamp": datetime.utcnow().timestamp()}},
        upsert=True
    )
    return response
