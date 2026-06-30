from __future__ import annotations

import pandas as pd
import numpy as np


class TaylorCalculator:

    def __init__(self):
        pass

    # =====================================================
    # CORE CALCULATION ENGINE
    # =====================================================

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

        required = ["Open", "High", "Low", "Close"]
        if any(c not in df.columns for c in required):
            raise ValueError("Missing OHLC columns")

        # ensure compatibility columns exist (IMPORTANT for app.py)
        for c in [
            "Rally", "Decline",
            "BuyingHigh", "BuyingLow",
            "AverageBuy", "AverageSell",
            "TomorrowBreakoutHigh", "TomorrowBreakoutLow",
            "YesterdayHighMinusAverage", "YesterdayLowMinusAverage",
            "Rally3DayAvg", "BuyingHigh3DayAvg",
            "Decline3DayAvg", "BuyingLow3DayAvg",
            "TomorrowAnticipatedHighFromLow",
            "TomorrowAnticipatedHighFromHigh",
        ]:
            if c not in df.columns:
                df[c] = 0.0

        if len(df) < 2:
            return df

        # =====================================================
        # MAIN LOOP
        # =====================================================

        for i in range(1, len(df)):

            r = df.index[i]
            p = df.index[i - 1]

            H = df.at[r, "High"]
            L = df.at[r, "Low"]
            C = df.at[r, "Close"]

            prevH = df.at[p, "High"]
            prevL = df.at[p, "Low"]
            prevC = df.at[p, "Close"]

            # -------------------------------------------------
            # CORE TAYLOR CYCLICAL VALUES
            # -------------------------------------------------

            df.at[r, "Rally"] = H - prevL
            df.at[r, "Decline"] = prevH - L
            df.at[r, "BuyingHigh"] = H - prevH
            df.at[r, "BuyingLow"] = prevL - L

            # -------------------------------------------------
            # SIMPLE 3-DAY AVERAGES (STABLE)
            # -------------------------------------------------

            def safe(col):
                return (
                    df.at[df.index[i - 1], col]
                    if i >= 1 else 0
                )

            def safe2(col):
                return (
                    df.at[df.index[i - 2], col]
                    if i >= 2 else 0
                )

            df.at[r, "Rally3DayAvg"] = (safe("Rally") + safe2("Rally") + df.at[r, "Rally"]) / 3
            df.at[r, "Decline3DayAvg"] = (safe("Decline") + safe2("Decline") + df.at[r, "Decline"]) / 3
            df.at[r, "BuyingHigh3DayAvg"] = (safe("BuyingHigh") + safe2("BuyingHigh") + df.at[r, "BuyingHigh"]) / 3
            df.at[r, "BuyingLow3DayAvg"] = (safe("BuyingLow") + safe2("BuyingLow") + df.at[r, "BuyingLow"]) / 3

            # -------------------------------------------------
            # PROJECTIONS (LIGHTWEIGHT ENVELOPES)
            # -------------------------------------------------

            df.at[r, "TomorrowAnticipatedHighFromLow"] = L + df.at[r, "Rally3DayAvg"]
            df.at[r, "TomorrowAnticipatedHighFromHigh"] = H + df.at[r, "BuyingHigh3DayAvg"]

            pivot = (H + L + C) / 3

            df.at[r, "TomorrowBreakoutHigh"] = (2 * pivot) - L
            df.at[r, "TomorrowBreakoutLow"] = (2 * pivot) - H

            # -------------------------------------------------
            # FINAL LEVELS (COMPATIBLE WITH YOUR APP)
            # -------------------------------------------------

            df.at[r, "AverageSell"] = (
                df.at[r, "TomorrowBreakoutHigh"]
                + df.at[r, "TomorrowAnticipatedHighFromHigh"]
                + df.at[r, "TomorrowAnticipatedHighFromLow"]
                + H
            ) / 4

            df.at[r, "AverageBuy"] = (
                df.at[r, "TomorrowBreakoutLow"]
                + df.at[r, "YesterdayHighMinusAverage"]
                + df.at[r, "YesterdayLowMinusAverage"]
                + L
            ) / 4

            df.at[r, "YesterdayHighMinusAverage"] = H - df.at[r, "Decline3DayAvg"]
            df.at[r, "YesterdayLowMinusAverage"] = L - df.at[r, "BuyingLow3DayAvg"]

        return df

    # =====================================================
    # SAFE OUTPUT FOR STREAMLIT
    # =====================================================

    def latest(self, df: pd.DataFrame):

        d = self.calculate(df)
        r = d.iloc[-1]

        return {
            "AverageBuy": float(r["AverageBuy"]),
            "AverageSell": float(r["AverageSell"]),
            "BreakoutHigh": float(r["TomorrowBreakoutHigh"]),
            "BreakoutLow": float(r["TomorrowBreakoutLow"]),
        }
