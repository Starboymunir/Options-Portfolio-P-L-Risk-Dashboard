"""Helper utilities for authenticating with the Tastytrade API."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Credentials:
    """A small dataclass to hold credential details."""

    username: str
    password: str
    account_id: Optional[str] = None

    @classmethod
    def from_env(cls) -> "Credentials":
        """Load credentials from environment variables."""
        username = os.environ.get("TASTYTRADE_USERNAME")
        password = os.environ.get("TASTYTRADE_PASSWORD")
        account_id = os.environ.get("TASTYTRADE_ACCOUNT_ID")
        if not username or not password:
            raise RuntimeError(
                "Tastytrade credentials missing. Set TASTYTRADE_USERNAME and TASTYTRADE_PASSWORD."
            )
        return cls(username=username, password=password, account_id=account_id)
