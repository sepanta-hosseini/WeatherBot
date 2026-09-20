import requests

weather_descriptions = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️",
    2: "Partly cloudy ⛅",
    3: "Overcast ☁️",
    45: "Fog 🌫️",
    48: "Depositing rime fog 🌫️",
    51: "Light drizzle 🌦️",
    53: "Moderate drizzle 🌦️",
    55: "Dense drizzle 🌧️",
    56: "Light freezing drizzle 🧊🌧️",
    57: "Dense freezing drizzle 🧊🌧️",
    61: "Slight rain 🌧️",
    63: "Moderate rain 🌧️",
    65: "Heavy rain 🌧️",
    66: "Light freezing rain 🧊🌧️",
    67: "Heavy freezing rain 🧊🌧️",
    71: "Slight snow 🌨️",
    73: "Moderate snow 🌨️",
    75: "Heavy snow ❄️",
    77: "Snow grains ❄️",
    80: "Slight rain showers 🌦️",
    81: "Moderate rain showers 🌦️",
    82: "Violent rain showers ⛈️",
    85: "Slight snow showers 🌨️",
    86: "Heavy snow showers ❄️",
    95: "Thunderstorm ⛈️",
    96: "Thunderstorm with slight hail ⛈️🧊",
    99: "Thunderstorm with heavy hail ⛈️🧊"
}

def get_weather_data(latitude, longitude):
    """
    Fetches weather data for the given coordinates.
    """
    daily_params = "daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code&"
    hourly_params = "hourly=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m&"
    current_params = "current=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m"
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&{current_params}&timezone=auto&{hourly_params}{daily_params}"
    response_weather = requests.get(url=weather_url)
    return response_weather

def current_weather(current, current_units):
    """
    Returns a formatted string with the current weather information.
    """
    temperature = f"{current['temperature_2m']} {current_units['temperature_2m']}"
    humidity = f"{current['relative_humidity_2m']} {current_units['relative_humidity_2m']}"
    precipitation = f"{current['precipitation_probability']} {current_units['precipitation_probability']}"
    wind_speed = f"{current['wind_speed_10m']} {current_units['wind_speed_10m']}"
    weather_code = current["weather_code"]

    return temperature,\
        humidity,\
        precipitation,\
        wind_speed,\
        get_weather_description(weather_code)

def get_weather_description(weather_code):
    """
    Returns a description of the weather based on the weather code.
    """
    return weather_descriptions[weather_code] if weather_code in weather_descriptions else "Unknown weather code"

def daily_weather(daily):
    dates = daily["time"]
    max_temperatures = daily["temperature_2m_max"]
    min_temperatures = daily["temperature_2m_min"]
    precipitation_sums = daily["precipitation_sum"]
    weather_codes = daily["weather_code"]

    for i in range(len(dates)):
        print(f"Date: {dates[i]}\
        \nMax Temperature: {max_temperatures[i]}°C\
        \nMin Temperature: {min_temperatures[i]}°C\
        \nPrecipitation: {precipitation_sums[i]} mm\
        \nWeather Code: {get_weather_description(weather_codes[i])}\n")

