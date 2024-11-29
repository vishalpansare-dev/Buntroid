# notes.py

notes = []

def add_note(note):
    """Add a note."""
    notes.append(note)
    return f"Note added: {note}"

def list_notes():
    """List all notes."""
    if not notes:
        return "No notes available."
    return "\n".join(notes)

def remove_note(note):
    """Remove a note."""
    if note in notes:
        notes.remove(note)
        return f"Note '{note}' removed."
    else:
        return f"Note '{note}' not found."
