import tkinter as tk
from tkinter import messagebox
import datetime as dt
import requests

# OpenWeatherMap API configuration
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
API_KEY = '48ca7dc8e2e3a0fc8848b84c509870fe'

# Function to convert temperature from Kelvin to Celsius and Fahrenheit
def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32 
    return celsius, fahrenheit

# Function to get weather data and display it in the GUI
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return
    
    url = f"{BASE_URL}appid={API_KEY}&q={city}"
    response = requests.get(url).json()
    
    if response['cod'] != 200:
        messagebox.showerror("Error", f"City '{city}' not found or other error occurred.")
        return

    # Extract and convert weather data
    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)


    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)


    wind_speed = response['wind']['speed']


    humidity = response['main']['humidity']


    description = response['weather'][0]['description']


    sunrise_time = dt.datetime.fromtimestamp(response['sys']['sunrise'] + response['timezone'], dt.timezone.utc)
    sunset_time = dt.datetime.fromtimestamp(response['sys']['sunset'] + response['timezone'], dt.timezone.utc)

    # Display weather data
    temp_label.config(text=f"Temperature: {temp_celsius:.2f}°C / {temp_fahrenheit:.2f}°F")
  
    feels_like_label.config(text=f"Feels Like: {feels_like_celsius:.2f}°C / {feels_like_fahrenheit:.2f}°F")
  
    humidity_label.config(text=f"Humidity: {humidity}%")
   
    wind_speed_label.config(text=f"Wind Speed: {wind_speed} km/h")
   
    description_label.config(text=f"Description: {description.capitalize()}")
    
    sunrise_label.config(text=f"Sunrise: {sunrise_time.strftime('%H:%M:%S')} UTC")
    
    sunset_label.config(text=f"Sunset: {sunset_time.strftime('%H:%M:%S')} UTC")

# GUI setup
root = tk.Tk()
root.title("Weather App")

# Input field for city name
tk.Label(root, text="Enter City:").grid(row=0, column=0, padx=10, pady=10)
city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=10)

# Button to get weather data
get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.grid(row=0, column=2, padx=10, pady=10)

# Labels to display weather information
temp_label = tk.Label(root, text="Temperature:")
temp_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

#GUI for Feels like temp
feels_like_label = tk.Label(root, text="Feels Like:")
feels_like_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

#GUI for Humidity
humidity_label = tk.Label(root, text="Humidity:")
humidity_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

#GUI for Wind Speed
wind_speed_label = tk.Label(root, text="Wind Speed:")
wind_speed_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

#GUI for Description
description_label = tk.Label(root, text="Description:")
description_label.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

#GUI for sunrise and sunset
sunrise_label = tk.Label(root, text="Sunrise:")
sunrise_label.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

sunset_label = tk.Label(root, text="Sunset:")
sunset_label.grid(row=7, column=0, columnspan=3, padx=10, pady=5)



# Run the GUI
root.mainloop()
 #end of code...Code created by Davis and Anantha Shayi With the help of OPENAI