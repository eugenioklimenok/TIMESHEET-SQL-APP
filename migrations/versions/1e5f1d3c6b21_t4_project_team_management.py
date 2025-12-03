"""t4 project & team management basics

Revision ID: 1e5f1d3c6b21
Revises: 7b2f3d8f2c2b
Create Date: 2025-02-01 00:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "1e5f1d3c6b21"
down_revision = "7b2f3d8f2c2b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("code", sa.String(length=16), nullable=True))
    op.add_column("projects", sa.Column("client_name", sa.String(length=150), nullable=True))
    op.add_column(
        "projects",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("TRUE"),
        ),
    )
    op.add_column(
        "projects",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.alter_column(
        "projects",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
    )

    op.execute("UPDATE projects SET code = project_id WHERE code IS NULL")
    op.alter_column("projects", "code", nullable=False)
    op.create_index("ix_projects_code", "projects", ["code"], unique=True)

    op.create_table(
        "user_project_membership",
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            primary_key=True,
        ),
        sa.Column(
            "project_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("projects.id"),
            primary_key=True,
        ),
        sa.Column("role_in_project", sa.String(length=50), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("user_project_membership")
    op.drop_index("ix_projects_code", table_name="projects")
    op.drop_column("projects", "updated_at")
    op.drop_column("projects", "is_active")
    op.drop_column("projects", "client_name")
    op.drop_column("projects", "code")
    op.alter_column(
        "projects",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=True,
    )
