"""Aurora/PostgreSQL compatible SQLAlchemy models."""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Position(Base):
    __tablename__ = "positions"
    __table_args__ = (
        UniqueConstraint("account_id", "symbol", "expiry", "strike", name="uniq_position"),
    )

    id = Column(Integer, primary_key=True)
    account_id = Column(String, index=True, nullable=False)
    underlying = Column(String, index=True, nullable=False)
    symbol = Column(String, index=True, nullable=False)
    expiry = Column(Date, nullable=True)
    strike = Column(Numeric(18, 4), nullable=True)
    quantity = Column(Integer, nullable=False)
    avg_price = Column(Numeric(18, 4), nullable=True)
    mark_price = Column(Numeric(18, 4), nullable=True)
    delta = Column(Numeric(18, 6), nullable=True)
    gamma = Column(Numeric(18, 6), nullable=True)
    theta = Column(Numeric(18, 6), nullable=True)
    vega = Column(Numeric(18, 6), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    account_id = Column(String, index=True, nullable=False)
    symbol = Column(String, index=True, nullable=False)
    transaction_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    net_amount = Column(Numeric(18, 4), nullable=False)


class Price(Base):
    __tablename__ = "prices"
    __table_args__ = (
        UniqueConstraint("symbol", "price_date", name="uniq_price_symbol_date"),
    )

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True, nullable=False)
    price_date = Column(Date, nullable=False)
    close_price = Column(Numeric(18, 4), nullable=False)
