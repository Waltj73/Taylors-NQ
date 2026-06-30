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
        "HIGH", "LOW",
        "Rally", "Rally3DayAvg", "TomorrowAnticipatedHighFromLow",
        "BuyingHigh", "BuyingHigh3DayAvg", "TomorrowAnticipatedHighFromHigh",
        "TodaysHigh", "TomorrowBreakoutHigh", "AverageSell",
        "Decline", "Decline3DayAvg", "YesterdayHighMinusAverage",
        "BuyingLow", "BuyingLow3DayAvg", "YesterdayLowMinusAverage",
        "TodaysLow", "TomorrowBreakoutLow", "AverageBuy",
    ]

    def __init__(self):
        pass

    def calculate(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        df = dataframe.copy()

        # FORCE NUMERIC (prevents Excel-style #VALUE propagation)
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

        required = ["Open", "High", "Low", "Close"]
        missing = [c for c in required if c not in df.columns]

        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        for col in self.COLUMNS:
            if col not in df.columns:
                df[col] = 0.0

        if df.empty:
            return df

        first = df.index[0]

        # SEEDS (CRITICAL FIX)
        df.at[first, "Decline"] = SEED_DECLINE
        df.at[first, "Decline3DayAvg"] = SEED_DECLINE_AVG
        df.at[first, "BuyingLow"] = SEED_BUYING_LOW
        df.at[first, "BuyingLow3DayAvg"] = SEED_BUYING_LOW
        df.at[first, "BuyingHigh"] = 0.0
        df.at[first, "BuyingHigh3DayAvg"] = 0.0

        for i in range(1, len(df)):

            r = df.index[i]
            p = df.index[i - 1]

            O = df.at[r, "Open"]
            H = df.at[r, "High"]
            L = df.at[r, "Low"]
            C = df.at[r, "Close"]

            prevO = df.at[p, "Open"]
            prevH = df.at[p, "High"]
            prevL = df.at[p, "Low"]

            # -------------------
            # Rally
            # -------------------
            rally = H - prevL
            df.at[r, "Rally"] = rally

            r1 = df.at[df.index[i-1], "Rally"] if i >= 1 else 0
            r2 = df.at[df.index[i-2], "Rally"] if i >= 2 else 0
            rally_avg = (r1 + r2 + rally) / 3

            df.at[r, "Rally3DayAvg"] = rally_avg
            df.at[r, "TomorrowAnticipatedHighFromLow"] = L + rally_avg

            # -------------------
            # Buying High
            # -------------------
            bh = H - prevO
            df.at[r, "BuyingHigh"] = bh

            bh1 = df.at[df.index[i-1], "BuyingHigh"] if i >= 1 else 0
            bh2 = df.at[df.index[i-2], "BuyingHigh"] if i >= 2 else 0
            bh_avg = (bh1 + bh2 + bh) / 3

            df.at[r, "BuyingHigh3DayAvg"] = bh_avg
            df.at[r, "TomorrowAnticipatedHighFromHigh"] = H + bh_avg

            df.at[r, "TodaysHigh"] = H

            # -------------------
            # Pivot / Breakout
            # -------------------
            pivot = (H + L + C) / 3
            df.at[r, "TomorrowBreakoutHigh"] = (2 * pivot) - L

            df.at[r, "AverageSell"] = (
                df.at[r, "TomorrowBreakoutHigh"]
                + H
                + df.at[r, "TomorrowAnticipatedHighFromHigh"]
                + df.at[r, "TomorrowAnticipatedHighFromLow"]
            ) / 4

            df.at[r, "HIGH"] = df.at[r, "AverageSell"]

            # -------------------
            # Decline
            # -------------------
            decline = prevH - L
            df.at[r, "Decline"] = decline

            d1 = df.at[df.index[i-1], "Decline"] if i >= 1 else SEED_DECLINE
            d2 = df.at[df.index[i-2], "Decline"] if i >= 2 else SEED_DECLINE
            d_avg = (d1 + d2 + decline) / 3

            df.at[r, "Decline3DayAvg"] = d_avg
            df.at[r, "YesterdayHighMinusAverage"] = H - d_avg

            # -------------------
            # Buying Low
            # -------------------
            bl = prevL - L
            df.at[r, "BuyingLow"] = bl

            bl1 = df.at[df.index[i-1], "BuyingLow"] if i >= 1 else SEED_BUYING_LOW
            bl2 = df.at[df.index[i-2], "BuyingLow"] if i >= 2 else SEED_BUYING_LOW
            bl_avg = (bl1 + bl2 + bl) / 3

            df.at[r, "BuyingLow3DayAvg"] = bl_avg
            df.at[r, "YesterdayLowMinusAverage"] = L - bl_avg

            df.at[r, "TodaysLow"] = L
            df.at[r, "TomorrowBreakoutLow"] = (2 * pivot) - H

            df.at[r, "AverageBuy"] = (
                df.at[r, "TomorrowBreakoutLow"]
                + L
                + df.at[r, "YesterdayLowMinusAverage"]
                + df.at[r, "YesterdayHighMinusAverage"]
            ) / 4

            df.at[r, "LOW"] = df.at[r, "AverageBuy"]

        return df

    def latest(self, dataframe: pd.DataFrame) -> TaylorLevels:

        df = self.calculate(dataframe)
        row = df.iloc[-1]

        return TaylorLevels(
            average_buy=float(row["AverageBuy"]),
            average_sell=float(row["AverageSell"]),
            breakout_high=float(row["TomorrowBreakoutHigh"]),
            breakout_low=float(row["TomorrowBreakoutLow"]),
            anticipated_high_from_low=float(row["TomorrowAnticipatedHighFromLow"]),
            anticipated_high_from_high=float(row["TomorrowAnticipatedHighFromHigh"]),
            yesterday_high_minus_average=float(row["YesterdayHighMinusAverage"]),
            yesterday_low_minus_average=float(row["YesterdayLowMinusAverage"]),
        )
