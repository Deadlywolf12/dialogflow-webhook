import os
import requests
from flask import Flask, jsonify, request
from datetime import datetime, timezone
from pytz import timezone
from timezonefinder import TimezoneFinder
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch


# Loading model from hugging face
# adding model to cache
# os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface"

# model_name = "Deadlywolf12/Weather_chatbot_Ai_Model"  # Replace with your actual HF repo name
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)




def detect_intent(message: str) -> str:
    msg = message.lower()
    if any(word in msg for word in ["umbrella", "rain", "wet"]):
        return "UmbrellaAdvice"
    elif any(word in msg for word in ["wear", "clothes", "dress", "jacket", "hot", "cold"]):
        return "ClothingAdvice"
    elif "sunset" in msg:
        return "SunSetQuery"
    elif "sunrise" in msg:
        return "SunRiseQuery"
    elif "walk" in msg:
        return "TimeForWalk"
    elif any(word in msg for word in ["weather", "temperature", "forecast", "today"]):
        return "todayWeather"
    elif any(word in msg for word in ["ty", "thanks", "thank you", "shukriya","good"]):
        return "thanking"
    elif any(word in msg for word in ["morning", "hi", "hello","help","afternoon","noon","evening","salam"]):
        return "greetings"
    else:
        return "Unknown"

# def detect_intent(message: str) -> str:
#     inputs = tokenizer(message, return_tensors="pt", truncation=True, padding=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#         logits = outputs.logits
#         predicted_class_id = logits.argmax().item()

#     labels = model.config.id2label  # e.g., {0: "greetings", 1: "todayWeather", ...}
#     return labels[predicted_class_id]





app = Flask(__name__)




@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    payload = req.get("originalDetectIntentRequest", {}).get("payload", {})
    lat = payload.get("latitude")
    long = payload.get("longitude")
    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lat=lat, lng=long)  # e.g. "Asia/Karachi"
    local_tz = timezone(tz_str)

    user_message = req.get("queryResult", {}).get("queryText", "")
    # vec = vectorizer.transform([user_message])
    # intent = model.predict(vec)[0]
    intent = detect_intent(user_message)

    api_key = os.getenv("OPENWEATHER_KEY")
    print("Predicted Intent:", intent)
    



    if not api_key:
        return jsonify({"fulfillmentText": "Missing weather API key!"})

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={api_key}&units=metric"
    weather = requests.get(url).json()
    
    condition = weather.get("weather", [{}])[0].get("main", "").lower()
    description = weather.get("weather", [{}])[0].get("description", "").lower()
    temp = weather.get("main", {}).get("temp", 0)
    sunset = weather.get("sys", {}).get("sunset", 0)
    sunrise = weather.get("sys", {}).get("sunrise", 0)
    windSpeed = weather.get("wind", {}).get("speed", 0)
    feelsLike = weather.get("main", {}).get("feels_like", 0)
    lowTemp = weather.get("main", {}).get("temp_min", 0)
    highTemp = weather.get("main", {}).get("temp_max", 0)

    rainy_conditions = ["rain", "drizzle", "thunderstorm", "shower"]

    if intent == "UmbrellaAdvice":
        if any(word in condition for word in rainy_conditions) or "rain" in description:
            response = "Yes,Its raining outside take an umbrella!"
        else:
            response = "No umbrella needed. there's no raining outside"

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

    elif intent == "SunSetQuery":
        sunset_local = datetime.fromtimestamp(sunset, tz=local_tz)
        response = f"Sunset is at {sunset_local.strftime('%I:%M %p')}."


    elif intent == "SunRiseQuery":
        sunrise_local = datetime.fromtimestamp(sunrise, tz=local_tz)
        response = f"Sunrise is at {sunrise_local.strftime('%I:%M %p')}."

    elif intent == "TimeForWalk":
        now = datetime.now(local_tz).timestamp()
        if now < sunrise or now > sunset:
            response = "It’s already dark outside. If you still want to walk, make sure it's a safe area."
        elif any(word in condition for word in rainy_conditions):
            response = "It might not be a good time — it's currently raining outside."
        elif temp >= 35:
            response = "It's a bit too hot outside. Maybe wait until it cools down."
        elif temp <= 5:
            response = "It's quite cold right now. If you go out, dress warmly!"
        else:
            response = "Yes, it's a great time for a walk! The weather is clear and pleasant."

    elif intent =="todayWeather":
        response = (
    f"Here's what the weather looks like today:\n\n"
    f"• 🌦 Weather: {description.capitalize()}\n"
    f"• 🌡 Temperature: {temp}°C (Feels like {feelsLike}°C)\n"
    f"• 🔼 Max Temp: {highTemp}°C\n"
    f"• 🔽 Min Temp: {lowTemp}°C\n"
    f"• 💨 Wind Speed: {windSpeed} m/s\n\n"
    f"Don't forget to dress accordingly. Stay safe and enjoy your day!"
    
)
    elif intent == "thanking":
        response = "Your Welcome, Happy to Help, let me know if you need help with other thing"
    elif intent == "greetings":
        response = "Hello there! How can i help you today?"




    else:
        response = ("Oops, I didn’t quite catch that. Could you please rephrase?\n\n"
                    "• You can ask me things like:\n"
                   "• What's the weather like today?\n"
                    "• What should I wear?\n"
                    "• When’s the best time to go for a walk?")

    return jsonify({"fulfillmentText": response})


if __name__ == "__main__":
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))

