import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Read DATABASE_URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
#unset DATABASE_URL
#export DATABASE_URL="postgresql+psycopg2://baxbox:7String7@pgdb-baxbox-staging.postgres.database.azure.com:5432/postgres?sslmode=require"

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
