from weather_app.services import (
    get_current_weather,
    get_daily_forecast,
    get_hourly_forecast,
    get_location_summary,
    get_weather_description,
)


def test_weather_description():
    assert get_weather_description(0) == "Clear sky ☀️"


def test_unknown_weather_description():
    assert get_weather_description(999) == (
        "Unknown weather condition"
    )


def test_location_summary():
    city_data = {
        "name": "Rasht",
        "country": "Iran",
        "latitude": 37.27611,
        "longitude": 49.58862,
    }

    result = get_location_summary(city_data)
    assert result["city"] == "Rasht"
    assert result["country"] == "Iran"
    assert result["latitude"] == 37.27611
    assert result["longitude"] == 49.58862


def test_current_weather():
    weather_data = {
        "current": {
            "time": "2026-09-20T12:00",
            "temperature_2m": 25,
            "relative_humidity_2m": 60,
            "precipitation_probability": 20,
            "weather_code": 0,
            "wind_speed_10m": 10,
        },
        "current_units": {
            "temperature_2m": "°C",
            "relative_humidity_2m": "%",
            "precipitation_probability": "%",
            "wind_speed_10m": "km/h",
        },
    }

    result = get_current_weather(weather_data)
    assert result["temperature"] == 25
    assert result["humidity"] == 60
    assert result["precipitation_probability"] == 20
    assert result["weather"] == "Clear sky ☀️"


def test_daily_forecast():
    weather_data = {
        "daily": {
            "time": ["2026-09-20"],
            "temperature_2m_max": [30],
            "temperature_2m_min": [20],
            "precipitation_sum": [2.5],
            "weather_code": [1],
        },
        "daily_units": {
            "temperature_2m_max": "°C",
            "temperature_2m_min": "°C",
            "precipitation_sum": "mm",
        },
    }

    result = get_daily_forecast(weather_data)
    assert len(result) == 1
    assert result[0]["date"] == "2026-09-20"
    assert result[0]["max_temperature"] == 30
    assert result[0]["min_temperature"] == 20
    assert result[0]["precipitation"] == 2.5
