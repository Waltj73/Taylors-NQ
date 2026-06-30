from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


# =========================================================
# OUTPUT
# =========================================================

@dataclass
class TaylorLevels:
    AverageBuy: float
    AverageSell: float
    BreakoutHigh: float
    BreakoutLow: float
    Rally: float
    Decline: float
    BuyingHigh: float
    BuyingUnder: float


# =========================================================
# ENGINE
# =========================================================

class TaylorCalculator:

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        required = ["Open", "High", "Low", "Close"]
        if any(c not in df.columns for c in required):
            raise ValueError("Missing OHLC")

        # -----------------------------
        # CORE DAILY METRICS
        # -----------------------------

        df["Rally"] = df["High"] - df["Low"].shift(1)
        df["Decline"] = df["High"].shift(1) - df["Low"]
        df["BuyingHigh"] = df["High"] - df["High"].shift(1)
        df["BuyingUnder"] = df["Low"].shift(1) - df["Low"]

        # -----------------------------
        # 3-DAY AVERAGES
        # -----------------------------

        df["RallyAvg"] = df["Rally"].rolling(3).mean()
        df["DeclineAvg"] = df["Decline"].rolling(3).mean()
        df["BuyingHighAvg"] = df["BuyingHigh"].rolling(3).mean()
        df["BuyingUnderAvg"] = df["BuyingUnder"].rolling(3).mean()

        # -----------------------------
        # PIVOT STRUCTURE
        # -----------------------------

        X = (df["High"] + df["Low"] + df["Close"]) / 3

        df["BreakoutHigh"] = (2 * X) - df["Low"]
        df["BreakoutLow"] = (2 * X) - df["High"]

        # -----------------------------
        # ENVELOPE LOGIC
        # -----------------------------

        df["AverageSell"] = df["High"] + (df["RallyAvg"] + df["BuyingHighAvg"]) / 2
        df["AverageBuy"] = df["Low"] - (df["DeclineAvg"] + df["BuyingUnderAvg"]) / 2

        return df

    # =========================================================
    # OUTPUT
    # =========================================================

    def latest(self, df: pd.DataFrame) -> TaylorLevels:

        d = self.calculate(df)
        r = d.iloc[-1]

        return TaylorLevels(
            AverageBuy=float(r["AverageBuy"]),
            AverageSell=float(r["AverageSell"]),
            BreakoutHigh=float(r["BreakoutHigh"]),
            BreakoutLow=float(r["BreakoutLow"]),
            Rally=float(r["Rally"]),
            Decline=float(r["Decline"]),
            BuyingHigh=float(r["BuyingHigh"]),
            BuyingUnder=float(r["BuyingUnder"]),
        )
