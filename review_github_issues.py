import os
import json
import logging
import requests
from github import Github, Auth
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

# === Setup ===
load_dotenv()
logging.basicConfig(level=logging.INFO)

# === Config ===
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
LABEL_NAME = os.getenv("LABEL_NAME", "design-review")
FASTAPI_URL = "http://localhost:8000/review"

# === Prompt Setup ===
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# === GitHub Setup ===
auth = Auth.Token(GITHUB_TOKEN) # type: ignore
g = Github(auth=auth)
repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

# === Functions ===
def get_open_design_issues():
    label = repo.get_label(LABEL_NAME)
    issues = repo.get_issues(labels=[label], state="open")
    return issues

def has_bot_comment(issue):
    for comment in issue.get_comments():
        if comment.body.startswith("🤖 Lead Dev Feedback"):
            return True
    return False

def send_to_fastapi(issue_body):
    payload = {"body": issue_body}
    try:
        response = requests.post(FASTAPI_URL, json=payload, timeout=300)
        response.raise_for_status()
        return response.json()["feedback"]
    except requests.exceptions.ReadTimeout:
        logging.error("🚨 FastAPI call timed out — LLM is taking too long.")
        return "🚨 Timed out waiting for feedback. Try simplifying the prompt or upgrading your model."

    except Exception as e:
        logging.error(f"Error calling FastAPI: {str(e)}")
        return f"🚨 Failed to get feedback: {str(e)}"

def post_feedback_comment(issue, feedback):
    comment = f"🤖 Lead Dev Feedback (Jared Mode)\n-------------------------------\n\n{feedback}"
    issue.create_comment(comment)

# === Main ===
def main():
    print(f"🔍 Checking {repo.full_name} for open `{LABEL_NAME}` issues...")
    issues = get_open_design_issues()

    if not issues:
        print("📭 No open design review issues found.")
        return

    for issue in issues:
        print(f"\n📌 Reviewing issue: #{issue.number} - {issue.title}")
        if has_bot_comment(issue):
            print(f"💬 Already reviewed. Skipping.")
            continue

        feedback = send_to_fastapi(issue.body)
        post_feedback_comment(issue, feedback)
        print(f"✅ Posted feedback to issue #{issue.number}")

if __name__ == "__main__":
    main()