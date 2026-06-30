# engine/workbook_calculator.py

"""
Taylor Workbook Calculator

This module reproduces the formulas in the NQ worksheet exactly
(column-for-column) so the application can be verified against
the Excel workbook.

The formulas below are copied directly from Taylors NQ.xlsx.
"""

from __future__ import annotations

import pandas as pd


class WorkbookCalculator:

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        out = df.copy()

        #
        # Excel Columns
        #
        # B  Todays Open
        # C  Todays High
        # D  Todays Low
        # E  Todays Close
        #

        #
        # F HIGH
        # =U
        #

        #
        # G LOW
        # =AI
        #

        #
        # I Rally
        # = Today's High - Yesterday's Low
        #

        out["Rally"] = (
            out["High"]
            - out["Low"].shift(1)
        )

        #
        # J
        # =SUM(last 3 Rally values)/3
        #

        out["Rally3DayAvg"] = (
            out["Rally"]
            .rolling(3)
            .mean()
        )

        #
        # K
        # = Today's Low + Rally Avg
        #

        out["TomorrowAnticipatedHighFromLow"] = (
            out["Low"]
            + out["Rally3DayAvg"]
        )

        #
        # M
        # = Today's High - Yesterday's Open
        #

        out["BuyingHigh"] = (
            out["High"]
            - out["Open"].shift(1)
        )

        #
        # N
        # 3 Day Avg
        #

        out["BuyingHigh3DayAvg"] = (
            out["BuyingHigh"]
            .rolling(3)
            .mean()
        )

        #
        # O
        # = Today's High + Avg
        #

        out["TomorrowAnticipatedHighFromHigh"] = (
            out["High"]
            + out["BuyingHigh3DayAvg"]
        )

        #
        # Q
        # Today's High
        #

        out["TodaysHigh"] = out["High"]

        #
        # S
        # Pivot Breakout High
        # =2*PP-Low
        #

        pp = (
            out["High"]
            + out["Low"]
            + out["Close"]
        ) / 3

        out["TomorrowBreakoutHigh"] = (
            (2 * pp)
            - out["Low"]
        )

        #
        # U
        # Average Sell
        #

        out["AverageSell"] = (
            out[
                [
                    "TomorrowBreakoutHigh",
                    "TodaysHigh",
                    "TomorrowAnticipatedHighFromHigh",
                    "TomorrowAnticipatedHighFromLow",
                ]
            ]
            .mean(axis=1)
        )

        #
        # W
        # Decline
        # = Yesterday High - Today's Low
        #

        out["Decline"] = (
            out["High"].shift(1)
            - out["Low"]
        )

        #
        # X
        # 3 Day Avg
        #

        out["Decline3DayAvg"] = (
            out["Decline"]
            .rolling(3)
            .mean()
        )

        #
        # Y
        # Yesterday High - Avg
        #

        out["YesterdayHighMinusAverage"] = (
            out["High"]
            - out["Decline3DayAvg"]
        )

        #
        # AA
        # Buying Low
        # = Yesterday Low - Today's Open
        #

        out["BuyingLow"] = (
            out["Low"].shift(1)
            - out["Open"]
        )

        #
        # AB
        # 3 Day Avg
        #

        out["BuyingLow3DayAvg"] = (
            out["BuyingLow"]
            .rolling(3)
            .mean()
        )

        #
        # AC
        # Yesterday Low - Avg
        #

        out["YesterdayLowMinusAverage"] = (
            out["Low"]
            - out["BuyingLow3DayAvg"]
        )

        #
        # AE
        # Today's Low
        #

        out["TodaysLow"] = out["Low"]

        #
        # AG
        # Pivot Breakout Low
        # =2*PP-High
        #

        out["TomorrowBreakoutLow"] = (
            (2 * pp)
            - out["High"]
        )

        #
        # AI
        # Average Buy
        #

        out["AverageBuy"] = (
            out[
                [
                    "TomorrowBreakoutLow",
                    "TodaysLow",
                    "YesterdayLowMinusAverage",
                    "YesterdayHighMinusAverage",
                ]
            ]
            .mean(axis=1)
        )

        #
        # Workbook aliases
        #

        out["HIGH"] = out["AverageSell"]
        out["LOW"] = out["AverageBuy"]

        return out
