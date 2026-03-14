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
    user_msg = request.message.lower().strip()

    # 1. FIXED GREETING LOGIC
    if user_msg in ["hi", "hello", "hey", "hii"]:
        return {
            "task": "Greeting",
            "status": "completed",
            "participants": [],
            "logged_to_sheet": False,
            "reply": "Hi! I am your AI-Pass Assistant. How can I help you today?"
        }

    # 2. TASK LOGIC (Calling Gemini)
    ai_result_string = analyze_task(request.message)
    try:
        parsed = json.loads(ai_result_string)
    except Exception:
        return {"reply": "I'm sorry, I couldn't process that task. Could you rephrase it?"}

    log_success = log_task(parsed.get("task", "Unknown"), parsed.get("participants", []))

    return {
        "task": parsed.get("task"),
        "status": "completed" if log_success else "failed",
        "participants": parsed.get("participants"),
        "logged_to_sheet": log_success,
        "reply": f"Understood! I've logged the task: '{parsed.get('task')}' to the sheet."
    }
