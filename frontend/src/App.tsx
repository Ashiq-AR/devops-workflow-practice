import { useEffect, useState } from "react";
import { getNotes, addNote, updateNote, deleteNote } from "./api";
import "./App.css";

interface Note {
  id: number;
  content: string;
}

// Logger utility
const log = {
  info: (message: string, data?: any) => {
    console.log(`[APP] ${new Date().toISOString()} - ${message}`, data || "");
  },
  error: (message: string, error?: any) => {
    console.error(
      `[APP] ${new Date().toISOString()} - ${message}`,
      error || ""
    );
  },
};

function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [newNote, setNewNote] = useState("");
  const [editId, setEditId] = useState<number | null>(null);
  const [editContent, setEditContent] = useState("");

  useEffect(() => {
    log.info("App initialized - Loading notes");
    getNotes()
      .then((data) => {
        setNotes(data);
        log.info(`Loaded ${data.length} notes on startup`);
      })
      .catch((error) => {
        log.error("Failed to load notes on startup", error);
      });
  }, []);

  const handleAdd = async () => {
    if (!newNote.trim()) {
      log.info("Add note aborted - empty content");
      return;
    }
    log.info(`User action: Adding new note`);
    try {
      await addNote(newNote);
      setNewNote("");
      const updatedNotes = await getNotes();
      setNotes(updatedNotes);
      log.info("Note added successfully and list refreshed");
    } catch (error) {
      log.error("Failed to add note", error);
      alert("Failed to add note. Please try again.");
    }
  };

  const handleEdit = (note: Note) => {
    log.info(`User action: Editing note ID ${note.id}`);
    setEditId(note.id);
    setEditContent(note.content);
  };

  const handleUpdate = async () => {
    if (editId === null) return;
    log.info(`User action: Saving changes to note ID ${editId}`);
    try {
      await updateNote(editId, editContent);
      setEditId(null);
      setEditContent("");
      const updatedNotes = await getNotes();
      setNotes(updatedNotes);
      log.info(`Note ID ${editId} updated successfully and list refreshed`);
    } catch (error) {
      log.error(`Failed to update note ID ${editId}`, error);
      alert("Failed to update note. Please try again.");
    }
  };

  const handleDelete = async (id: number) => {
    log.info(`User action: Deleting note ID ${id}`);
    try {
      await deleteNote(id);
      const updatedNotes = await getNotes();
      setNotes(updatedNotes);
      log.info(`Note ID ${id} deleted successfully and list refreshed`);
    } catch (error) {
      log.error(`Failed to delete note ID ${id}`, error);
      alert("Failed to delete note. Please try again.");
    }
  };

  const handleCancelEdit = () => {
    log.info(`User action: Cancelled editing note ID ${editId}`);
    setEditId(null);
    setEditContent("");
  };

  return (
    <div className="App">
      <h1>Notes</h1>
      <div>
        <input
          value={newNote}
          onChange={(e) => setNewNote(e.target.value)}
          placeholder="Add a note"
        />
        <button onClick={handleAdd}>Add</button>
      </div>
      <ul>
        {notes.map((note) => (
          <li key={note.id}>
            {editId === note.id ? (
              <>
                <input
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                />
                <button onClick={handleUpdate}>Save</button>
                <button onClick={handleCancelEdit}>Cancel</button>
              </>
            ) : (
              <>
                {note.content}
                <button onClick={() => handleEdit(note)}>Edit</button>
                <button onClick={() => handleDelete(note.id)}>Delete</button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
