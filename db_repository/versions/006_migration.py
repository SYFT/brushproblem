from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
problem = Table('problem', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('answer', VARCHAR(length=128)),
    Column('content', VARCHAR(length=512)),
    Column('source', INTEGER),
)

problem = Table('problem', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('documentId', Integer),
    Column('content', String(length=512)),
    Column('choice', String(length=512)),
    Column('answer', String(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['problem'].columns['source'].drop()
    post_meta.tables['problem'].columns['choice'].create()
    post_meta.tables['problem'].columns['documentId'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['problem'].columns['source'].create()
    post_meta.tables['problem'].columns['choice'].drop()
    post_meta.tables['problem'].columns['documentId'].drop()
