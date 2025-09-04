"""add tickets

Revision ID: 0a1f3b2e0d9a
Revises: b261c5f9902e
Create Date: 2025-09-04 15:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a1f3b2e0d9a'
down_revision = 'b261c5f9902e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ticket',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('org_id', sa.Integer(), sa.ForeignKey('organization.id'), nullable=False),
        sa.Column('created_by_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('assigned_to_id', sa.Integer(), sa.ForeignKey('user.id')),
        sa.Column('subject', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='new'),
        sa.Column('priority', sa.String(length=20), nullable=False, server_default='normal'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'ticket_comment',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('ticket_id', sa.Integer(), sa.ForeignKey('ticket.id'), nullable=False),
        sa.Column('author_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
    )


def downgrade():
    op.drop_table('ticket_comment')
    op.drop_table('ticket')

