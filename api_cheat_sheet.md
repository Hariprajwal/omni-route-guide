# OmniRoute API Cheat Sheet

Keep this file handy! You can copy-paste these snippets into any new project to use your free local AI gateway.

## 🔑 Your "API Key" Details (Always the Same)

```
Base URL : http://localhost:20128/v1
API Key  : dummy          ← literally any text works
Model    : felo/auto      
← free, keyless, works instantly
```

---

## 📋 Copy-Paste Templates

### 🐍 Python (openai library)
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:20128/v1",
    api_key="dummy"
)

response = client.chat.completions.create(
    model="felo/auto",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

---

### 🐍 Python (requests — no install needed)
```python
import requests

response = requests.post(
    "http://localhost:20128/v1/chat/completions",
    headers={"Authorization": "Bearer dummy"},
    json={
        "model": "felo/auto",
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)
print(response.json()["choices"][0]["message"]["content"])
```

---

### 📄 JSON (for tools like Insomnia / Postman)
```json
{
  "base_url": "http://localhost:20128/v1",
  "api_key": "dummy",
  "model": "felo/auto"
}
```

---

### ⚙️ .env file (for any framework)
```env
OPENAI_API_KEY=dummy
OPENAI_BASE_URL=http://localhost:20128/v1
OPENAI_MODEL=felo/auto
```

---

### 🟨 JavaScript / Node.js
```js
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:20128/v1",
  apiKey: "dummy",
});

const res = await client.chat.completions.create({
  model: "felo/auto",
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(res.choices[0].message.content);
```

---

### 🔵 cURL (terminal test)
```bash
curl http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer dummy" \
  -H "Content-Type: application/json" \
  -d '{"model":"felo/auto","messages":[{"role":"user","content":"Hello!"}]}'
```

---

### 🛠️ For AI Tools (Cursor, Cline, Continue, etc.)

| Setting | Value |
|---|---|
| API Base URL | `http://localhost:20128/v1` |
| API Key | `dummy` |
| Model | `felo/auto` |

---

> ⚡ **Rule of thumb:** Wherever any tool asks for an OpenAI API key or base URL — just plug in `dummy` and `http://localhost:20128/v1`. It will work!
