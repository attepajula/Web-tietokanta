from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.sql import text
import logging

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
app.logger.setLevel(logging.INFO)
db = SQLAlchemy(app)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT user_id, password FROM users WHERE username=:username"
        result = db.session.execute(text(sql), {"username": username})
        user = result.fetchone()

        if not user:
            flash("Login failed", "error")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username
                flash("Login successful", "success")
            else:
                flash("Login failed", "error")

    return redirect("/")

@app.route("/add_new_user", methods=["POST"])
def add_new_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        try:
            db.session.execute(text(sql), {"username": username, "password": hash_value})
            db.session.commit()
            flash("User created", "success")
        except:
            flash("Username taken", "error")
      
    return redirect("/signup")

@app.route("/add_project", methods=["POST"])
def add_project():
    if request.method == "POST":
        print("mentii")
        project_name = request.form["project_name"]
        owner_name = request.form["owner_name"]
        notes = request.form["notes"]
        start_date = request.form["start_date"]
        start_stage = request.form["start_stage"]
        end_stage = request.form["end_stage"]

        # query
        sql = """
            INSERT INTO projects (project_name, owner_name, notes, start_date, start_stage, end_stage)
            VALUES (:project_name, :owner_name, :notes, :start_date, :start_stage, :end_stage)
        """
        params = {
            "project_name": project_name,
            "owner_name": owner_name,
            "notes": notes,
            "start_date": start_date,
            "start_stage": start_stage,
            "end_stage": end_stage
            }

        try:
            # Run SQL
            db.session.execute(text(sql), params)
            # Commit changes
            db.session.commit()
            flash("Project added")
        except Exception as e:
            app.logger.error(f"Error executing query: {str(e)}")
            flash("Something went wrong")
    return redirect("/projects")

@app.route("/logout")
def logout():
    session.pop("username", None)  # Log out user
    return redirect("/")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/show_project", methods=["GET", "POST"])
def show_project():
    if request.method == "POST":
        project = request.form["selected_project"]
        session["selected_project"] = project
    elif request.method == "GET":
        project = session.get("selected_project")
    else:
        app.logger.info("Request method is invalid")
    sql = "SELECT * FROM projects WHERE owner_name = :owner_name AND project_name = :project_name;"
    try:
        data = db.session.execute(text(sql), {"project_name": project, "owner_name": session.get("username")}).fetchone()
        session["selected_data"] = list(data)
        app.logger.info("Query executed successfully.")
        app.logger.info(f"Data: {data}")
    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")
    return projects(data=data)

@app.route("/projects", methods=["GET"])
def projects(data=None):
    username = session.get("username")
    sql = "SELECT project_name FROM projects WHERE owner_name = :username;"
    try:
        projects = db.session.execute(text(sql), {"username": username}).fetchall()
    except:
        projects = []
        flash("No projects yet", "error")
    return render_template("projects.html", projects=projects, data=data)

@app.route("/confirm")
def confirm():
    data = session.get("selected_data")
    sql = "UPDATE projects SET start_stage = :start_stage WHERE owner_name = :owner_name AND project_name = :project_name;"
    app.logger.info(f"try to confirm: {data}")
    try:
        db.session.execute(text(sql), {"start_stage": data[5]+1, "project_name":data[1], "owner_name":data[2]})
        db.session.commit()
        flash("Operation confirmed", "success")
    except:
        flash("Operation failed", "error")
    return redirect(url_for("show_project"))

@app.route("/resources")
def resources():
    return render_template("resources.html")

if __name__ == "__main__":
    app.run(debug=True)
