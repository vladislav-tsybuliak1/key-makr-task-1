import asyncio
import csv
import logging
import os
import sys

import aiofiles
import aiohttp
import aiosqlite


FILES_DIR = "scripts/fetch_posts_files"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename=f"{FILES_DIR}/requests.log", mode="a"),
        logging.StreamHandler(stream=sys.stdout),
    ],
)


DB_FILE = f"{FILES_DIR}/posts.db"
CSV_FILE = f"{FILES_DIR}/posts.csv"
API_URL = "https://jsonplaceholder.typicode.com/posts"


async def setup_db() -> None:
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL
            )
            """
        )
        await db.commit()


async def fetch_post(
    session: aiohttp.ClientSession,
    post_id: int,
    db_queue: asyncio.Queue,
    csv_queue: asyncio.Queue,
):
    try:
        async with session.get(f"{API_URL}/{post_id}/") as response:
            logging.info(f"Fetching post {post_id}: Status {response.status}")
            if response.status == 200:
                data = await response.json()
                post = (
                    data["id"],
                    data["userId"],
                    data["title"],
                    data["body"],
                )
                await db_queue.put(post)
                await csv_queue.put(post)
            else:
                logging.error(
                    f"Error {response.status} fetching post {post_id}"
                )
    except Exception as e:
        logging.error(f"Exception fetching post {post_id}: {e}")


async def fetch_all_posts() -> tuple[asyncio.Queue, asyncio.Queue]:
    db_queue = asyncio.Queue()
    csv_queue = asyncio.Queue()
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_post(
                session=session,
                post_id=i,
                db_queue=db_queue,
                csv_queue=csv_queue,
            )
            for i in range(1, 101)
        ]
        await asyncio.gather(*tasks)
    return db_queue, csv_queue


async def save_to_db(queue: asyncio.Queue) -> None:
    async with aiosqlite.connect(DB_FILE) as db:
        while not queue.empty():
            post = await queue.get()
            await db.execute("INSERT INTO posts VALUES (?, ?, ?, ?)", post)
            await db.commit()
    logging.info(f"Saved posts to {DB_FILE}")


async def save_to_csv(queue: asyncio.Queue) -> None:
    file_exists = os.path.exists(CSV_FILE)
    async with aiofiles.open(
        CSV_FILE, "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        if not file_exists:
            await writer.writerow(["id", "user_id", "title", "body"])
        while not queue.empty():
            post = await queue.get()
            await writer.writerow(post)
    logging.info(f"Exported data to {CSV_FILE}")


async def main() -> None:
    await setup_db()
    db_queue, csv_queue = await fetch_all_posts()
    await asyncio.gather(save_to_db(db_queue), save_to_csv(csv_queue))


if __name__ == "__main__":
    asyncio.run(main())
