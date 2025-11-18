"""Thin wrapper around the official tastytrade Python client."""
from __future__ import annotations

from datetime import date
from typing import Any, Dict, Iterable, List, Optional

from tastytrade import Account, Session

from .auth import Credentials


class TastyClient:
    """Fetch portfolio data using the tastytrade Python SDK."""

    def __init__(self, credentials: Optional[Credentials] = None) -> None:
        self.credentials = credentials or Credentials.from_env()
        self.session = Session(self.credentials.username, self.credentials.password)
        account_id = self.credentials.account_id
        accounts = Account.get_accounts(self.session)
        if account_id:
            account = next((acct for acct in accounts if acct.account_number == account_id), None)
            if account is None:
                raise ValueError(f"Account {account_id} not found for user {self.credentials.username}")
            self.account = account
        else:
            self.account = accounts[0]

    def _normalize_positions(self, raw_positions: Iterable[Any]) -> List[Dict[str, Any]]:
        normalized = []
        for pos in raw_positions:
            normalized.append(
                {
                    "account_id": self.account.account_number,
                    "underlying": pos.symbol,  # tastytrade uses symbol for underlying
                    "symbol": pos.symbol,
                    "expiry": getattr(pos, "expiration_date", None),
                    "strike": getattr(pos, "strike_price", None),
                    "quantity": pos.quantity,
                    "avg_price": getattr(pos, "average_price", None),
                    "mark_price": getattr(pos, "mark_price", None),
                    "delta": getattr(pos, "delta", None),
                    "gamma": getattr(pos, "gamma", None),
                    "theta": getattr(pos, "theta", None),
                    "vega": getattr(pos, "vega", None),
                }
            )
        return normalized

    def get_positions(self) -> List[Dict[str, Any]]:
        positions = self.account.get_positions()
        return self._normalize_positions(positions)

    def get_activity(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        activity = self.account.get_activity(start_date, end_date)
        normalized: List[Dict[str, Any]] = []
        for entry in activity:
            normalized.append(
                {
                    "transaction_date": entry.transaction_date,
                    "description": entry.description,
                    "net_amount": entry.net_amount,
                }
            )
        return normalized
