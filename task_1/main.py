import asyncio

import aiosqlite


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="requests.log",
    filemode="a",
)


DB_FILE = "posts.db"


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


async def main() -> None:
    await setup_db()


if __name__ == "__main__":
    asyncio.run(main())
