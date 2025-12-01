"""initial schema

Revision ID: 9c1e41e7a8b0
Revises: 
Create Date: 2024-06-01 00:00:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "9c1e41e7a8b0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    op.create_table(
        "user_status",
        sa.Column("id", sa.SmallInteger(), nullable=False),
        sa.Column("status_name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("status_name"),
    )

    op.create_table(
        "accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("account_id", sa.String(length=25), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("account_id"),
    )
    op.create_index("ix_accounts_account_id", "accounts", ["account_id"], unique=True)

    op.create_table(
        "project_status",
        sa.Column("id", sa.SmallInteger(), nullable=False),
        sa.Column("status_name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "timesheet_status",
        sa.Column("id", sa.SmallInteger(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("user_id", sa.String(length=25), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("profile", sa.String(length=50), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=True),
        sa.Column("status_id", sa.SmallInteger(), server_default=sa.text("1"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.ForeignKeyConstraint(["status_id"], ["user_status.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_users_user_id", "users", ["user_id"], unique=True)

    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("project_id", sa.String(length=25), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("account_uuid", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("status_id", sa.SmallInteger(), server_default=sa.text("1"), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.ForeignKeyConstraint(["account_uuid"], ["accounts.id"]),
        sa.ForeignKeyConstraint(["status_id"], ["project_status.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id"),
    )
    op.create_index("ix_projects_project_id", "projects", ["project_id"], unique=True)

    op.create_table(
        "timesheet_header",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("user_uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("work_date", sa.Date(), nullable=False),
        sa.Column("status_id", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.ForeignKeyConstraint(["project_uuid"], ["projects.id"]),
        sa.ForeignKeyConstraint(["status_id"], ["timesheet_status.id"]),
        sa.ForeignKeyConstraint(["user_uuid"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "timesheet_item",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("header_uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("hours", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("billable", sa.Boolean(), server_default=sa.text("TRUE"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.ForeignKeyConstraint(["header_uuid"], ["timesheet_header.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("hours >= 0", name="ck_timesheet_item_hours_positive"),
    )


def downgrade() -> None:
    op.drop_table("timesheet_item")
    op.drop_table("timesheet_header")
    op.drop_index("ix_projects_project_id", table_name="projects")
    op.drop_table("projects")
    op.drop_index("ix_users_user_id", table_name="users")
    op.drop_table("users")
    op.drop_table("timesheet_status")
    op.drop_table("project_status")
    op.drop_index("ix_accounts_account_id", table_name="accounts")
    op.drop_table("accounts")
    op.drop_table("user_status")
