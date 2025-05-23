import os
import requests
import json
import datetime
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.tools import Tool
from typing import TypedDict

load_dotenv()

# Definir el esquema de estado mínimo requerido

class AgentState(TypedDict):
    input: str

class WeatherAgent:
    def __init__(self):
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )
        self.current_weather = None
        self.tomorrow_forecast = None
        # Definir herramientas para el agente
        self.tools = [
            Tool(
                name="Weather",
                description="Obtiene el clima actual de una ciudad.",
                func=self.get_weather
            ),
            Tool(
                name="Forecast",
                description="Obtiene el pronóstico de temperatura promedio y sensación térmica para mañana en una ciudad.",
                func=self.get_tomorrow_forecast
            )
        ]
        # Crear el agente LangGraph (ReAct)
        self.agent = create_react_agent(self.llm, self.tools)
        self.graph = StateGraph(state_schema=AgentState)
        self.graph.add_node("agent", self.agent)
        self.graph.set_entry_point("agent")
        self.graph.add_edge("agent", END)
        self.graph.compile()

    def get_weather(self, city: str) -> str:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric&lang=es"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            desc = data['weather'][0]['description']
            temp = data['main']['temp']
            feels_like = data['main'].get('feels_like', None)
            self.current_weather = {
                "city": city,
                "temp": temp,
                "feels_like": feels_like
            }
            return f"El clima en {city} es '{desc}' con temperatura de {temp}°C."
        else:
            self.current_weather = None
            return f"No se pudo obtener el clima para {city}."

    def get_tomorrow_forecast(self, city: str) -> str:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.weather_api_key}&units=metric&lang=es"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            tomorrow = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)).date()
            temps = []
            feels = []
            for entry in data["list"]:
                dt = datetime.datetime.fromtimestamp(entry["dt"])
                if dt.date() == tomorrow:
                    temps.append(entry["main"]["temp"])
                    feels.append(entry["main"].get("feels_like", None))
            if temps:
                avg_temp = sum(temps) / len(temps)
                avg_feels = sum([f for f in feels if f is not None]) / len([f for f in feels if f is not None]) if any(feels) else None
                self.tomorrow_forecast = {
                    "avg_temp": avg_temp,
                    "avg_feels_like": avg_feels
                }
                return f"La temperatura promedio para mañana en {city} será de {avg_temp:.1f}°C."
            else:
                self.tomorrow_forecast = None
                return f"No se encontró pronóstico para mañana en {city}."
        else:
            self.tomorrow_forecast = None
            return f"No se pudo obtener el pronóstico para {city}."

    def save_weather_json(self, city: str, filename: str = "weather_result.json"):
        result = {
            "city": city,
            "temp": self.current_weather.get("temp") if self.current_weather else None,
            "feels_like": self.current_weather.get("feels_like") if self.current_weather else None,
            "avg_temp": self.tomorrow_forecast.get("avg_temp") if self.tomorrow_forecast else None,
            "avg_feels_like": self.tomorrow_forecast.get("avg_feels_like") if self.tomorrow_forecast else None
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
