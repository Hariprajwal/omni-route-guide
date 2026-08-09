import urllib.request
import urllib.parse
import os

# We will use Pollinations.ai directly as it provides truly unlimited free image generation
# without requiring any API keys or local server routing.

prompt = "A cute cat sitting on a laptop typing code, cyberpunk style, high quality"
encoded_prompt = urllib.parse.quote(prompt)

url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
output_filename = "generated_cat.jpg"

print(f"Sending image generation request for prompt: '{prompt}'...")
print("This might take a few seconds...")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        with open(output_filename, 'wb') as f:
            f.write(response.read())
            
    print("\n--- Success! ---")
    print(f"Image successfully saved to: {os.path.abspath(output_filename)}")
    print("-------------------------")
except Exception as e:
    print(f"Failed to connect or get response: {e}")
