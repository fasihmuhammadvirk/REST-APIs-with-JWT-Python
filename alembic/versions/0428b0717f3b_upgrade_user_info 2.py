"""Upgrade User Info

Revision ID: 0428b0717f3b
Revises: 
Create Date: 2023-07-25 11:44:29.720147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0428b0717f3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('child')
    op.drop_table('parent')
    op.drop_table('items')
    op.drop_table('association')
    op.drop_table('posts')
    op.drop_table('customers')
    op.drop_table('products')
    op.alter_column('user_info', 'jwt_token',
               existing_type=sa.VARCHAR(length=400),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_info', 'jwt_token',
               existing_type=sa.VARCHAR(length=400),
               nullable=False)
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('products_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='products_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('customers',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('customers_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='customers_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=45), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(length=225), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users_info.id'], name='posts_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='posts_pkey')
    )
    op.create_table('association',
    sa.Column('customer_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], name='association_customer_id_fkey'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name='association_product_id_fkey')
    )
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=45), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('on_offer', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='items_pkey')
    )
    op.create_table('parent',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('parent_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='parent_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('child',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    sa.Column('parent_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['parent.id'], name='child_parent_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='child_pkey')
    )
    op.create_table('users_info',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_info_pkey')
    )
    # ### end Alembic commands ###
