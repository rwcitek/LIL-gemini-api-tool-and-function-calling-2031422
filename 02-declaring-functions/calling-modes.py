from google import genai
from google.genai import types

# Step 1: Define a simple function for demonstration
get_time_declaration = {
    "name": "get_current_time",
    "description": "Gets the current time in a specified timezone",
    "parameters": {
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": "Timezone (e.g., 'UTC', 'EST', 'PST')",
            }
        },
        "required": ["timezone"],
    },
}

# Step 2: Set up client and tools
client = genai.Client()
tools = types.Tool(function_declarations=[get_time_declaration])

test_prompt = "Hello, how are you?"
function_mode = "AUTO"

print(f"{function_mode} MODE Demo")
print("-"*30)
print(f"Prompt: {test_prompt}")

generation_config = types.GenerateContentConfig(
    tools = [tools],
    tool_config = types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode=function_mode
        )
    )
)

response = client.models.generate_content(
    model = "gemini-3.6-flash",
    contents=test_prompt,
    config= generation_config
)

function_part = response.candidates[0].content.parts[0]

if hasattr(function_part, "function_call") and function_part.function_call is not None:
    print("Model returns a Function Call")
    function_call = function_part.function_call
    print(f"Function: {function_call.name}")
    print(f"Arguments: {dict(function_call.args)}")
else:
    print("Model returned a plain text response")
    print(f"Direct Response: {response.text}")