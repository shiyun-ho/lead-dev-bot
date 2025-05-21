import os
from fastapi import FastAPI
from jinja2 import Environment, FileSystemLoader
import requests
from pydantic import BaseModel

# === App Setup ===
app = FastAPI()

# === Template Setup ===
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# === LLM Config ===
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

# === Input Schema ===
class DesignPlanRequest(BaseModel):
    body: str

# === Routes ===
@app.post("/review")
async def review_design(request: DesignPlanRequest):
    # Load template
    prompt_template = jinja_env.get_template("lead_dev_prompt.j2")
    rendered_prompt = prompt_template.render(issue_body=request.body)

    # Call Ollama
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": rendered_prompt},
            timeout=60
        )
        response.raise_for_status()
        feedback = response.json()["response"]
    except Exception as e:
        return {"error": str(e)}

    return {
        "prompt": rendered_prompt,
        "feedback": feedback
    }