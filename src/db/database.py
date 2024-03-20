from src.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


# create engine
DBINFO = settings.database
if DBINFO.type == "sqlite":
    SQLALCHEMY_DATABASE_URL = f"{DBINFO.type}:///{DBINFO.location}"
else:
    SQLALCHEMY_DATABASE_URL = (
        f"{DBINFO.type}://{DBINFO.user}:{DBINFO.password}@{DBINFO.server}/{DBINFO.db}"
    )


# create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# create session
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
