AI-Pass: Mini AI Task Automation Agent
An autonomous orchestration platform that leverages LLMs to analyze user intent and execute multi-step automation workflows via real-world API integrations.

* Live Demo
Public URL: https://your-app-name.onrender.com


* Architecture Overview
The system follows a Decoupled Agentic Workflow:

Intent Extraction: Natural language input is processed by Gemini 1.5 Flash to identify the specific task and relevant participants.

Tool Orchestration: A reasoning layer determines the necessary "tools" (APIs) required to satisfy the request.

Automation Execution: The system interacts with the Google Sheets API to provide persistent logging and monitoring of all agent activities.

Structured Output: Every request returns a machine-readable JSON object conforming to the platform's reliability standards.

* Technical Stack
AI Model: Google Gemini 1.5 Flash.

Framework: FastAPI (Python) for high-performance asynchronous request handling.

APIs: Google Workspace (Sheets).

Deployment: Hosted on Render with secure environment variable management.

* Environment Variables
To maintain security, credentials are not stored in the repository. The following secrets are configured in the production environment:

GEMINI_API_KEY: Authentication for the generative AI layer.

SERVICE_ACCOUNT_JSON: Full JSON credentials for Google Cloud service account access.

* Features
AI Task Analysis: Dynamically extracts data from unstructured text.

Workflow Logging: Automatically appends every successful task to a centralized Google Sheet.

Error Handling: Implements a "fail-safe" mechanism to ensure the system remains operational even if the LLM encounters versioning conflicts.

Live Monitoring: Users can track agent actions in real-time via the shared Google Sheet.

* Testing the Agent
To test the live system, send a POST request to the /task endpoint:

Request Body:

JSON
{
  "message": "Schedule a project sync with Sarah and John for next Monday."
}
Expected Response:

JSON
{
  "task": "Schedule a project sync",
  "status": "completed",
  "participants": ["Sarah", "John"],
  "logged_to_sheet": true
}