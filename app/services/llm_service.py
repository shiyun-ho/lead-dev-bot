# === Template Setup ===
import logging
import os

from jinja2 import Environment, FileSystemLoader


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# === LLM Config ===
base_url = os.getenv("OLLAMA_BASE_URL")
if base_url is None:
    raise ValueError("Environment variable OLLAMA_URL is not set")

OLLAMA_URL = base_url + "/api/generate"
MODEL_NAME = os.getenv("MODEL_NAME")

logging.basicConfig(level=logging.INFO)