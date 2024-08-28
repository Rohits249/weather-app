Weather App by Rohit Suri

This is a Flask-based weather application that allows users to enter a city name or use their current location to retrieve the current weather and a 5-day forecast.

Features
- Retrieve current weather and a 5-day forecast for any city.
- Use your current location to get weather details.
- Displays weather icons and weather data.

How to Run the Project

1. Clone the Repository
First, clone this repository to your local machine,

2. Install the Dependencies
Install the necessary dependencies listed in the requirements.txt file:
pip install -r requirements.txt

3. Set Up the Environment Variables
Create a .env file in the root directory of the project and add your OpenWeatherMap API key:
OPENWEATHERMAP_API_KEY=your_api_key

5. Run the Application
Run the Flask application:
python app.py
Open your web browser and go to http://127.0.0.1:5000/ to view the application.

What Was Done to Make the Project
1. Flask Setup: A Flask web application was set up to handle routes and render HTML templates.
2. OpenWeatherMap API Integration: Used the OpenWeatherMap API to fetch current weather data and a 5-day forecast.
3. Geolocation Integration: Used an IP-based geolocation API to let users retrieve weather data based on their location.
4. Environment Variables: Used a .env file to securely store the OpenWeatherMap API key and accessed it via the python-dotenv package.
5. Error Handling: Implemented error handling to manage issues like network errors, invalid API responses, etc.
6. User Interface: Created HTML templates to display weather data, including icons, temperatures, and weather descriptions.