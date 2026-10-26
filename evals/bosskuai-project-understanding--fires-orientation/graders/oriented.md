---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Says it is a FastAPI app (from pyproject.toml and app/main.py) and points out that the README's 'Flask' and `python app.py` do not match the code.
- Gives the run command from the Makefile (`uvicorn app.main:app --reload`, or `make run`).
- Points to where the logic lives: routes in app/routes/notes.py calling app/services/notes.py, with the database session from app/db.py.
- Marks what it could not confirm (the unseen services, db and tests files) instead of describing them as fact.

Pass only if every point holds.
