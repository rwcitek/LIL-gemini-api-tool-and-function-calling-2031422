from google import genai
from google.genai import types
import time
import threading
import sys

# Step 1: Define function declarations
check_balance_declaration = {
    "name": "check_balance",
    "description": "Checks the account balance for a given account ID",
    "parameters": {
        "type": "object",
        "properties": {
            "account_id": {
                "type": "string",
                "description": "The account ID to check (e.g., 'ACC123')",
            }
        },
        "required": ["account_id"],
    },
}

transfer_money_declaration = {
    "name": "transfer_money",
    "description": "Transfers money between accounts. Only call this if sufficient balance is confirmed.",
    "parameters": {
        "type": "object",
        "properties": {
            "from_account": {
                "type": "string",
                "description": "Source account ID",
            },
            "to_account": {
                "type": "string",
                "description": "Destination account ID",
            },
            "amount": {
                "type": "number",
                "description": "Amount to transfer",
            }
        },
        "required": ["from_account", "to_account", "amount"],
    },
}

# Step 2: Implement functions
def check_balance(account_id: str) -> dict:
    """Mock function to check account balance"""
    balances = {
        "ACC123": 500.00,    # Low balance
        "ACC456": 1200.00,   # Higher balance
        "ACC789": 2500.00    # High balance
    }
    
    balance = balances.get(account_id, 0.00)
    return {
        "account_id": account_id,
        "balance": balance,
        "currency": "USD"
    }

def transfer_money(from_account: str, to_account: str, amount: float) -> dict:
    """Mock function to transfer money"""
    return {
        "transaction_id": "TXN987654",
        "from_account": from_account,
        "to_account": to_account,
        "amount": amount,
        "status": "completed",
        "fee": 2.50
    }

# Step 3: Loading indicator
class LoadingIndicator:
    def __init__(self, message="Processing"):
        self.message = message
        self.is_running = False
        self.thread = None
    
    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()
    
    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()
        # Clear the loading line
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.flush()
    
    def _animate(self):
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        while self.is_running:
            sys.stdout.write(f'\r{spinner[i % len(spinner)]} {self.message}...')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

# Step 4: Set up Gemini
client = genai.Client()
tools = types.Tool(function_declarations=[check_balance_declaration, transfer_money_declaration])
config = types.GenerateContentConfig(tools=[tools])

# Step 5: FIXED Function to handle function calls
def handle_function_call(response, conversation_history, show_details=False):
    """Handle function call execution and add to conversation history - FIXED VERSION"""
    # FIXED: Check all parts and ensure function_call is not None
    parts = response.candidates[0].content.parts
    function_call = None
    
    for part in parts:
        if hasattr(part, 'function_call') and part.function_call is not None:
            function_call = part.function_call
            break
    
    if function_call is None:
        if show_details:
            print("🚫 No function call found in response")
        return None
    
    if show_details:
        print(f"🔧 Calling function: {function_call.name}")
        print(f"📥 Arguments: {dict(function_call.args)}")
    
    # Execute the appropriate function
    if function_call.name == "check_balance":
        result = check_balance(**function_call.args)
    elif function_call.name == "transfer_money":
        result = transfer_money(**function_call.args)
    else:
        result = {"error": f"Unknown function: {function_call.name}"}
    
    if show_details:
        print(f"📤 Result: {result}")
    
    # Add function call and response to conversation
    conversation_history.append(response.candidates[0].content)
    conversation_history.append(
        types.Content(role="user", parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"result": result}
            )
        ])
    )
    
    return result

# Step 6: Main interactive loop
def main():
    print("🏦 INTERACTIVE BANKING ASSISTANT (FIXED VERSION)")
    print("=" * 60)
    print("Available accounts: ACC123 ($500), ACC456 ($1200), ACC789 ($2500)")
    print("Commands:")
    print("- Check balance: 'What's the balance in ACC123?'")
    print("- Transfer money: 'Transfer $300 from ACC456 to ACC789'")
    print("- Type 'quit' to exit")
    print("- Type 'details' to toggle function call details")
    print("- Type 'clear' to clear conversation history")
    print("=" * 60)
    
    conversation_history = []
    show_details = False
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'details':
                show_details = not show_details
                print(f"🔧 Function call details: {'ON' if show_details else 'OFF'}")
                continue
            
            if user_input.lower() == 'clear':
                conversation_history = []
                print("🗑️ Conversation history cleared!")
                continue
            
            if not user_input:
                continue
            
            # Add user message to conversation
            conversation_history.append(
                types.Content(role="user", parts=[types.Part(text=user_input)])
            )
            
            # Start loading indicator
            loader = LoadingIndicator("AI is thinking")
            loader.start()
            
            # Process with potential multi-turn function calling
            max_turns = 5  # Prevent infinite loops
            turn_count = 0
            
            try:
                while turn_count < max_turns:
                    # Get model response
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=conversation_history,
                        config=config,
                    )
                    
                    # Try to handle function call - FIXED: Check return value
                    function_result = handle_function_call(response, conversation_history, show_details)
                    
                    if function_result is not None:
                        # Function was called, continue the loop
                        turn_count += 1
                        if show_details:
                            print(f"🔄 Turn {turn_count} completed")
                    else:
                        # No function call, this is the final response
                        loader.stop()
                        print(f"🤖 Assistant: {response.text}")
                        conversation_history.append(response.candidates[0].content)
                        break
                
                if turn_count >= max_turns:
                    loader.stop()
                    print(f"⚠️  Maximum function call turns ({max_turns}) reached")
                    # Still add the final response to conversation
                    conversation_history.append(response.candidates[0].content)
                    
            except Exception as e:
                loader.stop()
                print(f"❌ Error during processing: {e}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

# Step 7: Example prompts for testing
def show_examples():
    print("\n💡 EXAMPLE PROMPTS TO TRY:")
    print("-" * 30)
    print("1. What's the balance in ACC123?")
    print("2. Transfer $200 from ACC456 to ACC789")
    print("3. Transfer $1000 from ACC123 to ACC456  (insufficient funds)")
    print("4. Check balance for ACC789")
    print("5. Move $100 from ACC789 to ACC123")
    print("6. I want to send $600 from ACC456 to ACC123")

if __name__ == "__main__":
    show_examples()
    main()