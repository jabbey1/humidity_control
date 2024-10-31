import math
from datetime import datetime
import requests

def get_coordinates(city_name):
    # Use Nominatim to get latitude and longitude
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
    data = get_url_content(url)

    if data:
        latitude = data[0]["lat"]
        longitude = data[0]["lon"]
        return latitude, longitude
    else:
        print("City not found.")
        return None, None

def get_weather_data(city_name) -> (float, float, datetime):
    lat, long = get_coordinates(city_name)

    if lat and long:
        url = f"https://api.weather.gov/points/{lat},{long}"

        try:
            response = get_url_content(url)
            forecast_url = response["properties"]["forecastHourly"]

            forecast_data = get_url_content(forecast_url)
            period = forecast_data["properties"]["periods"][0]
            temp_outdoor = period["temperature"]
            outdoor_humidity = period["relativeHumidity"]["value"]
            time = period["startTime"]
            print(f'{temp_outdoor=}, {outdoor_humidity=}, {time=}')

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")

        return temp_outdoor, outdoor_humidity, time

def get_url_content(url):
    headers = {"User-Agent": "HumidityControl"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def find_humidity_fahrenheit_input(temp_indoor, temp_outdoor, humidity_outdoors):
    temp_indoor = fahrenheit_to_celsius(temp_indoor)
    temp_outdoor = fahrenheit_to_celsius(temp_outdoor)
    p_sat_indoor = magnus_equation(temp_indoor)
    p_sat_outdoor = magnus_equation(temp_outdoor)
    return calc_incoming_humidity(p_sat_outdoor, p_sat_indoor, temp_indoor, temp_outdoor, humidity_outdoors)

def find_humidity_celsius_input(temp_indoor, temp_outdoor, humidity_outdoors):
    p_sat_indoor = magnus_equation(temp_indoor)
    p_sat_outdoor = magnus_equation(temp_outdoor)
    return calc_incoming_humidity(p_sat_outdoor, p_sat_indoor, temp_indoor, temp_outdoor, humidity_outdoors)

def magnus_equation(temp: float) -> float:
    p_sat = 6.122 * math.exp((17.62 * temp) / (243.12 + temp))
    return p_sat

def calc_incoming_humidity(p_sat_outdoor, p_sat_indoor, temp_indoor, temp_outdoor, humidity_outdoors) -> float:
    top = (temp_indoor + 273) * p_sat_outdoor * humidity_outdoors
    bottom = (temp_outdoor + 273) * p_sat_indoor
    humidity_indoor = top / bottom
    return humidity_indoor

def fahrenheit_to_celsius(temp) -> float:
    return (5 / 9)*(temp - 32)

def celsius_to_fahrenheit(temp) -> float:
    return (9 / 5)* temp + 32

def get_user_inputs() -> tuple[float, float, float, float]:
    temp_indoor = float(input('What is the indoor temperature?'))
    temp_outdoor = float(input('What is the outdoor temperature?'))
    humidity_outdoors = float(input('What is the humidity outside?'))
    room_humidity = float(input('What is the humidity of the room?'))
    return temp_indoor, temp_outdoor, humidity_outdoors, room_humidity

def should_open_window(indoor_humidity, incoming_humidity) -> bool:
    return incoming_humidity < indoor_humidity


if __name__ == "__main__":
    print('HumidityControl')
    print('Using Fahrenheit')
    temp_outdoor, outdoor_humidity, time = get_weather_data('Kirkland')
    temp_indoor = float(input('What is the temperature in the room?'))
    indoor_humidity = float(input('What is the humidity in the room?'))
    incoming_humidity = find_humidity_celsius_input(temp_indoor, temp_outdoor, outdoor_humidity)
    delta = 'decrease' if temp_outdoor < temp_indoor else 'increase'
    if should_open_window(indoor_humidity, incoming_humidity):
        print(f'If you want to decrease the humidity in your room (currently {indoor_humidity}%),\n'
              f'you should open a window as the humidity of the air entering your room will be {incoming_humidity:.0f}%')
        print(f'\nThis will {delta} the temperature in the room.')
    else:
        print(f'Opening a window will not decrease the humidity in the room. Incoming humidity will be {incoming_humidity}% while indoor humidity is {indoor_humidity:.0f}%')




