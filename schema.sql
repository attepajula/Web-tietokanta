-- Drop old tables if they exist
DROP TABLE IF EXISTS permissions, users, project_inventory_usage, projects, inventories , materials, material_inventory, project_material_needs CASCADE;

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

CREATE TABLE IF NOT EXISTS materials (
    material_id SERIAL PRIMARY KEY,
    material_name VARCHAR(255) NOT NULL,
    description TEXT,
    unit VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS material_inventory (
    material_inventory_id SERIAL PRIMARY KEY,
    material_id INTEGER REFERENCES materials(material_id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS project_material_needs (
    project_material_needs_id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(project_id) ON DELETE CASCADE,
    stage_id INTEGER,
    material_id INTEGER REFERENCES materials(material_id) ON DELETE CASCADE,
    quantity_needed INTEGER NOT NULL
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
