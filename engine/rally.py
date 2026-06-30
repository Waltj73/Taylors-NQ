"""
Taylor Rally Calculations
"""

from .averages import rolling_average


def calculate(df):

    df["Rally"] = (
        df["High"]
        - df["Low"].shift(1)
    )

    df["Avg_Rally"] = rolling_average(
        df["Rally"]
    )

    df["Projected_High_Rally"] = (
        df["Low"]
        + df["Avg_Rally"]
    )

    return df
