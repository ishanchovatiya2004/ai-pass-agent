from fastapi import FastAPI
from pydantic import BaseModel
import json
from ai_agent import analyze_task
from sheets_logger import log_task

# 1. Initialize the app
app = FastAPI()

class TaskRequest(BaseModel):
    message: str

# 2. Add the Home route
@app.get("/")
def home():
    return {"message": "AI-Pass Automation Agent is Live"}

# 3. Add the Task route
@app.post("/task")
def run_task(request: TaskRequest):
    ai_result_string = analyze_task(request.message)
    try:
        parsed = json.loads(ai_result_string)
    except Exception:
        return {"error": "AI returned invalid JSON", "raw": ai_result_string}

    log_success = log_task(parsed.get("task", "Unknown"), parsed.get("participants", []))

    return {
        "task": parsed.get("task"),
        "status": "completed" if log_success else "failed",
        "participants": parsed.get("participants"),
        "logged_to_sheet": log_success
    }
