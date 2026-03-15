from fastapi import FastAPI
from pydantic import BaseModel
import json
import re
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
    user_msg = request.message.strip()
    
    # --- 1. GREETING CHECK ---
    if user_msg.lower() in ["hi", "hello", "hii", "hey"]:
        return {"reply": "Hi! I am your AI-Pass Assistant. How can I help you today?"}

    # --- 2. GIBBERISH/NONSENSE CHECK (The Fix) ---
    # If the message is just one long word of gibberish or too short
    if " " not in user_msg or len(user_msg) < 8:
        return {
            "reply": "⚠️ **I didn't quite get that.**\n\n**Guide:** Please type a full instruction like: *'Meeting with Ishan'* or *'Task for Sarah'*."
        }

    # --- 3. NORMAL AI LOGIC ---
    try:
        ai_result_string = analyze_task(user_msg)
        parsed = json.loads(ai_result_string)
        
        # Log to Google Sheets
        log_success = log_task(parsed.get("task", "Unknown"), parsed.get("participants", []))
        
        return {
            "reply": f"Understood! I've logged the task: '{parsed.get('task')}' to your Google Sheet."
        }
    except Exception:
        return {
            "reply": "⚠️ **Invalid Task**\n\n**Guide:** Please use real words. Example: *'Schedule project review'*."
        }
