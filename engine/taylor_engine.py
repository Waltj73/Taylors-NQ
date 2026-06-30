# engine/taylor_engine.py

from __future__ import annotations

import pandas as pd

from engine.calculations import calculate
from engine.models import TaylorLevels


class TaylorEngine:
    """
    Taylor Trading Engine

    Input:
        DataFrame containing

        Date
        Open
        High
        Low
        Close

    Output:
        DataFrame with every Taylor calculation
    """

    def __init__(self, dataframe: pd.DataFrame):

        if dataframe is None:
            raise ValueError("No dataframe supplied.")

        if dataframe.empty:
            raise ValueError("Dataframe is empty.")

        self.df = dataframe.copy()

    # ----------------------------------------------------
    # Calculate every row
    # ----------------------------------------------------

    def calculate_all(self) -> pd.DataFrame:

        return calculate(self.df)

    # ----------------------------------------------------
    # Latest trading day only
    # ----------------------------------------------------

    def latest(self) -> TaylorLevels:

        df = calculate(self.df)

        row = df.iloc[-1]

        return TaylorLevels(

            date=str(row["Date"]),

            open=float(row["Open"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            close=float(row["Close"]),

            projected_high_1=float(row["Projected_High_1"]),
            projected_high_2=float(row["Projected_High_2"]),

            projected_low_1=float(row["Projected_Low_1"]),
            projected_low_2=float(row["Projected_Low_2"]),

            average_sell=float(row["Average_Sell"]),
            average_buy=float(row["Average_Buy"]),

            breakout_buy=float(row["Breakout_Buy"]),
            breakout_sell=float(row["Breakout_Sell"]),

            pivot=float(row["Pivot"]),
        )

    # ----------------------------------------------------
    # Latest dataframe row
    # ----------------------------------------------------

    def latest_row(self) -> pd.Series:

        df = calculate(self.df)

        return df.iloc[-1]

    # ----------------------------------------------------
    # Entire calculation history
    # ----------------------------------------------------

    def history(self) -> pd.DataFrame:

        return calculate(self.df)
