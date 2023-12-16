-- Drop old tables if they exist
DROP TABLE IF EXISTS permissions, users, project_inventory_usage, projects, inventories CASCADE;

-- Define new tables
CREATE TABLE IF NOT EXISTS inventories (
    owner_name VARCHAR(50) NOT NULL,
    inventory_id SERIAL PRIMARY KEY,
    inventory_name VARCHAR(255) NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    owner_name VARCHAR(50) NOT NULL,
    notes TEXT,
    start_date DATE,
    start_stage INTEGER,
    end_stage INTEGER,
    inventory_id INTEGER REFERENCES inventories(inventory_id)
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS permissions (
    permission_id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(project_id) ON DELETE CASCADE,
    username VARCHAR(50) NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    project_owner_name VARCHAR(50) NOT NULL,
    can_modify BOOLEAN
);

-- Define a new view
CREATE OR REPLACE VIEW project_inventory_usage_view AS
SELECT
    p.project_id,
    p.project_name,
    p.inventory_id,
    i.inventory_name
FROM
    projects p
LEFT JOIN
    inventories i ON p.inventory_id = i.inventory_id;
