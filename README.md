# Server-DB FastAPI Student Records

This repository provides two FastAPI applications for managing student records:

1. **SQLite version** (`fastapi_sqlite.py`) – stores data in a local SQLite database.
2. **Supabase/PostgreSQL version** (`fastapi_supabase.py`) – connects to a hosted Supabase PostgreSQL instance via a full connection URL.

---

## Prerequisites

* **Python 3.12**

  * **Windows**: Install from the [official Python website](https://www.python.org/downloads/windows/) or via the Microsoft Store (search for **Python 3.12**).
  * **macOS**: Download from the [official Python website](https://www.python.org/downloads/macos/) or via the App Store (search **Python 3.12**).
  * **Linux**: Use your distro’s package manager, e.g.:

    ```bash
    sudo apt update && sudo apt install python3.12
    ```

* **Git**
  * **Windows**: Install from [https://git-scm.com/download/win](https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/Git-2.49.0-64-bit.exe)
  * **macOS**:
  ```bash
      brew install git
  ```  
  * **Linux**: Use your distro’s package manager, e.g.:
  ```bash
  sudo apt update && sudo apt install git
  ```

---

## Video Reference
1. **Windows** -- https://drive.google.com/file/d/1rJGdjBTe1bqk5Xe-nNz_s3t7rpc2F0vK/view?usp=sharing
2. **Mac** -- https://drive.google.com/file/d/1liPUaegh7R207ARe6HhpNII34j-eroBK/view?usp=sharing

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/hari-shreehari/server-db
   cd server-db
   ```

2. **Install dependencies**

   ```bash
   pip install fastapi uvicorn python-dotenv aiosqlite asyncpg
   ```

3. **Add your `.env` file**

   In the project root, create a file named `.env` with the following content:

   ```dotenv
   # SQLite (optional override)
   SQLITE_DB_PATH=students.db

   # Postgres URL for Supabase project
   # Uncomment the DATABASE_URL line you need
   # DATABASE_URL=postgresql://postgres:I_die_at_CIT@db.hwapncrvlvmlsjtghjpt.supabase.co:5432/postgres
   DATABASE_URL=postgresql://postgres.egezsyopwnypvvuybbnd:Student123_cit@aws-0-ap-south-1.pooler.supabase.com:5432/postgres
   ```

---

## Running the Applications

Each script includes a built-in Uvicorn startup block. To run:

* **SQLite version**:

  ```bash
  python fastapi_sqlite.py
  ```

* **Supabase/PostgreSQL version**:

  ```bash
  python fastapi_supabase.py
  ```

By default, both listen on `http://0.0.0.0:8000` with hot-reload enabled.

---

## Testing with cURL

### Linux/macOS

* **SQLite app**

  ```bash
  curl -X POST http://localhost:8000/add_record \
       -H "Content-Type: application/json" \
       -d '{"roll_number":1,"name":"Alice"}'
  ```

* **Supabase app**

  ```bash
  curl -X POST http://localhost:8000/add_record \
       -H "Content-Type: application/json" \
       -d '{"roll_number":2,"name":"Bob"}'
  ```

### Windows PowerShell

* **SQLite app**

  ```powershell
  curl -Method POST -Uri http://localhost:8000/add_record `
       -Headers @{"Content-Type"="application/json"} `
       -Body '{"roll_number":1,"name":"Alice"}'
  ```

* **Supabase app**

  ```powershell
  curl -Method POST -Uri http://localhost:8000/add_record `
       -Headers @{"Content-Type"="application/json"} `
       -Body '{"roll_number":2,"name":"Bob"}'
  ```

---

## Enter your name and a random number when you hit the curl... not Bob or Alice 
