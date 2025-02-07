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


## Task 3: Nginx log analyzer

### Description
It is a script for analyzing web server logs in Nginx format.
The scripy identifies key metrics such as top IPs by request count, most frequent errors, and average response sizes.

### Usage
Run the script and analyze log file:

`python scripts/log_analyzer.py path/to/access.log`

#### Output
1) **Analysis Results**: Displayed in the console.
2) **Log (log_analyzer.log)**: Records information about the analysis process.

#### Key Metrics Extracted
1) Top 5 IP Addresses: Ranked by the number of requests.
2) Most Frequent Errors: 4xx and 5xx status codes.
3) Average Response Size: Calculated across all requests.


## Task 4: Task Manager with Lite DB

### Description
It is a Python-based CLI task management system backed by SQLite.
It allows users to add, update, delete, and list tasks with logging for all operations.

### Usage
To interact with the task manager, use one of the following commands:

 - **Add a Task**:

`python scripts/task_manager.py --add "Title" "Description" "2025-12-30 12:00`

Adds a new task with the specified title, description, and due date.

 - **Update a Task's Status**:

`python scripts/task_manager.py --update TaskID Status`

Updates the status of the task to pending, in_progress, or completed

 - **Delete a Task**:

`python scripts/task_manager.py --delete TaskID`

Deletes the task with the specified TaskID.

 - **List Tasks**:

`python scripts/task_manager.py --list`

Lists all tasks sorted by due date.

 - **Filter List Tasks by Status**:

`python scripts/task_manager.py --list --filter-status Status`

Displays tasks filtered by status.

#### Examples
**Add a Task**:

`python scripts/task_manager.py --add "Finish Report" "Complete quarterly report" "2025-02-10 15:00"`

**Update a Task**:

`python scripts/task_manager.py --update 1 completed`

**Delete a Task**:

`python scripts/task_manager.py --delete 2`

**List Tasks**:

`python scripts/task_manager.py --list`

**List Tasks with filter**:

`python scripts/task_manager.py --list --filter-status completed`


#### Output
1) **Database (tasks.db)**: Contains a task table with columns id, title, title, description, due_date, and status.
2) **Log (task_manager.log)**: Records information about the operations.


## Contact

For any inquiries, please contact [vladislav.tsybuliak@gmail.com](mailto:vladislav.tsybuliak@gmail.com).
