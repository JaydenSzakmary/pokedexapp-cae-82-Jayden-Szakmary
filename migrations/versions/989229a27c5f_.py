"""empty message

Revision ID: 989229a27c5f
Revises: 53d942899dd1
Create Date: 2022-02-08 16:06:54.668931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '989229a27c5f'
down_revision = '53d942899dd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_pokemon',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('poke_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['poke_id'], ['pokemon.poke_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'poke_id')
    )
    op.drop_table('user__pokemon')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user__pokemon',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('poke_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['poke_id'], ['pokemon.poke_id'], name='user__pokemon_poke_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user__pokemon_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'poke_id', name='user__pokemon_pkey')
    )
    op.drop_table('user_pokemon')
    # ### end Alembic commands ###
