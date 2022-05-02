import databases
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    MetaData
)

from databases import Database

DATABASE_URL = "mysql://root:password@127.0.0.1:3306/test"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

Article = Table(
    "article",
    metadata,
    Column("id", Integer, primary_key = True),
    Column("title", String(100)),
    Column("description", String(500))  
)

User = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key = True),
    Column("username", String(100)),
    Column("password", String(200))
)


database = Database(DATABASE_URL)
