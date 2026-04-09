import requests
import json
url = "http://localhost:11434/api/generate"
payload = {
    "model": "phi3",
    "prompt": "Hello, how are you?",
    "stream": False
}
try:
    print("Sending request to Ollama...")
    response = requests.post(url, json=payload, timeout=60)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result.get('response', 'No response')}")
except Exception as e:
    print(f"Error: {e}")