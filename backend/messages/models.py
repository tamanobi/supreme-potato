import sqlalchemy
from db import metadata, engine

messages = sqlalchemy.Table(
    "messages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("message", sqlalchemy.String)
)

metadata.create_all(bind=engine)
