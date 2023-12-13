-- Define the projects table
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

-- Define the users table
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Define the permissions table
CREATE TABLE IF NOT EXISTS permissions (
    permission_id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(project_id) ON DELETE CASCADE,
    username VARCHAR(50) NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    project_owner_name VARCHAR(50) NOT NULL,
    can_modify BOOLEAN
);

-- Define the inventories table
CREATE TABLE IF NOT EXISTS inventories (
    owner_name VARCHAR(50) NOT NULL UNIQUE,
    inventory_id SERIAL PRIMARY KEY,
    inventory_name VARCHAR(255) NOT NULL,
    notes TEXT
);

-- Define the inventory_usage table
CREATE TABLE IF NOT EXISTS inventory_usage (
    inventory_usage_id SERIAL PRIMARY KEY,
    inventory_id INTEGER REFERENCES inventories(inventory_id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(project_id) ON DELETE CASCADE
);
