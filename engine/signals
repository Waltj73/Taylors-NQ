# engine/signals.py

"""
Signal engine for the Taylor NQ application.

Consumes calculated Taylor values and determines the current
Taylor day type and actionable trading levels.

This module contains no UI and no Yahoo Finance code.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import pandas as pd


class DayType(str, Enum):
    BUY = "BUY DAY"
    SELL = "SELL DAY"
    BUY_SELL = "BUY/SELL DAY"
    SELL_BUY = "SELL/BUY DAY"
    UNKNOWN = "UNKNOWN"


@dataclass(slots=True)
class SignalResult:

    date: pd.Timestamp

    day_type: DayType

    bullish: bool
    bearish: bool

    avg_buy: float | None
    avg_sell: float | None

    pivot_high: float | None
    pivot_low: float | None

    close: float

    above_avg_buy: bool
    below_avg_sell: bool


class SignalEngine:

    def evaluate(
        self,
        calculations: pd.DataFrame,
    ) -> SignalResult:

        row = calculations.iloc[-1]

        close = float(row["Close"])

        avg_buy = self._value(row.get("AvgBuy"))
        avg_sell = self._value(row.get("AvgSell"))

        pivot_high = self._value(row.get("PivotBreakoutHigh"))
        pivot_low = self._value(row.get("PivotBreakoutLow"))

        bullish = False
        bearish = False

        if avg_buy is not None:
            bullish = close >= avg_buy

        if avg_sell is not None:
            bearish = close <= avg_sell

        day_type = self._determine_day_type(
            bullish=bullish,
            bearish=bearish,
            close=close,
            avg_buy=avg_buy,
            avg_sell=avg_sell,
        )

        return SignalResult(
            date=calculations.index[-1],
            day_type=day_type,
            bullish=bullish,
            bearish=bearish,
            avg_buy=avg_buy,
            avg_sell=avg_sell,
            pivot_high=pivot_high,
            pivot_low=pivot_low,
            close=close,
            above_avg_buy=(
                avg_buy is not None and close >= avg_buy
            ),
            below_avg_sell=(
                avg_sell is not None and close <= avg_sell
            ),
        )

    @staticmethod
    def _determine_day_type(
        *,
        bullish: bool,
        bearish: bool,
        close: float,
        avg_buy: float | None,
        avg_sell: float | None,
    ) -> DayType:

        if bullish and not bearish:
            return DayType.BUY

        if bearish and not bullish:
            return DayType.SELL

        if avg_buy is None or avg_sell is None:
            return DayType.UNKNOWN

        midpoint = (avg_buy + avg_sell) / 2

        if close >= midpoint:
            return DayType.BUY_SELL

        return DayType.SELL_BUY

    @staticmethod
    def _value(v):

        if pd.isna(v):
            return None

        return float(v)
