
import logging
import sys
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from models import get_notes, add_note, update_note, delete_note, init_db

# Configure structured logging for Kubernetes
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": "backend-notes-api"
        }
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        return json.dumps(log_data)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Notes API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Request completed: {request.method} {request.url.path} - Status: {response.status_code}")
    return response

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Notes API service...")
    try:
        init_db()
        logger.info("Database initialized successfully. Service is ready to accept requests.")
    except Exception as e:
        logger.error(f"CRITICAL: Failed to initialize database: {e}", exc_info=True)
        raise

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Notes API service...")

@app.get("/notes")
def read_notes():
    logger.info("Fetching all notes from database")
    try:
        notes = get_notes()
        logger.info(f"Successfully retrieved {len(notes)} notes")
        return notes
    except Exception as e:
        logger.error(f"Error fetching notes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching notes")

@app.post("/notes")
def create_note(note: dict):
    content = note.get("content", "")
    logger.info(f"Creating new note with content length: {len(content)}")
    try:
        note_id = add_note(content)
        logger.info(f"Successfully created note with ID: {note_id}")
        return {"id": note_id}
    except Exception as e:
        logger.error(f"Error creating note: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error creating note")

@app.put("/notes/{note_id}")
def update_note_api(note_id: int, note: dict):
    content = note.get("content", "")
    logger.info(f"Updating note ID: {note_id} with new content length: {len(content)}")
    try:
        update_note(note_id, content)
        logger.info(f"Successfully updated note ID: {note_id}")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error updating note ID {note_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error updating note")

@app.delete("/notes/{note_id}")
def delete_note_api(note_id: int):
    logger.info(f"Deleting note ID: {note_id}")
    try:
        delete_note(note_id)
        logger.info(f"Successfully deleted note ID: {note_id}")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error deleting note ID {note_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error deleting note")

@app.get("/health")
def health_check():
    """Health check endpoint for Kubernetes liveness/readiness probes"""
    return {"status": "healthy", "service": "backend-notes-api"}

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"service": "Notes API", "version": "1.0.0", "status": "running"}