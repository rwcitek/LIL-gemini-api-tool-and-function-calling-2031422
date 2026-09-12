from google import genai
from google.genai import types

client = genai.Client()

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

prompt = "Who won the 2025 US Open?"

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config=config
)

print("Model Response:")
print(response.text)