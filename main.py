from api_interaction.weather_agent import WeatherAgent
from dotenv import load_dotenv
import json
from prediction.data_preprocessing import load_weather_json, prepare_prophet_input
from prediction.predictor import load_prophet_model, predict_sales

load_dotenv()

if __name__ == "__main__":
    city = input("¿De qué ciudad quieres saber el clima? ")
    agent = WeatherAgent()
    print(agent.get_weather(city))
    print(agent.get_tomorrow_forecast(city))
    agent.save_weather_json(city)

    # --- Predicción de ventas ---
    weather = load_weather_json("weather_result.json")
    if weather["temp"] is not None and weather["avg_temp"] is not None:
        prophet_input = prepare_prophet_input(weather)
        model = load_prophet_model()
        sales_pred = predict_sales(prophet_input, model)
        print(f"Predicción de ventas para mañana: {sales_pred:.2f}")
        # Guardar todo en un JSON
        result = weather.copy()
        result["sales_prediction"] = sales_pred
        with open("weather_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        print("No se pudo obtener el clima o el pronóstico, no se realiza la predicción de ventas.")
