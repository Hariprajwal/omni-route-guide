import urllib.request
import json
import sys

# Windows UTF-8 console output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

url = "http://localhost:20129/v1/chat/completions"
data = {
    "model": "felo/auto",
    "stream": False,
    "messages": [
        {"role": "user", "content": "Hello! Please reply with exactly: 'Super Gateway is working perfectly!'"}
    ]
}

req = urllib.request.Request(
    url, 
    data=json.dumps(data).encode('utf-8'), 
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer dummy'
    }
)

print("Sending test request to local Super Gateway server (port 20129)...")
try:
    with urllib.request.urlopen(req, timeout=15) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("\n--- Response Received ---")
        print(result['choices'][0]['message']['content'])
        print("-------------------------")
except Exception as e:
    print(f"Failed to connect or get response: {e}")
