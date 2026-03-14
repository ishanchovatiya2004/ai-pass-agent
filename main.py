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
    user_msg = request.message.lower().strip()

    # 1. Handle Greetings (Mentor Requirement)
    greetings = ["hi", "hello", "hey", "hii", "hey there"]
    if user_msg in greetings:
        return {
            "reply": "Hi! I am your AI-Pass Assistant. How can I help you today?"
        }

    # 2. Handle Tasks
    ai_result_string = analyze_task(request.message)
    try:
        parsed = json.loads(ai_result_string)
    except Exception:
        return {"reply": "I'm sorry, I couldn't process that. Can you please describe the task again?"}

    log_success = log_task(parsed.get("task", "Unknown"), parsed.get("participants", []))

    return {
        "reply": f"Understood! I've logged the task: '{parsed.get('task')}' to your Google Sheet."
    }
