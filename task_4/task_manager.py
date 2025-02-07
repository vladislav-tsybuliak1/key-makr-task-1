import logging
import sqlite3
import sys
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename="task_manager.log", mode="a"),
        logging.StreamHandler(stream=sys.stdout),
    ],
)


DB_FILE = "tasks.db"



def adapt_datetime(dt):
    return dt.isoformat()

sqlite3.register_adapter(datetime, adapt_datetime)


def setup_db() -> None:
    with sqlite3.connect(DB_FILE) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                due_date DATETIME NOT NULL,
                status TEXT CHECK(status IN ('pending', 'in_progress', 'completed')) NOT NULL DEFAULT 'pending'
            )
            """
        )


def add_task(title: str, due_date: datetime, description: str = None) -> None:
    with sqlite3.connect(DB_FILE) as db:
        db.execute(
            "INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)",
            (title, description, due_date),
        )


if __name__ == "__main__":
    setup_db()
    add_task(title="Title", due_date=datetime(2023, 12, 31, 12))
