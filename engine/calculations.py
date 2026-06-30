from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
import numpy as np


# =========================================================
# OUTPUT STRUCTURE (APP SAFE)
# =========================================================

@dataclass
class TaylorLevels:
    AverageBuy: float = 0.0
    AverageSell: float = 0.0
    TomorrowBreakoutHigh: float = 0.0
    TomorrowBreakoutLow: float = 0.0
    BuyingHigh: float = 0.0
    BuyingLow: float = 0.0
    Decline: float = 0.0
    Rally: float = 0.0


# =========================================================
# TAYLOR BOOK METHOD ENGINE
# =========================================================

class TaylorCalculator:

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

        required = ["Open", "High", "Low", "Close"]
        if any(c not in df.columns for c in required):
            raise ValueError("Missing OHLC columns")

        # ensure columns exist
        cols = [
            "Rally", "Decline", "BuyingHigh", "BuyingLow",
            "Rally3Avg", "Decline3Avg", "BuyHigh3Avg", "BuyLow3Avg",
            "Pivot", "PivotBreakoutHigh", "PivotBreakoutLow",
            "AverageBuy", "AverageSell"
        ]

        for c in cols:
            if c not in df.columns:
                df[c] = 0.0

        if len(df) < 2:
            return df

        # =====================================================
        # CORE CALCULATIONS
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
            # CORE TAYLOR DEFINITIONS (FROM YOUR SLIDES)
            # -------------------------------------------------

            rally = H - prevL
            decline = prevH - L
            buying_high = H - prevH
            buying_low = prevL - L

            df.at[r, "Rally"] = rally
            df.at[r, "Decline"] = decline
            df.at[r, "BuyingHigh"] = buying_high
            df.at[r, "BuyingLow"] = buying_low

            # -------------------------------------------------
            # 3-DAY AVERAGES (ENVELOPE COMPONENTS)
            # -------------------------------------------------

            def avg(col):
                vals = []
                for j in range(max(0, i-2), i+1):
                    vals.append(df.at[df.index[j], col])
                return sum(vals) / len(vals)

            df.at[r, "Rally3Avg"] = avg("Rally")
            df.at[r, "Decline3Avg"] = avg("Decline")
            df.at[r, "BuyHigh3Avg"] = avg("BuyingHigh")
            df.at[r, "BuyLow3Avg"] = avg("BuyingLow")

            # -------------------------------------------------
            # PIVOT (TAYLOR STANDARD)
            # -------------------------------------------------

            pivot = (H + L + C) / 3
            df.at[r, "Pivot"] = pivot

            df.at[r, "PivotBreakoutHigh"] = (2 * pivot) - H
            df.at[r, "PivotBreakoutLow"] = (2 * pivot) - L

            # -------------------------------------------------
            # ENVELOPES (FROM SLIDES LOGIC)
            # -------------------------------------------------

            # Sell envelope uses rally + buying high pressure
            sell_pressure = df.at[r, "Rally3Avg"] + df.at[r, "BuyHigh3Avg"]

            df.at[r, "AverageSell"] = H + (sell_pressure / 2)

            # Buy envelope uses decline + buying low pressure
            buy_pressure = df.at[r, "Decline3Avg"] + df.at[r, "BuyLow3Avg"]

            df.at[r, "AverageBuy"] = L - (buy_pressure / 2)

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
            TomorrowBreakoutHigh=float(r["PivotBreakoutHigh"]),
            TomorrowBreakoutLow=float(r["PivotBreakoutLow"]),
            BuyingHigh=float(r["BuyingHigh"]),
            BuyingLow=float(r["BuyingLow"]),
            Decline=float(r["Decline"]),
            Rally=float(r["Rally"]),
        )
