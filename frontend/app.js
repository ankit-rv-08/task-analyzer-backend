const API_BASE = "http://localhost:8000/api";

const tasksInput = document.getElementById("tasksInput");
const strategySelect = document.getElementById("strategySelect");
const analyzeBtn = document.getElementById("analyzeBtn");
const suggestBtn = document.getElementById("suggestBtn");
const resultsDiv = document.getElementById("results");
const errorDiv = document.getElementById("error");

function getPriorityClass(score) {
  if (score >= 70) return "high";
  if (score >= 40) return "medium";
  return "low";
}

function renderAnalyzeResult(data) {
  resultsDiv.innerHTML = "";
  const tasks = data.tasks || [];
  tasks.forEach(t => {
    const div = document.createElement("div");
    div.className = "task " + getPriorityClass(t.score);
    div.innerHTML = `
      <div><span class="score">${t.score}</span> - ${t.title}</div>
      <div><small>Due: ${t.due_date || "None"} | Hours: ${t.estimated_hours ?? "?"} | Importance: ${t.importance}</small></div>
      <div><small>Strategy: ${data.strategy}</small></div>
      <div><small>${t.explanation || ""}</small></div>
    `;
    resultsDiv.appendChild(div);
  });
}

function renderSuggestResult(data) {
  resultsDiv.innerHTML = "";
  const tasks = data.top_tasks || [];
  tasks.forEach(t => {
    const div = document.createElement("div");
    div.className = "task " + getPriorityClass(t.score);
    div.innerHTML = `
      <div><span class="score">${t.score}</span> - ${t.title}</div>
      <div><small>Strategy: ${data.strategy}</small></div>
    `;
    resultsDiv.appendChild(div);
  });
}

function parseTasksJson() {
  try {
    const text = tasksInput.value;
    const tasks = JSON.parse(text);
    if (!Array.isArray(tasks)) {
      throw new Error("JSON must be an array of tasks");
    }
    return tasks;
  } catch (err) {
    throw new Error("Invalid JSON: " + err.message);
  }
}

async function callApi(path, renderFn) {
  errorDiv.textContent = "";
  resultsDiv.innerHTML = "Loading...";
  let tasks;
  try {
    tasks = parseTasksJson();
  } catch (err) {
    resultsDiv.innerHTML = "";
    errorDiv.textContent = err.message;
    return;
  }

  const strategy = strategySelect.value;

  try {
    const resp = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ strategy, tasks })
    });

    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(`Error ${resp.status}: ${text}`);
    }

    const data = await resp.json();
    renderFn(data);
  } catch (err) {
    resultsDiv.innerHTML = "";
    errorDiv.textContent = err.message;
  }
}

analyzeBtn.addEventListener("click", () => {
  callApi("/tasks/analyze/", renderAnalyzeResult);
});

suggestBtn.addEventListener("click", () => {
  callApi("/tasks/suggest/", renderSuggestResult);
});
