# engine/models.py

"""
Taylor NQ Models

Shared dataclasses used throughout the application.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass(slots=True)
class MarketSnapshot:

    symbol: str

    timestamp: datetime

    last: float

    open: float

    high: float

    low: float

    previous_close: float

    volume: float


@dataclass(slots=True)
class TaylorDay:

    trading_day: date

    open: float

    high: float

    low: float

    close: float


@dataclass(slots=True)
class TaylorProjection:

    avg_buy: Optional[float]

    avg_sell: Optional[float]

    pivot_high: Optional[float]

    pivot_low: Optional[float]

    anticipated_high_from_low: Optional[float]

    anticipated_high_from_high: Optional[float]

    yesterday_high_minus_avg: Optional[float]

    yesterday_low_minus_avg: Optional[float]


@dataclass(slots=True)
class VerificationItem:

    column: str

    workbook: Optional[float]

    application: Optional[float]

    difference: Optional[float]

    passed: bool


@dataclass(slots=True)
class SignalState:

    day_type: str

    bullish: bool

    bearish: bool

    above_avg_buy: bool

    below_avg_sell: bool


@dataclass(slots=True)
class AppState:

    market: MarketSnapshot

    day: TaylorDay

    projections: TaylorProjection

    signal: SignalState
