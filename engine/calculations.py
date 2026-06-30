"""
Taylor Workstation
Core Calculations
"""

import pandas as pd


def calculate(df: pd.DataFrame) -> pd.DataFrame:

    # ==========================================================
    # Previous Day Values
    # ==========================================================

    df["Prev_Open"] = df["Open"].shift(1)
    df["Prev_High"] = df["High"].shift(1)
    df["Prev_Low"] = df["Low"].shift(1)
    df["Prev_Close"] = df["Close"].shift(1)

    # ==========================================================
    # Rally Projection
    # ==========================================================

    df["Rally"] = (
        df["High"] -
        df["Prev_Low"]
    )

    df["Avg_Rally"] = (
        df["Rally"]
        .rolling(3)
        .mean()
    )

    df["Projected_High_1"] = (
        df["Low"] +
        df["Avg_Rally"]
    )

    # ==========================================================
    # Buying High
    # ==========================================================

    df["Buying_High"] = (
        df["High"] -
        df["Prev_Open"]
    )

    df["Avg_Buying_High"] = (
        df["Buying_High"]
        .rolling(3)
        .mean()
    )

    df["Projected_High_2"] = (
        df["High"] +
        df["Avg_Buying_High"]
    )

    # ==========================================================
    # Decline
    # ==========================================================

    df["Decline"] = (
        df["Prev_High"] -
        df["Low"]
    )

    df["Avg_Decline"] = (
        df["Decline"]
        .rolling(3)
        .mean()
    )

    df["Projected_Low_1"] = (
        df["High"] -
        df["Avg_Decline"]
    )

    # ==========================================================
    # Buying Low
    # ==========================================================

    df["Buying_Low"] = (
        df["Prev_Open"] -
        df["Low"]
    )

    df["Avg_Buying_Low"] = (
        df["Buying_Low"]
        .rolling(3)
        .mean()
    )

    df["Projected_Low_2"] = (
        df["Low"] -
        df["Avg_Buying_Low"]
    )

    # ==========================================================
    # Pivot
    # ==========================================================

    df["Pivot"] = (
        df["High"] +
        df["Low"] +
        df["Close"]
    ) / 3

    # ==========================================================
    # LSS Breakouts
    # ==========================================================

    df["Breakout_Buy"] = (
        2 * df["Pivot"]
        - df["Low"]
    )

    df["Breakout_Sell"] = (
        2 * df["Pivot"]
        - df["High"]
    )

    # ==========================================================
    # Average Projections
    # ==========================================================

    df["Average_Sell"] = (
        df[
            [
                "Projected_High_1",
                "Projected_High_2",
                "Breakout_Buy"
            ]
        ]
        .mean(axis=1)
    )

    df["Average_Buy"] = (
        df[
            [
                "Projected_Low_1",
                "Projected_Low_2",
                "Breakout_Sell"
            ]
        ]
        .mean(axis=1)
    )

    return df
