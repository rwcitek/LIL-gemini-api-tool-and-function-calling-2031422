from google import genai
from google.genai import types

print("🚀 WELCOME TO GEMINI FUNCTION CALLING!")
print("="*50)
print("This example shows how Gemini can call functions to solve problems.\n")

# Step 1: Define a simple function declaration
add_numbers_declaration = {
    "name": "add_numbers",
    "description": "Adds two numbers together",
    "parameters": {
        "type": "object",
        "properties": {
            "first_number": {
                "type": "number",
                "description": "The first number to add",
            },
            "second_number": {
                "type": "number", 
                "description": "The second number to add",
            },
        },
        "required": ["first_number", "second_number"],
    },
}

# Step 2: Define the actual function
def add_numbers(first_number: float, second_number: float) -> dict:
    """Add two numbers and return the result"""
    result = first_number + second_number
    return {
        "calculation": f"{first_number} + {second_number} = {result}",
        "result": result
    }

# Step 3: Set up Gemini with the function
client = genai.Client()
tools = types.Tool(function_declarations=[add_numbers_declaration])
config = types.GenerateContentConfig(tools=[tools])

print("🔧 FUNCTION READY: add_numbers")
print("📝 What it does: Adds two numbers together")
print("🤖 Now let's ask Gemini to use it!\n")

# Step 4: Ask Gemini to solve a problem
user_question = "What is 25 + 37?"
print(f"❓ User asks: {user_question}")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_question,
    config=config,
)

# Step 5: Check if Gemini wants to call our function
function_call = response.candidates[0].content.parts[0].function_call

print(f"🧠 Gemini thinks: I need to call the add_numbers function!")
print(f"📞 Function call: {function_call.name}")
print(f"📥 Arguments: {dict(function_call.args)}")

# Step 6: Execute the function
if function_call.name == "add_numbers":
    result = add_numbers(**function_call.args)
    print(f"⚡ Function executed: {result['calculation']}")