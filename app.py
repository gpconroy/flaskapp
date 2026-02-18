from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Open-Meteo API (free, no API key required)
GEOCODING_URL = 'https://geocoding-api.open-meteo.com/v1/search'
WEATHER_URL = 'https://api.open-meteo.com/v1/forecast'

# Weather condition to icon mapping based on WMO codes
WEATHER_ICONS = {
    0: '☀️',      # Clear sky
    1: '⛅',      # Mainly clear
    2: '⛅',      # Partly cloudy
    3: '☁️',      # Overcast
    45: '🌫️',     # Foggy
    48: '🌫️',     # Depositing rime fog
    51: '🌧️',     # Light drizzle
    53: '🌧️',     # Moderate drizzle
    55: '🌧️',     # Dense drizzle
    61: '🌦️',     # Slight rain
    63: '🌧️',     # Moderate rain
    65: '🌧️',     # Heavy rain
    71: '❄️',      # Slight snow
    73: '❄️',      # Moderate snow
    75: '❄️',      # Heavy snow
    77: '❄️',      # Snow grains
    80: '🌦️',     # Slight rain showers
    81: '🌧️',     # Moderate rain showers
    82: '🌧️',     # Violent rain showers
    85: '❄️',      # Slight snow showers
    86: '❄️',      # Heavy snow showers
    95: '⛈️',      # Thunderstorm
    96: '⛈️',      # Thunderstorm with slight hail
    99: '⛈️',      # Thunderstorm with heavy hail
}


@app.route('/')
def index():
    """Render the main page with city input form"""
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def get_weather():
    """Fetch weather data for the given city"""
    city = request.form.get('city', '').strip()
    
    if not city:
        return render_template('index.html', error='Please enter a city name')
    
    try:
        # First, geocode the city name to get latitude/longitude
        geocoding_params = {
            'name': city,
            'count': 1,
            'language': 'en',
            'format': 'json'
        }
        geocoding_response = requests.get(GEOCODING_URL, params=geocoding_params, timeout=5)
        geocoding_response.raise_for_status()
        geocoding_data = geocoding_response.json()
        
        if not geocoding_data.get('results'):
            return render_template('index.html', error=f'City "{city}" not found. Please try again.')
        
        # Get the first result
        location = geocoding_data['results'][0]
        latitude = location['latitude']
        longitude = location['longitude']
        city_name = location['name']
        country = location.get('country', '')
        
        # Fetch weather data using coordinates
        weather_params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,cloud_cover',
            'temperature_unit': 'celsius',
            'wind_speed_unit': 'ms',
            'timezone': 'auto'
        }
        weather_response = requests.get(WEATHER_URL, params=weather_params, timeout=5)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        current = weather_data['current']
        
        # Map WMO weather code to description
        wmo_code = current['weather_code']
        weather_descriptions = {
            0: 'Clear sky',
            1: 'Mainly clear',
            2: 'Partly cloudy',
            3: 'Overcast',
            45: 'Foggy',
            48: 'Foggy',
            51: 'Light drizzle',
            53: 'Moderate drizzle',
            55: 'Dense drizzle',
            61: 'Slight rain',
            63: 'Moderate rain',
            65: 'Heavy rain',
            71: 'Slight snow',
            73: 'Moderate snow',
            75: 'Heavy snow',
            77: 'Snow grains',
            80: 'Rain showers',
            81: 'Rain showers',
            82: 'Violent rain showers',
            85: 'Snow showers',
            86: 'Snow showers',
            95: 'Thunderstorm',
            96: 'Thunderstorm with hail',
            99: 'Thunderstorm with hail',
        }
        
        weather_info = {
            'city': city_name,
            'country': country,
            'temperature': round(current['temperature_2m']),
            'feels_like': round(current['apparent_temperature']),
            'humidity': current['relative_humidity_2m'],
            'wind_speed': current['wind_speed_10m'],
            'description': weather_descriptions.get(wmo_code, 'Unknown'),
            'icon': WEATHER_ICONS.get(wmo_code, '🌤️'),
            'cloudiness': current['cloud_cover'],
        }
        
        return render_template('weather.html', weather=weather_info)
    
    except requests.exceptions.Timeout:
        error = 'Request timed out. Please check your internet connection.'
    except requests.exceptions.RequestException:
        error = 'Unable to connect to weather service. Please try again later.'
    except Exception as e:
        error = f'An error occurred: {str(e)}'
    
    return render_template('index.html', error=error)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)