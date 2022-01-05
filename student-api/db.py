from datetime import datetime
from os import environ

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


connect_str =\
    'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'\
    .format(**environ)


engine = sa.create_engine(connect_str)

metadata = sa.MetaData()
metadata.bind = engine


now = datetime.utcnow
default_now = dict(default=now, server_default=sa.func.now())
new_uuid = sa.text('uuid_generate_v4()')


students = sa.Table(
    'students',
    metadata,
    sa.Column('id', UUID(as_uuid=True),
              nullable=False, server_default=new_uuid),
    sa.Column('name', sa.String, nullable=False),
    sa.Column("gender", sa.String),
    sa.Column("state", sa.String),
    sa.Column("department", sa.String),
    sa.Column('birth_date', sa.DateTime, nullable=False, **default_now),
    sa.Column('created_at', sa.DateTime, nullable=False, **default_now),
    sa.Column('updated_at', sa.DateTime, nullable=False,
              onupdate=now, **default_now),
)


with engine.begin() as conn:
    conn.execute(sa.text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))

metadata.create_all(engine)
