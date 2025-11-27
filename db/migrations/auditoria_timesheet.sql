-- Crear tabla para auditoría de transacciones del Timesheet
CREATE TABLE auditoria_timesheet (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  usuario character varying NOT NULL,
  fecha timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  entidad character varying NOT NULL,
  registro_id uuid NOT NULL,
  accion character varying NOT NULL,
  old_data jsonb,
  new_data jsonb,
  PRIMARY KEY (id)
);
-- Crear función para insertar en auditoría
CREATE OR REPLACE FUNCTION insertar_auditoria(
  p_usuario character varying,
  p_entidad character varying,
  p_registro_id uuid,
  p_accion character varying,
  p_old_data jsonb,
  p_new_data jsonb
)
RETURNS void AS $$
BEGIN
  INSERT INTO auditoria_timesheet(
    usuario,
    fecha,
    entidad,
    registro_id,
    accion,
    old_data,
    new_data
  )
  VALUES (
    p_usuario,
    NOW(),
    p_entidad,
    p_registro_id,
    p_accion,
    p_old_data,
    p_new_data
  );
END;
$$ LANGUAGE plpgsql;