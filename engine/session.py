# engine/session.py

"""
Session utilities for the Taylor NQ application.

Responsible for determining the current trading session,
session boundaries, and session-specific metadata.

No UI.
No calculations.
No Yahoo Finance downloads.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from zoneinfo import ZoneInfo

import pandas as pd


CHICAGO = ZoneInfo("America/Chicago")
EASTERN = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")


class Session(Enum):
    GLOBEX = "Globex"
    RTH = "Regular Trading Hours"
    CLOSED = "Closed"


@dataclass(slots=True)
class SessionInfo:

    now: datetime

    session: Session

    trading_day: datetime.date

    session_open: datetime
    session_close: datetime

    minutes_until_close: int
    minutes_since_open: int

    is_open: bool


class SessionManager:

    def now(self) -> datetime:
        return datetime.now(CHICAGO)

    def info(self) -> SessionInfo:

        now = self.now()

        trading_day = self._trading_day(now)

        rth_open = datetime.combine(
            trading_day,
            datetime.min.time(),
            tzinfo=CHICAGO,
        ).replace(hour=8, minute=30)

        rth_close = datetime.combine(
            trading_day,
            datetime.min.time(),
            tzinfo=CHICAGO,
        ).replace(hour=15, minute=0)

        globex_open = (
            datetime.combine(
                trading_day,
                datetime.min.time(),
                tzinfo=CHICAGO,
            )
            - timedelta(days=1)
        ).replace(hour=17, minute=0)

        globex_close = rth_close

        if rth_open <= now <= rth_close:

            session = Session.RTH
            open_time = rth_open
            close_time = rth_close

        elif globex_open <= now < rth_open:

            session = Session.GLOBEX
            open_time = globex_open
            close_time = rth_open

        else:

            session = Session.CLOSED
            open_time = rth_close
            close_time = globex_open + timedelta(days=1)

        return SessionInfo(
            now=now,
            session=session,
            trading_day=trading_day,
            session_open=open_time,
            session_close=close_time,
            minutes_until_close=max(
                0,
                int((close_time - now).total_seconds() / 60),
            ),
            minutes_since_open=max(
                0,
                int((now - open_time).total_seconds() / 60),
            ),
            is_open=session != Session.CLOSED,
        )

    def is_rth(self) -> bool:
        return self.info().session == Session.RTH

    def is_globex(self) -> bool:
        return self.info().session == Session.GLOBEX

    def is_market_open(self) -> bool:
        return self.info().is_open

    @staticmethod
    def _trading_day(now: datetime):

        if now.hour >= 17:
            return (now + timedelta(days=1)).date()

        return now.date()

    @staticmethod
    def previous_session(df: pd.DataFrame) -> pd.DataFrame:

        if df.empty:
            return df

        last_date = df.index[-1].date()

        previous = df[df.index.date < last_date]

        if previous.empty:
            return previous

        session_date = previous.index[-1].date()

        return previous[previous.index.date == session_date]

    @staticmethod
    def current_session(df: pd.DataFrame) -> pd.DataFrame:

        if df.empty:
            return df

        session_date = df.index[-1].date()

        return df[df.index.date == session_date]
