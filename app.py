from flask import Flask, render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.sql import text

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
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
            flash("Virheelliset kirjautumistiedot", "error")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username  # Tallenna käyttäjänimi sessioon
                flash("Kirjautuminen onnistui", "success")
            else:
                flash("Virheelliset kirjautumistiedot", "error")

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
            flash("Käyttäjä luotu", "success")
        except:
            flash("Virhe: käyttäjänimi varattu", "error")
      
    return redirect("/signup")

@app.route("/add_project", methods=["POST"])
def add_project():
    if request.method == "POST":
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


        # Run SQL
        db.session.execute(text(sql), params)
        # Commit changes
        db.session.commit()
        flash("Projektin tiedot lisätty onnistuneesti.")

    return redirect("/projects")


@app.route("/logout")
def logout():
    session.pop("username", None)  # Log out user
    return redirect("/")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

if __name__ == "__main__":
    app.run(debug=True)
