"""
engine/calculations.py

Taylor NQ calculation engine.

The formulas implemented in this file are taken directly from the
Taylors NQ.xlsx workbook. Live OHLC data is expected to come from
Yahoo Finance before being passed into this module.

No UI code.
No network code.
Only calculations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
]


@dataclass(slots=True)
class TaylorLevels:
    date: pd.Timestamp

    open: float
    high: float
    low: float
    close: float

    rally: Optional[float]
    rally_avg: Optional[float]
    anticipated_high_from_low: Optional[float]

    buying_high: Optional[float]
    buying_high_avg: Optional[float]
    anticipated_high_from_high: Optional[float]

    pivot_breakout_high: Optional[float]
    avg_sell: Optional[float]

    decline: Optional[float]
    decline_avg: Optional[float]
    yesterday_high_minus_avg: Optional[float]

    buying_low: Optional[float]
    buying_low_avg: Optional[float]
    yesterday_low_minus_avg: Optional[float]

    pivot_breakout_low: Optional[float]
    avg_buy: Optional[float]


class TaylorCalculator:
    """
    Implements the calculations contained in Taylors NQ.xlsx.
    """

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("DataFrame index must be a DatetimeIndex.")

        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        out = df.copy()

        prev_open = out["Open"].shift(1)
        prev_high = out["High"].shift(1)
        prev_low = out["Low"].shift(1)

        #
        # ===== Workbook Columns =====
        #

        # I
        out["Rally"] = out["High"] - prev_low

        # J
        out["RallyAvg3"] = out["Rally"].rolling(3).mean()

        # K
        out["AnticipatedHighFromLow"] = (
            out["Low"] + out["RallyAvg3"]
        )

        # M
        out["BuyingHigh"] = out["High"] - prev_open

        # N
        out["BuyingHighAvg3"] = (
            out["BuyingHigh"].rolling(3).mean()
        )

        # O
        out["AnticipatedHighFromHigh"] = (
            out["High"] + out["BuyingHighAvg3"]
        )

        # Q
        out["TodayHigh"] = out["High"]

        # S
        out["PivotBreakoutHigh"] = (
            2 * ((out["High"] + out["Low"] + out["Close"]) / 3)
            - out["Low"]
        )

        # U
        out["AvgSell"] = (
            out[
                [
                    "PivotBreakoutHigh",
                    "TodayHigh",
                    "AnticipatedHighFromHigh",
                    "AnticipatedHighFromLow",
                ]
            ]
            .mean(axis=1)
        )

        # W
        out["Decline"] = prev_high - out["Low"]

        # X
        out["DeclineAvg3"] = (
            out["Decline"].rolling(3).mean()
        )

        # Y
        out["YesterdayHighMinusAvg"] = (
            out["High"] - out["DeclineAvg3"]
        )

        # AA
        out["BuyingLow"] = prev_low - out["Low"]

        # AB
        out["BuyingLowAvg3"] = (
            out["BuyingLow"].rolling(3).mean()
        )

        # AC
        out["YesterdayLowMinusAvg"] = (
            out["Low"] - out["BuyingLowAvg3"]
        )

        # AE
        out["TodayLow"] = out["Low"]

        # AG
        out["PivotBreakoutLow"] = (
            2 * ((out["High"] + out["Low"] + out["Close"]) / 3)
            - out["High"]
        )

        # AI
        out["AvgBuy"] = (
            out[
                [
                    "PivotBreakoutLow",
                    "TodayLow",
                    "YesterdayLowMinusAvg",
                    "YesterdayHighMinusAvg",
                ]
            ]
            .mean(axis=1)
        )

        return out

    def latest(self, df: pd.DataFrame) -> TaylorLevels:

        calc = self.calculate(df)
        row = calc.iloc[-1]

        return TaylorLevels(
            date=calc.index[-1],

            open=float(row["Open"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            close=float(row["Close"]),

            rally=self._num(row["Rally"]),
            rally_avg=self._num(row["RallyAvg3"]),
            anticipated_high_from_low=self._num(
                row["AnticipatedHighFromLow"]
            ),

            buying_high=self._num(row["BuyingHigh"]),
            buying_high_avg=self._num(row["BuyingHighAvg3"]),
            anticipated_high_from_high=self._num(
                row["AnticipatedHighFromHigh"]
            ),

            pivot_breakout_high=self._num(
                row["PivotBreakoutHigh"]
            ),
            avg_sell=self._num(row["AvgSell"]),

            decline=self._num(row["Decline"]),
            decline_avg=self._num(row["DeclineAvg3"]),
            yesterday_high_minus_avg=self._num(
                row["YesterdayHighMinusAvg"]
            ),

            buying_low=self._num(row["BuyingLow"]),
            buying_low_avg=self._num(row["BuyingLowAvg3"]),
            yesterday_low_minus_avg=self._num(
                row["YesterdayLowMinusAvg"]
            ),

            pivot_breakout_low=self._num(
                row["PivotBreakoutLow"]
            ),
            avg_buy=self._num(row["AvgBuy"]),
        )

    @staticmethod
    def _num(value):

        if pd.isna(value):
            return None

        if isinstance(value, (np.floating, np.integer)):
            return float(value)

        return float(value)
