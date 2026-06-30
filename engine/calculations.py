from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
import numpy as np


# =========================================================
# OUTPUT CONTRACT (DO NOT CHANGE - MATCHES app.py)
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
    TomorrowAnticipatedHighFromLow: float = 0.0
    TomorrowAnticipatedHighFromHigh: float = 0.0


# =========================================================
# ENGINE
# =========================================================

class TaylorCalculator:

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

        required = ["Open", "High", "Low", "Close"]
        if any(c not in df.columns for c in required):
            raise ValueError("Missing OHLC columns")

        # ensure ALL expected columns exist
        for col in TaylorLevels.__annotations__.keys():
            if col not in df.columns:
                df[col] = 0.0

        if len(df) < 2:
            return df

        # =====================================================
        # MAIN LOOP (Taylor cycle math)
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
            # CORE TAYLOR DEFINITIONS (FROM YOUR VIDEO)
            # -------------------------------------------------

            df.at[r, "Rally"] = H - prevL
            df.at[r, "Decline"] = prevH - L
            df.at[r, "BuyingHigh"] = H - prevH
            df.at[r, "BuyingLow"] = prevL - L

            # -------------------------------------------------
            # PIVOT (STANDARD TAYLOR STYLE)
            # -------------------------------------------------

            pivot = (H + L + C) / 3

            df.at[r, "TomorrowBreakoutHigh"] = (2 * pivot) - L
            df.at[r, "TomorrowBreakoutLow"] = (2 * pivot) - H

            # -------------------------------------------------
            # ENVELOPE (STABLE SIMPLE VERSION)
            # -------------------------------------------------

            df.at[r, "AverageBuy"] = (df.at[r, "TomorrowBreakoutLow"] + L) / 2
            df.at[r, "AverageSell"] = (df.at[r, "TomorrowBreakoutHigh"] + H) / 2

            # -------------------------------------------------
            # ANTICIPATION LAYERS (APP REQUIREMENT)
            # -------------------------------------------------

            df.at[r, "TomorrowAnticipatedHighFromLow"] = L + df.at[r, "Rally"]
            df.at[r, "TomorrowAnticipatedHighFromHigh"] = H + df.at[r, "BuyingHigh"]

        return df

    # =========================================================
    # SAFE OUTPUT (NO KEYERRORS EVER)
    # =========================================================

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
            Rally=float(r["Rally"]),
            TomorrowAnticipatedHighFromLow=float(r["TomorrowAnticipatedHighFromLow"]),
            TomorrowAnticipatedHighFromHigh=float(r["TomorrowAnticipatedHighFromHigh"]),
        )
