from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
import numpy as np


# =========================================================
# REQUIRED FOR engine/__init__.py IMPORT
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
    TomorrowAnticipatedHighFromLow: float = 0.0
    TomorrowAnticipatedHighFromHigh: float = 0.0


# =========================================================
# CALC ENGINE
# =========================================================

class TaylorCalculator:

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

        required = ["Open", "High", "Low", "Close"]
        if any(c not in df.columns for c in required):
            raise ValueError("Missing OHLC columns")

        for c in TaylorLevels.__annotations__.keys():
            if c not in df.columns:
                df[c] = 0.0

        if len(df) < 2:
            return df

        for i in range(1, len(df)):

            r = df.index[i]
            p = df.index[i - 1]

            H = df.at[r, "High"]
            L = df.at[r, "Low"]
            C = df.at[r, "Close"]

            prevH = df.at[p, "High"]
            prevL = df.at[p, "Low"]

            # -------------------------
            # CORE CYCLICAL VALUES
            # -------------------------

            df.at[r, "Rally"] = H - prevL
            df.at[r, "Decline"] = prevH - L
            df.at[r, "BuyingHigh"] = H - prevH
            df.at[r, "BuyingLow"] = prevL - L

            # -------------------------
            # PIVOT MODEL
            # -------------------------

            pivot = (H + L + C) / 3

            df.at[r, "TomorrowBreakoutHigh"] = (2 * pivot) - L
            df.at[r, "TomorrowBreakoutLow"] = (2 * pivot) - H

            # -------------------------
            # ENVELOPE
            # -------------------------

            df.at[r, "AverageBuy"] = (df.at[r, "TomorrowBreakoutLow"] + L) / 2
            df.at[r, "AverageSell"] = (df.at[r, "TomorrowBreakoutHigh"] + H) / 2

            # -------------------------
            # DERIVED (APP REQUIRED)
            # -------------------------

            df.at[r, "TomorrowAnticipatedHighFromLow"] = L + df.at[r, "Rally"]
            df.at[r, "TomorrowAnticipatedHighFromHigh"] = H + df.at[r, "BuyingHigh"]

        return df

    def latest(self, df: pd.DataFrame) -> TaylorLevels:

        d = self.calculate(df)
        r = d.iloc[-1]

        return TaylorLevels(
            AverageBuy=float(r["AverageBuy"]),
            AverageSell=float(r["AverageSell"]),
            TomorrowBreakoutHigh=float(r["TomorrowBreakoutHigh"]),
            TomorrowBreakoutLow=float(r["TomorrowBreakoutLow"]),
            BuyingHigh=float(r["BuyingHigh"]),
            BuyingLow=float(r["BuyingLow"]),
            Decline=float(r["Decline"]),
            TomorrowAnticipatedHighFromLow=float(r["TomorrowAnticipatedHighFromLow"]),
            TomorrowAnticipatedHighFromHigh=float(r["TomorrowAnticipatedHighFromHigh"]),
        )
