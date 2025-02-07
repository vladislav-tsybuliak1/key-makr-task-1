# Keymakr test tasks

## Task 1: Working with APIs and Multithreading

### Description

This is a script to fetch data from the JSONPlaceholder API, store it in an SQLite database, and export it to a CSV file.
It is written in asynchronous programming with efficient parallel requests using aiohttp, aiosqlite, and aiofiles.

### Usage

To run the script and fetch posts from the API:

`python scripts/fetch_posts.py`

#### Output

1) **Database (posts.db)**: Contains a posts table with columns id, user_id, title, and body.
2) **CSV (posts.csv)**: Stores the same data as the database.
3) **Log (requests.log)**: Logs all API requests and errors.
