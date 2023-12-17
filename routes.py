from flask import render_template, redirect, request, session
from dotenv import load_dotenv

from app import app
from appfunctions import login, add_new_user, add_inventory, add_project, show_project, projects, confirm_operation, permissions, grant, remove_permission, delete_project
from materialfunctions import resources, show_project_material_needs, insert_material_need_view

load_dotenv()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login_route", methods=["POST"])
def login_route():
    return login()

@app.route("/add_new_user_route", methods=["POST"])
def add_new_user_route():
    return add_new_user()

@app.route("/add_inventory_route", methods=["POST"])
def add_inventory_route():
    username = session.get("username")
    return add_inventory(username)

@app.route("/add_project_route", methods=["POST"])
def add_project_route():
    username = session.get("username")
    return add_project(username)

@app.route("/logout")
def logout():
    session.pop("username", None)  # Log out user
    return redirect("/")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/show_project_route", methods=["GET", "POST"])
def show_project_route():
    username = session.get("username")
    return show_project(username)

@app.route("/show_project_material_needs_route", methods=["GET", "POST"])
def show_project_material_needs_route():
    username = session.get("username")
    return show_project_material_needs(username)

@app.route("/projects_route", methods=["GET"])
def projects_route(data=None):
    username = session.get("username")
    return projects(username0=username, data=data)

@app.route("/confirm")
def confirm():
    data = session.get("selected_data")
    username = session.get("username")
    return confirm_operation(data, username)

@app.route("/resources_route", methods=["GET"])
def resources_route():
    data = session.get("selected_data")
    username = session.get("username")
    return resources(username0=username, data=data)

@app.route("/inventories")
def inventories():
    return render_template("inventories.html")

@app.route("/permissions_route")
def permissions_route():
    data = session.get("selected_data")
    project_owner_name = session.get("username")
    return permissions(data, project_owner_name)

@app.route("/grant_route", methods=["POST"])
def grant_route():
    data = session.get("selected_data")
    return grant(data)

@app.route("/remove_permission_route", methods=["POST"])
def remove_permission_route():
    username = session.get("username")
    permission_id = request.form["selected_permission"]
    return remove_permission(username, permission_id)

@app.route("/delete_route", methods=["POST"])
def delete_route():
    username = session.get("username")
    data = session.get("selected_data")
    return delete_project(username, data)

if __name__ == "__main__":
    app.run(debug=True)
