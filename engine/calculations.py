from __future__ import annotations

import pandas as pd
import numpy as np


class TaylorCalculator:

    def __init__(self):
        pass

    # =========================================================
    # MAIN CALC ENGINE
    # =========================================================
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

        required = ["Open", "High", "Low", "Close"]
        if any(c not in df.columns for c in required):
            raise ValueError("Missing OHLC columns")

        # ensure ALL expected columns exist (prevents KeyErrors everywhere)
        cols = [
            "Rally",
            "Decline",
            "BuyingHigh",
            "BuyingLow",
            "AverageBuy",
            "AverageSell",
            "TomorrowBreakoutHigh",
            "TomorrowBreakoutLow",
            "TomorrowAnticipatedHighFromLow",
            "TomorrowAnticipatedHighFromHigh",
        ]

        for c in cols:
            if c not in df.columns:
                df[c] = 0.0

        if len(df) < 2:
            return df

        # =====================================================
        # LOOP
        # =====================================================
        for i in range(1, len(df)):

            r = df.index[i]
            p = df.index[i - 1]

            H = df.at[r, "High"]
            L = df.at[r, "Low"]
            C = df.at[r, "Close"]

            prevH = df.at[p, "High"]
            prevL = df.at[p, "Low"]

            # -------------------------------------------------
            # CORE TAYLOR VALUES (simple + stable)
            # -------------------------------------------------

            df.at[r, "Rally"] = H - prevL
            df.at[r, "Decline"] = prevH - L
            df.at[r, "BuyingHigh"] = H - prevH
            df.at[r, "BuyingLow"] = prevL - L

            # -------------------------------------------------
            # PIVOT BASED MODEL
            # -------------------------------------------------

            pivot = (H + L + C) / 3

            breakout_high = (2 * pivot) - L
            breakout_low = (2 * pivot) - H

            df.at[r, "TomorrowBreakoutHigh"] = breakout_high
            df.at[r, "TomorrowBreakoutLow"] = breakout_low

            # -------------------------------------------------
            # SIMPLE ENVELOPES (NO DRIFT)
            # -------------------------------------------------

            df.at[r, "AverageBuy"] = (breakout_low + L) / 2
            df.at[r, "AverageSell"] = (breakout_high + H) / 2

            # -------------------------------------------------
            # DERIVED FIELDS (PREVENT KEYERRORS IN APP)
            # -------------------------------------------------

            df.at[r, "TomorrowAnticipatedHighFromLow"] = L + df.at[r, "Rally"]
            df.at[r, "TomorrowAnticipatedHighFromHigh"] = H + df.at[r, "BuyingHigh"]

        return df

    # =========================================================
    # OUTPUT FOR APP (CRASH-PROOF)
    # =========================================================
    def latest(self, df: pd.DataFrame):

        d = self.calculate(df)
        r = d.iloc[-1]

        return {
            "AverageBuy": float(r["AverageBuy"]),
            "AverageSell": float(r["AverageSell"]),

            "TomorrowBreakoutHigh": float(r["TomorrowBreakoutHigh"]),
            "TomorrowBreakoutLow": float(r["TomorrowBreakoutLow"]),

            "BuyingHigh": float(r["BuyingHigh"]),
            "BuyingLow": float(r["BuyingLow"]),
            "Decline": float(r["Decline"]),

            "TomorrowAnticipatedHighFromLow": float(r["TomorrowAnticipatedHighFromLow"]),
            "TomorrowAnticipatedHighFromHigh": float(r["TomorrowAnticipatedHighFromHigh"]),
        }
