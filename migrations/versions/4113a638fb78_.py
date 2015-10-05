"""empty message

Revision ID: 4113a638fb78
Revises: None
Create Date: 2015-06-22 17:12:44.325000

"""

# revision identifiers, used by Alembic.
revision = '4113a638fb78'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###  
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('real_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('url', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('token_name', sa.VARCHAR(length=60), nullable=False),
    sa.Column('slack_teamid', sa.VARCHAR(length=255), nullable=True),
    sa.Column('name', sa.VARCHAR(length=255), nullable=False),
    sa.Column('code', sa.VARCHAR(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )   
    op.create_table('users_organizations',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('organization_id', sa.INTEGER(), nullable=True),
    sa.Column('org_tokens', sa.FLOAT(), nullable=True),
    sa.Column('org_reputation', sa.FLOAT(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contribution',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('ownerId', sa.INTEGER(), nullable=True),
    sa.Column('users_organizations_id', sa.INTEGER(), nullable=True),
    sa.Column('min_reputation_to_close', sa.INTEGER(), nullable=True),
    sa.Column('time_created', sa.DATETIME(), nullable=True),
    sa.Column('file', sa.TEXT(), nullable=True),
    sa.Column('title', sa.VARCHAR(length=340), nullable=True),
    sa.Column('status', sa.VARCHAR(length=100), nullable=True),
    sa.ForeignKeyConstraint(['ownerId'], ['user.id'], ),
    sa.ForeignKeyConstraint(['users_organizations_id'], ['users_organizations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contribution_contributer',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('contribution_id', sa.INTEGER(), nullable=True),
    sa.Column('contributor_id', sa.INTEGER(), nullable=True),
    sa.Column('percentage', sa.FLOAT(), nullable=True),
    sa.ForeignKeyConstraint(['contributor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['contribution_id'], ['contribution.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    
    op.create_table('bid',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('ownerId', sa.INTEGER(), nullable=True),
    sa.Column('contribution_id', sa.INTEGER(), nullable=True),
    sa.Column('tokens', sa.FLOAT(), nullable=True),
    sa.Column('stake', sa.FLOAT(), nullable=True),
    sa.Column('reputation', sa.FLOAT(), nullable=True),
    sa.Column('current_rep_to_return', sa.FLOAT(), nullable=True),
    sa.Column('contribution_value_after_bid', sa.FLOAT(), nullable=True),
    sa.Column('time_created', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['contribution_id'], ['contribution.id'], ),
    sa.ForeignKeyConstraint(['ownerId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bid')
    op.drop_table('contribution_contributor')
    op.drop_table('contribution')
    op.drop_table('users_organizations')
    op.drop_table('user')
    op.drop_table('organization')
    
    ### end Alembic commands ###
