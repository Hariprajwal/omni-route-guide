import requests
import json

# OmniRoute Local Server Endpoint
API_URL = "http://localhost:20128/v1/chat/completions"

# Headers: OmniRoute mimics OpenAI, so we pass a dummy Bearer token
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer dummy-key"
}

# Payload
data = {
    "model": "felo/auto", # Explicitly use the free keyless Felo provider
    "stream": False,      # Set to True if you want a streaming response
    "messages": [
        {"role": "user", "content": "Hello! What can you do?"}
    ]
}

print("Sending request to OmniRoute...")
try:
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status() # Check for HTTP errors
    
    result = response.json()
    print("\n--- Response ---")
    print(result['choices'][0]['message']['content'])
    
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Server replied: {e.response.text}")
