import os
import sys
import json
import time
import urllib.request
import urllib.error

# Ensure stdout handles utf-8 on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

print("=" * 60)
print("[*] STANDALONE PROVIDER TEST SUITE")
print("Testing each provider independently before integration")
print("=" * 60)

results = {}

# -------------------------------------------------------------
# Test 1: Pollinations AI Text API (Zero-Key Instant Free)
# -------------------------------------------------------------
print("\n[1/4] Testing Pollinations.ai Text API...")
t0 = time.time()
try:
    req = urllib.request.Request(
        "https://text.pollinations.ai/openai/chat/completions",
        data=json.dumps({
            "model": "openai",
            "messages": [{"role": "user", "content": "Reply with: 'Pollinations OK'"}],
            "stream": False
        }).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"].strip()
        elapsed = round(time.time() - t0, 2)
        print(f"  ✅ SUCCESS ({elapsed}s): {content}")
        results["Pollinations Text"] = {"status": "LIVE", "latency": f"{elapsed}s", "key_needed": False}
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    results["Pollinations Text"] = {"status": "FAILED", "error": str(e), "key_needed": False}

# -------------------------------------------------------------
# Test 2: Pollinations AI Image API (Zero-Key Instant Free)
# -------------------------------------------------------------
print("\n[2/4] Testing Pollinations.ai Image Generation...")
t0 = time.time()
try:
    test_img_url = "https://image.pollinations.ai/prompt/cat?width=128&height=128&nologo=true"
    img_req = urllib.request.Request(test_img_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(img_req, timeout=12) as resp:
        img_bytes = resp.read()
        elapsed = round(time.time() - t0, 2)
        print(f"  ✅ SUCCESS ({elapsed}s): Received {len(img_bytes)} image bytes")
        results["Pollinations Image"] = {"status": "LIVE", "latency": f"{elapsed}s", "key_needed": False}
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    results["Pollinations Image"] = {"status": "FAILED", "error": str(e), "key_needed": False}

# -------------------------------------------------------------
# Test 3: Local OmniRoute Server (Current State at :20128)
# -------------------------------------------------------------
print("\n[3/4] Testing Local OmniRoute Server (localhost:20128)...")
t0 = time.time()
try:
    req = urllib.request.Request(
        "http://localhost:20128/v1/chat/completions",
        data=json.dumps({
            "model": "felo/auto",
            "messages": [{"role": "user", "content": "Hi"}],
            "stream": False
        }).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer dummy"}
    )
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"][:40]
        elapsed = round(time.time() - t0, 2)
        print(f"  ✅ SUCCESS ({elapsed}s): {content}")
        results["OmniRoute (Local)"] = {"status": "LIVE", "latency": f"{elapsed}s"}
except urllib.error.HTTPError as e:
    err_body = e.read().decode("utf-8", errors="ignore")
    try:
        err_msg = json.loads(err_body).get("error", {}).get("message", err_body[:80])
    except:
        err_msg = err_body[:80]
    print(f"  ❌ FAILED (HTTP {e.code}): {err_msg}")
    results["OmniRoute (Local)"] = {"status": f"DOWN (HTTP {e.code})", "error": err_msg}
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    results["OmniRoute (Local)"] = {"status": "DOWN", "error": str(e)}

# -------------------------------------------------------------
# Test 4: g4f (GPT4Free) Local Engine
# -------------------------------------------------------------
print("\n[4/4] Testing g4f (GPT4Free) Engine...")
try:
    import g4f
    print(f"  ℹ️ g4f version {g4f.__version__} loaded.")
    # Check if any provider has open keyless access
    results["g4f Engine"] = {"status": "INSTALLED", "note": "Web providers currently require Cloudflare solver or free model selection"}
    print("  ✅ g4f library installed and available as secondary fallback.")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    results["g4f Engine"] = {"status": "FAILED", "error": str(e)}

# -------------------------------------------------------------
# Summary Report
# -------------------------------------------------------------
print("\n" + "=" * 60)
print("📊 TEST SUMMARY REPORT")
print("=" * 60)
for name, data in results.items():
    status = data.get("status")
    print(f"  • {name:<22}: {status}")
print("=" * 60)
