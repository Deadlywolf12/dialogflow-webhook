from datetime import datetime, timezone
from typing import Optional, Dict, Any
from weather_api import get_weather_by_coords
from aqi_api import make_aqi_req_to_api
from flask_caching import Cache
from weather_by_city import get_weather_by_city_api_call



cache = Cache(config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 1200  # 20 minutes
})


def get_cached_weather(lat,lon)->Optional[Dict[str,Any]]:

    cache_key = f"weather_{lat}_{lon}"
    cached_data = cache.get(cache_key)
    if cached_data:
        print("using data from cache")
        return cached_data
    else:
        
        #call api and add data if data is 20 minutes old or first call
        data = get_weather_by_coords(lat,lon)
        if data:
            data['cached_at'] =  datetime.now(timezone.utc).isoformat()
            cache.set(cache_key,data)
            print("using data from api call")
            return data
        else:
            return None
        

def get_cached_aqi(lat,lon)->Optional[Dict[str,Any]]:

    cache_key = f"aqi_{lat}_{lon}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    else:
        
        #call api and add data
        data = make_aqi_req_to_api(lat,lon)
        if data:
            data['cached_at'] =  datetime.now(timezone.utc).isoformat()
            cache.set(cache_key,data)
            return data
        else:
            return None
        



def get_cached_city_weather(city)->Optional[Dict[str,Any]]:

    cache_key = f"weather_by_city_{city}"
    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"got {city} weather data from cache")
        return cached_data
    else:
        
        #call api and add data
        data = get_weather_by_city_api_call(city)
        if data:
            data['cached_at'] = datetime.now(timezone.utc).isoformat()
            cache.set(cache_key,data)
            print(f"got {city} weather data from api")
            return data
        else:
            return None
        


        









