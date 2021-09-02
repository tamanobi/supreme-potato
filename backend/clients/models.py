import sqlalchemy
from db import metadata, engine

clients = sqlalchemy.Table(
    "clients",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("key", sqlalchemy.String, index=True),
)

metadata.create_all(bind=engine)
