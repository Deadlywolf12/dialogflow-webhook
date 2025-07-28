from config import Config
import requests
from typing import Optional, Dict, Any
import logging

def make_aqi_req_to_api(lat,lon)-> Optional[Dict[str,Any]]:
    try:
        url = f"{Config.AQI_API_URL}?lat={lat}&lon={lon}&appid={Config.OPENWEATHER_KEY}"
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Weather API error: {e}")
        return None