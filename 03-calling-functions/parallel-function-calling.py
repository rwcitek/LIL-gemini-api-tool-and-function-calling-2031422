#!/usr/bin/env python

from google import genai
from google.genai import types

def get_current_temperature(city: str) -> dict:
    """Gets the current temperature for a given city.
    
    Args:
        city: The name of the city (e.g., 'New York', 'London')
    
    Returns:
        A dictionary containing temperature information for the city.
    """
    # Mock temperature data
    temperatures = {
        "new york": {"temp": 22, "unit": "°C", "condition": "sunny"},
        "london": {"temp": 15, "unit": "°C", "condition": "cloudy"},
        "tokyo": {"temp": 28, "unit": "°C", "condition": "humid"},
        "paris": {"temp": 18, "unit": "°C", "condition": "rainy"},
        "sydney": {"temp": 25, "unit": "°C", "condition": "clear"}
    }
    
    city_lower = city.lower()
    if city_lower in temperatures:
        result = temperatures[city_lower].copy()
        result["city"] = city
        return result
    else:
        return {"city": city, "temp": "N/A", "unit": "°C", "condition": "unknown"}

def get_time_zone(city: str) -> dict:
    """Gets the time zone information for a given city.
    
    Args:
        city: The name of the city (e.g., 'New York', 'London')
    
    Returns:
        A dictionary containing time zone information for the city.
    """
    # Mock timezone data
    timezones = {
        "new york": {"timezone": "EST (UTC-5)", "current_time": "14:30"},
        "london": {"timezone": "GMT (UTC+0)", "current_time": "19:30"},
        "tokyo": {"timezone": "JST (UTC+9)", "current_time": "04:30"},
        "paris": {"timezone": "CET (UTC+1)", "current_time": "20:30"},
        "sydney": {"timezone": "AEDT (UTC+11)", "current_time": "06:30"}
    }
    
    city_lower = city.lower()
    if city_lower in timezones:
        result = timezones[city_lower].copy()
        result["city"] = city
        return result
    else:
        return {"city": city, "timezone": "UTC+0", "current_time": "Unknown"}

def get_population(city: str) -> dict:
    """Gets the population information for a given city.
    
    Args:
        city: The name of the city (e.g., 'New York', 'London')
    
    Returns:
        A dictionary containing population information for the city.
    """
    # Mock population data
    populations = {
        "new york": {"population": "8.3 million", "metro_area": "20.1 million"},
        "london": {"population": "9.0 million", "metro_area": "15.8 million"},
        "tokyo": {"population": "13.9 million", "metro_area": "37.4 million"},
        "paris": {"population": "2.2 million", "metro_area": "12.2 million"},
        "sydney": {"population": "5.3 million", "metro_area": "5.4 million"}
    }
    
    city_lower = city.lower()
    if city_lower in populations:
        result = populations[city_lower].copy()
        result["city"] = city
        return result
    else:
        return {"city": city, "population": "Unknown", "metro_area": "Unknown"}

client = genai.Client()

config = types.GenerateContentConfig(
    tools = [get_current_temperature, get_time_zone, get_population]
)

prompt = "I'm planning a trip to Tokyo. Can you give me the current temperature, time zone, and population information for Tokyo? I need all this information at once"

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config=config
)

print("Final Response:")
print(response.text)