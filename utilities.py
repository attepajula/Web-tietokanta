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
    try:
        query = "SELECT COUNT(*) FROM inventories WHERE owner_name = :owner_name AND inventory_id = :inventory_id"
        result = db.session.execute(text(query), {"owner_name": username, "inventory_id": inventory_id}).scalar()
        app.logger.info("User checked successfully.")
    except Exception as e:
        app.logger.error(f"Error executing query: {str(e)}")
    return result > 0

def material_exists(material_id):
    """
    Check if the material exists in the database.

    Args:
    - material_id: Identifier of the material.

    Returns:
    - True if the material exists; otherwise, False.
    """
    sql = "SELECT COUNT(*) FROM materials WHERE material_id = :material_id;"
    try:
        result = db.session.execute(text(sql), {"material_id": material_id}).scalar()
        return result > 0
    except Exception as e:
        app.logger.error(f"Error checking material existence: {str(e)}")
        return False

def validate_stage(project_id, stage_id):
    """
    Check if the provided stage_id is within the valid range for the given project.

    Args:
    - project_id: Identifier of the project.
    - stage_id: Stage identifier to validate.

    Returns:
    - True if the stage_id is within the valid range; otherwise, False.
    """
    try:
        sql = "SELECT end_stage FROM projects WHERE project_id = :project_id;"
        result = db.session.execute(text(sql), {"project_id": project_id}).fetchone()
        
        # Tarkista, onko stage_id suurempi kuin end_stage
        if result and result[0] and int(stage_id) > result[0]:
            return result[0]  # Jos stage_id on suurempi, palauta end_stage
        else:
            return int(stage_id)  # Muuten palauta alkuperäinen stage_id
    except Exception as e:
        # Käsittele poikkeukset tarvittaessa
        print(f"Error getting end stage: {e}")
        return stage_id
    
def can_modify_helper(username, project_id):
    allowed_projects = []

    # Projects owned by the user
    sql_owned = "SELECT project_id FROM projects WHERE owner_name = :owner_name;"
    try:
        result_owned = db.session.execute(text(sql_owned), {"owner_name": username}).fetchall()
        allowed_projects.extend([int(row[0]) for row in result_owned])
        app.logger.info("User checked successfully for owned projects.")
    except Exception as e:
        app.logger.error(f"Error executing query for owned projects: {str(e)}")

    # Projects where the user has modify permission
    sql_permissions = "SELECT project_id FROM permissions WHERE username = :username AND can_modify = true;"
    try:
        result_permissions = db.session.execute(text(sql_permissions), {"username": username}).fetchall()
        allowed_projects.extend([int(row[0]) for row in result_permissions])
        app.logger.info("User checked successfully for projects with modify permissions.")
    except Exception as e:
        app.logger.error(f"Error executing query for projects with modify permissions: {str(e)}")

    app.logger.info(f"User: {username}, Project ID: {project_id}, Allowed Projects: {allowed_projects}")
    
    return int(project_id) in allowed_projects