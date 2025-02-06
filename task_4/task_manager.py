import logging
import sqlite3
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename="task_manager.log", mode="a"),
        logging.StreamHandler(stream=sys.stdout),
    ],
)


DB_FILE = "tasks.db"


def setup_db() -> None:
    with sqlite3.connect(DB_FILE) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                due_date DATETIME,
                status TEXT CHECK(status IN ('pending', 'in_progress', 'completed')) NOT NULL DEFAULT 'pending'
            )
            """
        )


if __name__ == "__main__":
    setup_db()
