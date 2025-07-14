import requests

headers = {
    "ngrok-skip-browser-warning": "true"
}

response = requests.get("https://55d07ccdc79b.ngrok-free.app", headers=headers)
print(response.text)
