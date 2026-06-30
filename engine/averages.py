"""
Moving averages used throughout the Taylor model.
"""

import pandas as pd


def rolling_average(series: pd.Series, lookback: int = 3):
    """
    Generic rolling average.

    Default is Taylor's 3-day average.
    """

    return series.rolling(
        window=lookback,
        min_periods=lookback
    ).mean()
