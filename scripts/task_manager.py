import argparse
import logging
import sqlite3
import sys
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename="task_4/task_manager.log", mode="a"),
        logging.StreamHandler(stream=sys.stdout),
    ],
)


DB_FILE = "task_4/tasks.db"

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
                description TEXT NOT NULL,
                due_date DATETIME NOT NULL,
                status TEXT CHECK(status IN {TASK_STATUSES}) NOT NULL DEFAULT 'pending'
            )
            """
        )
        db.commit()


def validate_task(title: str, description: str, due_date: str) -> bool:
    if not title.strip():
        logging.error("Title cannot be empty")
        return False

    if len(title.strip()) > 255:
        logging.error("Title should contain maximum 255 symbols")
        return False

    if not description.strip():
        logging.error("Description cannot be empty")
        return False

    try:
        datetime.strptime(due_date, "%Y-%m-%d %H:%M")
    except ValueError:
        logging.error("Invalid due date format. Use 'YYYY-MM-DD HH:MM'")
        return False

    return True


def add_task(title: str, description: str, due_date: str) -> None:
    if not validate_task(title, description, due_date):
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    parser.add_argument(
        "--add",
        nargs=3,
        metavar=("TITLE", "DESCRIPTION", "DUE_DATE"),
        help="Add a new task",
    )
    parser.add_argument(
        "--update",
        nargs=2,
        metavar=("ID", "STATUS"),
        help="Update task status",
    )
    parser.add_argument("--delete", metavar="ID", help="Delete a task")
    parser.add_argument("--list", action="store_true", help="List all tasks")
    parser.add_argument(
        "--filter-status",
        metavar="STATUS",
        help="Filter tasks by status",
    )

    args = parser.parse_args()
    setup_db()

    if args.add:
        add_task(*args.add)
    elif args.update:
        update_task_status(args.update[0], args.update[1])
    elif args.delete:
        delete_task(args.delete)
    elif args.list:
        list_tasks(args.filter_status)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
