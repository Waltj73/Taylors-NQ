# engine/calculations.py

"""
Taylor Calculation Engine

This module reproduces the Taylor workbook calculations.

Workbook Source
---------------
Sheet : NQ

Rows
----
3   Headers
4   Seed Row
5+  Calculated Rows

Columns
-------

A   Date
B   Open
C   High
D   Low
E   Close

F   HIGH (Average Sell Alias)
G   LOW  (Average Buy Alias)

I   Rally
J   Rally 3-Day Average
K   Tomorrow Anticipated High (Low + Avg)

M   Buying High
N   Buying High 3-Day Average
O   Tomorrow Anticipated High (High + Avg)

Q   Today's High
S   Breakout High
U   Average Sell

W   Decline
X   Decline 3-Day Average
Y   Yesterday High Minus Avg

AA  Buying Low
AB  Buying Low 3-Day Average
AC  Yesterday Low Minus Avg

AE  Today's Low
AG  Breakout Low
AI  Average Buy

The implementation intentionally mirrors Excel row-by-row instead
of using rolling windows so the output matches the workbook exactly.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


# ----------------------------------------------------------------------
# Seed values taken directly from workbook row 4
# ----------------------------------------------------------------------

SEED_W = 45.0
SEED_X = 51.0
SEED_AA = 12.0


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

    def __init__(self):

        pass

    # ---------------------------------------------------------------

    def calculate(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        df = dataframe.copy()

        #
        # Ensure required columns exist.
        #

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

        #
        # Allocate workbook columns.
        #

        workbook_columns = [

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

        for column in workbook_columns:

            if column not in df.columns:

                df[column] = np.nan

        #
        # ------------------------------------------------------------------
        # Seed rows
        #
        # Excel begins calculations using row 4.
        #
        # DataFrame row 0 represents workbook row 4.
        # DataFrame row 1 represents workbook row 5.
        # ------------------------------------------------------------------
        #

        if len(df) == 0:

            return df

        #
        # Workbook constants.
        #

        df.at[df.index[0], "Decline"] = SEED_W

        df.at[df.index[0], "Decline3DayAvg"] = SEED_X

        df.at[df.index[0], "BuyingLow"] = SEED_AA

        #
        # Workbook formula:
        #
        # M4 = C4 - B3
        #
        # We cannot reproduce B3 because it precedes the imported
        # history. The workbook uses it only as a seed.
        #
        # Therefore we initialize BuyingHigh to NaN and allow row 5
        # to begin normal calculations.
        #

        df.at[df.index[0], "BuyingHigh"] = np.nan

        #
        # Alias columns
        #

        df.at[df.index[0], "HIGH"] = np.nan
        df.at[df.index[0], "LOW"] = np.nan

        #
        # ==============================================================
        # Begin workbook calculations.
        #
        # Workbook Row 5 == DataFrame Row 1
        # ==============================================================
        #

        for row in range(1, len(df)):

            previous = row - 1

            open_price = float(
                df.iloc[row]["Open"]
            )

            high = float(
                df.iloc[row]["High"]
            )

            low = float(
                df.iloc[row]["Low"]
            )

            close = float(
                df.iloc[row]["Close"]
            )

            previous_open = float(
                df.iloc[previous]["Open"]
            )

            previous_high = float(
                df.iloc[previous]["High"]
            )

            previous_low = float(
                df.iloc[previous]["Low"]
            )

            #
            # Column I
            #
            # = High - Previous Low
            #

            rally = (
                high
                - previous_low
            )

            df.iat[
                row,
                df.columns.get_loc("Rally")
            ] = rally

            #
            # Remaining workbook columns continue...
            #
                        #
            # ----------------------------------------------------------
            # Column J
            #
            # =SUM(I[r-2],I[r-1],I[r])/3
            # ----------------------------------------------------------
            #

            def _avg3(column: str) -> float:

                values = []

                for offset in (-2, -1, 0):

                    idx = row + offset

                    if idx < 0:
                        continue

                    value = df.iat[
                        idx,
                        df.columns.get_loc(column),
                    ]

                    if pd.notna(value):
                        values.append(float(value))

                if not values:
                    return np.nan

                #
                # Excel always divides by 3.
                # Missing seed values are treated as zero.
                #

                while len(values) < 3:
                    values.insert(0, 0.0)

                return sum(values) / 3.0

            rally_avg = _avg3(
                "Rally"
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "Rally3DayAvg"
                ),
            ] = rally_avg

            #
            # ----------------------------------------------------------
            # Column K
            #
            # =Low + Rally Average
            # ----------------------------------------------------------
            #

            anticipated_high_low = (
                low
                + rally_avg
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "TomorrowAnticipatedHighFromLow"
                ),
            ] = anticipated_high_low

            #
            # ----------------------------------------------------------
            # Column M
            #
            # =High - Previous Open
            # ----------------------------------------------------------
            #

            buying_high = (
                high
                - previous_open
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "BuyingHigh"
                ),
            ] = buying_high

            #
            # ----------------------------------------------------------
            # Column N
            #
            # =SUM(M[r-2]:M[r])/3
            # ----------------------------------------------------------
            #

            buying_high_avg = _avg3(
                "BuyingHigh"
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "BuyingHigh3DayAvg"
                ),
            ] = buying_high_avg

            #
            # ----------------------------------------------------------
            # Column O
            #
            # =High + Buying High Average
            # ----------------------------------------------------------
            #

            anticipated_high_high = (
                high
                + buying_high_avg
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "TomorrowAnticipatedHighFromHigh"
                ),
            ] = anticipated_high_high

            #
            # ----------------------------------------------------------
            # Column Q
            #
            # =Today's High
            # ----------------------------------------------------------
            #

            df.iat[
                row,
                df.columns.get_loc(
                    "TodaysHigh"
                ),
            ] = high

            #
            # ----------------------------------------------------------
            # Pivot Point
            #
            # =(High+Low+Close)/3
            # ----------------------------------------------------------
            #

            pivot = (
                high
                + low
                + close
            ) / 3.0

            #
            # ----------------------------------------------------------
            # Column S
            #
            # =2*Pivot-Low
            # ----------------------------------------------------------
            #

            breakout_high = (
                (2.0 * pivot)
                - low
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "TomorrowBreakoutHigh"
                ),
            ] = breakout_high

            #
            # ----------------------------------------------------------
            # Column U
            #
            # =AVERAGE(S,Q,O,K)
            # ----------------------------------------------------------
            #

            average_sell = (
                breakout_high
                + high
                + anticipated_high_high
                + anticipated_high_low
            ) / 4.0

            df.iat[
                row,
                df.columns.get_loc(
                    "AverageSell"
                ),
            ] = average_sell

            #
            # Excel alias
            #
            # F = U
            #

            df.iat[
                row,
                df.columns.get_loc(
                    "HIGH"
                ),
            ] = average_sell

            #
            # Continue with Column W...
            #
                        #
            # ----------------------------------------------------------
            # Column W
            #
            # =Previous High - Current Low
            # ----------------------------------------------------------
            #

            decline = (
                previous_high
                - low
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "Decline"
                ),
            ] = decline

            #
            # ----------------------------------------------------------
            # Column X
            #
            # =SUM(W[r-2]:W[r])/3
            # ----------------------------------------------------------
            #

            decline_avg = _avg3(
                "Decline"
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "Decline3DayAvg"
                ),
            ] = decline_avg

            #
            # ----------------------------------------------------------
            # Column Y
            #
            # =High - Decline Average
            # ----------------------------------------------------------
            #

            yesterday_high_minus_average = (
                high
                - decline_avg
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "YesterdayHighMinusAverage"
                ),
            ] = yesterday_high_minus_average

            #
            # ----------------------------------------------------------
            # Column AA
            #
            # =Previous Low - Current Low
            #
            # Excel:
            #
            # AA5 = D4 - D5
            # ----------------------------------------------------------
            #

            buying_low = (
                previous_low
                - low
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "BuyingLow"
                ),
            ] = buying_low

            #
            # ----------------------------------------------------------
            # Column AB
            #
            # =SUM(AA[r-2]:AA[r])/3
            # ----------------------------------------------------------
            #

            buying_low_avg = _avg3(
                "BuyingLow"
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "BuyingLow3DayAvg"
                ),
            ] = buying_low_avg

            #
            # ----------------------------------------------------------
            # Column AC
            #
            # =Low - Buying Low Average
            # ----------------------------------------------------------
            #

            yesterday_low_minus_average = (
                low
                - buying_low_avg
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "YesterdayLowMinusAverage"
                ),
            ] = yesterday_low_minus_average

            #
            # ----------------------------------------------------------
            # Column AE
            #
            # =Today's Low
            # ----------------------------------------------------------
            #

            df.iat[
                row,
                df.columns.get_loc(
                    "TodaysLow"
                ),
            ] = low

            #
            # ----------------------------------------------------------
            # Column AG
            #
            # =2*Pivot-High
            # ----------------------------------------------------------
            #

            breakout_low = (
                (2.0 * pivot)
                - high
            )

            df.iat[
                row,
                df.columns.get_loc(
                    "TomorrowBreakoutLow"
                ),
            ] = breakout_low

            #
            # ----------------------------------------------------------
            # Column AI
            #
            # =AVERAGE(AG,AE,AC,Y)
            # ----------------------------------------------------------
            #

            average_buy = (
                breakout_low
                + low
                + yesterday_low_minus_average
                + yesterday_high_minus_average
            ) / 4.0

            df.iat[
                row,
                df.columns.get_loc(
                    "AverageBuy"
                ),
            ] = average_buy

            #
            # Excel alias
            #
            # G = AI
            #

            df.iat[
                row,
                df.columns.get_loc(
                    "LOW"
                ),
            ] = average_buy

        #
        # ==============================================================
        # Workbook complete
        # ==============================================================
        #

        return df

    # ------------------------------------------------------------------
    # Latest calculated Taylor levels
    # ------------------------------------------------------------------

    def latest(
        self,
        dataframe: pd.DataFrame,
    ) -> TaylorLevels:

        calculated = self.calculate(
            dataframe
        )

        row = calculated.iloc[-1]

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
                row[
                    "TomorrowAnticipatedHighFromLow"
                ]
            ),

            anticipated_high_from_high=float(
                row[
                    "TomorrowAnticipatedHighFromHigh"
                ]
            ),

            yesterday_high_minus_average=float(
                row[
                    "YesterdayHighMinusAverage"
                ]
            ),

            yesterday_low_minus_average=float(
                row[
                    "YesterdayLowMinusAverage"
                ]
            ),
        )
        
