import os
import telebot
from api_interaction.weather_agent import WeatherAgent
from dotenv import load_dotenv
from prediction.data_preprocessing import load_weather_json, prepare_prophet_input
from prediction.predictor import load_prophet_model, predict_sales

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hola! Envíame el nombre de una ciudad y te diré el clima, el pronóstico de mañana y la predicción de ventas.")

@bot.message_handler(func=lambda message: True)
def handle_city(message):
    city = message.text.strip()
    agent = WeatherAgent()
    clima = agent.get_weather(city)
    pronostico = agent.get_tomorrow_forecast(city)
    agent.save_weather_json(city)
    # Predicción de ventas
    weather = load_weather_json("weather_result.json")
    if weather["temp"] is not None and weather["avg_temp"] is not None:
        prophet_input = prepare_prophet_input(weather)
        model = load_prophet_model()
        sales_pred = predict_sales(prophet_input, model)
        result = f"{clima}\n{pronostico}\nPredicción de ventas para mañana: {sales_pred:.2f}"
    else:
        result = f"{clima}\n{pronostico}\nNo se pudo realizar la predicción de ventas."
    bot.send_message(message.chat.id, result)

if __name__ == "__main__":
    print("Bot de Telegram iniciado...")
    bot.polling()
