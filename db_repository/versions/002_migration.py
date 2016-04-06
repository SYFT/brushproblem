from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
problem = Table('problem', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('userId', Integer),
    Column('timeStamp', DateTime),
    Column('title', String(length=256)),
    Column('storage', String(length=256)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['problem'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['problem'].drop()
