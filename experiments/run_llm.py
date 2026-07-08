import requests
import json

def call_llama(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3:latest",
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "seed": 42
            # temperature = 0.7
        }
    }

    response = requests.post(url, json=payload)
    return response.json()["response"]