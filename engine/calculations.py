from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


# =========================================================
# Seeds (match workbook initialization behavior)
# =========================================================

SEED_DECLINE = 45.0
SEED_DECLINE_AVG = 51.0
SEED_BUYING_LOW = 12.0


# =========================================================
# Output Model
# =========================================================

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


# =========================================================
# Calculator
# =========================================================

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

    # =====================================================
    # MAIN CALC ENGINE
    # =====================================================

    def calculate(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        df = dataframe.copy()

        # force numeric safety (prevents Excel-style errors)
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

        required = ["Open", "High", "Low", "Close"]
        missing = [c for c in required if c not in df.columns]

        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # ensure columns exist
        for col in self.COLUMNS:
            if col not in df.columns:
                df[col] = 0.0

        if len(df) < 5:
            return df

        first = df.index[0]

        # seed row (Excel warm start behavior)
        df.at[first, "Decline"] = SEED_DECLINE
        df.at[first, "Decline3DayAvg"] = SEED_DECLINE_AVG
        df.at[first, "BuyingLow"] = SEED_BUYING_LOW
        df.at[first, "BuyingLow3DayAvg"] = SEED_BUYING_LOW
        df.at[first, "BuyingHigh"] = 0.0
        df.at[first, "BuyingHigh3DayAvg"] = 0.0

        # =====================================================
        # LOOP START (Excel aligned at row 5)
        # =====================================================

        for i in range(4, len(df)):

            r = df.index[i]
            p = df.index[i - 1]

            H = df.at[r, "High"]
            L = df.at[r, "Low"]
            C = df.at[r, "Close"]
            prevO = df.at[p, "Open"]
            prevH = df.at[p, "High"]
            prevL = df.at[p, "Low"]

            # ---------------------
            # Rally
            # ---------------------
            rally = H - prevL
            df.at[r, "Rally"] = rally

            r1 = df.at[df.index[i-1], "Rally"]
            r2 = df.at[df.index[i-2], "Rally"]
            r3 = df.at[df.index[i-3], "Rally"]
            df.at[r, "Rally3DayAvg"] = (r1 + r2 + r3) / 3

            df.at[r, "TomorrowAnticipatedHighFromLow"] = L + df.at[r, "Rally3DayAvg"]

            # ---------------------
            # Buying High
            # ---------------------
            bh = H - prevO
            df.at[r, "BuyingHigh"] = bh

            bh1 = df.at[df.index[i-1], "BuyingHigh"]
            bh2 = df.at[df.index[i-2], "BuyingHigh"]
            bh3 = df.at[df.index[i-3], "BuyingHigh"]
            df.at[r, "BuyingHigh3DayAvg"] = (bh1 + bh2 + bh3) / 3

            df.at[r, "TomorrowAnticipatedHighFromHigh"] = H + df.at[r, "BuyingHigh3DayAvg"]
            df.at[r, "TodaysHigh"] = H

            # ---------------------
            # Pivot
            # ---------------------
            pivot = (H + L + C) / 3

            df.at[r, "TomorrowBreakoutHigh"] = (2 * pivot) - L
            df.at[r, "TomorrowBreakoutLow"] = (2 * pivot) - H

            df.at[r, "AverageSell"] = (
                df.at[r, "TomorrowBreakoutHigh"]
                + H
                + df.at[r, "TomorrowAnticipatedHighFromHigh"]
                + df.at[r, "TomorrowAnticipatedHighFromLow"]
            ) / 4

            df.at[r, "HIGH"] = df.at[r, "AverageSell"]

            # ---------------------
            # Decline
            # ---------------------
            decline = prevH - L
            df.at[r, "Decline"] = decline

            d1 = df.at[df.index[i-1], "Decline"]
            d2 = df.at[df.index[i-2], "Decline"]
            d3 = df.at[df.index[i-3], "Decline"]
            df.at[r, "Decline3DayAvg"] = (d1 + d2 + d3) / 3

            df.at[r, "YesterdayHighMinusAverage"] = H - df.at[r, "Decline3DayAvg"]

            # ---------------------
            # Buying Low
            # ---------------------
            bl = prevL - L
            df.at[r, "BuyingLow"] = bl

            bl1 = df.at[df.index[i-1], "BuyingLow"]
            bl2 = df.at[df.index[i-2], "BuyingLow"]
            bl3 = df.at[df.index[i-3], "BuyingLow"]
            df.at[r, "BuyingLow3DayAvg"] = (bl1 + bl2 + bl3) / 3

            df.at[r, "YesterdayLowMinusAverage"] = L - df.at[r, "BuyingLow3DayAvg"]

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

    # =====================================================
    # Latest Output
    # =====================================================

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
