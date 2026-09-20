def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def display_location(location):
    """Display location information."""
    print_header("LOCATION")
    print(f"📍 City: {location['city']}")
    print(f"🌍 Country: {location['country']}")
    print(
        f"🧭 Coordinates: "
        f"{location['latitude']}, "
        f"{location['longitude']}"
    )


def display_current_weather(weather):
    """Display current weather information."""
    print_header("CURRENT WEATHER")
    
    print(f"🕐 Local time: {weather['time']}")
  
    print(
        f"🌡 Temperature: "
        f"{weather['temperature']} "
        f"{weather['temperature_unit']}"
    )

    print(
        f"💧 Humidity: "
        f"{weather['humidity']} "
        f"{weather['humidity_unit']}"
    )

    print(
        f"🌧 Precipitation probability: "
        f"{weather['precipitation_probability']} "
        f"{weather['precipitation_unit']}"
    )

    print(
        f"💨 Wind speed: "
        f"{weather['wind_speed']} "
        f"{weather['wind_unit']}"
    )

    print(f"🌤 Weather: {weather['weather']}")


def display_hourly_forecast(forecast):
    """Display the hourly forecast."""
    print_header("24-HOUR FORECAST")
    for item in forecast:
        print(
            f"\n🕐 {item['time']}\n"
            f"   🌡 {item['temperature']} "
            f"{item['temperature_unit']}\n"
            f"   💧 {item['humidity']} "
            f"{item['humidity_unit']}\n"
            f"   🌧 {item['precipitation_probability']} "
            f"{item['precipitation_unit']}\n"
            f"   💨 {item['wind_speed']} "
            f"{item['wind_unit']}\n"
            f"   🌤 {item['weather']}"
        )


def display_daily_forecast(forecast):
    """Display the 7-day forecast."""
    print_header("7-DAY FORECAST")
    for item in forecast:
        print(
            f"\n📅 {item['date']}\n"
            f"   🌡 Max: {item['max_temperature']} "
            f"{item['temperature_unit']}\n"
            f"   🌡 Min: {item['min_temperature']} "
            f"{item['temperature_unit']}\n"
            f"   🌧 Precipitation: {item['precipitation']} "
            f"{item['precipitation_unit']}\n"
            f"   🌤 {item['weather']}"
        )
