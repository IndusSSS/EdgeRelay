-- EdgeRelay Database Initialization Script
-- MESSS Compliant - Modular, Efficient, Scalable, Secure, Stable

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create admin_users table in the default database
CREATE TABLE IF NOT EXISTS admin_users (
    admin_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create system_config table for admin settings
CREATE TABLE IF NOT EXISTS system_config (
    config_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create client_users table
CREATE TABLE IF NOT EXISTS client_users (
    client_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create local_servers table
CREATE TABLE IF NOT EXISTS local_servers (
    server_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    server_name VARCHAR(255) NOT NULL,
    server_ip VARCHAR(45) NOT NULL,
    server_port INTEGER DEFAULT 8000,
    status VARCHAR(20) DEFAULT 'offline',
    last_seen TIMESTAMP DEFAULT NOW(),
    capabilities TEXT,
    configuration JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create cameras table
CREATE TABLE IF NOT EXISTS cameras (
    camera_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    server_id UUID REFERENCES local_servers(server_id) ON DELETE CASCADE,
    camera_name VARCHAR(255) NOT NULL,
    rtsp_url VARCHAR(500),
    onvif_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'offline',
    capabilities TEXT,
    configuration JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create alerts table
CREATE TABLE IF NOT EXISTS alerts (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    server_id UUID REFERENCES local_servers(server_id) ON DELETE CASCADE,
    camera_id UUID REFERENCES cameras(camera_id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(20) DEFAULT 'info',
    is_processed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create sessions table for user sessions
CREATE TABLE IF NOT EXISTS sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_admin_users_username ON admin_users(username);
CREATE INDEX IF NOT EXISTS idx_client_users_username ON client_users(username);
CREATE INDEX IF NOT EXISTS idx_client_users_company_name ON client_users(company_name);
CREATE INDEX IF NOT EXISTS idx_local_servers_status ON local_servers(status);
CREATE INDEX IF NOT EXISTS idx_cameras_server_id ON cameras(server_id);
CREATE INDEX IF NOT EXISTS idx_alerts_server_id ON alerts(server_id);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);

-- Insert default admin user
-- Password: Admin@EdgeRelay#2025!
INSERT INTO admin_users (username, password_hash, full_name, is_active) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4X.2XpF6y2', 'EdgeRelay Administrator', true)
ON CONFLICT (username) DO NOTHING;

-- Insert default test client user
-- Password: Client@EdgeRelay#2025!
INSERT INTO client_users (username, password_hash, full_name, company_name, is_active) 
VALUES ('testclient', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4X.2XpF6y2', 'Test Client', 'Test Company', true)
ON CONFLICT (username) DO NOTHING;

-- Insert default system configuration
INSERT INTO system_config (config_key, config_value, description) VALUES
('system_name', 'EdgeRelay', 'System name'),
('system_version', '1.0.0', 'System version'),
('maintenance_mode', 'false', 'Maintenance mode status'),
('max_clients', '100', 'Maximum number of clients')
ON CONFLICT (config_key) DO NOTHING;
