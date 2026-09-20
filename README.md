# 🌤 Weather API

A professional command-line weather application built with Python and the Open-Meteo API.

The application allows users to search for a city and retrieve current weather conditions, a 24-hour forecast, and a 7-day forecast.

## 🚀 Features

- 🌍 Search weather by city name
- 🌡 Current temperature
- 💧 Current humidity
- 🌧 Precipitation probability
- 💨 Wind speed
- 🌤 Weather condition descriptions
- 🕐 Local time
- 📅 24-hour weather forecast
- 📆 7-day weather forecast
- ⚠️ API error handling
- 🔌 Connection and timeout handling
- 🧪 Automated tests with pytest
- 🧩 Modular project architecture

## 🛠 Technologies

- Python
- Requests
- Pytest
- Open-Meteo API
- Git & GitHub

## 📁 Project Structure

```text
weather-api/
│
├── src/
│   └── weather_app/
│       ├── __init__.py
│       ├── main.py
│       ├── api.py
│       ├── services.py
│       ├── display.py
│       ├── constants.py
│       └── exceptions.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_services.py
│
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
