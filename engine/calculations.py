"""
Taylor Calculation Engine

Rewritten directly from the Taylor workbook.

The workbook is the source of truth.

Every calculation below corresponds to an Excel formula.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


# ----------------------------------------------------------------------
# Workbook seed values (Workbook Row 4)
# ----------------------------------------------------------------------

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

    WORKBOOK_COLUMNS = [

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

        for column in self.WORKBOOK_COLUMNS:

            if column not in df.columns:
                df[column] = np.nan

        if df.empty:
            return df

        #
        # Workbook Row 4
        #

        first = df.index[0]

        df.at[first, "Decline"] = SEED_DECLINE
        df.at[first, "Decline3DayAvg"] = SEED_DECLINE_AVG
        df.at[first, "BuyingLow"] = SEED_BUYING_LOW

        #
        # Everything else is calculated
        # beginning with Workbook Row 5.
        #
        """
Taylor Calculation Engine

Rewritten directly from the Taylor workbook.

The workbook is the source of truth.

Every calculation below corresponds to an Excel formula.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


# ----------------------------------------------------------------------
# Workbook seed values (Workbook Row 4)
# ----------------------------------------------------------------------

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

    WORKBOOK_COLUMNS = [

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

        for column in self.WORKBOOK_COLUMNS:

            if column not in df.columns:
                df[column] = np.nan

        if df.empty:
            return df

        #
        # Workbook Row 4
        #

        first = df.index[0]

        df.at[first, "Decline"] = SEED_DECLINE
        df.at[first, "Decline3DayAvg"] = SEED_DECLINE_AVG
        df.at[first, "BuyingLow"] = SEED_BUYING_LOW

        #
        # Everything else is calculated
        # beginning with Workbook Row 5.
        #
                    # =====================================================
            # S
            # Tomorrow Breakout High
            # =2*((H+L+C)/3)-L
            # =====================================================

            pivot = (
                H +
                L +
                C
            ) / 3.0

            df.at[r, "TomorrowBreakoutHigh"] = (
                (2.0 * pivot)
                - L
            )

            # =====================================================
            # U
            # Average Sell
            # =AVERAGE(S,Q,O,K)
            # =====================================================

            df.at[r, "AverageSell"] = (

                df.at[r, "TomorrowBreakoutHigh"]

                + df.at[r, "TodaysHigh"]

                + df.at[r, "TomorrowAnticipatedHighFromHigh"]

                + df.at[r, "TomorrowAnticipatedHighFromLow"]

            ) / 4.0

            #
            # Workbook Alias
            #

            df.at[r, "HIGH"] = df.at[r, "AverageSell"]

            # =====================================================
            # W
            # Decline
            # =Previous High - Current Low
            # =====================================================

            df.at[r, "Decline"] = (

                prevH

                - L

            )

            # =====================================================
            # X
            # =SUM(W[r-2]:W[r])/3
            # =====================================================

            if row == 1:

                w1 = 0.0
                w2 = SEED_DECLINE

            elif row == 2:

                w1 = SEED_DECLINE
                w2 = float(
                    df.at[
                        df.index[row-1],
                        "Decline",
                    ]
                )

            else:

                w1 = float(
                    df.at[
                        df.index[row-2],
                        "Decline",
                    ]
                )

                w2 = float(
                    df.at[
                        df.index[row-1],
                        "Decline",
                    ]
                )

            df.at[r, "Decline3DayAvg"] = (

                w1

                + w2

                + df.at[r, "Decline"]

            ) / 3.0

            # =====================================================
            # Y
            # =====================================================

            df.at[r, "YesterdayHighMinusAverage"] = (

                H

                - df.at[r, "Decline3DayAvg"]

            )
                    # =====================================================
            # AA
            # Buying Low
            # =Previous Low - Current Low
            # =====================================================

            df.at[r, "BuyingLow"] = (
                prevL
                - L
            )

            # =====================================================
            # AB
            # =SUM(AA[r-2]:AA[r])/3
            # =====================================================

            if row == 1:

                aa1 = 0.0
                aa2 = SEED_BUYING_LOW

            elif row == 2:

                aa1 = SEED_BUYING_LOW
                aa2 = float(
                    df.at[
                        df.index[row - 1],
                        "BuyingLow",
                    ]
                )

            else:

                aa1 = float(
                    df.at[
                        df.index[row - 2],
                        "BuyingLow",
                    ]
                )

                aa2 = float(
                    df.at[
                        df.index[row - 1],
                        "BuyingLow",
                    ]
                )

            df.at[r, "BuyingLow3DayAvg"] = (
                aa1
                + aa2
                + df.at[r, "BuyingLow"]
            ) / 3.0

            # =====================================================
            # AC
            # Yesterday Low Minus Average
            # =====================================================

            df.at[r, "YesterdayLowMinusAverage"] = (
                L
                - df.at[r, "BuyingLow3DayAvg"]
            )

            # =====================================================
            # AE
            # Today's Low
            # =====================================================

            df.at[r, "TodaysLow"] = L

            # =====================================================
            # AG
            # Tomorrow Breakout Low
            # =====================================================

            df.at[r, "TomorrowBreakoutLow"] = (
                (2.0 * pivot)
                - H
            )

            # =====================================================
            # AI
            # Average Buy
            # =====================================================

            df.at[r, "AverageBuy"] = (

                df.at[r, "TomorrowBreakoutLow"]

                + df.at[r, "TodaysLow"]

                + df.at[r, "YesterdayLowMinusAverage"]

                + df.at[r, "YesterdayHighMinusAverage"]

            ) / 4.0

            #
            # Workbook Alias
            #

            df.at[r, "LOW"] = df.at[r, "AverageBuy"]

        return df
            # ------------------------------------------------------------------
    # Latest Taylor Levels
    # ------------------------------------------------------------------

    def latest(
        self,
        dataframe: pd.DataFrame,
    ) -> TaylorLevels:

        df = self.calculate(dataframe)

        row = df.iloc[-1]

        return TaylorLevels(

            average_buy=float(
                row["AverageBuy"]
            ),

            average_sell=float(
                row["AverageSell"]
            ),

            breakout_high=float(
                row["TomorrowBreakoutHigh"]
            ),

            breakout_low=float(
                row["TomorrowBreakoutLow"]
            ),

            anticipated_high_from_low=float(
                row["TomorrowAnticipatedHighFromLow"]
            ),

            anticipated_high_from_high=float(
                row["TomorrowAnticipatedHighFromHigh"]
            ),

            yesterday_high_minus_average=float(
                row["YesterdayHighMinusAverage"]
            ),

            yesterday_low_minus_average=float(
                row["YesterdayLowMinusAverage"]
            ),
        )
