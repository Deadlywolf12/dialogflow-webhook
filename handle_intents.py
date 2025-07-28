


from weather_data import WeatherData
from responses import Responses,get_temp_response,get_humidity_response,get_wind_response,get_air_quality_response,get_weather_response,get_sunrise_sunset_responses
import random
from datetime import timezone,datetime
from pytz import timezone
from timezonefinder import TimezoneFinder
from weather_by_city import extract_city_name,parse_weather_response
from cache import get_cached_city_weather
from typing import Optional,Dict,Any



def handle_intents(intent,lat,long,user_message)->str:
    #defined intents that needs weather data
    weather_related_intents = {
        "rain_query", "temp_query", "wind_query", "air_query", 
        "clothing_advice", "walk_query", "cycle_query", "outing_query","weather_query","humid_query"
    }

    rainy_conditions = ["rain", "drizzle", "thunderstorm", "shower"]
    res = Responses()
    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lat=lat, lng=long)  # e.g. "Asia/Karachi"
    local_tz = timezone(tz_str)
    wd =WeatherData(lat,long)


    #   we are only going to get data if the intent requires else we show simple response 
    if intent in weather_related_intents:
        metrics = wd.get_weather_metrics()
        if not metrics:
            return "could'nt process your request right now"
    else:
        metrics = None

    match intent:
            case "rain_query":
                if any(word in metrics['condition'] for word in rainy_conditions) or "rain" in metrics['description']:
                    response = get_random_item(res.rain_response)
                else:
                    response = get_random_item(res.no_rain_responses)

            case "clothing_advice":
                if metrics['temp'] <= 10:
                    response = get_random_item(res.cold_weather_responses)
                elif 10 < metrics['temp'] <= 20:
                    response = get_random_item(res.cool_weather_responses)
                elif 20 < metrics['temp'] <= 30:
                    response = get_random_item(res.warm_weather_responses)
                else:
                    response = get_random_item(res.hot_weather_responses)
        
                if any(word in metrics['condition'] for word in rainy_conditions):
                    response += "Also, take a raincoat or umbrella."

            case "sun_query":
                sunset_local = datetime.fromtimestamp(metrics['sunset'], tz=local_tz)
                sunrise_local = datetime.fromtimestamp(metrics['sunrise'], tz=local_tz)
                sunrise_local= sunrise_local.strftime('%I:%M %p')
                sunset_local = sunset_local.strftime('%I:%M %p')
       
                response = get_random_item(get_sunrise_sunset_responses(sunrise_local,sunset_local))

            case "walk_query":
                now = datetime.now(local_tz).timestamp()
                if now < metrics['sunrise'] or now > metrics['sunset']:
                    response = get_random_item(res.dark_walk_responses)
                elif any(word in metrics['condition'] for word in rainy_conditions):
                    response = get_random_item(res.raining_walk_responses)
                elif metrics['temp'] >= 35:
                    response = get_random_item(res.too_hot_walk_responses)
                elif metrics['temp'] <= 5:
                    response = get_random_item(res.too_cold_walk_responses)
                else:
                    response = get_random_item(res.perfect_walk_responses)

            case "weather_query":
                response = get_random_item(get_weather_response(metrics['description'], metrics['temp'],metrics['feelsLike'],metrics['highTemp'],metrics['lowTemp'],metrics['windSpeed']))
            case "agree_query":
                response = get_random_item(res.agree_responses)

            case "greeting":
                response = get_random_item(res.greeting_responses)
            case "farewell":
                response = get_random_item(res.farewell_responses)


            case "small_talk":
                response = get_random_item(res.small_talk_responses)

            case "neg_res":
                response = get_random_item(res.neg_responses)

            case "help":
                response = get_random_item(res.help_responses)

            case "confused":
                response = get_random_item(res.confused_responses)

            

            case "temp_query":
                response = get_random_item(get_temp_response(metrics['temp']))

            case "humid_query":
                response = get_random_item(get_humidity_response(metrics['humid']))

            case "wind_query":
                response = get_random_item(get_wind_response(metrics['windSpeed']))
       
            case "air_query":
                response =  get_air_quality_response(metrics['aqi'],metrics['pm2_5'],metrics['pm10'] ,metrics['co'] ,metrics['no2'] ,metrics['o3'])

            case "mood_good":
                response = get_random_item(res.good_mood_responses)
            case "mood_bad":
                response = get_random_item(res.bad_mood_responses)
            case "cycle_query":
                now = datetime.now(local_tz).timestamp()
                if now < metrics['sunrise'] or now > metrics['sunset']:
                    response = get_random_item(res.dark_cycle_responses)

                elif any(word in metrics['condition'] for word in rainy_conditions):
                    return get_random_item(res.rainy_cycle_responses)
                elif metrics['temp'] > 38:
                    return get_random_item(res.hot_cycle_responses)
                elif metrics['temp'] < 10:
                    return get_random_item(res.cold_cycle_responses)
                elif metrics['aqi'] >= 4:
                    return get_random_item(res.bad_air_cycle_responses)
                else:
                    response = get_random_item(res.perfect_cycle_responses)

            case "outing_query":
                now = datetime.now(local_tz).timestamp()
                if now < metrics['sunrise'] or now > metrics['sunset']:
                    response = get_random_item(res.dark_outing_responses)

                elif any(word in metrics['condition'] for word in rainy_conditions):
                    return get_random_item(res.rainy_outing_responses)
                elif metrics['temp'] > 38:
                    return get_random_item(res.hot_outing_responses)
                elif metrics['temp'] < 10:
                    return get_random_item(res.cold_outing_responses)
                elif metrics['aqi'] >= 4:
                    return get_random_item(res.bad_air_outing_responses)
                else:
                    response = get_random_item(res.perfect_outing_responses)

            case "location_specific_weather_query":
                response =  send_city_data_if_valid(user_message)

    return response




def get_random_item(choices):
    if not choices:
        return None  
    return random.choice(choices)


def send_city_data_if_valid(message: str)->Optional[Dict[str,Any]]:
   #extract city from message here
   city = extract_city_name(message)
   if not city or len(city.strip()) <= 2:
      return f"Oops, I couldn't recognize that city - {city}. Could you double-check the name?"
   else:
      city_data = get_cached_city_weather(city)
      if isinstance(city_data,dict):
         return parse_weather_response(city_data,city)
      else:
        return f"Oops, I couldn't find weather data of {city}. Could you double-check the name?"

