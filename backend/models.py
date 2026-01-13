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
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        logger.info(f"Connected to PostgreSQL at {DB_HOST}:{DB_PORT}, DB: {DB_NAME}")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        raise


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()


def get_notes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM notes ORDER BY id DESC;')
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return notes


def add_note(content):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO notes (content) VALUES (%s) RETURNING id;', (content,))
    note_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return note_id


def update_note(note_id, content):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE notes SET content=%s WHERE id=%s;', (content, note_id))
    conn.commit()
    cur.close()
    conn.close()


def delete_note(note_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE id=%s;', (note_id,))
    conn.commit()
    cur.close()
    conn.close()
