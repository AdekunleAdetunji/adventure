-- Delete dabase if it exists
DROP DATABASE IF EXISTS adventure;

-- Delete role/user if it exists
DROP ROLE IF EXISTS adventure;

-- Create role/user
CREATE USER adventure WITH PASSWORD 'adventure';

-- Create database
CREATE DATABASE adventure;

-- Grant all permissions on database adventure to user
GRANT ALL PRIVILEGES ON DATABASE adventure to adventure;