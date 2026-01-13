export const API_URL = "http://localhost:8000";

export async function getNotes() {
  const res = await fetch(`${API_URL}/notes`);
  return res.json();
}

export async function addNote(content: string) {
  const res = await fetch(`${API_URL}/notes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });
  return res.json();
}

export async function updateNote(id: number, content: string) {
  const res = await fetch(`${API_URL}/notes/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });
  return res.json();
}

export async function deleteNote(id: number) {
  const res = await fetch(`${API_URL}/notes/${id}`, {
    method: "DELETE",
  });
  return res.json();
}
