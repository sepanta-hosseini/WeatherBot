import requests
from .constants import (
    DAILY_FORECAST_DAYS,
    GEOCODING_URL,
    HOURLY_FORECAST_HOURS,
    REQUEST_TIMEOUT,
    WEATHER_URL,
)
from .exceptions import APIError, CityNotFoundError, InvalidResponseError


def make_request(url, params=None):
    """Send an HTTP GET request and return the response."""
    try:
        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.Timeout as error:
        raise APIError("The request timed out.") from error
    except requests.exceptions.ConnectionError as error:
        raise APIError("Could not connect to the server.") from error
    except requests.exceptions.RequestException as error:
        raise APIError(f"Request failed: {error}") from error
    if not response.ok:
        raise APIError(
            f"Request failed with status code "
            f"{response.status_code}: {response.reason}"
        )

    return response


def get_city_information(city):
    """Get location information for a city."""
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }
    response = make_request(
        GEOCODING_URL,
        params=params,
    )
    try:
        data = response.json()
    except ValueError as error:
        raise InvalidResponseError(
            "The geocoding API returned invalid JSON."
        ) from error

    results = data.get("results")

    if not results:
        raise CityNotFoundError(
            f"City not found: {city}"
        )

    return results[0]


def get_weather_data(latitude, longitude):
    """Get current, hourly, and daily weather data."""

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

    response = make_request(
        WEATHER_URL,
        params=params,
    )

    try:
        return response.json()
    except ValueError as error:
        raise InvalidResponseError(
            "The weather API returned invalid JSON."
        ) from error
