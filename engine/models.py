# engine/models.py

from dataclasses import dataclass


@dataclass(slots=True)
class TaylorLevels:
    """
    Holds the latest calculated Taylor levels.
    """

    # Candle
    date: str

    open: float
    high: float
    low: float
    close: float

    # Sell Side
    projected_high_1: float
    projected_high_2: float

    # Buy Side
    projected_low_1: float
    projected_low_2: float

    # Averages
    average_sell: float
    average_buy: float

    # Breakouts
    breakout_buy: float
    breakout_sell: float

    # Pivot
    pivot: float


@dataclass(slots=True)
class DailyBar:
    """
    Standard OHLC bar.
    """

    date: str

    open: float
    high: float
    low: float
    close: float

    volume: float
