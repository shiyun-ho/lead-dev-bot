# Lead Dev Bot – Because You Need Someone to Roast You for localStorage JWTs 🔥

<p align="center">
  <img src="demo.gif" alt="Lead Dev Bot Demo Animation" /><br>
  <em>Watch as Lead Dev Bot roasts me for localStorage JWTs and eval() abuse 🤖🔥</em>
</p>

## Why Do This?

I knew there was something missing in my life — a lead dev who would look at my code and say:

> "What is this? A GitHub issue or a dumpster fire?"

Unfortunately, being the only dev at a startup means the only feedback I get is from my own inner voice — which has been on vacation since 2022 with the brainrot (TUNG TUNG SAHUR!) I'm consuming.

Without a real lead dev to stop me from doing localStorage JWTs:

- I found myself reinventing auth (again)
- Asking ChatGPT if `eval()` is safe “in moderation”
- Wondering if tech debt is just a lifestyle choice

So I did what any sane dev would do:

> 🧠 "I could code it myself."  
> 🤖 And thus, Lead Dev Bot was born.

### What Is It?

A local-first, privacy-respecting, slightly unhinged reviewer bot that gives actionable feedback — without letting you deploy XSS-prone garbage.

Built with:

- FastAPI (`app/main.py`)
- Ollama (`phi3`, `mistral`, etc.)
- GitHub Issue templates
- Way too much caffeine

Would’ve called it *Jared*... but don’t want a C&D letter 🙃

## Features

- Automatically reviews GitHub issues labeled for design review.
- Provides feedback in a concise, bullet-point format.
- Integrates with OpenAI's LLMs for generating feedback.
- Posts feedback directly as comments on GitHub issues.

## How It Works

1. **GitHub Integration**: The bot scans your GitHub repository for issues labeled with `design-review`.
2. **Feedback Generation**: It sends the issue content to a FastAPI endpoint, which uses a Jinja2 template to craft a prompt for the LLM.
3. **Feedback Posting**: The bot posts the generated feedback as a comment on the GitHub issue.

## Setup Instructions

### Prerequisites

- Python 3.12 or higher
- A GitHub repository with issues enabled
- A GitHub personal access token with `repo` scope
- FastAPI and required dependencies (see `pyproject.toml`)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/lead-dev-bot.git
   cd lead-dev-bot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.lock
   ```

3. Set up your environment variables in a `.env` file:

   ```env
   GITHUB_TOKEN=your_github_token
   REPO_OWNER=your_github_username
   REPO_NAME=your_repository_name
   LABEL_NAME=design-review
   OLLAMA_BASE_URL=http://localhost:8000
   MODEL_NAME=your_model_name
   ```

4. Start the FastAPI server:

   ```bash
   uvicorn app.main:app --reload
   ```

### Usage

1. Label GitHub issues with `design-review` to mark them for feedback.
2. Run the bot to review issues:

   ```bash
   python review_github_issues.py
   ```

3. Feedback will be posted as comments on the labeled issues.

## Example Feedback

Here’s an example of the feedback you can expect:

```
- 🔥 Critical flaw: localStorage JWT = hacker playground. HttpOnly cookies exist for a reason.
  - One XSS later and every user gets hijacked.

- 🤦‍♂️ Reinventing auth? Bold move. Auth0 exists. Firebase exists.

- 🐞 Token leakage via logs? Hope you like explaining breaches at 2 AM.
```
