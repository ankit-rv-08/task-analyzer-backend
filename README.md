
# Task Priority Assistant

Task Priority Assistant is a small web app that scores and sorts tasks to help decide what to work on next. It provides a Django + Django REST Framework backend for scoring and a lightweight HTML/JavaScript frontend for interacting with the APIs.

---

## Tech Stack

- Backend:
  - Django
  - Django REST Framework
  - django-cors-headers
- Frontend:
  - HTML, CSS, vanilla JavaScript
- Dev environment:
  - GitHub Codespaces / VS Code
  - Python virtual environment

---

## Project Structure

- `task_analyzer/` – Django project configuration
- `tasks/` – app with scoring logic, serializers, views, and tests
- `frontend/`
  - `index.html` – UI for entering tasks and viewing results
  - `app.js` – calls backend APIs and renders responses
- `manage.py` – Django management script
- `requirements.txt` – Python dependencies
- `README.md` – this file

---

## Setup and Running (Backend)

1. Clone the repository.

2. Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate # Linux/macOS

On Windows: venv\Scripts\activate
text

3. Install dependencies:

pip install -r requirements.txt

text

4. Apply migrations:

python manage.py migrate

text

5. Run the development server:

python manage.py runserver 0.0.0.0:8000

text

The backend will be available at `http://localhost:8000/`.

---

## Setup and Running (Frontend)

1. Open the project folder in VS Code.

2. Use an extension like “Live Server” (or any static server) to open `frontend/index.html`:

   - Right‑click `frontend/index.html` → “Open with Live Server”, or
   - Serve the `frontend/` directory with any HTTP server.

3. Ensure the backend is running on `http://localhost:8000`.

The frontend expects the API base URL to be:

const API_BASE = "http://localhost:8000/api";

text

---

## Task Model (Conceptual)

Each task in the API is represented as a JSON object:

{
"id": "1",
"title": "Fix login bug",
"due_date": "2025-11-30",
"estimated_hours": 3,
"importance": 8,
"dependencies": []
}

text

Fields:

- `id` (string) – client‑side identifier for dependency linking
- `title` (string) – task title
- `due_date` (string, `YYYY-MM-DD`, optional)
- `estimated_hours` (number, optional)
- `importance` (integer 1–10)
- `dependencies` (array of task IDs that this task depends on)

---

## API Endpoints

### 1. Analyze Tasks

- Method: `POST`
- URL: `/api/tasks/analyze/`

Request body:

{
"strategy": "smart_balance",
"tasks": [
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
}

text

Response shape:

{
"strategy": "smart_balance",
"tasks": [
{
"id": "1",
"title": "Fix login bug",
"due_date": "2025-11-30",
"estimated_hours": 3.0,
"importance": 8,
"dependencies": [],
"score": 74.0,
"explanation": "Balanced by urgency, importance, effort, and dependencies."
},
{
"id": "2",
"title": "Write docs",
"due_date": "2025-12-05",
"estimated_hours": 1.0,
"importance": 6,
"dependencies": ["1"],
"score": 57.0,
"explanation": "Balanced by urgency, importance, effort, and dependencies."
}
]
}

text

Tasks are sorted in descending order of `score`.

### 2. Suggest Top Tasks

- Method: `POST`
- URL: `/api/tasks/suggest/`

Request body is the same as `/api/tasks/analyze/`.

Example response:

{
"strategy": "smart_balance",
"top_tasks": [
{
"id": "1",
"title": "Fix login bug",
"score": 74.0,
"strategy": "smart_balance"
},
{
"id": "3",
"title": "Refactor dashboard",
"score": 62.0,
"strategy": "smart_balance"
},
{
"id": "2",
"title": "Write docs",
"score": 57.0,
"strategy": "smart_balance"
}
],
"message": "Top 3 tasks prioritized using Smart Balance strategy."
}

text

---

## Scoring Strategies

The project supports several strategies that decide how scores are computed:

- `fastest_wins`  
  Favors tasks with lower `estimated_hours` so that quick tasks rise to the top.

- `high_impact`  
  Favors tasks with high `importance`, ignoring effort and due date.

- `deadline_driven`  
  Favors tasks with near or overdue `due_date`, focusing primarily on urgency.

- `smart_balance`  
  Uses a weighted mix of:
  - importance (how impactful the task is),
  - urgency (how soon it is due),
  - effort (time required),
  - dependency impact (how many other tasks rely on it).

Each strategy uses the same input but different weights so the same task list can be re‑prioritized in multiple ways.

---

## Frontend Usage

1. Open the frontend in a browser.

2. Paste or edit the JSON array of tasks in the textarea.

3. Choose a strategy from the dropdown.

4. Click:
   - “Analyze Tasks” to see all tasks sorted by score.
   - “Suggest Top 3” to see only the three highest‑priority tasks.

The UI highlights tasks by score:

- High priority (score ≥ 70) – red accent
- Medium priority (40–70) – amber accent
- Low priority (< 40) – green accent

---

## Tests

Basic automated tests are included in `tasks/tests.py`:

- Verifies that `/api/tasks/analyze/` returns a valid response.
- Verifies that `/api/tasks/suggest/` returns up to three tasks.
- Verifies that an invalid strategy returns HTTP 400.

Run tests with:

python manage.py test tasks

text

---

## Future Improvements

Potential extensions:

- Richer task creation and editing UI.
- User accounts and persistent task lists.
- More advanced learning system that adjusts weights based on user feedback.
- Visualization of task dependencies and schedules.
