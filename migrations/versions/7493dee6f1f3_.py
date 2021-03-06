"""empty message

Revision ID: 7493dee6f1f3
Revises: 2b9e7890fa2c
Create Date: 2017-08-17 22:10:25.804167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7493dee6f1f3'
down_revision = '2b9e7890fa2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('bucketlists_description_key', 'bucketlists', type_='unique')
    op.alter_column('items', 'title',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
    op.drop_constraint('items_description_key', 'items', type_='unique')
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.create_unique_constraint('items_description_key', 'items', ['description'])
    op.alter_column('items', 'title',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
    op.create_unique_constraint('bucketlists_description_key', 'bucketlists', ['description'])
    # ### end Alembic commands ###
