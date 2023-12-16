from sqlalchemy.sql import text
from app import app, db

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

def permission_to_use_inv(username, inventory_id):
    sql = "SELECT inventory_id FROM inventories WHERE owner_name = :owner_name;"
    try:
        result = db.session.execute(text(sql), {"owner_name": username}).fetchall()
        allowed_inventories = [int(row[0]) for row in result]
        app.logger.info("User checked successfully.")
    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")

    app.logger.info(inventory_id)
    app.logger.info(allowed_inventories)
    return int(inventory_id) in allowed_inventories