
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import get_notes, add_note, update_note, delete_note, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    try:
        init_db()
        logger.info("Database initialized.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

@app.get("/notes")
def read_notes():
    try:
        return get_notes()
    except Exception as e:
        logger.error(f"Error fetching notes: {e}")
        raise HTTPException(status_code=500, detail="Error fetching notes")

@app.post("/notes")
def create_note(note: dict):
    try:
        note_id = add_note(note.get("content", ""))
        return {"id": note_id}
    except Exception as e:
        logger.error(f"Error creating note: {e}")
        raise HTTPException(status_code=500, detail="Error creating note")

@app.put("/notes/{note_id}")
def update_note_api(note_id: int, note: dict):
    try:
        update_note(note_id, note.get("content", ""))
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error updating note: {e}")
        raise HTTPException(status_code=500, detail="Error updating note")

@app.delete("/notes/{note_id}")
def delete_note_api(note_id: int):
    try:
        delete_note(note_id)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error deleting note: {e}")
        raise HTTPException(status_code=500, detail="Error deleting note")