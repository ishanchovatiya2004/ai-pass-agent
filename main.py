from fastapi import FastAPI
from pydantic import BaseModel
import json
from ai_agent import analyze_task
from sheets_logger import log_task

app = FastAPI()

class TaskRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "AI-Pass Automation Agent is Live"}

@app.post("/task")
def run_task(request: TaskRequest):
    # 1. AI Analysis
    ai_result_string = analyze_task(request.message)
    
    try:
        parsed = json.loads(ai_result_string)
    except Exception as e:
        return {"error": "AI returned invalid JSON", "raw_output": ai_result_string}

    # 2. Log to Google Sheets
    log_success = log_task(parsed.get("task", "Unknown"), parsed.get("participants", []))

    # 3. Structured Output
    return {
        "task": parsed.get("task"),
        "status": "completed" if log_success else "failed_to_log",
        "participants": parsed.get("participants"),
        "logged_to_sheet": log_success
    }