"""add institution_type, city, data_source_url, and last_verified_at to schools

Revision ID: f8a1c9e3b4d2
Revises: e4b7c2a91f3d
Create Date: 2026-10-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8a1c9e3b4d2'
down_revision = 'e4b7c2a91f3d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('schools', sa.Column('institution_type', sa.String(length=50), nullable=True))
    op.add_column('schools', sa.Column('city', sa.String(length=100), nullable=True))
    op.create_index(op.f('ix_schools_city'), 'schools', ['city'], unique=False)
    op.add_column('schools', sa.Column('data_source_url', sa.String(), nullable=True))
    op.add_column('schools', sa.Column('last_verified_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('schools', 'last_verified_at')
    op.drop_column('schools', 'data_source_url')
    op.drop_index(op.f('ix_schools_city'), table_name='schools')
    op.drop_column('schools', 'city')
    op.drop_column('schools', 'institution_type')
