"""
Taylor Calculation Engine
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


SEED_DECLINE = 45.0
SEED_DECLINE_AVG = 51.0
SEED_BUYING_LOW = 12.0


@dataclass(slots=True)
class TaylorLevels:

    average_buy: float
    average_sell: float

    breakout_high: float
    breakout_low: float

    anticipated_high_from_low: float
    anticipated_high_from_high: float

    yesterday_high_minus_average: float
    yesterday_low_minus_average: float


class TaylorCalculator:

    COLUMNS = [

        "HIGH",
        "LOW",

        "Rally",
        "Rally3DayAvg",
        "TomorrowAnticipatedHighFromLow",

        "BuyingHigh",
        "BuyingHigh3DayAvg",
        "TomorrowAnticipatedHighFromHigh",

        "TodaysHigh",
        "TomorrowBreakoutHigh",
        "AverageSell",

        "Decline",
        "Decline3DayAvg",
        "YesterdayHighMinusAverage",

        "BuyingLow",
        "BuyingLow3DayAvg",
        "YesterdayLowMinusAverage",

        "TodaysLow",
        "TomorrowBreakoutLow",
        "AverageBuy",
    ]

    def __init__(self):
        pass

    def calculate(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        df = dataframe.copy()

        required = [
            "Open",
            "High",
            "Low",
            "Close",
        ]

        missing = [
            c
            for c in required
            if c not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        for column in self.COLUMNS:

            if column not in df.columns:
                df[column] = np.nan

        if df.empty:
            return df
