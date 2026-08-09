# 🚀 Free Unlimited AI API — 1.5 Billion Tokens/Month, $0

> **Stop paying for AI. Stack 90+ free provider tiers through one local endpoint — Claude, GPT-4o, Gemini, DeepSeek, and 500+ models, all for free, auto-switching when limits hit.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Powered by OmniRoute](https://img.shields.io/badge/Powered%20by-OmniRoute-blue)](https://github.com/diegosouzapw/OmniRoute)
[![Free Tokens](https://img.shields.io/badge/Free%20Tokens-~1.5B%2Fmonth-brightgreen)](https://github.com/diegosouzapw/OmniRoute)
[![Works with](https://img.shields.io/badge/Works%20with-Cursor%20%7C%20Cline%20%7C%20Copilot-orange)](https://github.com/diegosouzapw/OmniRoute)

---

## 🤔 What Is This?

This is a **beginner-friendly setup guide + ready-to-run Python scripts** for running [OmniRoute](https://github.com/diegosouzapw/OmniRoute) — an open-source AI gateway that:

- Aggregates **90+ free AI provider tiers** (Google, Mistral, DeepSeek, Felo, etc.)
- Routes all your AI requests through **one local API endpoint** on your computer
- **Auto-switches** to the next free provider when you hit a rate limit — so you never stop
- Gives you access to **~1.53 Billion free tokens per month**
- Works with **Cursor, Cline, Copilot, Claude Code, ChatGPT API** and any OpenAI-compatible tool

Think of it as your own personal, infinitely rotating free AI API key — running 100% on your machine.

---

## 💡 How Does It Work?

```
Your Tool (Cursor, Python, etc.)
        ↓
http://localhost:20128/v1   ← Your local OmniRoute server
        ↓
┌──────────────────────────────────────────────────────┐
│   OmniRoute Smart Router                             │
│   Checks 90+ free provider free tiers               │
│   Auto-switches when limits hit                      │
└──────────────────────────────────────────────────────┘
        ↓
Free Provider #1 (Felo)     → Hit limit? →
Free Provider #2 (OpenCode) → Hit limit? →
Free Provider #3 (Kimi)     → Hit limit? →
... and 87 more providers
```

**The result:** You effectively get unlimited access because by the time you exhaust one provider's free tier, OmniRoute has silently moved to the next one. The total pooled budget across all free tiers is ~1.53 Billion tokens/month.

---

## ⚡ Quick Start (5 Minutes)

### Prerequisites
- [Node.js](https://nodejs.org/) (v18 or higher) — required to run OmniRoute
- [Python 3](https://www.python.org/) — to run the test scripts in this repo

### Step 1: Install OmniRoute on your D Drive (saves C drive space)

Open PowerShell and run:
```powershell
mkdir D:\OmniRoute
cd D:\OmniRoute
npm install omniroute
```

### Step 2: Start the local server

```powershell
cd D:\OmniRoute
npx omniroute
```

You should see the server boot up. Your local AI API is now live at:
```
http://localhost:20128/v1
```

### Step 3: Test it!

Run any of the Python scripts from this repo (see below). You'll get real AI responses for **free**.

---

## 🤖 Make It Run Automatically on Windows Startup

So you don't have to manually start it every time:

1. Press `Win + R`, type `shell:startup`, press Enter
2. Create a new file called `StartOmniRoute.vbs` in that folder
3. Paste this single line inside it and save:

```vbscript
CreateObject("WScript.Shell").Run "cmd /c cd /d D:\OmniRoute && npx omniroute", 0, False
```

That's it! Every time you turn on your PC, OmniRoute starts silently in the background with no window or popup. Your AI API will always be ready within 10 seconds of login.

---

## 🐍 Python Scripts — Ready to Run

### 📄 Script 1: `test_omniroute.py` — Basic Chat Completion Test

**What it does:** Sends a simple text message to the free AI and prints the response. This is your "hello world" for the API.

```python
import urllib.request
import json

url = "http://localhost:20128/v1/chat/completions"
data = {
    "model": "felo/auto",   # felo is a 100% free, keyless provider
    "stream": False,         # IMPORTANT: must be False to get plain JSON back
    "messages": [
        {"role": "user", "content": "Hello! Please reply with exactly: 'OmniRoute is working perfectly!'"}
    ]
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

print("Sending test request to local OmniRoute server...")
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("\n--- Response Received ---")
        print(result['choices'][0]['message']['content'])
        print("-------------------------")
except Exception as e:
    print(f"Failed to connect or get response: {e}")
```

**How to run:**
```bash
python test_omniroute.py
```

**Expected output:**
```
Sending test request to local OmniRoute server...

--- Response Received ---
OmniRoute is working perfectly!
-------------------------
```

> ⚠️ **Important:** Always set `"stream": False`. Without it, OmniRoute returns a streaming (SSE) response that `json.loads()` cannot parse, causing an "Expecting value" error.

> ⚠️ **Important:** Use `"felo/auto"` not just `"auto"` as the model. Plain `"auto"` requires you to have connected providers set up first.

---

### 🖼️ Script 2: `generate_image.py` — Free AI Image Generation

**What it does:** Generates an image from a text prompt using Pollinations AI — a permanently free, keyless image generation API. The image is saved as a `.jpg` file on your computer.

```python
import urllib.request
import urllib.parse
import os

# Pollinations.ai provides unlimited free image generation with no API key needed.
# It uses open models (FLUX, Stable Diffusion) and has no rate limits for basic use.

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
```

**How to run:**
```bash
python generate_image.py
```

**Expected output:**
```
Sending image generation request for prompt: 'A cute cat sitting on a laptop typing code, cyberpunk style, high quality'...
This might take a few seconds...

--- Success! ---
Image successfully saved to: D:\your_folder\generated_cat.jpg
-------------------------
```

**To generate a different image**, just change the `prompt` variable to whatever you want:
```python
prompt = "A futuristic city at night, neon lights, rain, photorealistic"
prompt = "A logo for a startup called NovaMind, minimalist, blue and white"
prompt = "An oil painting of a dog playing chess"
```

---

### 💬 Script 3: `chat_agent.py` — Live Web Agent with Memory

**What it does:** An interactive, terminal-based chatbot that keeps track of your conversation history and streams the AI's response word-by-word (just like ChatGPT). Because it runs on the `felo/auto` model, **it natively searches the real-time internet** for you to answer questions about current events.

```python
import urllib.request
import json

url = "http://localhost:20128/v1/chat/completions"
messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']: break
        
    messages.append({"role": "user", "content": user_input})
    data = {"model": "felo/auto", "stream": True, "messages": messages}
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), 
                                 headers={'Content-Type': 'application/json', 'Authorization': 'Bearer dummy'})
    
    print("Agent: ", end="", flush=True)
    full_response = ""
    with urllib.request.urlopen(req) as response:
        for line in response:
            line = line.decode('utf-8').strip()
            if line.startswith("data: ") and line != "data: [DONE]":
                try:
                    content = json.loads(line[6:])['choices'][0].get('delta', {}).get('content', '')
                    print(content, end="", flush=True)
                    full_response += content
                except: pass
    print("\n")
    messages.append({"role": "assistant", "content": full_response})
```

**How to run:**
```bash
python chat_agent.py
```

**Features shown in this script:**
- **Streaming:** Receiving the answer in real-time chunks
- **Memory:** Passing the `messages` array back and forth so the AI remembers context
- **Web Search:** Ask it about today's weather or news, and it will search the web!

---

## 🎛️ Using OmniRoute in Your AI Coding Tools

Point any OpenAI-compatible tool at your local server:

| Setting | Value |
|---|---|
| **API Base URL** | `http://localhost:20128/v1` |
| **Model** | `felo/auto` |
| **API Key** | `dummy` (any text works) |
| **Monthly Cost** | `$0` |

### Cursor IDE
`Settings → Models → OpenAI API Key → dummy` and `Override OpenAI Base URL → http://localhost:20128/v1`

### Cline (VS Code Extension)
`Extension Settings → API Provider → OpenAI Compatible → Base URL: http://localhost:20128/v1 → Model: felo/auto`

### Continue (VS Code Extension)
In your `~/.continue/config.json`:
```json
{
  "models": [{
    "title": "Free AI (OmniRoute)",
    "provider": "openai",
    "model": "felo/auto",
    "apiBase": "http://localhost:20128/v1",
    "apiKey": "dummy"
  }]
}
```

---

## 📊 How Many Free Tokens Do I Get?

OmniRoute pools the documented free tiers of **43 provider pools / 516 models**:

| Time Period | Available Tokens |
|---|---|
| Per Month (steady) | **~1.53 Billion** |
| First Month (with signup credits) | **~2.15 Billion** |

To see your **live usage and remaining budget**, open this URL while your server is running:

👉 **[http://localhost:20128/dashboard/free-tiers](http://localhost:20128/dashboard/free-tiers)**

This dashboard shows you a live breakdown of which providers have been used, how many tokens remain in each pool, and when each pool resets.

---

## ❓ FAQ

**Q: Is this legal?**
> Yes. OmniRoute only uses the officially documented free tiers from each AI provider. You're not hacking anything — you're just using multiple companies' free samples at once, which they intended for developer use.

**Q: Will AI companies ban me for using this?**
> Unlikely for normal usage. They tolerate free tier use. However, if you generate millions of requests per day, some providers may throttle you.

**Q: What happens when a provider's free tier is exhausted?**
> OmniRoute automatically and instantly tries the next provider. You won't see any interruption — the response just comes from a different free source.

**Q: Do I need API keys for any of this?**
> No. The scripts in this repo and the `felo/auto` model work with zero configuration and zero API keys. Some providers offer even more tokens if you sign up for a free account and add your key.

**Q: What's the difference between `auto` and `felo/auto`?**
> `auto` is OmniRoute's smart routing mode that scores all your connected providers. `felo/auto` explicitly routes to the Felo provider, which is keyless and works out of the box. Use `felo/auto` for a guaranteed working model without any configuration.

---

## 🗺️ What's Next?

- [ ] Add a script for streaming responses (real-time token-by-token output)
- [ ] Add a script for multi-turn conversations
- [ ] Add a script to compare response quality across different free providers
- [ ] Windows Service installer for an even cleaner startup experience

PRs are welcome!

---

## 🙏 Credits

- **[OmniRoute](https://github.com/diegosouzapw/OmniRoute)** by [@diegosouzapw](https://github.com/diegosouzapw) — the incredible open-source gateway that makes all of this possible. Star their repo!
- **[Pollinations AI](https://pollinations.ai/)** — free, unlimited image generation API

---

## 📄 License

MIT — do whatever you want with this.
