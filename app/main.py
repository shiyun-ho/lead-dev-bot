import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from jinja2 import Environment, FileSystemLoader
import requests
from pydantic import BaseModel
import logging
from lead_dev_bot.routes.design_review_routes import router as design_router

# === App Setup ===
app = FastAPI()

app.include_router(design_router, prefix="/review", tags=["Review"])

