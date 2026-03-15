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

    # 1. Handle Greetings
    greetings = ["hi", "hello", "hey", "hii", "hey there"]
    if user_msg in greetings:
        return {
            "reply": "Hi! I am your AI-Pass Assistant. How can I help you today?"
        }

    # 2. Handle Tasks with Error Handling
    try:
        ai_result_string = analyze_task(request.message)
        parsed = json.loads(ai_result_string)
        
        # Log to Google Sheets
        log_success = log_task(parsed.get("task", "Unknown"), parsed.get("participants", []))
        
        return {
            "reply": f"Understood! I've logged the task: '{parsed.get('task')}' to your Google Sheet."
        }

    except Exception as e:
        # Error Guidance Scenario
        return {
            "reply": "⚠️ I encountered an issue processing that. \n\n**Guide:** Please try typing a specific instruction like: *'Schedule a sync with Sarah'* or *'Follow up on the project with John'*. Make sure to include a task and a person's name."
        }
