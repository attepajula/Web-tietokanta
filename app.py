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
        if len(username) < 3 or len(password) < 8:
            flash("Please choose a username and password that are each at least 3 and 8 characters long, respectively.", "error")
            return redirect("/signup")
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        try:
            db.session.execute(text(sql), {"username": username, "password": hash_value})
            db.session.commit()
            flash("User created", "success")
        except:
            flash("Username taken", "error")
      
    return redirect("/signup")

@app.route("/add_inventory", methods=["POST"])
def add_inventory():
    if request.method == "POST":
        inventory_name = request.form["inventory_name"]
        owner_name = request.form["owner_name"]
        notes = request.form["notes"]

        # query
        sql = "INSERT INTO inventories (owner_name, inventory_name, notes) VALUES (:owner_name, :inventory_name, :notes)"

        try:
            # Run SQL
            db.session.execute(text(sql), {"owner_name": owner_name, "inventory_name": inventory_name, "notes": notes})
            # Commit changes
            db.session.commit()
            flash("Inventory added")
        except Exception as e:
            app.logger.error(f"Error executing query: {str(e)}")
            flash("Something went wrong")
    return redirect("/projects")

@app.route("/add_project", methods=["POST"])
def add_project():
    if request.method == "POST":
        project_name = request.form["project_name"]
        owner_name = request.form["owner_name"]
        notes = request.form["notes"]
        start_date = request.form["start_date"]
        start_stage = request.form["start_stage"]
        end_stage = request.form["end_stage"]
        inventory_id = request.form["selected_inventory"]

        # query
        sql = """
            INSERT INTO projects (project_name, owner_name, notes, start_date, start_stage, end_stage, inventory_id)
            VALUES (:project_name, :owner_name, :notes, :start_date, :start_stage, :end_stage, :inventory_id)
        """
        params = {
            "project_name": project_name,
            "owner_name": owner_name,
            "notes": notes,
            "start_date": start_date,
            "start_stage": start_stage,
            "end_stage": end_stage,
            "inventory_id": inventory_id
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
    username = session.get("username")
    if request.method == "POST":
        project_id = request.form["selected_project"]
        session["selected_project"] = project_id
    elif request.method == "GET":
        project_id = session.get("selected_project")
    else:
        app.logger.info("Request method is invalid")
    if not user_has_permission_project(username, project_id):
        # Input is manipulated:
        app.logger.warning("Unauthorized access attempt.")
        flash("Unauthorized access attempt")
        return redirect("/projects")

    sql = "SELECT * FROM projects WHERE project_id = :project_id;"
    try:
        data = db.session.execute(text(sql), {"project_id": project_id[0]}).fetchone()
        session["selected_data"] = list(data)
        app.logger.info("Query executed successfully.")
        app.logger.info(f"Data: {data}")
    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")
    return projects(data=data)

@app.route("/projects", methods=["GET"])
def projects(data=None):
    username = session.get("username")
    sql = "SELECT project_name, project_id FROM projects WHERE owner_name = :username;"
    sql2 = "SELECT project_name, project_id FROM permissions WHERE username = :username;"
    try:
        projects = db.session.execute(text(sql), {"username": username}).fetchall()
        others_projects = db.session.execute(text(sql2), {"username": username}).fetchall()
        combined_projects = projects + others_projects
        app.logger.info(combined_projects)

    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")
        combined_projects = []
        flash("No projects yet", "error")

    sql2 = "SELECT inventory_name, inventory_id FROM inventories WHERE owner_name = :username;"
    try:
        inventories = db.session.execute(text(sql2), {"username": username}).fetchall()
        app.logger.info(inventories)

    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")
        inventories = []
        flash("No inventories yet", "error")

    return render_template("projects.html", inventories=inventories, projects=combined_projects, data=data)

@app.route("/confirm")
def confirm():
    data = session.get("selected_data")
    username = session.get("username")
    if data[5] < data[6]:
        if username == data[2]:
            sql = "UPDATE projects SET start_stage = :start_stage WHERE owner_name = :owner_name AND project_name = :project_name;"
            app.logger.info(f"try to confirm: {data}")
            try:
                db.session.execute(text(sql), {"start_stage": data[5]+1, "project_name":data[1], "owner_name":data[2]})
                db.session.commit()
                flash("Operation confirmed", "success")
            except:
                flash("Operation failed", "error")
            return redirect(url_for("show_project"))
        else:
            sql = "SELECT can_modify FROM permissions WHERE username = :username;"
            can_modify = db.session.execute(text(sql), {"username":username}).fetchone()
            app.logger.info(can_modify[0])
            if can_modify[0] == True:
                sql = "UPDATE projects SET start_stage = :start_stage WHERE owner_name = :owner_name AND project_name = :project_name;"
                app.logger.info(f"try to confirm someone else's: {data}")
                try:
                    db.session.execute(text(sql), {"start_stage": data[5]+1, "project_name":data[1], "owner_name":data[2]})
                    db.session.commit()
                    flash("Operation confirmed", "success")
                except:
                    flash("Operation failed", "error")
                return redirect(url_for("show_project"))
            else:
                flash("No permission", "error")
                return redirect(url_for("show_project"))
    else: 
        flash("Project completed", "error")
        return redirect(url_for("show_project"))

def user_has_permission_project(username, project_id):
    sql = "SELECT project_id FROM projects WHERE owner_name = :owner_name;"
    try:
        result = db.session.execute(text(sql), {"owner_name": username}).fetchall()
        allowed_projects = [int(row[0]) for row in result]
        app.logger.info("User checked successfully.")
    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")

    sql2 = "SELECT project_id FROM permissions WHERE username = :username;"
    try:
        result = db.session.execute(text(sql2), {"username": username}).fetchall()
        projects_permissons = [int(row[0]) for row in result]
        app.logger.info("User checked successfully.")
    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")

    allowed_projects += projects_permissons
    app.logger.info(project_id)
    app.logger.info(allowed_projects)
    return int(project_id) in allowed_projects

def user_has_permission_remove(username, permission_id):
    sql = "SELECT permission_id FROM permissions WHERE project_owner_name = :project_owner_name;"
    try:
        result = db.session.execute(text(sql), {"project_owner_name": username}).fetchall()
        allowed_permissons = [int(row[0]) for row in result]
        app.logger.info("User checked successfully.")
    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")

    app.logger.info(permission_id)
    app.logger.info(allowed_permissons)
    return int(permission_id) in allowed_permissons

@app.route("/resources")
def resources():
    return render_template("resources.html")

@app.route("/permission")
def permission():
    data = session.get("selected_data")
    project_owner_name = session.get("username")
    project_id = data[0]
    app.logger.info(f"Logged in as: {project_owner_name}")
    sql = "SELECT username, project_name, permission_id FROM permissions WHERE project_owner_name = :project_owner_name AND project_id = :project_id;"
    try:
        permissions = db.session.execute(text(sql), {"project_owner_name":  project_owner_name, "project_id":  project_id}).fetchall()
    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")
        permissions = []
        flash("No permissions yet", "error")

    return render_template("permission.html", data=data, permissions=permissions)

@app.route("/grant", methods=["POST"])
def grant():
    data = session.get("selected_data")
    app.logger.info(f"Data: {data}")
    if request.method == "POST":
        project_id = data[0]
        username = request.form["username"]
        project_name = data[1]
        project_owner_name = data[2]
        can_modify = request.form.get("canModify")

        app.logger.info(f"Can modify: {can_modify}")
        if can_modify == "true":
            can_modify = "true"
        else: 
            can_modify = "false"

        existing_permission = db.session.execute(text("SELECT permission_id FROM permissions WHERE project_id = :project_id AND username = :username"), {"project_id": project_id, "username": username}).fetchone()
        if existing_permission:
            flash("Permission already exists for this user and project")
            return redirect("/permission")
        
        # query
        sql = "INSERT INTO permissions (project_id, username, project_name, project_owner_name, can_modify) VALUES (:project_id, :username, :project_name, :project_owner_name, :can_modify)"

        try:
            # Run SQL
            db.session.execute(text(sql), {"project_id": project_id, "username": username, "project_owner_name": project_owner_name, "project_name": project_name, "can_modify": can_modify})
            # Commit changes
            db.session.commit()
            flash("Permission added")
        except Exception as e:
            app.logger.error(f"Error executing query: {str(e)}")
            flash("Something went wrong")

    return redirect("/permission")

@app.route("/remove_permission", methods=["POST"])
def remove_permission():
    username = session.get("username")
    
    if request.method == "POST":
        permission_id = request.form["selected_permission"]
        sql = "DELETE FROM permissions WHERE permission_id = :permission_id;"

    if not user_has_permission_remove(username, permission_id):
        # Input is manipulated:
        app.logger.warning("Unauthorized access attempt.")
        flash("Unauthorized access attempt")
        return redirect("/permission")
    
    try:
        db.session.execute(text(sql), {"permission_id": permission_id})
        # Commit changes
        db.session.commit()
        app.logger.info("Query executed successfully.")
        flash("Permission deleted")
    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")
        flash("Something went wrong while deleting permission")

    return redirect("/permission")
    
@app.route("/delete", methods=["POST"])
def delete():
    username = session.get("username")
    data = session.get("selected_data")
    project_id = data[0]
    if request.method == "POST":
        sql = "DELETE FROM projects WHERE project_id = :project_id;"

    if username != data[2]:
        # Input is infected:
        app.logger.warning("Infected access attempt.")
        flash("Unauthorized")
        return redirect("/projects")
    
    try:
        db.session.execute(text(sql), {"project_id": project_id})
        # Commit changes
        db.session.commit()
        app.logger.info("Query executed successfully.")
        flash("Project deleted")
    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")
        flash("Something went wrong while deleting project")

    return redirect("/projects")

if __name__ == "__main__":
    app.run(debug=True)
