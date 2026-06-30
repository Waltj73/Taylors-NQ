from __future__ import annotations

import pandas as pd


class TaylorCalculator:

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        required = ["Open", "High", "Low", "Close"]
        if any(c not in df.columns for c in required):
            raise ValueError("Missing OHLC columns")

        # -----------------------------
        # CORE SCREENSHOT LOGIC
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

        pivot = (df["High"] + df["Low"] + df["Close"]) / 3

        df["TomorrowBreakoutHigh"] = (2 * pivot) - df["Low"]
        df["TomorrowBreakoutLow"] = (2 * pivot) - df["High"]

        # -----------------------------
        # ENVELOPES
        # -----------------------------

        df["AverageSell"] = df["High"] + (df["RallyAvg"] + df["BuyingHighAvg"]) / 2
        df["AverageBuy"] = df["Low"] - (df["DeclineAvg"] + df["BuyingUnderAvg"]) / 2

        return df

    # =====================================================
    # APP OUTPUT (KEY FIX HERE)
    # =====================================================

    def latest(self, df: pd.DataFrame):

        d = self.calculate(df)
        r = d.iloc[-1]

        return {
            "AverageBuy": float(r["AverageBuy"]),
            "AverageSell": float(r["AverageSell"]),

            "TomorrowBreakoutHigh": float(r["TomorrowBreakoutHigh"]),
            "TomorrowBreakoutLow": float(r["TomorrowBreakoutLow"]),

            "BuyingHigh": float(r["BuyingHigh"]),

            # 🔴 FIX: app expects BuyingLow, not BuyingUnder
            "BuyingLow": float(r["BuyingUnder"]),

            "Decline": float(r["Decline"]),
            "Rally": float(r["Rally"]),
        }
