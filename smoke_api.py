import requests


# 1. Health
response = requests.get("http://127.0.0.1:8000/health")

print(response.status_code)
print(response.json())

response = requests.post(
    "http://127.0.0.1:8000/ask",
    json={"question": "你好"}
)

print(response.status_code)
print(response.json())

response = requests.post(
    "http://127.0.0.1:8000/ask",
    json={}
)

print(response.status_code)
print(response.json())