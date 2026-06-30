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

        first = df.index[0]

        df.at[first, "Decline"] = SEED_DECLINE
        df.at[first, "Decline3DayAvg"] = SEED_DECLINE_AVG
        df.at[first, "BuyingLow"] = SEED_BUYING_LOW
                #
        # Workbook calculations
        #

        for row in range(1, len(df)):

            r = df.index[row]
            p = df.index[row - 1]

            O = float(df.at[r, "Open"])
            H = float(df.at[r, "High"])
            L = float(df.at[r, "Low"])
            C = float(df.at[r, "Close"])

            prevO = float(df.at[p, "Open"])
            prevH = float(df.at[p, "High"])
            prevL = float(df.at[p, "Low"])

            #
            # Rally
            #

            rally = H - prevL

            df.at[r, "Rally"] = rally

            #
            # Rally Average
            #

            if row == 1:

                rally_avg = rally / 3.0

            elif row == 2:

                rally_avg = (
                    float(
                        df.at[
                            df.index[row - 1],
                            "Rally",
                        ]
                    )
                    + rally
                ) / 3.0

            else:

                rally_avg = (

                    float(
                        df.at[
                            df.index[row - 2],
                            "Rally",
                        ]
                    )

                    + float(
                        df.at[
                            df.index[row - 1],
                            "Rally",
                        ]
                    )

                    + rally

                ) / 3.0

            df.at[r, "Rally3DayAvg"] = rally_avg

            #
            # Tomorrow Anticipated High From Low
            #

            df.at[
                r,
                "TomorrowAnticipatedHighFromLow",
            ] = (

                L

                + rally_avg

            )

            #
            # Buying High
            #

            buying_high = H - prevO

            df.at[
                r,
                "BuyingHigh",
            ] = buying_high

            #
            # Buying High Average
            #

            if row == 1:

                buying_high_avg = buying_high / 3.0

            elif row == 2:

                buying_high_avg = (

                    float(
                        df.at[
                            df.index[row - 1],
                            "BuyingHigh",
                        ]
                    )

                    + buying_high

                ) / 3.0

            else:

                buying_high_avg = (

                    float(
                        df.at[
                            df.index[row - 2],
                            "BuyingHigh",
                        ]
                    )

                    + float(
                        df.at[
                            df.index[row - 1],
                            "BuyingHigh",
                        ]
                    )

                    + buying_high

                ) / 3.0

            df.at[
                r,
                "BuyingHigh3DayAvg",
            ] = buying_high_avg

            #
            # Tomorrow Anticipated High From High
            #

            df.at[
                r,
                "TomorrowAnticipatedHighFromHigh",
            ] = (

                H

                + buying_high_avg

            )

            #
            # Today's High
            #

            df.at[
                r,
                "TodaysHigh",
            ] = H
                        #
            # Pivot
            #

            pivot = (
                H +
                L +
                C
            ) / 3.0

            #
            # Tomorrow Breakout High
            #

            breakout_high = (
                (2.0 * pivot)
                - L
            )

            df.at[
                r,
                "TomorrowBreakoutHigh",
            ] = breakout_high

            #
            # Average Sell
            #

            average_sell = (

                breakout_high

                + H

                + df.at[
                    r,
                    "TomorrowAnticipatedHighFromHigh",
                ]

                + df.at[
                    r,
                    "TomorrowAnticipatedHighFromLow",
                ]

            ) / 4.0

            df.at[
                r,
                "AverageSell",
            ] = average_sell

            #
            # Workbook HIGH
            #

            df.at[
                r,
                "HIGH",
            ] = average_sell

            #
            # Decline
            #

            decline = (
                prevH
                - L
            )

            df.at[
                r,
                "Decline",
            ] = decline

            #
            # Decline Average
            #

            if row == 1:

                decline_avg = (
                    SEED_DECLINE
                    + decline
                ) / 3.0

            elif row == 2:

                decline_avg = (

                    SEED_DECLINE

                    + float(
                        df.at[
                            df.index[row - 1],
                            "Decline",
                        ]
                    )

                    + decline

                ) / 3.0

            else:

                decline_avg = (

                    float(
                        df.at[
                            df.index[row - 2],
                            "Decline",
                        ]
                    )

                    + float(
                        df.at[
                            df.index[row - 1],
                            "Decline",
                        ]
                    )

                    + decline

                ) / 3.0

            df.at[
                r,
                "Decline3DayAvg",
            ] = decline_avg

            #
            # Yesterday High Minus Average
            #

            df.at[
                r,
                "YesterdayHighMinusAverage",
            ] = (

                H

                - decline_avg

            )
                        #
            # Buying Low
            #

            buying_low = (
                prevL
                - L
            )

            df.at[
                r,
                "BuyingLow",
            ] = buying_low

            #
            # Buying Low Average
            #

            if row == 1:

                buying_low_avg = (
                    SEED_BUYING_LOW
                    + buying_low
                ) / 3.0

            elif row == 2:

                buying_low_avg = (

                    SEED_BUYING_LOW

                    + float(
                        df.at[
                            df.index[row - 1],
                            "BuyingLow",
                        ]
                    )

                    + buying_low

                ) / 3.0

            else:

                buying_low_avg = (

                    float(
                        df.at[
                            df.index[row - 2],
                            "BuyingLow",
                        ]
                    )

                    + float(
                        df.at[
                            df.index[row - 1],
                            "BuyingLow",
                        ]
                    )

                    + buying_low

                ) / 3.0

            df.at[
                r,
                "BuyingLow3DayAvg",
            ] = buying_low_avg

            #
            # Yesterday Low Minus Average
            #

            df.at[
                r,
                "YesterdayLowMinusAverage",
            ] = (
                L
                - buying_low_avg
            )

            #
            # Today's Low
            #

            df.at[
                r,
                "TodaysLow",
            ] = L

            #
            # Tomorrow Breakout Low
            #

            breakout_low = (
                (2.0 * pivot)
                - H
            )

            df.at[
                r,
                "TomorrowBreakoutLow",
            ] = breakout_low

            #
            # Average Buy
            #

            average_buy = (

                breakout_low

                + L

                + df.at[
                    r,
                    "YesterdayLowMinusAverage",
                ]

                + df.at[
                    r,
                    "YesterdayHighMinusAverage",
                ]

            ) / 4.0

            df.at[
                r,
                "AverageBuy",
            ] = average_buy

            #
            # Workbook LOW
            #

            df.at[
                r,
                "LOW",
            ] = average_buy
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

        return df
        
