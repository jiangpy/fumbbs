"""empty message

Revision ID: 7de4a7dc9e6b
Revises: 
Create Date: 2017-05-11 22:11:11.119000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7de4a7dc9e6b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cms_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('desc', sa.String(length=200), nullable=True),
    sa.Column('create_tine', sa.DateTime(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cmsuser',
    sa.Column('uid', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('_password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_login_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('email')
    )
    op.create_table('front_user',
    sa.Column('uid', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('telephone', sa.String(length=11), nullable=False),
    sa.Column('_password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_login_time', sa.DateTime(), nullable=True),
    sa.Column('now_login_time', sa.DateTime(), nullable=True),
    sa.Column('qq', sa.String(length=15), nullable=True),
    sa.Column('realname', sa.String(length=20), nullable=True),
    sa.Column('gender', sa.Integer(), nullable=True),
    sa.Column('signature', sa.String(length=200), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.Column('avater', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('telephone')
    )
    op.create_table('boards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('edit_time', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['cmsuser.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cms_user_role',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['cms_role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['cmsuser.uid'], ),
    sa.PrimaryKeyConstraint('role_id', 'user_id')
    )
    op.create_table('elitepost',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('create_user_id', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['create_user_id'], ['cmsuser.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('read_count', sa.Integer(), nullable=True),
    sa.Column('is_remove', sa.Boolean(), nullable=True),
    sa.Column('updat_time', sa.DateTime(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.String(length=100), nullable=True),
    sa.Column('is_elite_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['front_user.uid'], ),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['is_elite_id'], ['elitepost.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('is_removed', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.String(length=100), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('origin_comment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['front_user.uid'], ),
    sa.ForeignKeyConstraint(['origin_comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('postpraise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.String(length=100), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['front_user.uid'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('postpraise')
    op.drop_table('comment')
    op.drop_table('post')
    op.drop_table('elitepost')
    op.drop_table('cms_user_role')
    op.drop_table('boards')
    op.drop_table('front_user')
    op.drop_table('cmsuser')
    op.drop_table('cms_role')
    # ### end Alembic commands ###