from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
document = Table('document', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('userId', Integer),
    Column('subjectId', Integer),
    Column('title', String(length=256, convert_unicode=True)),
    Column('keywordsForTitle', String(length=512, convert_unicode=True)),
    Column('timeStamp', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['document'].columns['keywordsForTitle'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['document'].columns['keywordsForTitle'].drop()
