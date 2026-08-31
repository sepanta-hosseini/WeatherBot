import pandas as pd
import requests

def responses(url):
    return requests.get(url=url)

def get_city_coordinates(response):
    # Getting json data from the response
    city_data = response.json()

    # Getting latitude and longitude from the json data
    latitude = city_data['results'][0]['latitude']
    longitude = city_data['results'][0]['longitude']

    return latitude, longitude

def status_code(n, response):
    # Getting status code from the response
    status = response.status_code
    if status == 200:
        print(f"{n} Response Status: {status}")
    elif status == 403:
        print(f"{n} Response Status:{status} \nThe request was declined")

def get_weather_data(latitude, longitude):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m&timezone=auto"
    response_weather = responses(weather_url)
    return response_weather

city = input("Enter your city: ")
city_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
response = responses(city_url)

status_code("City", response)

latitude, longitude = get_city_coordinates(response)
response_weather = get_weather_data(latitude, longitude)

status_code("Weather", response_weather)

weather_data = response_weather.json()

current_units = weather_data["current_units"]
current = weather_data["current"]

temperature = f"{current["temperature_2m"]} {current_units["temperature_2m"]}"
humidity = f"{current["relative_humidity_2m"]} {current_units["relative_humidity_2m"]}"
precipitation = f"{current["precipitation_probability"]} {current_units["precipitation_probability"]}"
wind_speed = f"{current["wind_speed_10m"]} {current_units["wind_speed_10m"]}"

print(f"Current temperature: {temperature}")
print(f"Current humidity: {humidity}")
print(f"Current precipitation: {precipitation}")
print(f"Current wind speed: {wind_speed}")