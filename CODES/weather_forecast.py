import requests

def get_requests(url):
    """
    Sends a GET request to the specified URL and returns the response.
    """
    return requests.get(url=url)

def get_city_coordinates(response):
    """
    Extracts the latitude and longitude from the city search response.
    """
    # Getting json data from the response
    city_data = response.json()

    # Getting latitude and longitude from the json data
    latitude = city_data['results'][0]['latitude']
    longitude = city_data['results'][0]['longitude']

    return latitude, longitude

def status_code(n, response):
    """
    Checks the status code of the response and prints an appropriate message.
    """
    # Getting status code from the response
    status = response.status_code
    if status == 200:
        print(f"{n} Response Status: {status}")
    elif status == 403:
        print(f"{n} Response Status:{status} \nThe request was declined")

def get_weather_data(latitude, longitude):
    """
    Fetches weather data for the given coordinates.
    """
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m&timezone=auto"
    response_weather = get_requests(weather_url)
    return response_weather

def current_weather(current, current_units):
    """
    Returns a formatted string with the current weather information.
    """
    temperature = f"{current["temperature_2m"]} {current_units["temperature_2m"]}"
    humidity = f"{current["relative_humidity_2m"]} {current_units["relative_humidity_2m"]}"
    precipitation = f"{current["precipitation_probability"]} {current_units["precipitation_probability"]}"
    wind_speed = f"{current["wind_speed_10m"]} {current_units["wind_speed_10m"]}"
    weather_code = current["weather_code"]

    return f"Current Weather:\
\nTemperature: {temperature}\
\nHumidity: {humidity}\
\nPrecipitation Probability: {precipitation}\
\nWind Speed: {wind_speed}\
\nWeather Code: {weather_code}"    
    

city = input("Enter your city: ")
city_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
response = get_requests(city_url)

status_code("City", response)

latitude, longitude = get_city_coordinates(response)
response_weather = get_weather_data(latitude, longitude)

status_code("Weather", response_weather)

weather_data = response_weather.json()

current_units = weather_data["current_units"]
current = weather_data["current"]

    
print(current_weather(current, current_units))