# Dockerfile para el bot de Telegram y agente de clima
FROM python:3.11-slim-bookworm

# Actualizar paquetes del sistema para corregir vulnerabilidades
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Variables de entorno para evitar prompts interactivos
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Añadir el directorio actual y subcarpetas al PYTHONPATH para imports relativos
ENV PYTHONPATH="/app:/app/api_interaction:/app/prediction:/app/model"

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y archivos del proyecto
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .

# Comando por defecto: ejecutar el bot de Telegram
CMD ["python", "api_interaction/telegram_bot.py"]
