import os
from flask import Flask, jsonify, request
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from cache import cache 
from handle_intents import handle_intents
import logging



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)

# Loading model from Hugging Face
os.environ['HF_HOME'] = "/tmp/huggingface"
model_name = "Deadlywolf12/Weather_chatbot_Ai_Model" 

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    logging.info("AI model loaded successfully")
except Exception as e:
    logging.error(f"Failed to load AI model: {str(e)}")
    raise

app = Flask(__name__)
cache.init_app(app)

def detect_intent(message: str) -> tuple[str, float]:
    """Detect intent from user message"""
    inputs = tokenizer(message, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)
        predicted_class_id = probs.argmax().item()
        confidence = probs[0][predicted_class_id].item()

    intent = model.config.id2label[predicted_class_id]
    logging.info(f"Detected intent: {intent} (Confidence: {confidence:.2f})")
    
    return intent, confidence

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json()
        payload = req.get("originalDetectIntentRequest", {}).get("payload", {})
        lat = payload.get("latitude")
        long = payload.get("longitude")
        user_message = req.get("queryResult", {}).get("queryText", "")

        intent, confidence = detect_intent(user_message)
        
        if confidence > 0.9:
            response_text = handle_intents(intent, lat, long, user_message)
        else:
            response_text = (
                "Oops, I didn't quite catch that. Could you please rephrase?\n\n"
                "• You can ask me things like:\n"
                "• What's the weather like today?\n"
                "• What should I wear?\n"
                "• When's the best time to go for a walk?"
            )
        
        return jsonify({"fulfillmentText": response_text})
    
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({"fulfillmentText": "Sorry, I encountered an error processing your request"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)