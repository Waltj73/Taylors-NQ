"""
Taylor Workstation
Core Calculation Engine

Version: 0.1
"""

import pandas as pd


class TaylorEngine:

    def __init__(self, df: pd.DataFrame):
        """
        DataFrame must contain:

        Date
        Open
        High
        Low
        Close
        """

        self.df = df.copy()

    def calculate(self):

        df = self.df

        # -------------------------------------------------
        # Previous Day Values
        # -------------------------------------------------

        df["Prev_Open"] = df["Open"].shift(1)
        df["Prev_High"] = df["High"].shift(1)
        df["Prev_Low"] = df["Low"].shift(1)
        df["Prev_Close"] = df["Close"].shift(1)

        # -------------------------------------------------
        # Rally Projection
        # (Column I)
        # Today's High - Yesterday's Low
        # -------------------------------------------------

        df["Rally"] = df["High"] - df["Prev_Low"]

        # -------------------------------------------------
        # 3-Day Average Rally
        # (Column J)
        # -------------------------------------------------

        df["Avg_Rally"] = df["Rally"].rolling(3).mean()

        # -------------------------------------------------
        # Tomorrow Anticipated High
        # (Column K)
        # -------------------------------------------------

        df["Projected_High_1"] = (
            df["Low"] +
            df["Avg_Rally"]
        )

        # -------------------------------------------------
        # Buying High
        # (Column M)
        # Today's High - Yesterday's Open
        # -------------------------------------------------

        df["Buying_High"] = (
            df["High"] -
            df["Prev_Open"]
        )

        # -------------------------------------------------
        # Average Buying High
        # (Column N)
        # -------------------------------------------------

        df["Avg_Buying_High"] = (
            df["Buying_High"]
            .rolling(3)
            .mean()
        )

        # -------------------------------------------------
        # Projection #2
        # (Column O)
        # -------------------------------------------------

        df["Projected_High_2"] = (
            df["High"] +
            df["Avg_Buying_High"]
        )

        # -------------------------------------------------
        # Pivot
        # -------------------------------------------------

        df["Pivot"] = (
            df["High"] +
            df["Low"] +
            df["Close"]
        ) / 3

        # -------------------------------------------------
        # LSS Breakout Buy
        # (Column S)
        # -------------------------------------------------

        df["Breakout_Buy"] = (
            2 * df["Pivot"]
            - df["Low"]
        )

        return df
