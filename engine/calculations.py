from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
import numpy as np


# =========================================================
# OUTPUT STRUCTURE (MATCHES app.py)
# =========================================================

@dataclass
class TaylorLevels:
    AverageBuy: float = 0.0
    AverageSell: float = 0.0
    BreakoutHigh: float = 0.0
    BreakoutLow: float = 0.0
    BuyingHigh: float = 0.0
    BuyingLow: float = 0.0
    Decline: float = 0.0


# =========================================================
# CALCULATION ENGINE
# =========================================================

class TaylorCalculator:

    def __init__(self):
        pass

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

        required = ["Open", "High", "Low", "Close"]
        if any(c not in df.columns for c in required):
            raise ValueError("Missing OHLC columns")

        # ensure all expected columns exist
        for col in [
            "AverageBuy", "AverageSell",
            "BreakoutHigh", "BreakoutLow",
            "BuyingHigh", "BuyingLow",
            "Decline"
        ]:
            if col not in df.columns:
                df[col] = 0.0

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

            # =================================================
            # CORE TAYLOR VALUES
            # =================================================

            df.at[r, "BuyingHigh"] = H - prevH
            df.at[r, "BuyingLow"] = prevL - L
            df.at[r, "Decline"] = prevH - L

            # =================================================
            # PIVOT MODEL
            # =================================================

            pivot = (H + L + C) / 3

            breakout_high = (2 * pivot) - L
            breakout_low = (2 * pivot) - H

            df.at[r, "BreakoutHigh"] = breakout_high
            df.at[r, "BreakoutLow"] = breakout_low

            # =================================================
            # FINAL LEVELS (STABLE + SIMPLE)
            # =================================================

            df.at[r, "AverageBuy"] = (breakout_low + L) / 2
            df.at[r, "AverageSell"] = (breakout_high + H) / 2

        return df

    # =========================================================
    # SAFE OUTPUT FOR APP
    # =========================================================

    def latest(self, df: pd.DataFrame) -> TaylorLevels:

        d = self.calculate(df)
        r = d.iloc[-1]

        return TaylorLevels(
            AverageBuy=float(r["AverageBuy"]),
            AverageSell=float(r["AverageSell"]),
            BreakoutHigh=float(r["BreakoutHigh"]),
            BreakoutLow=float(r["BreakoutLow"]),
            BuyingHigh=float(r["BuyingHigh"]),
            BuyingLow=float(r["BuyingLow"]),
            Decline=float(r["Decline"]),
        )
