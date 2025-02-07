# Keymakr test tasks


## Task 1: Working with APIs and Multithreading

### Description

This is a script to fetch data from the JSONPlaceholder API, store it in an SQLite database, and export it to a CSV file.
It is written in asynchronous programming with efficient parallel requests using aiohttp, aiosqlite, and aiofiles.

### Usage

Run the script and fetch posts from the API:

`python scripts/fetch_posts.py`

#### Output

1) **Database (posts.db)**: Contains a posts table with columns id, user_id, title, and body.
2) **CSV (posts.csv)**: Stores the same data as the database.
3) **Log (requests.log)**: Logs all API requests and errors.


## Task 2: XML to JSON Conversion

### Description

This is a script to parse product data from XML files, convert them to JSON, and save the results in a specified directory.
The script validates the data and logs important events, warnings, and errors during processing.

### Usage

Run the script and convert .xml files to .json:

`python scripts/convert_xml_to_json.py --input-dir path_to_xml_files_dir --output-dir json_dir`

#### Output

1) **Converted JSON Files**: Stored in the specified output directory
2) **Log (converting_xml_to_json.log)**: Logs information about the conversion process, validation errors, and file operations.
