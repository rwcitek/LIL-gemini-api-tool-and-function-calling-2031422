from google import genai
from google.genai import types
import requests

fetch_users_declaration = {
    "name": "fetch_users",
    "description": "Fetches a list of users from the JSONPlaceholder API with optional email inclusion",
    "parameters": {
        "type": "object",
        "properties": {
            "max_users": {
                "type": "integer",
                "description": "Maximum number of users to fetch (1-10)"
            },
            "include_email": {
                "type": "boolean",
                "description": "Whether to include email addresses in the response"
            }
        },
        "required": ["max_users", "include_email"]
    }
}

get_user_details_declaration = {
    "name": "get_user_details",
    "description": "Retrieves detailed information for a specific user by their ID",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "The user ID to fetch details for a specific user (1 - 10)"
            }
        },
        "required": ["user_id"]
    }
}

def fetch_users(max_users: int, include_email: bool) -> dict:
    """Fetch users from JSONPlaceholder API"""
    try:
        # Limit max_users to reasonable range
        max_users = min(max_users, 10)
        
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        response.raise_for_status()
        
        all_users = response.json()
        limited_users = all_users[:max_users]
        
        # Format user list based on email preference
        user_list = []
        for user in limited_users:
            if include_email:
                user_list.append({
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"]
                })
            else:
                user_list.append({
                    "id": user["id"],
                    "name": user["name"]
                })
        
        return {
            "users": user_list,
            "total_fetched": len(user_list),
            "emails_included": include_email
        }
    
    except requests.RequestException as e:
        return {"error": f"Failed to fetch users: {str(e)}"}

def get_user_details(user_id: int) -> dict:
    """Get detailed information for a specific user"""
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
        response.raise_for_status()
        
        user = response.json()
        
        return {
            "id": user["id"],
            "name": user["name"],
            "username": user["username"],
            "email": user["email"],
            "phone": user["phone"],
            "website": user["website"],
            "company": user["company"]["name"],
            "address": f"{user['address']['street']}, {user['address']['city']}"
        }
    
    except requests.RequestException as e:
        return {"error": f"Failed to fetch user details: {str(e)}"}
    


tools = types.Tool(
    function_declarations=[fetch_users_declaration, get_user_details_declaration]
)

client = genai.Client()

config = types.GenerateContentConfig(
    tools=[tools]
)

user_question = "Can you get me a list of 5 users including their email addresses?"

user_question2 = "Show me the detailed information for user 3"

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=user_question2,
    config=config
)

# print(response)

function_call = response.candidates[0].content.parts[0].function_call

print(f"Function Name: {function_call.name}")
print(f"Arguments: {dict(function_call.args)}")

if function_call.name == "fetch_users":
    result = fetch_users(**function_call.args)
    
elif function_call.name == "get_user_details":
    result = get_user_details(**function_call.args)
else:
    result = {"error": f"Unknown function: {function_call.name}"}

print(f"Answer: {result}")