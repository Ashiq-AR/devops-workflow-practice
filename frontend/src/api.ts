export const API_URL = import.meta.env.VITE_API_URL;

// Logger utility for frontend
const log = {
  info: (message: string, data?: any) => {
    console.log(`[INFO] ${new Date().toISOString()} - ${message}`, data || "");
  },
  error: (message: string, error?: any) => {
    console.error(
      `[ERROR] ${new Date().toISOString()} - ${message}`,
      error || ""
    );
  },
  debug: (message: string, data?: any) => {
    console.debug(
      `[DEBUG] ${new Date().toISOString()} - ${message}`,
      data || ""
    );
  },
};

log.info(`API_URL set to: ${API_URL}`);

export async function getNotes() {
  log.info("API Call: Fetching all notes");
  try {
    const res = await fetch(`${API_URL}/notes`);
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    const data = await res.json();
    log.info(`API Success: Retrieved ${data.length} notes`);
    return data;
  } catch (error) {
    log.error("API Error: Failed to fetch notes", error);
    throw error;
  }
}

export async function addNote(content: string) {
  log.info(`API Call: Creating new note with content length ${content.length}`);
  try {
    const res = await fetch(`${API_URL}/notes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    });
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    const data = await res.json();
    log.info(`API Success: Note created with ID ${data.id}`);
    return data;
  } catch (error) {
    log.error("API Error: Failed to create note", error);
    throw error;
  }
}

export async function updateNote(id: number, content: string) {
  log.info(
    `API Call: Updating note ID ${id} with content length ${content.length}`
  );
  try {
    const res = await fetch(`${API_URL}/notes/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    });
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    const data = await res.json();
    log.info(`API Success: Note ID ${id} updated successfully`);
    return data;
  } catch (error) {
    log.error(`API Error: Failed to update note ID ${id}`, error);
    throw error;
  }
}

export async function deleteNote(id: number) {
  log.info(`API Call: Deleting note ID ${id}`);
  try {
    const res = await fetch(`${API_URL}/notes/${id}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    const data = await res.json();
    log.info(`API Success: Note ID ${id} deleted successfully`);
    return data;
  } catch (error) {
    log.error(`API Error: Failed to delete note ID ${id}`, error);
    throw error;
  }
}
