import requests
import sys

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

    # Checking if the city was found
    if not city_data['results']:
        raise ValueError("City not found")

    result = city_data['results'][0]

    # Getting latitude and longitude from the json data
    latitude = result['latitude']
    longitude = result['longitude']

    return latitude, longitude

def status_code(name, response):
    """
    Checks the HTTP status code of the response
    and prints an appropriate message.
    """
    status = response.status_code

    if status == 200:
        print(f"{name} Response Status: {status}")
    else:
        print(f"{name} Response Status: {status}")
        print(f"Request failed: {response.reason}")

'''
    f"Current Weather:\
\n🌡 Temperature: {temperature}\
\n💧 Humidity: {humidity}\
\n🌧 Precipitation Probability: {precipitation}\
\n💨 Wind Speed: {wind_speed}"
\n🌤 Weather Code: {weather_code}"    
''' 

city = input("Enter your city: ")
city_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
response = get_requests(city_url)

status_code("City", response)

try:
    latitude, longitude = get_city_coordinates(response)
except ValueError as e:
    print(e)
    sys.exit()

response_weather = get_weather_data(latitude, longitude)

status_code("Weather", response_weather)

weather_data = response_weather.json()
daily = weather_data["daily"]
daily_weather(daily)

temperature, humidity, precipitation, wind_speed, weather_code = current_weather(
    weather_data["current"],
    weather_data["current_units"]
)

'''
print(f"Current Weather:\
\n🌡 Temperature: {temperature}\
\n💧 Humidity: {humidity}\
\n🌧 Precipitation Probability: {precipitation}\
\n💨 Wind Speed: {wind_speed}\
\n🌤 Weather Description: {weather_code}")
'''