import sys
from .api import get_city_information, get_weather_data
from .display import (
    display_current_weather,
    display_daily_forecast,
    display_hourly_forecast,
    display_location,
)
from .exceptions import WeatherAppError
from .services import (
    get_current_weather,
    get_daily_forecast,
    get_hourly_forecast,
    get_location_summary,
)


def main():
    """Run the weather application."""
    city = input("Enter your city: ").strip()
    if not city:
        print("Error: City name cannot be empty.")
        return
    try:
        city_data = get_city_information(city)

        latitude = city_data["latitude"]
        longitude = city_data["longitude"]

        weather_data = get_weather_data(
            latitude,
            longitude,
        )

        location = get_location_summary(city_data)
        current_weather = get_current_weather(weather_data)
        hourly_forecast = get_hourly_forecast(weather_data)
        daily_forecast = get_daily_forecast(weather_data)

        display_location(location)
        display_current_weather(current_weather)
        display_hourly_forecast(hourly_forecast)
        display_daily_forecast(daily_forecast)
    except WeatherAppError as error:
        print(f"\n❌ Error: {error}")
        sys.exit(1)
    except KeyError as error:
        print(
            f"\n❌ Unexpected API response. "
            f"Missing field: {error}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
