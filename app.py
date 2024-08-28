from flask import Flask, render_template, request  # Import necessary modules from Flask and requests
import requests  # Import requests to handle HTTP requests to the APIs
from collections import defaultdict  # Import defaultdict to handle default values in the forecast data
import os  # Import os to access environment variables
from dotenv import load_dotenv  # Import load_dotenv to read the .env file

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)  # Initialize the Flask application

# Get the API key from environment variables
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

# Function to get weather data from the OpenWeatherMap API
def get_weather_data(city):
    try:
        # Construct URLs for current weather and 5-day forecast
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'

        # Make API requests and parse the JSON responses
        weather_data = requests.get(weather_url).json()
        forecast_data = requests.get(forecast_url).json()

        # Check if the API returned an error
        if weather_data.get('cod') != 200 or forecast_data.get('cod') != "200":
            raise ValueError(f"Error fetching weather data: {weather_data.get('message', '')}")

        # Process forecast data to extract high and low temperatures for each day
        daily_forecast = defaultdict(lambda: {'high': -float('inf'), 'low': float('inf'), 'description': None, 'icon': None})
        
        for entry in forecast_data['list']:
            date = entry['dt_txt'].split(' ')[0]  # Extract the date from the forecast entry
            temp = entry['main']['temp']  # Get the temperature

            # Update the high and low temperatures for the day
            if temp > daily_forecast[date]['high']:
                daily_forecast[date]['high'] = temp
                daily_forecast[date]['description'] = entry['weather'][0]['description']
                daily_forecast[date]['icon'] = entry['weather'][0]['icon']
            if temp < daily_forecast[date]['low']:
                daily_forecast[date]['low'] = temp

        # Convert the daily_forecast to a regular dict and limit to 5 days
        daily_forecast = dict(list(daily_forecast.items())[:5])

        return weather_data, daily_forecast

    except requests.RequestException as e:
        # Handle network-related errors (e.g., connection issues)
        print(f"Request exception: {e}")
        return None, None
    except ValueError as e:
        # Handle API-related errors (e.g., invalid city name)
        print(f"Value error: {e}")
        return None, None
    except Exception as e:
        # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None, None

# Route for the home page where users can enter a city name
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']  # Get the city name entered by the user
        weather_data, forecast_data = get_weather_data(city)  # Fetch weather data for the city
        if weather_data and forecast_data:
            return render_template('weather.html', weather_data=weather_data, forecast_data=forecast_data, city=city)
        else:
            return render_template('index.html', error="Unable to retrieve weather data. Please try again.")
    return render_template('index.html')

# Route for using the user's location to determine the weather
@app.route('/location')
def location_weather():
    try:
        user_ip = request.remote_addr  # Get the real IP address of the user
        print(f"User IP: {user_ip}")  # Debugging: print the user's IP address

        geo_url = f'http://ip-api.com/json/{user_ip}'  # Geolocation API URL
        geo_data = requests.get(geo_url).json()  # Fetch geolocation data
        print(f"Geo Data: {geo_data}")  # Debugging: print the geolocation data
        
        if geo_data.get('status') == 'fail':
            # Handle failure to determine location
            raise ValueError("Failed to determine location")

        # Determine the city based on geolocation data
        city = geo_data.get('city') or geo_data.get('regionName') or geo_data.get('country')
        if not city:
            raise ValueError("City not found in geo data")

        print(f"Detected City: {city}")  # Debugging: print the detected city
        weather_data, forecast_data = get_weather_data(city)  # Fetch weather data for the detected city
        if weather_data and forecast_data:
            return render_template('weather.html', weather_data=weather_data, forecast_data=forecast_data, city=city)
        else:
            return render_template('index.html', error="Unable to retrieve weather data for your location. Please enter a city manually.")

    except requests.RequestException as e:
        # Handle network-related errors with the geolocation service
        print(f"Request exception: {e}")
        return render_template('index.html', error="There was an error with the geolocation service. Please enter a city manually.")
    except ValueError as e:
        # Handle errors related to missing or invalid location data
        print(f"Value error: {e}")
        return render_template('index.html', error=str(e))
    except Exception as e:
        # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")
        return render_template('index.html', error="An unexpected error occurred. Please try again.")

# Route for the info page 
@app.route('/info')
def info():
    return render_template('info.html')

# Main entry point to run the Flask application
if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off
