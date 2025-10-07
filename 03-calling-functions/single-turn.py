from google import genai
from google.genai import types
import re

GEMINI_MODEL = "gemini-2.5-flash"

client = genai.Client()

# Declare the function
validate_email_declaration = {
    "name": "validate_email",
    "description": "Validates an email address and provides detailed information about its format and components",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address to validate (e.g., 'user@example.com')",
            },
            "check_domain": {
                "type": "boolean",
                "description": "Whether to perform additional domain format checks (default: true)",
                "default": True
            },
        },
        "required": ["email"],
    },
}

# Define the function
def validate_email(email: str, check_domain: bool = True) -> dict:
    """Validate email address and return detailed analysis"""
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    result = {
        "email": email,
        "is_valid": False,
        "local_part": "",
        "domain": "",
        "issues": []
    }
    
    # Check if email matches basic pattern
    if re.match(email_pattern, email):
        result["is_valid"] = True
        local_part, domain = email.split('@', 1)
        result["local_part"] = local_part
        result["domain"] = domain
        
        # Additional checks if requested
        if check_domain:
            if len(local_part) > 64:
                result["issues"].append("Local part exceeds 64 characters")
                result["is_valid"] = False
            
            if len(domain) > 253:
                result["issues"].append("Domain exceeds 253 characters")
                result["is_valid"] = False
                
            if '..' in domain:
                result["issues"].append("Domain contains consecutive dots")
                result["is_valid"] = False
    else:
        result["issues"].append("Invalid email format")
        
        # Try to identify specific issues
        if '@' not in email:
            result["issues"].append("Missing @ symbol")
        elif email.count('@') > 1:
            result["issues"].append("Multiple @ symbols")
        elif not email.split('@')[-1]:
            result["issues"].append("Missing domain")
        elif '.' not in email.split('@')[-1]:
            result["issues"].append("Domain missing top-level domain")
    
    # Summary message
    if result["is_valid"]:
        result["summary"] = f"✅ '{email}' is a valid email address"
    else:
        result["summary"] = f"❌ '{email}' is not valid: {', '.join(result['issues'])}"
    
    return result

# Set up the tool 
tools = types.Tool(function_declarations=[validate_email_declaration])


config = types.GenerateContentConfig(
    tools = [tools]
)

# Prompt for the two states 
valid_email_prompt = "Can you check if 'john.doe@company-mail.com' is a valid email address? I want to make sure it's properly formatted."

invalid_email_prompt = "Please check if the email 'jdub@@company' is valid"

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part(
                text=invalid_email_prompt
            )
        ]
    )
]

print("=== EMAIL VALIDATION ASSISTANT ===\n")
response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents = contents,
    config = config,
)


print("Model's function call suggestion:")
function_call = response.candidates[0].content.parts[0].function_call

# Print the function details
function_name = function_call.name
function_arguments = function_call.args
print(f"Function Name: {function_name}")
print(f"Function Arguments: {dict(function_arguments)}")

# Execute the function with the delivered arguments
if function_name == "validate_email":
    result = validate_email(**function_arguments)

    # Print out the raw function results
    print(f"\nEmail Validation Result:")
    for key, value in result.items():
        print(f"{key}: {value}")
    print()

    function_response_part = types.Part.from_function_response(
        name=function_name,
        response = {
            "result": result
        }
    )

    contents.append(response.candidates[0].content)

    contents.append(
        types.Content(
            role="user",
            parts=[function_response_part]
        )
    )

    final_response = client.models.generate_content(
        model = GEMINI_MODEL,
        config = config,
        contents = contents
    )

    print("Final Response to the user")
    print(final_response.text)