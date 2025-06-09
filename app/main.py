import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from jinja2 import Environment, FileSystemLoader
import requests
from pydantic import BaseModel
import logging

# === App Setup ===
app = FastAPI()

# === Setup ===
load_dotenv()
logging.basicConfig(level=logging.INFO)

# === Template Setup ===
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# === LLM Config ===
base_url = os.getenv("OLLAMA_BASE_URL")
if base_url is None:
    raise ValueError("Environment variable OLLAMA_URL is not set")

OLLAMA_URL = base_url + "/api/generate"
MODEL_NAME = os.getenv("MODEL_NAME")

logging.basicConfig(level=logging.INFO)

# === Input Schema ===
class DesignPlanRequest(BaseModel):
    body: str

# === Routes ===
@app.post("/review")
async def review_design(request: DesignPlanRequest):
    # Load template
    prompt_template = jinja_env.get_template("lead_dev_prompt.j2")
    rendered_prompt = prompt_template.render(issue_body=request.body)

    logging.info("Sending prompt to LLM:")
    logging.info(rendered_prompt)

    # Call Ollama
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": rendered_prompt},
            timeout=60,
            stream=True  # Enable streaming
        )
        response.raise_for_status()

        # Combine streamed JSON chunks into one
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    json_line = json.loads(decoded_line)
                    full_response += json_line.get("response", "")
                except json.JSONDecodeError:
                    continue  # Skip malformed lines

        feedback = full_response.strip()

    except Exception as e:
        logging.error(f"Error calling LLM: {str(e)}")
        return {"error": str(e)}

    return {
        "prompt": rendered_prompt,
        "feedback": feedback
    }

@app.post("/review/cli")
async def review_design_cli(request: DesignPlanRequest):
    # Load template
    prompt_template = jinja_env.get_template("lead_dev_prompt.j2")
    rendered_prompt = prompt_template.render(issue_body=request.body)

    # Call Ollama
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": rendered_prompt},
            timeout=60,
            stream=True
        )
        response.raise_for_status()

        # Parse streamed response
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    json_line = json.loads(decoded_line)
                    full_response += json_line.get("response", "")
                except json.JSONDecodeError:
                    continue  # Skip invalid lines

        feedback = full_response.strip()

    except Exception as e:
        return {"error": str(e)}

    # Print clean markdown-style feedback in terminal
    print("🤖 Lead Dev Feedback:")
    print(feedback.replace("\\n", "\n"))
    print("---")

    return {
        "prompt": rendered_prompt,
        "feedback": feedback
    }