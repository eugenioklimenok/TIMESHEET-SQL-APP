-- Cabecera del parte diario
CREATE TABLE IF NOT EXISTS timesheet_header (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_uuid UUID NOT NULL REFERENCES users(id),
    project_uuid UUID NOT NULL REFERENCES projects(id),
    work_date DATE NOT NULL,
    status_id SMALLINT NOT NULL DEFAULT 0 REFERENCES timesheet_status(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
