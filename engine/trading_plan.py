# engine/trading_plan.py

"""
Taylor Trading Plan

Builds the actionable trading plan for the next session using the
Taylor workbook calculations.

No UI.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class TradingPlan:

    trading_date: pd.Timestamp

    average_buy: float

    average_sell: float

    breakout_high: float

    breakout_low: float

    projected_high_low: float

    projected_high_high: float

    bullish_bias: bool

    bearish_bias: bool

    long_entry: float

    short_entry: float

    long_target: float

    short_target: float

    long_stop: float

    short_stop: float


class TradingPlanBuilder:

    def build(
        self,
        calculations: pd.DataFrame,
    ) -> TradingPlan:

        row = calculations.iloc[-1]

        average_buy = float(row["AverageBuy"])
        average_sell = float(row["AverageSell"])

        breakout_high = float(
            row["TomorrowBreakoutHigh"]
        )

        breakout_low = float(
            row["TomorrowBreakoutLow"]
        )

        projected_high_low = float(
            row["TomorrowAnticipatedHighFromLow"]
        )

        projected_high_high = float(
            row["TomorrowAnticipatedHighFromHigh"]
        )

        close = float(row["Close"])

        bullish = close >= average_buy
        bearish = close <= average_sell

        #
        # Initial trading plan
        #

        long_entry = average_buy

        short_entry = average_sell

        long_target = projected_high_high

        short_target = breakout_low

        long_stop = breakout_low

        short_stop = breakout_high

        return TradingPlan(
            trading_date=calculations.index[-1],

            average_buy=average_buy,
            average_sell=average_sell,

            breakout_high=breakout_high,
            breakout_low=breakout_low,

            projected_high_low=projected_high_low,
            projected_high_high=projected_high_high,

            bullish_bias=bullish,
            bearish_bias=bearish,

            long_entry=long_entry,
            short_entry=short_entry,

            long_target=long_target,
            short_target=short_target,

            long_stop=long_stop,
            short_stop=short_stop,
        )
