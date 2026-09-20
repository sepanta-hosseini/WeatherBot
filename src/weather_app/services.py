from .constants import WEATHER_DESCRIPTIONS
from .exceptions import InvalidResponseError


def get_weather_description(weather_code):
    """Convert a WMO weather code into a readable description."""
    return WEATHER_DESCRIPTIONS.get(
        weather_code,
        "Unknown weather condition",
    )


def get_location_summary(city_data):
    """Extract useful location information."""
    try:
        return {
            "city": city_data["name"],
            "country": city_data["country"],
            "latitude": city_data["latitude"],
            "longitude": city_data["longitude"],
        }
    except KeyError as error:
        raise InvalidResponseError(
            f"Missing location field: {error}"
        ) from error


def get_current_weather(weather_data):
    """Extract current weather information."""
    try:
        current = weather_data["current"]
        units = weather_data["current_units"]
        weather_code = current["weather_code"]
      
        return {
            "time": current["time"],
            "temperature": current["temperature_2m"],
            "temperature_unit": units["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "humidity_unit": units["relative_humidity_2m"],
            "precipitation_probability": current[
                "precipitation_probability"
            ],
            "precipitation_unit": units[
                "precipitation_probability"
            ],
            "wind_speed": current["wind_speed_10m"],
            "wind_unit": units["wind_speed_10m"],
            "weather": get_weather_description(weather_code),
        }
    except KeyError as error:
        raise InvalidResponseError(
            f"Missing current weather field: {error}"
        ) from error


def get_hourly_forecast(weather_data):
    """Extract hourly forecast information."""
    try:
        hourly = weather_data["hourly"]
        units = weather_data["hourly_units"]
        forecast = []
        for i, time in enumerate(hourly["time"]):
            weather_code = hourly["weather_code"][i]
            forecast.append(
                {
                    "time": time,
                    "temperature": hourly["temperature_2m"][i],
                    "temperature_unit": units["temperature_2m"],
                    "humidity": hourly["relative_humidity_2m"][i],
                    "humidity_unit": units[
                        "relative_humidity_2m"
                    ],
                    "precipitation_probability": hourly[
                        "precipitation_probability"
                    ][i],
                    "precipitation_unit": units[
                        "precipitation_probability"
                    ],
                    "wind_speed": hourly["wind_speed_10m"][i],
                    "wind_unit": units["wind_speed_10m"],
                    "weather": get_weather_description(
                        weather_code
                    ),
                }
            )
        return forecast
    except KeyError as error:
        raise InvalidResponseError(
            f"Missing hourly forecast field: {error}"
        ) from error


def get_daily_forecast(weather_data):
    """Extract daily forecast information."""
    try:
        daily = weather_data["daily"]
        units = weather_data["daily_units"]
        forecast = []
        for i, date in enumerate(daily["time"]):
            weather_code = daily["weather_code"][i]

            forecast.append(
                {
                    "date": date,
                    "max_temperature": daily[
                        "temperature_2m_max"
                    ][i],
                    "min_temperature": daily[
                        "temperature_2m_min"
                    ][i],
                    "temperature_unit": units[
                        "temperature_2m_max"
                    ],
                    "precipitation": daily[
                        "precipitation_sum"
                    ][i],
                    "precipitation_unit": units[
                        "precipitation_sum"
                    ],
                    "weather": get_weather_description(
                        weather_code
                    ),
                }
            )
        return forecast
    except KeyError as error:
        raise InvalidResponseError(
            f"Missing daily forecast field: {error}"
        ) from error
