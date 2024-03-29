"""Add contacted_count property on Place

Revision ID: 7d40282fa7e0
Revises: 3c43978440d2
Create Date: 2023-02-15 10:25:42.542676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7d40282fa7e0"
down_revision = "3c43978440d2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("place", schema=None) as batch_op:
        batch_op.add_column(sa.Column("contacted_count", sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("place", schema=None) as batch_op:
        batch_op.drop_column("contacted_count")

    # ### end Alembic commands ###
