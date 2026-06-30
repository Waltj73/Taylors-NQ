from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
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
        "Rally", "Rally3DayAvg", "TomorrowAnticipatedHighFromLow",
        "BuyingHigh", "BuyingHigh3DayAvg", "TomorrowAnticipatedHighFromHigh",
        "Decline", "Decline3DayAvg", "YesterdayHighMinusAverage",
        "BuyingLow", "BuyingLow3DayAvg", "YesterdayLowMinusAverage",
        "TomorrowBreakoutHigh", "TomorrowBreakoutLow",
        "AverageBuy", "AverageSell"
    ]

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

        required = ["Open", "High", "Low", "Close"]
        if any(c not in df.columns for c in required):
            raise ValueError("Missing OHLC data")

        for c in self.COLUMNS:
            if c not in df.columns:
                df[c] = 0.0

        if len(df) < 5:
            return df

        for i in range(3, len(df)):

            r = df.index[i]
            p1 = df.index[i - 1]
            p2 = df.index[i - 2]
            p3 = df.index[i - 3]

            H = df.at[r, "High"]
            L = df.at[r, "Low"]
            C = df.at[r, "Close"]

            prevC = df.at[p1, "Close"]
            prevH = df.at[p1, "High"]
            prevL = df.at[p1, "Low"]

            # ----------------------
            # Rally
            # ----------------------
            rally = H - prevL
            df.at[r, "Rally"] = rally

            df.at[r, "Rally3DayAvg"] = (
                df.at[p1, "Rally"]
                + df.at[p2, "Rally"]
                + rally
            ) / 3

            df.at[r, "TomorrowAnticipatedHighFromLow"] = L + df.at[r, "Rally3DayAvg"]

            # ----------------------
            # Buying High (CLOSE-BASED)
            # ----------------------
            bh = H - prevC
            df.at[r, "BuyingHigh"] = bh

            df.at[r, "BuyingHigh3DayAvg"] = (
                df.at[p1, "BuyingHigh"]
                + df.at[p2, "BuyingHigh"]
                + bh
            ) / 3

            df.at[r, "TomorrowAnticipatedHighFromHigh"] = H + df.at[r, "BuyingHigh3DayAvg"]

            # ----------------------
            # Decline
            # ----------------------
            decline = prevH - L
            df.at[r, "Decline"] = decline

            df.at[r, "Decline3DayAvg"] = (
                df.at[p1, "Decline"]
                + df.at[p2, "Decline"]
                + decline
            ) / 3

            df.at[r, "YesterdayHighMinusAverage"] = H - df.at[r, "Decline3DayAvg"]

            # ----------------------
            # Buying Low (CLOSE-BASED)
            # ----------------------
            bl = prevC - L
            df.at[r, "BuyingLow"] = bl

            df.at[r, "BuyingLow3DayAvg"] = (
                df.at[p1, "BuyingLow"]
                + df.at[p2, "BuyingLow"]
                + bl
            ) / 3

            df.at[r, "YesterdayLowMinusAverage"] = L - df.at[r, "BuyingLow3DayAvg"]

            # ----------------------
            # Pivot + Breakouts
            # ----------------------
            pivot = (H + L + C) / 3

            df.at[r, "TomorrowBreakoutHigh"] = (2 * pivot) - L
            df.at[r, "TomorrowBreakoutLow"] = (2 * pivot) - H

            # ----------------------
            # Final Levels
            # ----------------------
            df.at[r, "AverageSell"] = (
                df.at[r, "TomorrowBreakoutHigh"]
                + H
                + df.at[r, "TomorrowAnticipatedHighFromHigh"]
                + df.at[r, "TomorrowAnticipatedHighFromLow"]
            ) / 4

            df.at[r, "AverageBuy"] = (
                df.at[r, "TomorrowBreakoutLow"]
                + L
                + df.at[r, "YesterdayLowMinusAverage"]
                + df.at[r, "YesterdayHighMinusAverage"]
            ) / 4

        return df

    def latest(self, df: pd.DataFrame) -> TaylorLevels:

        d = self.calculate(df)
        r = d.iloc[-1]

        return TaylorLevels(
            average_buy=r["AverageBuy"],
            average_sell=r["AverageSell"],
            breakout_high=r["TomorrowBreakoutHigh"],
            breakout_low=r["TomorrowBreakoutLow"],
            anticipated_high_from_low=r["TomorrowAnticipatedHighFromLow"],
            anticipated_high_from_high=r["TomorrowAnticipatedHighFromHigh"],
            yesterday_high_minus_average=r["YesterdayHighMinusAverage"],
            yesterday_low_minus_average=r["YesterdayLowMinusAverage"],
        )
