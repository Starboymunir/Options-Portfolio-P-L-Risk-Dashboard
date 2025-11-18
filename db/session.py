"""Session/engine factory utilities."""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

load_dotenv()


def get_engine(echo: bool = False):
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set. Update your .env file.")
    return create_engine(database_url, echo=echo, future=True)


def get_sessionmaker(echo: bool = False) -> sessionmaker[Session]:
    engine = get_engine(echo=echo)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


@contextmanager
def session_scope(echo: bool = False) -> Iterator[Session]:
    """Provide a transactional scope for DB operations."""
    SessionLocal = get_sessionmaker(echo=echo)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
