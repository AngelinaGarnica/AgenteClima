# 🤖🌦️🌡️ Proyecto de Agente de IA con LangChain, LangGraph, API de Clima y Bot de Telegram

Este proyecto es una base para crear agentes inteligentes usando LangChain, LangGraph y consultar información meteorológica a través de una API de clima. Además, integra un modelo Prophet para predicción de ventas y un bot de Telegram para interacción directa.

## 📁 Estructura sugerida

- `main.py`: Ejecución local del agente, clima, pronóstico y predicción de ventas.
- `api_interaction/weather_agent.py`: Lógica del agente y conexión con la API de clima usando LangGraph.
- `api_interaction/telegram_bot.py`: Bot de Telegram para consultar clima y ventas.
- `prediction/`: Preprocesamiento y predicción con Prophet.
- `model/modelo_prophet.pkl`: Modelo Prophet serializado.
- `.env`: Variables de entorno (API keys, etc).
- `requirements.txt`: Dependencias del proyecto.
- `Dockerfile` y `docker-compose.yml`: Para ejecución en contenedor Docker.

## ⚙️ Uso rápido

### 1. Variables de entorno
Crea un archivo `.env` con tus claves de API:

```env
GOOGLE_API_KEY=tu_clave_gemini
WEATHER_API_KEY=tu_clave_weather
TELEGRAM_TOKEN=tu_token_telegram
```

- Para obtener la API key de clima: [OpenWeatherMap](https://home.openweathermap.org/api_keys)
- Para el bot de Telegram: crea uno con [@BotFather](https://t.me/BotFather)

### 2. Instalación local

Instala las dependencias:
```powershell
pip install -r requirements.txt
```

### 3. Ejecución local

Para probar el flujo completo por consola:
```powershell
python main.py
```

### 4. Bot de Telegram

Ejecuta el bot:
```powershell
python api_interaction/telegram_bot.py
```

Envíale el nombre de una ciudad y recibirás el clima, el pronóstico de mañana y la predicción de ventas.

### 5. Ejecución en Docker

Construye y ejecuta el contenedor:
```powershell
docker compose up --build
```

El bot de Telegram quedará corriendo en el contenedor.

## 🛠️ Dependencias principales
- langchain
- langgraph
- langchain-google-genai
- openai
- requests
- python-dotenv
- pyTelegramBotAPI
- prophet
- plotly (opcional, para evitar warnings de Prophet)

## 📜 Notas
- El agente ahora usa LangGraph y Gemini 2.0 Flash como LLM.
- El bot de Telegram responde automáticamente con clima, pronóstico y predicción de ventas.
- El flujo es robusto: si no se puede obtener el clima, no se realiza la predicción de ventas.
- Puedes personalizar el nombre del archivo de salida o los mensajes del bot según tus necesidades.

---

Este proyecto está listo para que agregues tus propios agentes, cadenas y modelos predictivos usando LangChain, LangGraph y Prophet.
