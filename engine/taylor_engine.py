"""
Taylor Workstation
Main Engine
"""

from engine.calculations import calculate
from engine.models import TaylorLevels


class TaylorEngine:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    def calculate_all(self):

        self.df = calculate(self.df)

        return self.df

    def latest(self):

        df = calculate(self.df)

        row = df.iloc[-1]

        return TaylorLevels(

            date=str(row["Date"]),

            open=row["Open"],
            high=row["High"],
            low=row["Low"],
            close=row["Close"],

            projected_high_1=row["Projected_High_1"],
            projected_high_2=row["Projected_High_2"],

            projected_low_1=row["Projected_Low_1"],
            projected_low_2=row["Projected_Low_2"],

            breakout_buy=row["Breakout_Buy"],
            breakout_sell=row["Breakout_Sell"],

            average_buy=row["Average_Buy"],
            average_sell=row["Average_Sell"],

            pivot=row["Pivot"]

        )
