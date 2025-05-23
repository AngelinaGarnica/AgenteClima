import json
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

def load_weather_json(json_path: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Función para preparar el input para Prophet
def prepare_prophet_input(weather_data: dict) -> list:
    """
    Convierte el json de clima en un formato compatible con Prophet.
    Prophet espera una lista de diccionarios con las claves 'ds' (fecha).
    y la 'temperatura' como regresora.
    """
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    return [{
        'ds': tomorrow,
        'temperature': weather_data.get('avg_temp')
    }]