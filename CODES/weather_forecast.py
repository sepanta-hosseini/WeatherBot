import pandas as pd
import requests

city = input("Enter your city: ")
url_city = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
response = requests.get(url=url_city)

# Getting status code from the response
status = response.status_code
if status == 200:
    print(f"City Response Status: {status}")
elif status == 403:
    print(f"City Response Status:{status} \nThe request was declined")

# Getting json data from the response
json = response.json()

# Getting latitude and longitude from the json data
latitude = json['results'][0]['latitude']
longitude = json['results'][0]['longitude']

url_weather = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
response_weather = requests.get(url=url_weather)

# Getting status code from the response
if response_weather.status_code == 200:
    print(f"Weather Response Status: {response_weather.status_code}")
elif response_weather.status_code == 403:
    print(f"Weather Response Status:{response_weather.status_code} \nThe request was declined")

json_weather = response_weather.json()

print(json_weather)

