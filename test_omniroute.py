import urllib.request
import json

url = "http://localhost:20128/v1/chat/completions"
data = {
    "model": "felo/auto",
    "stream": False,
    "messages": [
        {"role": "user", "content": "Hello! Please reply with exactly: 'OmniRoute is working perfectly!'"}
    ]
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})

print("Sending test request to local OmniRoute server...")
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("\n--- Response Received ---")
        print(result['choices'][0]['message']['content'])
        print("-------------------------")
except Exception as e:
    print(f"Failed to connect or get response: {e}")
