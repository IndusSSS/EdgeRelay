-- Update clients table to add client_username and password_hash columns

-- Add client_username column
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'clients' AND column_name = 'client_username') THEN
        ALTER TABLE clients ADD COLUMN client_username VARCHAR(100) UNIQUE;
        RAISE NOTICE 'Added client_username column to clients table';
    ELSE
        RAISE NOTICE 'client_username column already exists in clients table';
    END IF;
END $$;

-- Add password_hash column
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'clients' AND column_name = 'password_hash') THEN
        ALTER TABLE clients ADD COLUMN password_hash VARCHAR(255);
        RAISE NOTICE 'Added password_hash column to clients table';
    ELSE
        RAISE NOTICE 'password_hash column already exists in clients table';
    END IF;
END $$;

-- Update existing client with default values
UPDATE clients 
SET 
    client_username = LOWER(REPLACE(company_name, ' ', '_')) || '_client',
    password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8K5K5K5K5K'  -- Default password hash
WHERE client_username IS NULL;

-- Show updated clients
SELECT client_id, company_name, client_username, email 
FROM clients 
ORDER BY created_at DESC;
