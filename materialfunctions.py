from flask import render_template, redirect, request, session, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
from sqlalchemy.sql import text
from utilities import user_has_permission_project, user_has_permission_remove, permission_to_use_inv, material_exists, validate_stage
from app import app, db

def resources(username0, needs=None):
    app.logger.info(f"Data: {needs}")
    sql = "SELECT project_name, project_id FROM projects WHERE owner_name = :username;"
    sql2 = "SELECT project_name, project_id FROM permissions WHERE username = :username;"
    try:
        projects = db.session.execute(text(sql), {"username": username0}).fetchall()
        others_projects = db.session.execute(text(sql2), {"username": username0}).fetchall()
        combined_projects = projects + others_projects
        app.logger.info(combined_projects)

    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")
        combined_projects = []

    if len(combined_projects) == 0:
        flash("No projects yet", "error")

    return render_template("resources.html",
                           projects=combined_projects, needs=needs)

def show_project_material_needs(username):
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
        return redirect("/resources_route")
    sql = """
        SELECT pmn.*, m.material_name, pmn.stage_id, p.project_name, p.start_stage
        FROM project_material_needs pmn
        JOIN materials m ON pmn.material_id = m.material_id
        JOIN projects p ON pmn.project_id = p.project_id
        WHERE pmn.project_id = :project_id
        ORDER BY pmn.stage_id;
    """
    try:
        project_needs = db.session.execute(text(sql), {"project_id": project_id}).fetchall()
        app.logger.info(f"Needs: {project_needs}")

    except Exception as e:
        app.logger.error(f"Error retrieving project needs: {str(e)}")
        project_needs = []
    
    if len(project_needs) == 0:
        flash("No project material needs yet", "error")
    return resources(username0=username, needs=project_needs)

def insert_material_need_view(username):
    if request.method == "POST":
        project_id = request.form["selected_project"]
        stage_id = request.form["stage_needed"]
        material_id = request.form["material_id"]
        quantity_needed = request.form["quantity_needed"]
    
    if not material_exists(material_id):
        flash("No such material")
        return show_project_material_needs(username)

    
    if not user_has_permission_project(username, project_id):
        # Input is manipulated:
        app.logger.warning("Unauthorized access attempt.")
        flash("Unauthorized access attempt")
        return redirect("/resources_route")
    
    stage_id = validate_stage(project_id, stage_id)
        
    sql = """INSERT INTO project_material_needs (project_id, stage_id, material_id, quantity_needed)
    VALUES (:project_id, :stage_id, :material_id, :quantity_needed);"""

    try:
        db.session.execute(text(sql), {"project_id": project_id, "stage_id": stage_id,
                                        "material_id": material_id,
                                        "quantity_needed": quantity_needed})
        db.session.commit()
        app.logger.info("Material need inserted successfully.")
        flash("Material need inserted successfully.")
    except Exception as e:
        app.logger.error(f"Error inserting material need: {str(e)}")


    return show_project_material_needs(username)
