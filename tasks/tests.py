from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import date

class TaskApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tasks = [
            {
                "id": "1",
                "title": "Fix login bug",
                "due_date": str(date.today()),
                "estimated_hours": 3,
                "importance": 8,
                "dependencies": []
            },
            {
                "id": "2",
                "title": "Write docs",
                "due_date": str(date.today()),
                "estimated_hours": 1,
                "importance": 6,
                "dependencies": ["1"]
            },
        ]

    def test_analyze_endpoint(self):
        url = "/api/tasks/analyze/"
        resp = self.client.post(url, {"strategy": "smart_balance", "tasks": self.tasks}, format="json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("tasks", data)
        self.assertEqual(len(data["tasks"]), 2)

    def test_suggest_endpoint(self):
        url = "/api/tasks/suggest/"
        resp = self.client.post(url, {"strategy": "smart_balance", "tasks": self.tasks}, format="json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("top_tasks", data)
        self.assertTrue(1 <= len(data["top_tasks"]) <= 3)

    def test_invalid_strategy(self):
        url = "/api/tasks/analyze/"
        resp = self.client.post(url, {"strategy": "unknown", "tasks": self.tasks}, format="json")
        self.assertEqual(resp.status_code, 400)
