import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase


def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return database_url

    required_variables = [
        "DB_HOST",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing = [
        name for name in required_variables
        if not os.getenv(name)
    ]

    if missing:
        raise RuntimeError(
            "Missing database configuration: "
            + ", ".join(missing)
        )

    return URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.environ["DB_NAME"],
        query={"sslmode": "verify-full", "sslrootcert": os.environ["DB_SSL_ROOT_CERT"]} if os.getenv("DB_SSL_ROOT_CERT") else {"sslmode": "require"},
    )


DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


class Base(DeclarativeBase):
    pass