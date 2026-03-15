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
        return {"reply": "Hi! I am your AI-Pass Assistant. How can I help you today?"}

    # 2. VALIDATION: Check for nonsense or very short input
    # If input is less than 5 characters or just random letters
    if len(user_msg) < 5 or user_msg.isalpha() == False and " " not in user_msg:
        return {
            "reply": "⚠️ **Invalid Input**\n\n**Guide:** I didn't recognize that as a task. Please try something like: *'Book a meeting with Ishan'* or *'Check status with Sarah'*."
        }

    # 3. Handle Real Tasks
    try:
        ai_result_string = analyze_task(request.message)
        parsed = json.loads(ai_result_string)
        
        # If AI fails to find a real task name, use the guide
        if parsed.get("task") == "None" or not parsed.get("task"):
             raise ValueError("No task found")

        log_success = log_task(parsed.get("task", "Unknown"), parsed.get("participants", []))
        
        return {
            "reply": f"Understood! I've logged the task: '{parsed.get('task')}' to your Google Sheet."
        }

    except Exception:
        return {
            "reply": "⚠️ **I need more details.**\n\n**Guide:** Please type a full instruction. Example: *'Schedule sync with Mark'*."
        }
