from scripts.database import connect_db

def add_note(note_text):
    """Add a note to the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (note) VALUES (?)", (note_text,))
    conn.commit()
    conn.close()

def remove_note(note_text):
    """Remove a note from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE note = ?", (note_text,))
    conn.commit()
    conn.close()

def list_notes():
    """List all notes from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT note FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return [note[0] for note in notes]  # Return as a list of strings
