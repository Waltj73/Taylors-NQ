"""
Taylor Decline Calculations
"""

from .averages import rolling_average


def calculate(df):

    df["Decline"] = (
        df["High"].shift(1)
        - df["Low"]
    )

    df["Avg_Decline"] = rolling_average(
        df["Decline"]
    )

    df["Projected_Low_Decline"] = (
        df["High"]
        - df["Avg_Decline"]
    )

    return df
