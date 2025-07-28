import logging
import re
from typing import Optional,Dict,Any
import requests
from config import Config







def extract_city_name(message: str) -> str | None:
    
    pattern = r"\b(?:in|at|for)\s+([A-Za-z\s]{2,})"
    match = re.search(pattern, message, re.IGNORECASE)
    
    if match:
        city = match.group(1).strip()
        
        city = re.sub(r"\b(now|please|today)\b", "", city, flags=re.IGNORECASE).strip()
        return city

    return None

def get_weather_by_city_api_call(city: str)->Optional[Dict[str,Any]]:
    url = f"{Config.CITY_API_URL}?q={city}&appid={Config.OPENWEATHER_KEY}&units=metric"
    cache_key = ""
    try:
     response = requests.get(url,timeout=10)
     response.raise_for_status()

     return response.json()
    
    except requests.exceptions.RequestException as e:
       
       logging.error(f"Weather API error: {e}")
       return None
    

def parse_weather_response(response,city):
      return (
    f"🌤️ Weather update of {city}:\n"
    f"- Description: {response['weather'][0]['description'].capitalize()}\n"
    f"- Temperature: {response['main']['temp']}°C\n"
    f"- Feels like: {response['main']['feels_like']}°C\n"
    f"- High: {response['main']['temp_max']}°C | Low: {response['main']['temp_min']}°C\n"
    f"- Wind speed: {response['wind']['speed']} m/s"
      )


