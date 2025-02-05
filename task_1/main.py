import asyncio
import logging

import aiohttp
import aiosqlite


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="requests.log",
    filemode="a",
)


DB_FILE = "posts.db"
API_URL = "https://jsonplaceholder.typicode.com/posts"


async def setup_db() -> None:
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT,
                body TEXT
            )
            """
        )
        await db.commit()


async def fetch_post(
    session: aiohttp.ClientSession,
    post_id: int,
    queue: asyncio.Queue,
):
    try:
        async with session.get(f"{API_URL}/{post_id}/") as response:
            logging.info(f"Fetching post {post_id}: Status {response.status}")
            if response.status == 200:
                data = await response.json()
                post = (data["id"], data["userId"], data["title"], data["body"])
                await queue.put(post)
            else:
                logging.error(f"Error {response.status} fetching post {post_id}")
    except Exception as e:
        logging.error(f"Exception fetching post {post_id}: {e}")


async def fetch_all_posts() -> asyncio.Queue:
    queue = asyncio.Queue()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_post(session, i, queue) for i in range(1, 101)]
        await asyncio.gather(*tasks)
    return queue


async def save_to_db(queue: asyncio.Queue) -> None:
    async with aiosqlite.connect(DB_FILE) as db:
        while not queue.empty():
            post = await queue.get()
            await db.execute("INSERT INTO posts VALUES (?, ?, ?, ?)", post)
        await db.commit()
    logging.info("Saved posts to db")


async def main() -> None:
    await setup_db()


if __name__ == "__main__":
    asyncio.run(main())
