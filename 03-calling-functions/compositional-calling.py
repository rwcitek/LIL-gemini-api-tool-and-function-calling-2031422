#!/usr/bin/env python

from google import genai
from google.genai import types

def get_user_location(user_id: str) -> dict:
    """Gets the stored location for a user by their ID.
    
    Args:
        user_id: The unique identifier for the user
    
    Returns:
        A dictionary containing the user's location information.
    """
    # Mock user database
    user_locations = {
        "user123": {"city": "Seattle", "state": "WA", "country": "USA"},
        "user456": {"city": "London", "state": "", "country": "UK"},
        "user789": {"city": "Toronto", "state": "ON", "country": "Canada"},
        "admin001": {"city": "San Francisco", "state": "CA", "country": "USA"}
    }
    
    if user_id in user_locations:
        result = user_locations[user_id].copy()
        result["user_id"] = user_id
        result["location_found"] = True
        # Format location string for next function
        if result["state"]:
            result["full_location"] = f"{result['city']}, {result['state']}"
        else:
            result["full_location"] = f"{result['city']}, {result['country']}"
        return result
    else:
        return {
            "user_id": user_id,
            "location_found": False,
            "error": "User not found",
            "full_location": ""
        }

def get_weather_forecast(location: str, days: int) -> dict:
    """Gets the weather forecast for a specific location and number of days.
    
    Args:
        location: The location string (e.g., 'Seattle, WA' or 'London, UK')
        days: Number of days to forecast (1-7)
    
    Returns:
        A dictionary containing weather forecast information.
    """
    # Mock weather data based on location
    weather_patterns = {
        "seattle": {"base_temp": 15, "condition": "rainy", "variation": 3},
        "london": {"base_temp": 12, "condition": "cloudy", "variation": 2},
        "toronto": {"base_temp": 8, "condition": "snowy", "variation": 4},
        "san francisco": {"base_temp": 18, "condition": "sunny", "variation": 1}
    }
    
    # Find matching weather pattern
    location_key = None
    for city in weather_patterns:
        if city in location.lower():
            location_key = city
            break
    
    if not location_key:
        return {
            "location": location,
            "error": "Weather data not available for this location",
            "forecast": []
        }
    
    pattern = weather_patterns[location_key]
    forecast = []
    
    for day in range(1, min(days + 1, 8)):  # Max 7 days
        temp_variation = (day % 3 - 1) * pattern["variation"]
        forecast.append({
            "day": day,
            "temperature": pattern["base_temp"] + temp_variation,
            "condition": pattern["condition"],
            "description": f"Day {day}: {pattern['base_temp'] + temp_variation}°C, {pattern['condition']}"
        })
    
    return {
        "location": location,
        "days_requested": days,
        "forecast": forecast,
        "summary": f"{days}-day forecast for {location}"
    }

def send_notification(user_id: str, message: str) -> dict:
    """Sends a notification message to a user.
    
    Args:
        user_id: The unique identifier for the user
        message: The notification message to send
    
    Returns:
        A dictionary containing the notification status.
    """
    notification_details = {}
    # Mock notification system
    if len(message) > 500:
        notification_details = {
            "user_id": user_id,
            "status": "failed",
            "error": "Message too long (max 500 characters)",
            "message_length": len(message)
        }
    
    notification_details = {
        "user_id": user_id,
        "status": "sent",
        "message": message,
        "timestamp": "2025-09-01 14:30:00",
        "delivery_method": "push_notification"
    }
    print("===== Final Notification Sent =====")
    print(notification_details)

    return notification_details

client = genai.Client()

config = types.GenerateContentConfig(
    tools = [get_user_location, get_weather_forecast, send_notification]
)

prompt = "Can you look up where user123 is located, get a 3-day weather forecast for their city, then send a notification with the weather summary"

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config=config
)

print("Final Response:")
print(response.text)