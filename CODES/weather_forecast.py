import pandas as pd
import requests

city = input("Enter your city: ")
city_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
response = requests.get(url=city_url)

# Getting status code from the response
status = response.status_code
if status == 200:
    print(f"City Response Status: {status}")
elif status == 403:
    print(f"City Response Status:{status} \nThe request was declined")

# Getting json data from the response
city_data = response.json()

# Getting latitude and longitude from the json data
latitude = city_data['results'][0]['latitude']
longitude = city_data['results'][0]['longitude']

weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m&timezone=auto"
response_weather = requests.get(url=weather_url)

# Getting status code from the response
if response_weather.status_code == 200:
    print(f"Weather Response Status: {response_weather.status_code}")
elif response_weather.status_code == 403:
    print(f"Weather Response Status:{response_weather.status_code} \nThe request was declined")

weather_data = response_weather.json()

current_units = weather_data["current_units"]
current = weather_data["current"]

print(f"Current temperature: {current["temperature_2m"]}{current_units["temperature_2m"]}")