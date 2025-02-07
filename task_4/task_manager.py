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

TASK_STATUSES = ("pending", "in_progress", "completed")


def adapt_datetime(dt):
    return dt.isoformat()


sqlite3.register_adapter(datetime, adapt_datetime)


def setup_db() -> None:
    with sqlite3.connect(DB_FILE) as db:
        db.execute(
            f"""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                due_date DATETIME NOT NULL,
                status TEXT CHECK(status IN {TASK_STATUSES}) NOT NULL DEFAULT 'pending'
            )
            """
        )
        db.commit()


def validate_task(title: str, due_date: str) -> bool:
    if not title.strip():
        logging.error("Title cannot be empty")
        return False

    if len(title.strip()) > 255:
        logging.error("Title should contain maximum 255 symbols")
        return False

    try:
        datetime.strptime(due_date, "%Y-%m-%d %H:%M")
    except ValueError:
        logging.error("Invalid due date format. Use 'YYYY-MM-DD HH:MM'")
        return False

    return True


def add_task(title: str, due_date: str, description: str = None) -> None:
    if not validate_task(title, due_date):
        logging.error(f"Task '{title}' not added")
        return

    with sqlite3.connect(DB_FILE) as db:
        db.execute(
            "INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)",
            (title, description, due_date),
        )
        db.commit()
    logging.info(f"Task '{title}' added successfully")


def update_task_status(task_id: int, status: str) -> None:
    if status not in TASK_STATUSES:
        logging.error(f"Status must be one of the following: {TASK_STATUSES}")
        return

    with sqlite3.connect(DB_FILE) as db:
        cursor = db.cursor()
        cursor.execute("SELECT title, status FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()

        if not task:
            logging.error(f"Task ID {task_id} not found")
            return

        task_title = task[0]
        prev_status = task[1]

        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        db.commit()

    logging.info(f"Task '{task_title}' was updated from '{prev_status}' to '{status}'")


def delete_task(task_id: int) -> None:
    with sqlite3.connect(DB_FILE) as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT title FROM tasks WHERE id = ?",
            (task_id,),
        )
        task = cursor.fetchone()

        if not task:
            logging.error(f"Task ID {task_id} not found")
            return

        title = task[0]

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.commit()
    logging.info(f"Task '{title}' deleted successfully")


def list_tasks(status=None) -> None:
    with sqlite3.connect(DB_FILE) as db:
        cursor = db.cursor()
        query = "SELECT id, title, description, due_date, status FROM tasks"
        params = []

        if status:
            query += " WHERE status = ?"
            params.append(status)

        query += " ORDER BY due_date"
        cursor.execute(query, params)
        tasks = cursor.fetchall()

    for task in tasks:
        logging.info(
            f"ID: {task[0]}, Title: {task[1]}, Due: {task[3]}, Status: {task[4]}, Description: {task[2]}"
        )


if __name__ == "__main__":
    setup_db()
    # add_task(title="some", due_date="2024-12-14 12:00", description="wer")
    update_task_status(4, "completed")
    # delete_task(2)
    list_tasks('completed')
