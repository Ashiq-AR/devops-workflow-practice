import React, { useEffect, useState } from "react";
import { getNotes, addNote, updateNote, deleteNote } from "./api";
import "./App.css";

interface Note {
  id: number;
  content: string;
}

function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [newNote, setNewNote] = useState("");
  const [editId, setEditId] = useState<number | null>(null);
  const [editContent, setEditContent] = useState("");

  useEffect(() => {
    getNotes().then(setNotes);
  }, []);

  const handleAdd = async () => {
    if (!newNote.trim()) return;
    await addNote(newNote);
    setNewNote("");
    setNotes(await getNotes());
  };

  const handleEdit = (note: Note) => {
    setEditId(note.id);
    setEditContent(note.content);
  };

  const handleUpdate = async () => {
    if (editId === null) return;
    await updateNote(editId, editContent);
    setEditId(null);
    setEditContent("");
    setNotes(await getNotes());
  };

  const handleDelete = async (id: number) => {
    await deleteNote(id);
    setNotes(await getNotes());
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
                <button onClick={() => setEditId(null)}>Cancel</button>
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
