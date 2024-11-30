import logging

from assistant.database.database import insert_log

logging.basicConfig(
    filename="/Users/vishal_pansare/PycharmProjects/Buntroid/logs/app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(message, level="info"):
    levels = {
        "debug": logging.debug,
        "info": logging.info,
        "warning": logging.warning,
        "error": logging.error,
        "critical": logging.critical
    }
    levels.get(level, logging.info)(message)
    print(message)
    insert_log(message,level)
