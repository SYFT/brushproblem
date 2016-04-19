from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
document = Table('document', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('userId', Integer),
    Column('subjectId', Integer),
    Column('title', String(length=256)),
    Column('timeStamp', DateTime),
)

subject = Table('subject', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=32)),
)

problem = Table('problem', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('userId', INTEGER),
    Column('timeStamp', DATETIME),
    Column('title', VARCHAR(length=256)),
    Column('storage', VARCHAR(length=256)),
)

problem = Table('problem', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('source', Integer),
    Column('content', String(length=512)),
    Column('answer', String(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['document'].create()
    post_meta.tables['subject'].create()
    pre_meta.tables['problem'].columns['storage'].drop()
    pre_meta.tables['problem'].columns['timeStamp'].drop()
    pre_meta.tables['problem'].columns['title'].drop()
    pre_meta.tables['problem'].columns['userId'].drop()
    post_meta.tables['problem'].columns['answer'].create()
    post_meta.tables['problem'].columns['content'].create()
    post_meta.tables['problem'].columns['source'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['document'].drop()
    post_meta.tables['subject'].drop()
    pre_meta.tables['problem'].columns['storage'].create()
    pre_meta.tables['problem'].columns['timeStamp'].create()
    pre_meta.tables['problem'].columns['title'].create()
    pre_meta.tables['problem'].columns['userId'].create()
    post_meta.tables['problem'].columns['answer'].drop()
    post_meta.tables['problem'].columns['content'].drop()
    post_meta.tables['problem'].columns['source'].drop()
