from google import genai
from google.genai import types
import random
import string

# Step 1: Define a simple function declaration
generate_password_declaration = {
    "name": "generate_password",
    "description": "Generates a secure password with specified length and character types",
    "parameters": {
        "type": "object",
        "properties": {
            "length": {
                "type": "integer",
                "description": "The desired length of the password (minimum 8)",
            },
            "include_symbols": {
                "type": "boolean", 
                "description": "Whether to include special symbols in the password",
            },
        },
        "required": ["length", "include_symbols"],
    },
}

# Step 2: Define the actual function
def generate_password(length: int, include_symbols: bool) -> dict:
    """Generate a secure password with specified criteria"""
    if length < 8:
        length = 8  # Minimum security requirement
    
    # Define character sets
    characters = string.ascii_letters + string.digits
    if include_symbols:
        characters += "!@#$%^&*"
    
    # Generate password
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return {
        "password": password,
        "length": len(password),
        "has_symbols": include_symbols,
        "strength": "Strong" if length >= 12 and include_symbols else "Good"
    }

client = genai.Client()
tool = types.Tool(
    function_declarations=[generate_password_declaration]
)

config = types.GenerateContentConfig(
    tools=[tool]
)

user_question = "I need a secure password that's 15 characters long and includes special symbols"

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=user_question,
    config=config
)

function_call = response.candidates[0].content.parts[0].function_call
print(f"Function suggested: {function_call.name}")
print(f"Arguments: {dict(function_call.args)}")

if function_call.name == "generate_password":
    result = generate_password(**function_call.args)
    print(f"Answer: {result}")