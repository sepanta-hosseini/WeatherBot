import sys
from urllib.parse import quote

import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

REQUEST_TIMEOUT = 10
HOURLY_FORECAST_HOURS = 24
DAILY_FORECAST_DAYS = 7


WEATHER_DESCRIPTIONS = {
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
    99: "Thunderstorm with heavy hail ⛈️🧊",
}


def get_request(url, params=None):
    """
    Send a GET request and return the response.

    Handles common network-related errors.
    """

    try:
        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

        return response

    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
        sys.exit(1)

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        sys.exit(1)

    except requests.exceptions.RequestException as error:
        print(f"Error: {error}")
        sys.exit(1)


def check_response(response, service_name):
    """
    Validate the HTTP response status.
    """

    if response.ok:
        return

    print(
        f"{service_name} request failed.\n"
        f"Status code: {response.status_code}\n"
        f"Reason: {response.reason}"
    )

    sys.exit(1)


def get_city_information(city):
    """
    Search for a city using the Open-Meteo geocoding API.

    Returns the first matching city result.
    """

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    response = get_request(
        GEOCODING_URL,
        params=params,
    )

    check_response(response, "City search")

    try:
        data = response.json()

    except ValueError:
        print("Error: The server returned invalid JSON.")
        sys.exit(1)

    results = data.get("results")

    if not results:
        print(f"City not found: {city}")
        sys.exit(1)

    return results[0]


def get_weather_data(latitude, longitude):
    """
    Fetch current, hourly, and daily weather data.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation_probability,"
            "weather_code,"
            "wind_speed_10m"
        ),

        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation_probability,"
            "weather_code,"
            "wind_speed_10m"
        ),

        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_sum,"
            "weather_code"
        ),

        "forecast_hours": HOURLY_FORECAST_HOURS,
        "forecast_days": DAILY_FORECAST_DAYS,
        "timezone": "auto",
    }

    response = get_request(
        WEATHER_URL,
        params=params,
    )

    check_response(response, "Weather")

    try:
        return response.json()

    except ValueError:
        print("Error: The weather API returned invalid JSON.")
        sys.exit(1)


def get_weather_description(weather_code):
    """
    Convert a WMO weather code into a readable description.
    """

    return WEATHER_DESCRIPTIONS.get(
        weather_code,
        "Unknown weather condition",
    )


def display_current_weather(weather_data):
    """
    Display current weather information.
    """

    current = weather_data["current"]
    units = weather_data["current_units"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    precipitation = current["precipitation_probability"]
    wind_speed = current["wind_speed_10m"]
    weather_code = current["weather_code"]

    print("\n" + "=" * 45)
    print("CURRENT WEATHER")
    print("=" * 45)

    print(
        f"🌡 Temperature: "
        f"{temperature} {units['temperature_2m']}"
    )

    print(
        f"💧 Humidity: "
        f"{humidity} {units['relative_humidity_2m']}"
    )

    print(
        f"🌧 Precipitation Probability: "
        f"{precipitation} "
        f"{units['precipitation_probability']}"
    )

    print(
        f"💨 Wind Speed: "
        f"{wind_speed} {units['wind_speed_10m']}"
    )

    print(
        f"🌤 Weather: "
        f"{get_weather_description(weather_code)}"
    )


def display_hourly_weather(weather_data):
    """
    Display the next 24 hours of weather data.
    """

    hourly = weather_data["hourly"]
    units = weather_data["hourly_units"]

    times = hourly["time"]
    temperatures = hourly["temperature_2m"]
    humidities = hourly["relative_humidity_2m"]
    precipitation = hourly["precipitation_probability"]
    wind_speeds = hourly["wind_speed_10m"]
    weather_codes = hourly["weather_code"]

    print("\n" + "=" * 45)
    print("HOURLY FORECAST")
    print("=" * 45)

    for i in range(len(times)):
        print(
            f"\n🕐 {times[i]}"
            f"\n   🌡 {temperatures[i]} "
            f"{units['temperature_2m']}"
            f"\n   💧 {humidities[i]} "
            f"{units['relative_humidity_2m']}"
            f"\n   🌧 {precipitation[i]} "
            f"{units['precipitation_probability']}"
            f"\n   💨 {wind_speeds[i]} "
            f"{units['wind_speed_10m']}"
            f"\n   🌤 "
            f"{get_weather_description(weather_codes[i])}"
        )


def display_daily_weather(weather_data):
    """
    Display the 7-day weather forecast.
    """

    daily = weather_data["daily"]
    units = weather_data["daily_units"]

    dates = daily["time"]
    max_temperatures = daily["temperature_2m_max"]
    min_temperatures = daily["temperature_2m_min"]
    precipitation = daily["precipitation_sum"]
    weather_codes = daily["weather_code"]

    print("\n" + "=" * 45)
    print("7-DAY FORECAST")
    print("=" * 45)

    for i in range(len(dates)):
        print(
            f"\n📅 {dates[i]}"
            f"\n   🌡 Max: "
            f"{max_temperatures[i]} "
            f"{units['temperature_2m_max']}"
            f"\n   🌡 Min: "
            f"{min_temperatures[i]} "
            f"{units['temperature_2m_min']}"
            f"\n   🌧 Precipitation: "
            f"{precipitation[i]} "
            f"{units['precipitation_sum']}"
            f"\n   🌤 "
            f"{get_weather_description(weather_codes[i])}"
        )


def display_location(city_data):
    """
    Display the selected city information.
    """

    name = city_data.get("name", "Unknown")
    country = city_data.get("country", "Unknown")
    latitude = city_data.get("latitude")
    longitude = city_data.get("longitude")

    print("\n" + "=" * 45)
    print("LOCATION")
    print("=" * 45)

    print(f"📍 City: {name}")
    print(f"🌍 Country: {country}")
    print(f"🧭 Coordinates: {latitude}, {longitude}")


def main():
    """
    Main application flow.
    """

    city = input("Enter your city: ").strip()

    if not city:
        print("Error: City name cannot be empty.")
        sys.exit(1)

    city_data = get_city_information(city)

    latitude = city_data["latitude"]
    longitude = city_data["longitude"]

    weather_data = get_weather_data(
        latitude,
        longitude,
    )

    display_location(city_data)

    display_current_weather(weather_data)

    display_hourly_weather(weather_data)

    display_daily_weather(weather_data)


if __name__ == "__main__":
    main()