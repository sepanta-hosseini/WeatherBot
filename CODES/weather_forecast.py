import pandas as pd
import requests

city = input("Enter your city: ")
url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"

response = requests.get(url=url)

status = response.status_code

if status == 200:
    print(f"Status: {status}")
elif status == 403:
    print(f"Status:{status} \nThe request was declined")

json = response.json()

print(json)

