# engine/workbook_adapter.py

"""
Taylor Workbook Adapter

Maps Yahoo Finance market data into the exact worksheet layout expected
by Taylors NQ.xlsx.

This is the bridge between external market data and the workbook.

Responsibilities

    Yahoo Finance
            │
            ▼
    Normalize OHLC
            │
            ▼
    Populate workbook input columns
            │
            ▼
    Return workbook-compatible DataFrame

No calculations occur here.
"""

from __future__ import annotations

import pandas as pd


class WorkbookAdapter:

    #
    # Workbook input columns.
    #
    # These correspond to the workbook's source columns and are the
    # only columns populated directly from Yahoo Finance.
    #
    COLUMN_MAP = {
        "Open": "Open",
        "High": "High",
        "Low": "Low",
        "Close": "Close",
    }

    def adapt(
        self,
        yahoo: pd.DataFrame,
    ) -> pd.DataFrame:

        if yahoo.empty:
            return pd.DataFrame()

        workbook = pd.DataFrame(index=yahoo.index)

        #
        # Populate workbook inputs.
        #

        for yahoo_column, workbook_column in self.COLUMN_MAP.items():

            if yahoo_column not in yahoo.columns:

                raise KeyError(
                    f"Missing Yahoo column '{yahoo_column}'."
                )

            workbook[workbook_column] = yahoo[
                yahoo_column
            ].astype(float)

        #
        # Preserve volume if available.
        #

        if "Volume" in yahoo.columns:

            workbook["Volume"] = yahoo[
                "Volume"
            ].astype(float)

        #
        # Create placeholder workbook columns.
        # These are later filled by the workbook execution engine.
        #

        workbook["Rally"] = pd.NA
        workbook["Rally3DayAvg"] = pd.NA
        workbook["TomorrowAnticipatedHighFromLow"] = pd.NA

        workbook["BuyingHigh"] = pd.NA
        workbook["BuyingHigh3DayAvg"] = pd.NA
        workbook["TomorrowAnticipatedHighFromHigh"] = pd.NA

        workbook["TodaysHigh"] = pd.NA
        workbook["TomorrowBreakoutHigh"] = pd.NA
        workbook["AverageSell"] = pd.NA

        workbook["Decline"] = pd.NA
        workbook["Decline3DayAvg"] = pd.NA
        workbook["YesterdayHighMinusAverage"] = pd.NA

        workbook["BuyingLow"] = pd.NA
        workbook["BuyingLow3DayAvg"] = pd.NA
        workbook["YesterdayLowMinusAverage"] = pd.NA

        workbook["TodaysLow"] = pd.NA
        workbook["TomorrowBreakoutLow"] = pd.NA
        workbook["AverageBuy"] = pd.NA

        #
        # Workbook aliases
        #

        workbook["HIGH"] = pd.NA
        workbook["LOW"] = pd.NA

        return workbook

    @staticmethod
    def workbook_columns() -> list[str]:

        return [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
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
            "HIGH",
            "LOW",
        ]
