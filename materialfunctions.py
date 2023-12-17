from flask import render_template, redirect, request, session, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
from sqlalchemy.sql import text
from utilities import user_has_permission_project, user_has_permission_remove, permission_to_use_inv, material_exists, validate_stage, can_modify_helper
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

        if not can_modify_helper(username, int(project_id)):
            flash("No permission")
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

def remove_material_need(username):
    if request.method == "POST":
        project_material_needs_id = request.form["material_need_id"]
        try:
            check_sql = """SELECT project_id FROM project_material_needs
            WHERE project_material_needs_id = :project_material_needs_id;"""
            result = db.session.execute(text(check_sql), 
                                        {"project_material_needs_id": project_material_needs_id}).fetchone()

            if not result:
                flash("Material need not found.", "error")
                return redirect("/resources_route")
            
            if not user_has_permission_project(username, session["selected_project"]):
                # Input is manipulated:
                app.logger.warning("Unauthorized access attempt.")
                flash("Unauthorized access attempt")
                return redirect("/resources_route")
            
            sql2 = """SELECT project_id FROM project_material_needs 
            WHERE project_material_needs_id = :project_material_needs_id;"""
            project_id = db.session.execute(text(sql2), 
                                            {"project_material_needs_id": project_material_needs_id}).fetchall()
            app.logger.info(f"PROJECT ID: {project_id[0][0]}")

            if not can_modify_helper(username, project_id[0][0]):
                flash("No permission")
                return show_project_material_needs(username)
            

            delete_sql = """DELETE FROM project_material_needs 
            WHERE project_material_needs_id = :project_material_needs_id;"""
            db.session.execute(text(delete_sql), 
                               {"project_material_needs_id": project_material_needs_id})
            db.session.commit()

            flash("Material need removed successfully.")
            app.logger.info("Material need removed successfully.")
        except Exception as e:
            app.logger.info(f"Error removing material need: {str(e)}", "error")

        return resources(username0=username)

def add_material_view():
    if request.method == "POST":
        material_name = request.form["material_name"]
        description = request.form["desc"]
        unit = request.form["unit"]

        sql = """INSERT INTO materials (material_name, description, unit) 
        VALUES (:material_name, :description, :unit);"""
        try:
            db.session.execute(text(sql), {"material_name": material_name, "description": description, "unit": unit})
            db.session.commit()
            flash("Material added successfully.")
        except Exception as e:
            app.logger.error(f"Error adding material: {str(e)}")
            flash("Error adding material", "error")

    return render_template("materials.html")

def material_exists(material_id):
    sql = "SELECT material_id FROM materials WHERE material_id = :material_id;"
    result = db.session.execute(text(sql), {"material_id": material_id}).fetchone()
    return result is not None

def add_material_to_inventory(username):
    if request.method == 'POST':
        material_id = request.form['material_id']
        quantity = request.form['quantity']
        inventory_id = request.form['inventory_id']

        if not permission_to_use_inv(username, inventory_id):
            flash("No permission")
            return add_material_view()
        
        try:
            material_check_sql = "SELECT material_id FROM materials WHERE material_id = :material_id;"
            material_exists = db.session.execute(text(material_check_sql), {"material_id": material_id}).fetchone()

            if not material_exists:
                flash("Material does not exist", "error")
                return redirect("/add_material_to_inventory_route")

            inventory_check_sql = "SELECT inventory_id FROM inventories WHERE inventory_id = :inventory_id;"
            inventory_exists = db.session.execute(text(inventory_check_sql), {"inventory_id": inventory_id}).fetchone()

            if not inventory_exists:
                flash("Inventory does not exist", "error")
                return redirect("/add_material_to_inventory_route")

            add_material_sql = """
                INSERT INTO material_inventory (material_id, quantity, inventory_id)
                VALUES (:material_id, :quantity, :inventory_id);
            """
            db.session.execute(text(add_material_sql), {"material_id": material_id,
                                                         "quantity": quantity, "inventory_id": inventory_id})
            db.session.commit()

            flash("Material added to inventory successfully.")
        except Exception as e:
            app.logger.error(f"Error adding material to inventory: {str(e)}")
            flash("Error adding material to inventory", "error")

    return redirect("/inventories")

def get_materials_by_inventory(username):
    if request.method == 'POST':
        inventory_id = request.form['inventory_id']
    if not permission_to_use_inv(username, inventory_id):
        flash("No permission")
        return add_material_view()
    try:
        sql = """
            SELECT * FROM material_inventory
            WHERE inventory_id = :inventory_id;
        """
        materials = db.session.execute(text(sql), {"inventory_id": inventory_id}).fetchall()
        return materials
    except Exception as e:
        app.logger.error(f"Error retrieving materials by inventory: {str(e)}")
        return []