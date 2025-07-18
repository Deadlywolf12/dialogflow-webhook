import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    payload = req.get("originalDetectIntentRequest", {}).get("payload", {})
    lat = payload.get("latitude")
    long = payload.get("longitude")

    intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
    api_key = os.getenv("OPENWEATHER_KEY")

    if not api_key:
        return jsonify({"fulfillmentText": "Missing weather API key!"})

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={api_key}&units=metric"
    weather = requests.get(url).json()
    
    condition = weather.get("weather", [{}])[0].get("main", "").lower()
    description = weather.get("weather", [{}])[0].get("description", "").lower()
    temp = weather.get("main", {}).get("temp", 0)

    rainy_conditions = ["rain", "drizzle", "thunderstorm", "shower"]

    if intent == "UmbrellaAdvice":
        if any(word in condition for word in rainy_conditions) or "rain" in description:
            response = "Yes, take an umbrella!"
        else:
            response = "No umbrella needed."

    elif intent == "ClothingAdvice":
        if temp <= 10:
            response = "It's quite cold. Wear a warm coat, scarf, and gloves."
        elif 10 < temp <= 20:
            response = "Cool weather. A jacket or hoodie would be good."
        elif 20 < temp <= 30:
            response = "Warm weather. Light clothes like t-shirts are fine."
        else:
            response = "It's hot outside! Wear shorts and stay hydrated."
        
        if any(word in condition for word in rainy_conditions):
            response += " Also, take a raincoat or umbrella."

    else:
        response = "Sorry, I can't help with that."

    return jsonify({"fulfillmentText": response})


if __name__ == "__main__":
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))

