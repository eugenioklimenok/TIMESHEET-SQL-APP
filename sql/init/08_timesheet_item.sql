-- Detalle por actividad
CREATE TABLE IF NOT EXISTS timesheet_item (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    header_uuid UUID NOT NULL REFERENCES timesheet_header(id),
    description TEXT NOT NULL,
    hours NUMERIC(5,2) NOT NULL CHECK (hours >= 0),
    billable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
