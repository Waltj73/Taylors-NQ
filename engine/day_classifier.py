# engine/day_classifier.py

"""
Taylor Day Classifier

Determines the Taylor Trading Day classification using the workbook
calculations.

This module contains no UI code.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import pandas as pd


class TaylorDayType(str, Enum):

    BUY = "BUY DAY"

    SELL = "SELL DAY"

    BUY_SELL = "BUY / SELL DAY"

    SELL_BUY = "SELL / BUY DAY"

    NEUTRAL = "NEUTRAL"


@dataclass(slots=True)
class DayClassification:

    date: pd.Timestamp

    close: float

    average_buy: float

    average_sell: float

    breakout_high: float

    breakout_low: float

    day_type: TaylorDayType

    bullish_bias: bool

    bearish_bias: bool


class DayClassifier:

    def classify(
        self,
        calculations: pd.DataFrame,
    ) -> DayClassification:

        row = calculations.iloc[-1]

        close = float(row["Close"])

        avg_buy = float(row["AverageBuy"])

        avg_sell = float(row["AverageSell"])

        breakout_high = float(
            row["TomorrowBreakoutHigh"]
        )

        breakout_low = float(
            row["TomorrowBreakoutLow"]
        )

        bullish = close >= avg_buy

        bearish = close <= avg_sell

        #
        # Taylor Classification
        #

        if bullish and not bearish:

            day = TaylorDayType.BUY

        elif bearish and not bullish:

            day = TaylorDayType.SELL

        elif close >= (
            (avg_buy + avg_sell) / 2
        ):

            day = TaylorDayType.BUY_SELL

        elif close < (
            (avg_buy + avg_sell) / 2
        ):

            day = TaylorDayType.SELL_BUY

        else:

            day = TaylorDayType.NEUTRAL

        return DayClassification(
            date=calculations.index[-1],
            close=close,
            average_buy=avg_buy,
            average_sell=avg_sell,
            breakout_high=breakout_high,
            breakout_low=breakout_low,
            day_type=day,
            bullish_bias=bullish,
            bearish_bias=bearish,
        )
