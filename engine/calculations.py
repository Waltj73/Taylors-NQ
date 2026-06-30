import pandas as pd


def calculate(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Previous Day
    df["Prev_Open"] = df["Open"].shift(1)
    df["Prev_High"] = df["High"].shift(1)
    df["Prev_Low"] = df["Low"].shift(1)
    df["Prev_Close"] = df["Close"].shift(1)

    #
    # SELL SIDE
    #

    # I
    df["Rally"] = df["High"] - df["Prev_Low"]

    # J
    df["Avg_Rally"] = df["Rally"].rolling(3).mean()

    # K
    df["Projected_High_1"] = df["Low"] + df["Avg_Rally"]

    # M
    df["Buying_High"] = df["High"] - df["Prev_Open"]

    # N
    df["Avg_Buying_High"] = df["Buying_High"].rolling(3).mean()

    # O
    df["Projected_High_2"] = df["High"] + df["Avg_Buying_High"]

    # Q
    df["Today_High"] = df["High"]

    # S
    df["Breakout_Buy"] = (
        2 * ((df["High"] + df["Low"] + df["Close"]) / 3)
        - df["Low"]
    )

    # U
    df["Average_Sell"] = (
        df["Projected_High_1"]
        + df["Projected_High_2"]
        + df["Today_High"]
        + df["Breakout_Buy"]
    ) / 4

    #
    # BUY SIDE
    #

    # W
    df["Decline"] = df["Prev_High"] - df["Low"]

    # X
    df["Avg_Decline"] = df["Decline"].rolling(3).mean()

    # Y
    df["Projected_Low_1"] = df["High"] - df["Avg_Decline"]

    # AA
    df["Buying_Low"] = df["Prev_Low"] - df["Low"]

    # AB
    df["Avg_Buying_Low"] = df["Buying_Low"].rolling(3).mean()

    # AC
    df["Projected_Low_2"] = df["Low"] - df["Avg_Buying_Low"]

    # AE
    df["Today_Low"] = df["Low"]

    # AG
    df["Breakout_Sell"] = (
        2 * ((df["High"] + df["Low"] + df["Close"]) / 3)
        - df["High"]
    )

    # AI
    df["Average_Buy"] = (
        df["Projected_Low_1"]
        + df["Projected_Low_2"]
        + df["Today_Low"]
        + df["Breakout_Sell"]
    ) / 4

    # Pivot
    df["Pivot"] = (
        df["High"] +
        df["Low"] +
        df["Close"]
    ) / 3

    return df
