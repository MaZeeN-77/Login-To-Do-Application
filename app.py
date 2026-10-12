import os
import bcrypt
import pyodbc
from flask import Flask, render_template, request, redirect, session, url_for
from dotenv import load_dotenv

from db import get_connection

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("todos"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", form={}, errors={})

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    errors = {}
    if not name:
        errors["name"] = "Name is required"
    if not email:
        errors["email"] = "Email is required"
    if not password:
        errors["password"] = "Password is required"
    if not confirm:
        errors["confirm"] = "Confirm password is required"
    elif password and password != confirm:
        errors["confirm"] = "Passwords do not match"

    form = {"name": name, "email": email}

    if errors:
        return render_template("register.html", form=form, errors=errors)

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
            (email, name, password_hash),
        )
        conn.commit()

        cursor.execute("SELECT user_id, name FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
    except pyodbc.IntegrityError:
        conn.rollback()
        errors["email"] = "Email Already Exists"
        return render_template("register.html", form=form, errors=errors)
    finally:
        conn.close()

    session["user_id"] = row.user_id
    session["name"] = row.name
    return redirect(url_for("todos"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", form={}, errors={})

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    errors = {}
    if not email:
        errors["email"] = "Email is required"
    if not password:
        errors["password"] = "Password is required"

    form = {"email": email}

    if errors:
        return render_template("login.html", form=form, errors=errors)

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, name, password_hash FROM users WHERE email = ?",
            (email,),
        )
        row = cursor.fetchone()
    finally:
        conn.close()

    valid = row is not None and bcrypt.checkpw(
        password.encode("utf-8"), row.password_hash.encode("utf-8")
    )

    if not valid:
        errors["general"] = "Invalid email or password"
        return render_template("login.html", form=form, errors=errors)

    session["user_id"] = row.user_id
    session["name"] = row.name
    return redirect(url_for("todos"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def render_todos(form=None, errors=None, edit_error=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT todo_id, title, is_done, created_at FROM todos "
            "WHERE user_id = ? ORDER BY todo_id DESC",
            (session["user_id"],),
        )
        rows = cursor.fetchall()
    finally:
        conn.close()

    return render_template(
        "todos.html",
        name=session["name"],
        todos=rows,
        form=form or {},
        errors=errors or {},
        edit_error=edit_error,
    )


@app.route("/todos")
def todos():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_todos()


@app.route("/todos/add", methods=["POST"])
def add_todo():
    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title", "").strip()

    if not title:
        return render_todos({"title": title}, {"title": "Title is required"})
    if len(title) > 200:
        return render_todos({"title": title}, {"title": "Title is too long (200 characters at most)"})

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (user_id, title) VALUES (?, ?)",
            (session["user_id"], title),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("todos"))

@app.route("/todos/<int:todo_id>/edit", methods=["POST"])
def edit_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title", "").strip()

    if not title:
        return render_todos(edit_error="Title is required")
    if len(title) > 200:
        return render_todos(edit_error="Title is too long (200 characters at most)")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE todos SET title = ? WHERE todo_id = ? AND user_id = ?",
            (title, todo_id, session["user_id"]),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
def toggle_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    is_done = 1 if request.form.get("is_done") == "1" else 0

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE todos SET is_done = ? WHERE todo_id = ? AND user_id = ?",
            (is_done, todo_id, session["user_id"]),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM todos WHERE todo_id = ? AND user_id = ?",
            (todo_id, session["user_id"]),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("todos"))


if __name__ == "__main__":
    app.run(debug=True)