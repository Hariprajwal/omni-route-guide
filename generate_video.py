import urllib.request
import json

# We will test the OmniRoute server with the free video model it reported earlier (veo-free/veo)
url = "http://localhost:20128/v1/chat/completions"
data = {
    "model": "veo-free/veo",
    "stream": False,
    "messages": [
        {"role": "user", "content": "A beautiful sunset over a futuristic city with flying cars, cyberpunk style, high quality video"}
    ]
}

req = urllib.request.Request(
    url, 
    data=json.dumps(data).encode('utf-8'), 
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer dummy-key'
    }
)

print(f"Sending video generation request using model: '{data['model']}'...")
print("This might take a while for a video...")

try:
    with urllib.request.urlopen(req) as response:
        raw_response = response.read().decode('utf-8')
        result = json.loads(raw_response)
        
        print("\n--- Response Received ---")
        print(json.dumps(result, indent=2))
        print("-------------------------")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Failed to connect or get response: {e}")
