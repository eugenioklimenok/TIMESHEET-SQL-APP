"""t6 timesheet item logic

Revision ID: 8c6f1b9af6a0
Revises: 1e5f1d3c6b21
Create Date: 2025-03-01 00:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "8c6f1b9af6a0"
down_revision = "1e5f1d3c6b21"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("timesheet_item")}
    checks = {check["name"] for check in inspector.get_check_constraints("timesheet_item")}

    with op.batch_alter_table("timesheet_item") as batch_op:
        if "header_uuid" in columns and "header_id" not in columns:
            batch_op.alter_column("header_uuid", new_column_name="header_id")

        if "billable" in columns:
            batch_op.drop_column("billable")

        if "project_id" not in columns:
            batch_op.add_column(sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True))

        if "date" not in columns:
            batch_op.add_column(
                sa.Column(
                    "date",
                    sa.Date(),
                    nullable=False,
                    server_default=sa.text("CURRENT_DATE"),
                )
            )

        if "updated_at" not in columns:
            batch_op.add_column(
                sa.Column(
                    "updated_at",
                    sa.DateTime(timezone=False),
                    nullable=True,
                    server_default=sa.text("CURRENT_TIMESTAMP"),
                )
            )

        if "ck_timesheet_item_hours_positive" in checks:
            batch_op.drop_constraint("ck_timesheet_item_hours_positive", type_="check")

    if "ck_timesheet_item_hours_range" not in checks:
        op.create_check_constraint(
            "ck_timesheet_item_hours_range",
            "timesheet_item",
            "hours > 0 AND hours <= 24",
        )

    fk_names = {fk["name"] for fk in inspector.get_foreign_keys("timesheet_item")}
    if "fk_timesheet_item_project" not in fk_names:
        op.create_foreign_key(
            "fk_timesheet_item_project",
            "timesheet_item",
            "projects",
            ["project_id"],
            ["id"],
        )

    with op.batch_alter_table("timesheet_item") as batch_op:
        batch_op.alter_column("date", server_default=None)


def downgrade() -> None:
    with op.batch_alter_table("timesheet_item") as batch_op:
        batch_op.alter_column("date", server_default=sa.text("CURRENT_DATE"))
        batch_op.drop_constraint("ck_timesheet_item_hours_range", type_="check")
        batch_op.drop_constraint("fk_timesheet_item_project", type_="foreignkey")
        batch_op.drop_column("updated_at")
        batch_op.drop_column("date")
        batch_op.drop_column("project_id")
        batch_op.add_column(sa.Column("billable", sa.Boolean(), server_default=sa.text("TRUE")))
        batch_op.alter_column("header_id", new_column_name="header_uuid")
