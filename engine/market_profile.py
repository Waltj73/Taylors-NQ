# engine/market_profile.py

"""
Taylor Market Profile

Calculates daily statistics used throughout the Taylor Trading
application.

This module intentionally contains no UI code.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class DailyProfile:

    date: pd.Timestamp

    open: float

    high: float

    low: float

    close: float

    range: float

    body: float

    upper_wick: float

    lower_wick: float

    midpoint: float

    pivot: float

    true_range: float


class MarketProfile:

    def calculate(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        df = dataframe.copy()

        previous_close = df["Close"].shift(1)

        df["Range"] = (
            df["High"] - df["Low"]
        )

        df["Body"] = (
            df["Close"] - df["Open"]
        ).abs()

        df["UpperWick"] = (
            df["High"]
            - df[["Open", "Close"]].max(axis=1)
        )

        df["LowerWick"] = (
            df[["Open", "Close"]].min(axis=1)
            - df["Low"]
        )

        df["Midpoint"] = (
            df["High"] + df["Low"]
        ) / 2

        df["Pivot"] = (
            df["High"]
            + df["Low"]
            + df["Close"]
        ) / 3

        df["TrueRange"] = pd.concat(
            [
                df["High"] - df["Low"],
                (
                    df["High"]
                    - previous_close
                ).abs(),
                (
                    df["Low"]
                    - previous_close
                ).abs(),
            ],
            axis=1,
        ).max(axis=1)

        return df

    def latest(
        self,
        dataframe: pd.DataFrame,
    ) -> DailyProfile:

        df = self.calculate(dataframe)

        row = df.iloc[-1]

        return DailyProfile(
            date=df.index[-1],
            open=float(row["Open"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            close=float(row["Close"]),
            range=float(row["Range"]),
            body=float(row["Body"]),
            upper_wick=float(row["UpperWick"]),
            lower_wick=float(row["LowerWick"]),
            midpoint=float(row["Midpoint"]),
            pivot=float(row["Pivot"]),
            true_range=float(row["TrueRange"]),
        )
