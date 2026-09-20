class WeatherAppError(Exception):
    """Base exception for the weather application."""


class APIError(WeatherAppError):
    """Raised when an API request fails."""


class CityNotFoundError(WeatherAppError):
    """Raised when the requested city cannot be found."""


class InvalidResponseError(WeatherAppError):
    """Raised when an API returns invalid or unexpected data."""
