# Login To-Do Application

A web application that lets users create an account, log in, and keep their own to-do list. Each user has a private list, so nobody can see or change another person's tasks.

The project is built with Flask (Python) on the backend and SQL Server as the database.

## Features

- Register a new account with name, email and password
- Log in and log out
- Add new tasks
- Edit a task
- Mark a task as done or not done
- Delete a task
- Each user only sees their own tasks
- Passwords are hashed, not stored as plain text
- Form validation with error messages (empty fields, passwords not matching, email already used)

## Technologies

- Python and Flask for the server
- SQL Server for storing users and tasks
- pyodbc to connect Python to SQL Server
- bcrypt for password hashing
- python-dotenv to load settings from a `.env` file
- HTML templates and CSS for the pages

## How It Works

A new user registers and the password is hashed before it is saved in the database. After logging in, the user is redirected to their to-do page, where they can add, edit, complete and delete tasks. If someone tries to open the to-do page without logging in, they are sent back to the login page.

The database has two tables: `users` (name, email, hashed password) and `todos` (title, done status, creation date, and the user who owns it).

## Project Structure

- `app.py` - the main Flask app with all the routes
- `db.py` - connects to the SQL Server database
- `test_db.py` - a small script to test the database connection
- `database/` - the SQL script that creates the tables
- `templates/` - the HTML pages
- `static/` - CSS and static files
- `screenshots/` - screenshots of the app
- `.env.example` - example of the settings the app needs

## Getting Started
Run the app:

```bash
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Usage

Open the app, register a new account, and log in. From the to-do page you can add tasks, tick them when they are done, edit their titles, or delete them. Use the logout link when you are finished.

## Author

MaZeeN-77
