---
description: "Onboarding to a small repo whose README disagrees with the code."
tags: ["lean", "bosskuai-project-understanding", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

I just joined this project and need a quick orientation: what it is, how to run it, and where the main logic lives. Here are the key files.

README.md:
```
# shopnotes
A Flask app for small shops to keep customer notes.
Run: python app.py
```

pyproject.toml:
```
[project]
name = "shopnotes"
dependencies = ["fastapi>=0.110", "uvicorn>=0.29", "sqlalchemy>=2.0"]
```

app/main.py:
```python
from fastapi import FastAPI
from app.routes import notes

app = FastAPI()
app.include_router(notes.router, prefix="/notes")
```

app/routes/notes.py:
```python
from fastapi import APIRouter, Depends
from app.db import get_session
from app.services.notes import create_note, list_notes

router = APIRouter()

@router.post("/")
def add(body: dict, session=Depends(get_session)):
    return create_note(session, body["customer_id"], body["text"])

@router.get("/{customer_id}")
def get_all(customer_id: int, session=Depends(get_session)):
    return list_notes(session, customer_id)
```

Makefile:
```
run:
	uvicorn app.main:app --reload
test:
	pytest -q
```

There is also app/services/notes.py, app/db.py and a tests/ folder (not shown).
