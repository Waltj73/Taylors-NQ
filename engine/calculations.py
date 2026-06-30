from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
import numpy as np


# =========================================================
# OUTPUT STRUCTURE (REQUIRED BY APP + SERVICE)
# =========================================================

@dataclass
class TaylorLevels:
    AverageBuy: float = 0.0
    AverageSell: float = 0.0
    BreakoutHigh: float = 0.0
    BreakoutLow: float = 0.0


# =========================================================
# MAIN ENGINE
# =========================================================

class TaylorCalculator:

    def __init__(self):
        pass

    # -----------------------------------------------------
    # CORE CALCULATION ENGINE
    # -----------------------------------------------------

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

        required = ["Open", "High", "Low", "Close"]
        if any(c not in df.columns for c in required):
            raise ValueError("Missing OHLC columns")

        # ensure required output columns exist
        for col in ["AverageBuy", "AverageSell", "TomorrowBreakoutHigh", "TomorrowBreakoutLow"]:
            if col not in df.columns:
                df[col] = 0.0

        if len(df) < 2:
            return df

        # =====================================================
        # LOOP (standard OHLC delta model)
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
            # CORE STRUCTURE (clean Taylor cycle)
            # -------------------------------------------------

            rally = H - prevL
            decline = prevH - L
            buying_high = H - prevH
            buying_low = prevL - L

            # rolling stability (simple 3-bar smoothing)
            if i >= 3:
                rally_avg = (
                    (df.at[df.index[i-1], "High"] - df.at[df.index[i-2], "Low"])
                    + rally
                ) / 2
            else:
                rally_avg = rally

            pivot = (H + L + C) / 3

            breakout_high = (2 * pivot) - L
            breakout_low = (2 * pivot) - H

            # -------------------------------------------------
            # FINAL OUTPUTS (stable, non-recursive)
            # -------------------------------------------------

            df.at[r, "AverageBuy"] = (breakout_low + L) / 2
            df.at[r, "AverageSell"] = (breakout_high + H) / 2

            df.at[r, "TomorrowBreakoutHigh"] = breakout_high
            df.at[r, "TomorrowBreakoutLow"] = breakout_low

        return df

    # -----------------------------------------------------
    # API OUTPUT FOR APP
    # -----------------------------------------------------

    def latest(self, df: pd.DataFrame) -> TaylorLevels:

        d = self.calculate(df)
        r = d.iloc[-1]

        return TaylorLevels(
            AverageBuy=float(r["AverageBuy"]),
            AverageSell=float(r["AverageSell"]),
            BreakoutHigh=float(r["TomorrowBreakoutHigh"]),
            BreakoutLow=float(r["TomorrowBreakoutLow"]),
        )
