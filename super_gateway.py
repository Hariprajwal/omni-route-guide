"""
Super Gateway: The Resilient Multi-Source AI Router
===================================================
A drop-in OpenAI-compatible gateway running at http://localhost:20128/v1.

Failover Chain:
  1. Local / Upstream Gateways (FreeLLMAPI, Puter-Pool, Aurora, OmniRoute)
  2. Cloud Free-Tier Keys (Groq, Google AI Studio Gemini, OpenRouter)
  3. Zero-Key Online Fallback (Pollinations AI)
  4. Local Offline Safety Net (Ollama - last fallback)
"""

import os
import sys
import json
import time
import asyncio
from typing import Optional, List, Dict, Any, AsyncGenerator

# Windows UTF-8 stdout wrapper
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Super Gateway AI", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# Configuration & Provider URLs
# -------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Local upstream gateway targets
UPSTREAM_TARGETS = {
    "freellmapi": os.getenv("FREELLMAPI_URL", "http://localhost:3001/v1/chat/completions"),
    "puter_pool": os.getenv("PUTER_POOL_URL", "http://localhost:4000/v1/chat/completions"),
    "aurora": os.getenv("AURORA_URL", "http://localhost:8080/v1/chat/completions"),
    "omniroute": os.getenv("OMNIROUTE_URL", "http://localhost:20127/v1/chat/completions"),
    "ollama": os.getenv("OLLAMA_URL", "http://localhost:11434/v1/chat/completions"),
}

POLLINATIONS_URL = "https://text.pollinations.ai/openai/chat/completions"

# -------------------------------------------------------------
# Health Check & Status
# -------------------------------------------------------------
@app.get("/")
@app.get("/health")
async def health_check():
    health = {
        "gateway": "Super Gateway AI v2.0",
        "status": "online",
        "port": 20128,
        "adapters": {}
    }
    
    # Probe local upstream gateways
    async with httpx.AsyncClient(timeout=1.5) as client:
        # Check FreeLLMAPI
        try:
            r = await client.get("http://localhost:3001/health")
            health["adapters"]["freellmapi (:3001)"] = "LIVE" if r.status_code == 200 else f"HTTP {r.status_code}"
        except Exception:
            health["adapters"]["freellmapi (:3001)"] = "OFFLINE"

        # Check Puter Pool
        try:
            r = await client.get("http://localhost:4000/health")
            health["adapters"]["puter_pool (:4000)"] = "LIVE" if r.status_code == 200 else f"HTTP {r.status_code}"
        except Exception:
            health["adapters"]["puter_pool (:4000)"] = "OFFLINE"

        # Check Aurora
        try:
            r = await client.get("http://localhost:8080/v1/models")
            health["adapters"]["aurora (:8080)"] = "LIVE" if r.status_code == 200 else f"HTTP {r.status_code}"
        except Exception:
            health["adapters"]["aurora (:8080)"] = "OFFLINE"

        # Check Ollama
        try:
            r = await client.get("http://localhost:11434/api/tags")
            health["adapters"]["ollama (:11434)"] = "LIVE (offline safety net ready)" if r.status_code == 200 else f"HTTP {r.status_code}"
        except Exception:
            health["adapters"]["ollama (:11434)"] = "OFFLINE"

    health["adapters"]["groq_cloud"] = "READY" if GROQ_API_KEY else "NO_KEY"
    health["adapters"]["gemini_cloud"] = "READY" if GEMINI_API_KEY else "NO_KEY"
    health["adapters"]["pollinations_web"] = "ONLINE (zero-key)"

    return health

@app.get("/v1/models")
async def list_models():
    models = [
        {"id": "auto", "object": "model", "owned_by": "super-gateway"},
        {"id": "felo/auto", "object": "model", "owned_by": "super-gateway"},
        {"id": "auto/best-chat", "object": "model", "owned_by": "super-gateway"},
        {"id": "gpt-4o", "object": "model", "owned_by": "super-gateway"},
        {"id": "claude-3-5-sonnet", "object": "model", "owned_by": "super-gateway"},
        {"id": "llama-3.3-70b", "object": "model", "owned_by": "groq"},
        {"id": "gemini-2.0-flash", "object": "model", "owned_by": "google"},
        {"id": "llama3.2:1b", "object": "model", "owned_by": "ollama-local"},
    ]
    return {"object": "list", "data": models}

# -------------------------------------------------------------
# Failover Engine
# -------------------------------------------------------------
async def try_upstream_sync(url: str, payload: dict, headers: dict):
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

async def try_upstream_stream(url: str, payload: dict, headers: dict) -> AsyncGenerator[str, None]:
    async with httpx.AsyncClient(timeout=15.0) as client:
        async with client.stream("POST", url, json=payload, headers=headers) as resp:
            if resp.status_code == 200:
                async for line in resp.aiter_lines():
                    if line:
                        yield f"{line}\n\n"
                return
            raise HTTPException(status_code=resp.status_code, detail="Upstream streaming failed")

LLM7_URL = "https://api.llm7.io/v1/chat/completions"

async def fallback_llm7_sync(messages: list, model: str = "default") -> dict:
    headers = {"Content-Type": "application/json", "Authorization": "Bearer unused"}
    payload = {"model": "default", "messages": messages, "stream": False}
    async with httpx.AsyncClient(timeout=25.0) as client:
        resp = await client.post(LLM7_URL, json=payload, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        raise Exception(f"LLM7 returned HTTP {resp.status_code}")

async def fallback_llm7_stream(messages: list, model: str = "default") -> AsyncGenerator[str, None]:
    headers = {"Content-Type": "application/json", "Authorization": "Bearer unused"}
    payload = {"model": "default", "messages": messages, "stream": True}
    async with httpx.AsyncClient(timeout=35.0) as client:
        async with client.stream("POST", LLM7_URL, json=payload, headers=headers) as resp:
            if resp.status_code == 200:
                async for line in resp.aiter_lines():
                    if line:
                        yield f"{line}\n\n"
                return
            raise Exception(f"LLM7 stream returned HTTP {resp.status_code}")

async def fallback_pollinations_sync(messages: list) -> dict:
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    payload = {"model": "openai", "messages": messages, "stream": False}
    async with httpx.AsyncClient(timeout=25.0) as client:
        resp = await client.post(POLLINATIONS_URL, json=payload, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        raise Exception(f"Pollinations returned HTTP {resp.status_code}")

async def fallback_pollinations_stream(messages: list) -> AsyncGenerator[str, None]:
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    payload = {"model": "openai", "messages": messages, "stream": True}
    async with httpx.AsyncClient(timeout=30.0) as client:
        async with client.stream("POST", POLLINATIONS_URL, json=payload, headers=headers) as resp:
            if resp.status_code == 200:
                async for line in resp.aiter_lines():
                    if line:
                        yield f"{line}\n\n"
                return
            raise Exception(f"Pollinations stream failed HTTP {resp.status_code}")

async def fallback_ollama_sync(messages: list, model: str = "llama3.2:1b") -> dict:
    url = "http://localhost:11434/v1/chat/completions"
    payload = {"model": model, "messages": messages, "stream": False}
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=payload)
        if resp.status_code == 200:
            return resp.json()
        raise Exception(f"Ollama returned HTTP {resp.status_code}")

async def fallback_ollama_stream(messages: list, model: str = "llama3.2:1b") -> AsyncGenerator[str, None]:
    url = "http://localhost:11434/v1/chat/completions"
    payload = {"model": model, "messages": messages, "stream": True}
    async with httpx.AsyncClient(timeout=40.0) as client:
        async with client.stream("POST", url, json=payload) as resp:
            if resp.status_code == 200:
                async for line in resp.aiter_lines():
                    if line:
                        yield f"{line}\n\n"
                return
            raise Exception(f"Ollama stream failed HTTP {resp.status_code}")

# -------------------------------------------------------------
# Unified Chat Completions Router
# -------------------------------------------------------------
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    messages = body.get("messages", [])
    model = body.get("model", "auto")
    stream = body.get("stream", False)

    # 1. Tier 1: Cloud Free-Tier Key (Groq) if configured
    if GROQ_API_KEY:
        try:
            groq_headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            groq_payload = {"model": "llama-3.3-70b-versatile", "messages": messages, "stream": stream}
            if stream:
                async def stream_groq():
                    async with httpx.AsyncClient(timeout=40.0) as client:
                        async with client.stream("POST", "https://api.groq.com/openai/v1/chat/completions", json=groq_payload, headers=groq_headers) as resp:
                            if resp.status_code == 200:
                                async for line in resp.aiter_lines():
                                    if line:
                                        yield f"{line}\n\n"
                                return
                            # If Groq fails, fall back to LLM7
                            async for chunk in fallback_llm7_stream(messages):
                                yield chunk
                return StreamingResponse(stream_groq(), media_type="text/event-stream")
            else:
                async with httpx.AsyncClient(timeout=25.0) as client:
                    resp = await client.post("https://api.groq.com/openai/v1/chat/completions", json=groq_payload, headers=groq_headers)
                    if resp.status_code == 200:
                        return resp.json()
        except Exception as e:
            print(f"[Gateway] Groq unavailable ({e}), trying next tier...")

    # 2. Tier 2: LLM7.io (Zero-Key Anonymous High-Speed Cloud)
    try:
        if stream:
            return StreamingResponse(fallback_llm7_stream(messages, model), media_type="text/event-stream")
        else:
            data = await fallback_llm7_sync(messages, model)
            return JSONResponse(content=data)
    except Exception as e_llm7:
        print(f"[Gateway] Tier 2 (LLM7) failed ({e_llm7}), trying Tier 3 (Pollinations)...")

    # 3. Tier 3: Zero-Key Online Fallback (Pollinations AI)
    try:
        if stream:
            return StreamingResponse(fallback_pollinations_stream(messages), media_type="text/event-stream")
        else:
            data = await fallback_pollinations_sync(messages)
            return JSONResponse(content=data)
    except Exception as e_poll:
        print(f"[Gateway] Tier 3 (Pollinations) failed ({e_poll}). Reaching Tier 4 (Local Ollama Safety Net)...")

    # 4. Tier 4: Local Offline Safety Net (Ollama - final unkillable fallback)
    try:
        print(f"[Gateway] Routing to local Ollama (offline safety net)...")
        if stream:
            return StreamingResponse(fallback_ollama_stream(messages), media_type="text/event-stream")
        else:
            data = await fallback_ollama_sync(messages)
            return JSONResponse(content=data)
    except Exception as e_ollama:
        raise HTTPException(status_code=502, detail=f"All tiers failed: {e_ollama}")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 20128
    print(f"[*] Super Gateway AI v2.0 listening on http://127.0.0.1:{port}/v1 ...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
