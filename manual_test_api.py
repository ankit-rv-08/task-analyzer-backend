import requests
import json

url = "http://localhost:8000/api/tasks/analyze/"

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
    }
]

payload = {
    "strategy": "fastest_wins",
    "tasks": tasks  # your existing tasks list
}
