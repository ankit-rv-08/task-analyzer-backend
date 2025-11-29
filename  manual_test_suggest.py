import requests
import json

url = "http://localhost:8000/api/tasks/suggest/"

tasks = [
    {
        "id": "1",
        "title": "Fix login bug",
        "due_date": "2025-11-30",
        "estimated_hours": 3,
        "importance": 8,
        "dependencies": []
    },
    {
        "id": "2",
        "title": "Write docs",
        "due_date": "2025-12-05",
        "estimated_hours": 1,
        "importance": 6,
        "dependencies": ["1"]
    },
    {
        "id": "3",
        "title": "Refactor dashboard",
        "due_date": "2025-12-10",
        "estimated_hours": 5,
        "importance": 9,
        "dependencies": []
    }
]

payload = {  # <-- THIS defines 'payload'
    "strategy": "smart_balance",
    "tasks": tasks
}

response = requests.post(url, json=payload)

print("Status code:", response.status_code)
print("Response JSON:", json.dumps(response.json(), indent=2))
