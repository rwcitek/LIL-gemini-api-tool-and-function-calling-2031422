from google import genai
from google.genai import types

client = genai.Client()

tools = [
    {"url_context": {}}
]

url1 = "https://www.foodnetwork.com/recipes/ina-garten/perfect-roast-chicken-recipe-1940592"
url2 = "https://www.thepioneerwoman.com/food-cooking/recipes/a10727/roast-chicken/"

prompt = f"Compare the ingredients and cooking times from the recipes at {url1} and {url2}"

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config = types.GenerateContentConfig(
        tools = tools
    )
)

for part in response.candidates[0].content.parts:
    print(part.text)