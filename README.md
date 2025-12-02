# AI Task Generator (Dash)

Dash web app that generates study/tasks by topic using OpenAI, lets you mark tasks as done,
exports tasks (TXT/JSON), and analyzes progress with AI recommendations + history.

## Features
- Generate tasks by topic (AI)
- Checklist to track progress
- Export tasks to TXT / JSON
- Progress analysis + recommendations
- Analysis history stored in browser session (Dash Store)

## Tech Stack
Python • Dash • dash-bootstrap-components • OpenAI API

## Setup
### 1) Create virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

#Install dependencies
pip install -r requirements.txt

3) Configure environment

Create .env from example and set your key:

# Windows:
copy .env.example .env
# Linux/Mac:
cp .env.example .env


#.env:

OPENAI_API_KEY — your OpenAI API key

#Run
python app.py


#Open:

http://127.0.0.1:8050

#Project structure

app.py — Dash UI + callbacks

ai_generator.py — generate_tasks() and analyze_progress() (OpenAI logic)

export.py — export helpers (txt/json)

#Notes

Do not commit .env (contains secrets).

If you want to deploy, run with a production server (gunicorn) instead of debug mode.
