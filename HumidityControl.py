import math
import requests
from typing import Tuple


def find_humidity_fahrenheit_input(temp_indoor, temp_outdoor, humidity_outdoors):
    temp_indoor = fahrenheit_to_celsius(temp_indoor)
    temp_outdoor = fahrenheit_to_celsius(temp_outdoor)
    p_sat_indoor = magnus_equation(temp_indoor)
    p_sat_outdoor = magnus_equation(temp_outdoor)
    return calc_indoor_humidity(p_sat_outdoor, p_sat_indoor, temp_indoor, temp_outdoor, humidity_outdoors)

def find_humidity_celsius_input(temp_indoor, temp_outdoor, humidity_outdoors):
    p_sat_indoor = magnus_equation(temp_indoor)
    p_sat_outdoor = magnus_equation(temp_outdoor)
    return calc_indoor_humidity(p_sat_outdoor, p_sat_indoor, temp_indoor, temp_outdoor, humidity_outdoors)

def magnus_equation(temp: float) -> float:
    p_sat = 6.122 * math.exp((17.62 * temp) / (243.12 + temp))
    return p_sat

def calc_indoor_humidity(p_sat_outdoor, p_sat_indoor, temp_indoor, temp_outdoor, humidity_outdoors) -> float:
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

def should_open_window(room_humidity, humidity_indoors) -> bool:
    return room_humidity > humidity_indoors


if __name__ == "__main__":
    print('HumidityControl')
    print('Using Fahrenheit')
    temp_indoor, temp_outdoor, humidity_outdoors, room_humidity = get_user_inputs()

    humidity_indoors = find_humidity_fahrenheit_input(temp_indoor, temp_outdoor, humidity_outdoors)
    print(f'Air entering your indoors will have a humidity of {humidity_indoors} after being warmed up.')
    input()
