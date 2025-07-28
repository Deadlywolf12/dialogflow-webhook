# config.py
import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    OPENWEATHER_KEY = os.getenv("WEATHER_API_KEY")
    CACHE_DURATION = 600  # 10 minutes
    WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
    AQI_API_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
    CITY_API_URL = "http://api.openweathermap.org/data/2.5/weather"


