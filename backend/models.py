import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'notesdb')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'admin')


def get_db_connection():
    try:
        logger.debug(f"Attempting to connect to PostgreSQL at {DB_HOST}:{DB_PORT}")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        logger.info(f"Successfully connected to PostgreSQL at {DB_HOST}:{DB_PORT}, DB: {DB_NAME}")
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"PostgreSQL connection failed - Service may not be available at {DB_HOST}:{DB_PORT}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error connecting to PostgreSQL: {e}", exc_info=True)
        raise


def init_db():
    logger.info("Initializing database schema...")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        );
    ''')
    conn.commit()
    logger.info("Database schema initialized: 'notes' table is ready")
    cur.close()
    conn.close()


def get_notes():
    logger.debug("Executing query to fetch all notes")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM notes ORDER BY id DESC;')
    notes = cur.fetchall()
    logger.debug(f"Query returned {len(notes)} notes")
    cur.close()
    conn.close()
    return notes


def add_note(content):
    logger.debug(f"Inserting new note into database")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO notes (content) VALUES (%s) RETURNING id;', (content,))
    note_id = cur.fetchone()['id']
    conn.commit()
    logger.debug(f"Note inserted with ID: {note_id}")
    cur.close()
    conn.close()
    return note_id


def update_note(note_id, content):
    logger.debug(f"Updating note ID: {note_id} in database")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE notes SET content=%s WHERE id=%s;', (content, note_id))
    rows_affected = cur.rowcount
    conn.commit()
    logger.debug(f"Note ID: {note_id} updated, rows affected: {rows_affected}")
    cur.close()
    conn.close()


def delete_note(note_id):
    logger.debug(f"Deleting note ID: {note_id} from database")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE id=%s;', (note_id,))
    rows_affected = cur.rowcount
    conn.commit()
    logger.debug(f"Note ID: {note_id} deleted, rows affected: {rows_affected}")
    cur.close()
    conn.close()
