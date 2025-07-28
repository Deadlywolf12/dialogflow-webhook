# WeatherBot AI Backend 🌦️🤖

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-orange.svg)](https://huggingface.co/)

A high-performance Flask backend server that uses AI to understand weather-related queries and provides intelligent responses using OpenWeatherMap API.

## ✨ Features

- **AI-Powered Intent Classification**  
  Custom NLP model trained to classify 20+ weather-related intents (temperature, rain, wind, clothing advice, etc.)
  
- **Smart Caching Layer**  
  Redis/SimpleCache implementation with 20-minute expiry to optimize API calls

- **Modular Architecture**  
  Clean separation of concerns with dedicated modules for:
  - Intent handling
  - Weather data processing
  - Response generation
  - Error management

- **Production-Ready**  
  Includes:
  - Proper exception handling
  - Rate limiting
  - Request validation
  - Comprehensive logging
 ## 🔗 Related Projects

- 📱 **Flutter Weather App**  
  [github.com/Deadlywolf12/weather_bloc_app](https://github.com/Deadlywolf12/weather_bloc_app)  
  *(Companion mobile app using this backend)*

- 🧠 **NLP Model for Intent Classification**  
  [github.com/Deadlywolf12/Ai-NLP-model](https://github.com/Deadlywolf12/Ai-NLP-model)  
  *(Custom transformer model used to understand user queries)*

  ## 🚀 Installation

### step:1 Clone the repository:

```bash
git clone https://github.com/yourusername/weatherbot-backend.git
cd weatherbot-backend
```

### step:2 Set up environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### step:3 Install dependencies:

```bash
pip install -r requirements.txt
```

### step:3 Configure environment variables:

```bash
cp .env.example .env
# Add your OpenWeatherMap API key
```






## 🛠️ System Architecture

```mermaid
flowchart TD
    A[User Request] --> B[Flask Server]
    B --> C[AI Model\nIntent Classification]
    C --> D{Intent Type?}
    D -->|Weather Intent| E[Cache Check]
    D -->|General Intent| F[Direct Response]
    E -->|Cache Hit| G[Return Cached Data]
    E -->|Cache Miss| H[OpenWeatherMap API]
    H --> I[Process & Cache]
    I --> J[Generate Response]
    G --> J
    J --> K[User Response]



