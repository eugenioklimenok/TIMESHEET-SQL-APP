
-- 06_timesheet_header.sql
CREATE TABLE IF NOT EXISTS timesheet_header (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    project_id UUID NOT NULL REFERENCES projects(id),
    work_date DATE NOT NULL,
    status_id SMALLINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
