from cache import get_cached_weather,get_cached_aqi

class WeatherData:
   

    
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self._weather = None
        self._air = None
    
    @property
    def weather(self):
        if self._weather is None:
            self._weather = get_cached_weather(self.lat, self.lon)
        return self._weather
    
    @property
    def air(self):
        if self._air is None:
            self._air = get_cached_aqi(self.lat, self.lon)
        return self._air
    
    def get_weather_metrics(self):
       #return the data when needed only
        if not isinstance(self.weather, dict) or not isinstance(self.air, dict):
            return None
            
        aqi_data = self.air["list"][0]
        return {
            "condition": self.weather.get("weather", [{}])[0].get("main", "").lower(),
            "description": self.weather.get("weather", [{}])[0].get("description", "").lower(),
            "temp": self.weather.get("main", {}).get("temp", 0),
            "sunset": self.weather.get("sys", {}).get("sunset", 0),
            "sunrise": self.weather.get("sys", {}).get("sunrise", 0),
            "windSpeed": self.weather.get("wind", {}).get("speed", 0),
            "feelsLike": self.weather.get("main", {}).get("feels_like", 0),
            "lowTemp": self.weather.get("main", {}).get("temp_min", 0),
            "highTemp": self.weather.get("main", {}).get("temp_max", 0),
            "humid": self.weather.get("main", {}).get("humidity", 0),
            "aqi": aqi_data["main"]["aqi"],
            "pm2_5": aqi_data["components"]["pm2_5"],
            "pm10": aqi_data["components"]["pm10"],
            "co": aqi_data["components"]["co"],
            "no2": aqi_data["components"]["no2"],
            "o3": aqi_data["components"]["o3"]
        }