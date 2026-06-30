# engine/formulas.py

"""
Taylor Formula Library

Centralized formula implementations used throughout the application.

Every calculation should call these functions rather than duplicating
math throughout the codebase.

These formulas mirror the Taylor workbook.
"""

from __future__ import annotations

import pandas as pd


class TaylorFormula:

    @staticmethod
    def rally(
        high: pd.Series,
        previous_low: pd.Series,
    ) -> pd.Series:

        return high - previous_low

    @staticmethod
    def decline(
        previous_high: pd.Series,
        low: pd.Series,
    ) -> pd.Series:

        return previous_high - low

    @staticmethod
    def buying_high(
        high: pd.Series,
        previous_open: pd.Series,
    ) -> pd.Series:

        return high - previous_open

    @staticmethod
    def buying_low(
        previous_low: pd.Series,
        open_price: pd.Series,
    ) -> pd.Series:

        return previous_low - open_price

    @staticmethod
    def average3(
        values: pd.Series,
    ) -> pd.Series:

        return (
            values
            .rolling(3)
            .mean()
        )

    @staticmethod
    def anticipated_high_from_low(
        low: pd.Series,
        rally_average: pd.Series,
    ) -> pd.Series:

        return low + rally_average

    @staticmethod
    def anticipated_high_from_high(
        high: pd.Series,
        buying_high_average: pd.Series,
    ) -> pd.Series:

        return high + buying_high_average

    @staticmethod
    def yesterday_high_minus_average(
        high: pd.Series,
        decline_average: pd.Series,
    ) -> pd.Series:

        return high - decline_average

    @staticmethod
    def yesterday_low_minus_average(
        low: pd.Series,
        buying_low_average: pd.Series,
    ) -> pd.Series:

        return low - buying_low_average

    @staticmethod
    def pivot_point(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
    ) -> pd.Series:

        return (
            high
            + low
            + close
        ) / 3

    @staticmethod
    def breakout_high(
        pivot: pd.Series,
        low: pd.Series,
    ) -> pd.Series:

        return (2 * pivot) - low

    @staticmethod
    def breakout_low(
        pivot: pd.Series,
        high: pd.Series,
    ) -> pd.Series:

        return (2 * pivot) - high

    @staticmethod
    def average_sell(
        breakout_high: pd.Series,
        today_high: pd.Series,
        anticipated_high_high: pd.Series,
        anticipated_high_low: pd.Series,
    ) -> pd.Series:

        return pd.concat(
            [
                breakout_high,
                today_high,
                anticipated_high_high,
                anticipated_high_low,
            ],
            axis=1,
        ).mean(axis=1)

    @staticmethod
    def average_buy(
        breakout_low: pd.Series,
        today_low: pd.Series,
        yesterday_low_average: pd.Series,
        yesterday_high_average: pd.Series,
    ) -> pd.Series:

        return pd.concat(
            [
                breakout_low,
                today_low,
                yesterday_low_average,
                yesterday_high_average,
            ],
            axis=1,
        ).mean(axis=1)
