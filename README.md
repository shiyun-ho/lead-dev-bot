## 🧾 README: Lead Dev Bot (aka "Jared")

> 🤖 A sarcastic, overworked lead dev bot who reviews your design plans like it's 7 PM on a Friday  
> Built with FastAPI + Ollama + local LLM + way too much caffeine

---

### 📦 What Is This?

This is your new best friend — **Jared**, a local design plan reviewer bot that:
- Reads GitHub-style issue templates
- Roasts bad design decisions
- Recommends real fixes
- Uses no cloud APIs — just your machine and a local LLM (like `phi3` or `llama3`)
- Keeps your code private and secure

Perfect for solo devs, bootstrapped startups, or anyone missing a tired tech lead.

---

### 🔧 Requirements

| Tool | Why You Need It |
|------|-----------------|
| Python 3.8+ | For FastAPI and Jinja2 templating |
| Ollama | To run local LLMs like `phi3`, `mistral`, or `llama3` |
| GitHub Account | If connecting to GitHub issues later |
| uv / pipenv / venv | For dependency isolation |

---

### 🛠️ Setup Instructions

#### 1. Clone the repo

```bash
git clone https://github.com/yourusername/lead-dev-bot.git
cd lead-dev-bot
```

#### 2. Set up virtual environment

Using `uv`:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Or using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 3. Install dependencies

```bash
pip install fastapi uvicorn ollama jinja2 pydantic python-dotenv requests
```

#### 4. Start Ollama

Make sure Ollama is running locally:

```bash
ollama serve
```

In another terminal, pull a model:

```bash
ollama pull phi3
# or
ollama pull llama3
```

#### 5. Configure GitHub access (optional)

If you want to connect this to GitHub later:

Create `.env` file:

```bash
GITHUB_TOKEN=your-personal-access-token
REPO_OWNER=your-github-username
REPO_NAME=your-repo-name
LABEL_NAME=design-review
```

> ⚠️ Never commit this file — add it to `.gitignore`

---

### 🚀 Running the Bot

#### Option A: Run the FastAPI server (for testing)

```bash
uvicorn app.main:app --reload
```

Then go to http://localhost:8000/docs to test `/review` endpoint.

#### Option B: Use CLI script to review a file

```bash
python review_cli.py sample_design_plan.md
```

You’ll get sassy feedback like:

```
🤖 Lead Dev Feedback (Jared Mode)
-------------------------------

- 🔥 Critical flaw: Storing JWTs in localStorage = XSS buffet.
  - Like giving hackers VIP access. At least warn us when the break-ins start.

- 🤦‍♂️ Reinventing auth? Bold move. Auth0 exists. Firebase exists.

📚 References:
- https://owasp.org/www-project-top-ten/
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
```

---

### 📁 Project Structure

```
lead-dev-bot/
├── app/
│   ├── main.py           # FastAPI bot server
│   └── templates/
│       └── lead_dev_prompt.j2  # Jared's personality lives here
├── review_cli.py         # CLI version for local use
├── requirements.txt
├── .env                  # GitHub token and repo config
└── README.md             # That's you reading this right now 😎
```

---

### 🧪 Sample Design Plan (`sample_design_plan.md`)

```markdown
Problem Statement: We need to store JWT tokens.

Proposed Approach: Store them in localStorage and send on every request.
```

---

### 🎯 Future Ideas

- GitHub Action integration for auto-commenting
- Auto-pull from GitHub issues
- Multiple bot personalities (e.g., “Senior Dev Mode”, “CTO Roast Mode”)
- CLI tool installable via `pipx`

---

### ❤️ Credits

Built with 💻 by [ShiYun](@shiyun-ho)  
For all the junior devs who just need one more reason to not store tokens in localStorage.
