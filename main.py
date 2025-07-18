import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Dialogflow webhook running!"

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

    if intent == "UmbrellaAdvice":
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={api_key}"
        weather = requests.get(url).json()
        condition = weather.get("weather", [{}])[0].get("main", "").lower()
        response = "Yes, take an umbrella!" if "rain" in condition else "No umbrella needed."
    else:
        response = "Sorry, I can't help with that."

    return jsonify({"fulfillmentText": response})
