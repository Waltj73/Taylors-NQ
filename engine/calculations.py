from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
import numpy as np


# =========================================================
# OUTPUT MODEL
# =========================================================

@dataclass
class TaylorLevels:
    rally: float
    decline: float
    buying_high: float
    buying_low: float


# =========================================================
# SIMPLE TAYLOR CYCLE ENGINE
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

        # ensure output columns exist
        for c in ["Rally", "Decline", "BuyingHigh", "BuyingLow"]:
            if c not in df.columns:
                df[c] = 0.0

        # need at least 2 rows for comparisons
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

            # =================================================
            # CORE TAYLOR CYCLE FORMULAS (RAW)
            # =================================================

            # Rally Number
            df.at[r, "Rally"] = H - prevL

            # Decline Number
            df.at[r, "Decline"] = prevH - L

            # Buying High Number
            df.at[r, "BuyingHigh"] = H - prevH

            # Buying Low Number
            df.at[r, "BuyingLow"] = prevL - L

        return df

    def latest(self, df: pd.DataFrame) -> TaylorLevels:

        d = self.calculate(df)
        r = d.iloc[-1]

        return TaylorLevels(
            rally=float(r["Rally"]),
            decline=float(r["Decline"]),
            buying_high=float(r["BuyingHigh"]),
            buying_low=float(r["BuyingLow"]),
        )
