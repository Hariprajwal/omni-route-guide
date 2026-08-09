import urllib.request
import json
import sys

url = "http://localhost:20128/v1/chat/completions"

print("=====================================================")
print("🤖 OmniRoute Live Web Agent (Interactive Chat)")
print("Powered by Felo (Natively searches the web in real-time)")
print("Ask it about current news, weather, or anything else!")
print("Type 'exit' to quit.")
print("=====================================================\n")

# This list stores the conversation memory
messages = [
    {"role": "system", "content": "You are a helpful AI assistant. You have real-time access to the internet. Provide detailed, up-to-date answers."}
]

while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        # Add user's question to the memory
        messages.append({"role": "user", "content": user_input})
        
        data = {
            "model": "felo/auto", 
            "stream": True,  # We will stream the response word-by-word like ChatGPT!
            "messages": messages
        }
        
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8'), 
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer dummy-key'
            }
        )
        
        print("\nAgent: ", end="", flush=True)
        
        full_response = ""
        # Connect to the local OmniRoute server
        with urllib.request.urlopen(req) as response:
            for line in response:
                line = line.decode('utf-8').strip()
                # Parse the streaming chunks
                if line.startswith("data: ") and line != "data: [DONE]":
                    try:
                        chunk = json.loads(line[6:])
                        content = chunk['choices'][0].get('delta', {}).get('content', '')
                        if content:
                            print(content, end="", flush=True)
                            full_response += content
                    except json.JSONDecodeError:
                        pass
        print("\n")
        print("-" * 50)
        
        # Add the AI's response to the memory so it remembers the context
        messages.append({"role": "assistant", "content": full_response})
        
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"\n[Error connecting to OmniRoute: {e}]")
