from logger import log_event
from scripts.database import setup_tables
from scripts.db_helper import initialize_database
from scripts.gui import create_gui


def main():
    try:
        initialize_database()
        log_event("Database initialized")
        create_gui()
        log_event("GUI launched successfully")
    except Exception as e:
        log_event(f"Critical Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
    # setup_tables()
