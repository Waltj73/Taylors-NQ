from dataclasses import dataclass


@dataclass
class TaylorLevels:

    date: str

    open: float
    high: float
    low: float
    close: float

    projected_high_1: float
    projected_high_2: float

    projected_low_1: float
    projected_low_2: float

    breakout_buy: float
    breakout_sell: float

    average_buy: float
    average_sell: float

    pivot: float
