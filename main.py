import os
from flask import Flask, jsonify, request
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from cache import cache 
from handle_intents import handle_intents





# Loading model from hugging face
# adding model to cache
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface"

model_name = "Deadlywolf12/Weather_chatbot_Ai_Model" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)


# detects intent from user message and return confidence and the intent itself
def detect_intent(message: str) -> tuple[str, float]:
    inputs = tokenizer(message, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_id = logits.argmax().item()
        probs = F.softmax(logits, dim=1)
        predicted_class_id = probs.argmax().item()
        confidence = probs[0][predicted_class_id].item()

    labels = model.config.id2label  # e.g., {0: "greetings", 1: "todayWeather", ...}
    return labels[predicted_class_id],confidence





app = Flask(__name__)

# initializing cache here
cache.init_app(app)



@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    payload = req.get("originalDetectIntentRequest", {}).get("payload", {})
    lat = payload.get("latitude")
    long = payload.get("longitude")
    user_message = req.get("queryResult", {}).get("queryText", "")
    intent,confidence = detect_intent(user_message)

    #for debugging
    print("Predicted Intent:", intent)
    print("confidence:", confidence)
    



    
    if confidence >0.9:

        response = handle_intents(intent,lat,long,user_message)
   
    else:
        response = ("Oops, I didn’t quite catch that. Could you please rephrase?\n\n"
                    "• You can ask me things like:\n"
                   "• What's the weather like today?\n"
                    "• What should I wear?\n"
                    "• When’s the best time to go for a walk?")

    return jsonify({"fulfillmentText": response})


if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000)

