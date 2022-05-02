from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

MYSQL_DATABASE_URL = "mysql://root:password@127.0.0.1:3306/fastapi"

engine = create_engine(MYSQL_DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()