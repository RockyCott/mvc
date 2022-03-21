"""empty message

Revision ID: b3b9a8b7e1f4
Revises: 
Create Date: 2021-05-11 20:19:18.552011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3b9a8b7e1f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('date_registered', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('username'),
    schema='users_info'
    )
    op.create_table('community',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.Column('picture', sa.Text(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users_info.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='communities'
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=60), nullable=False),
    sa.Column('content', sa.String(length=2000), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('community_id', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users_info.user.id'], ),
    sa.ForeignKeyConstraint(['community_id'], ['communities.community.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='communities'
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=2000), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users_info.user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['communities.post.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='communities'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment', schema='communities')
    op.drop_table('post', schema='communities')
    op.drop_table('community', schema='communities')
    op.drop_table('user', schema='users_info')
    # ### end Alembic commands ###