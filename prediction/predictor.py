import joblib
from typing import List, Dict
import pandas as pd
#from data_preprocessing import load_weather_json, prepare_prophet_input
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model/modelo_prophet.pkl')

# Cargar el modelo Prophet entrenado
def load_prophet_model(model_path: str = MODEL_PATH):
    with open(model_path, 'rb') as f:
        model = joblib.load(f)
    return model

# Realizar la predicción de ventas
def predict_sales(prophet_input: List[Dict], model=None):
    if model is None:
        model = load_prophet_model()
    df = pd.DataFrame(prophet_input)
    forecast = model.predict(df)
    # Se asume que la columna de predicción es 'yhat'
    return forecast['yhat'].iloc[0]
