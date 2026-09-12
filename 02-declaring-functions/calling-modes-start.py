#!/usr/bin/env python

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