# Login To-Do Application

A simple multi-user to-do web app built with **Flask** and **Microsoft SQL Server**. Users register and log in with a password-protected account, then manage their own private list of tasks.

## Features

- **User accounts**: register and log in with name, email and password
- **Secure passwords**: hashed with `bcrypt`, never stored in plain text
- **Session-based authentication**: protected pages redirect to the login page
- **Personal to-do list**: each user only sees and changes their own tasks
- **Full task management**: add, edit, mark as done/undone, and delete tasks
- **Form validation**: required fields, matching passwords, duplicate email detection, title length limit (200 characters)
- **Parameterized SQL queries** to protect against SQL injection

## Tech Stack

| Layer      | Technology                          |
| ---------- | ----------------------------------- |
| Backend    | Python, Flask                       |
| Database   | Microsoft SQL Server (via `pyodbc`) |
| Security   | `bcrypt`                            |
| Config     | `python-dotenv`                     |
| Frontend   | HTML templates (Jinja2), CSS        |

## Project Structure

```
Login-To-Do-Application/
├── app.py            # Flask app: routes for auth and to-dos
├── db.py             # SQL Server connection helper
├── test_db.py        # Quick script to check the database connection
├── database/         # SQL scripts for creating the database tables
├── templates/        # Jinja2 HTML pages (login, register, todos)
├── static/           # CSS and static assets
├── screenshots/      # App screenshots
├── .env.example      # Example environment configuration
└── README.md
```

## Database Schema

The app expects two tables in the SQL Server database (default name: `registration`):

- **users**: `user_id`, `email` (unique), `name`, `password_hash`
- **todos**: `todo_id`, `user_id` (belongs to a user), `title`, `is_done`, `created_at`

The SQL script to create them is in the `database/` folder.

## Getting Started

### Prerequisites

- Python 3.9+
- SQL Server (e.g. SQL Server Express)
- [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)

### 1. Clone the repository

```bash
git clone https://github.com/MaZeeN-77/Login-To-Do-Application.git
cd Login-To-Do-Application
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install flask bcrypt pyodbc python-dotenv
```

### 3. Set up the database

Create a database named `registration` (or any name you prefer) in SQL Server, then run the SQL script from the `database/` folder to create the `users` and `todos` tables.

### 4. Configure environment variables

Copy the example file and edit it:

```bash
# Windows
copy .env.example .env
# macOS / Linux
cp .env.example .env
```

| Variable      | Description                                                    | Example                         |
| ------------- | -------------------------------------------------------------- | ------------------------------- |
| `DB_SERVER`   | SQL Server instance                                            | `localhost\SQLEXPRESS`          |
| `DB_NAME`     | Database name                                                  | `registration`                  |
| `DB_DRIVER`   | ODBC driver name                                               | `ODBC Driver 18 for SQL Server` |
| `DB_TRUSTED`  | `yes` for Windows Authentication, `no` for SQL login           | `yes`                           |
| `DB_USER`     | SQL login username (only if `DB_TRUSTED=no`)                   |                                 |
| `DB_PASSWORD` | SQL login password (only if `DB_TRUSTED=no`)                   |                                 |
| `SECRET_KEY`  | Long random string used to sign Flask sessions                 | `change-me`                     |

Generate a strong secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```


