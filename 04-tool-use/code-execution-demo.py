from google import genai
from google.genai import types

client = genai.Client()

code_execution_tool = types.Tool(
    code_execution=types.ToolCodeExecution()
)

config = types.GenerateContentConfig(
    tools = [code_execution_tool]
)

prompt = "Calculate the area of a circle with radius 7. Show your work step by step"

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config=config
)

for i, part in enumerate(response.candidates[0].content.parts):

    if part.text is not None:
        print(f"Text Part {i+1}")
        print(part.text)
        print("-"*30)

    if part.executable_code is not None:
        print(f"Generated Code Part {i+1}")
        print("```python")
        print(part.executable_code.code)
        print("```")
        print("-"*30)

    if part.code_execution_result is not None:
        print(f"Code Exection Result Part {i+1}")
        print("Output:")
        print(part.code_execution_result.output)
        print("-"*30)