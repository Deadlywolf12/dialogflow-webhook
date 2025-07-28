import requests
from typing import Optional, Dict, Any
from config import Config
import logging

def get_weather_by_coords(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    try:
        url = f"{Config.WEATHER_API_URL}?lat={lat}&lon={lon}&appid={Config.OPENWEATHER_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Weather API error: {e}")
        return None