#!/bin/bash

# Simple cURL command to test OmniRoute from the terminal (Mac/Linux/Git Bash)

curl http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dummy-key" \
  -d '{
    "model": "felo/auto",
    "stream": false,
    "messages": [
      {
        "role": "user",
        "content": "Hello! What can you do?"
      }
    ]
  }'
