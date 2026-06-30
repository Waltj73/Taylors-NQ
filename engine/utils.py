# engine/utils.py

"""
Taylor NQ Utility Functions

Shared helper functions used throughout the application.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd


def is_number(value: Any) -> bool:
    return isinstance(
        value,
        (
            int,
            float,
            np.integer,
            np.floating,
        ),
    )


def safe_float(value: Any):

    if value is None:
        return None

    try:

        if pd.isna(value):
            return None

        return float(value)

    except Exception:

        return None


def round_price(
    value,
    decimals: int = 2,
):

    value = safe_float(value)

    if value is None:
        return None

    return round(value, decimals)


def format_price(
    value,
    decimals: int = 2,
):

    value = safe_float(value)

    if value is None:
        return "-"

    return f"{value:,.{decimals}f}"


def format_integer(value):

    value = safe_float(value)

    if value is None:
        return "-"

    return f"{int(value):,}"


def timestamp():

    return datetime.now()


def percent_change(
    current,
    previous,
):

    current = safe_float(current)
    previous = safe_float(previous)

    if current is None:
        return None

    if previous in (None, 0):
        return None

    return ((current - previous) / previous) * 100.0


def dataframe_copy(df: pd.DataFrame):

    return df.copy(deep=True)


def numeric_columns(df: pd.DataFrame):

    return df.select_dtypes(
        include=["number"]
    ).columns.tolist()


def clean_dataframe(df: pd.DataFrame):

    frame = df.copy()

    frame.columns = [
        str(c).strip()
        for c in frame.columns
    ]

    frame = frame.drop_duplicates()

    frame = frame.reset_index(drop=True)

    return frame


def latest_row(df: pd.DataFrame):

    if df.empty:
        return None

    return df.iloc[-1]


def previous_row(df: pd.DataFrame):

    if len(df) < 2:
        return None

    return df.iloc[-2]


def ensure_datetime_index(df: pd.DataFrame):

    if isinstance(
        df.index,
        pd.DatetimeIndex,
    ):
        return df

    frame = df.copy()

    frame.index = pd.to_datetime(
        frame.index
    )

    return frame


def difference(
    a,
    b,
):

    a = safe_float(a)
    b = safe_float(b)

    if a is None or b is None:
        return None

    return a - b


def almost_equal(
    a,
    b,
    tolerance: float = 0.01,
):

    a = safe_float(a)
    b = safe_float(b)

    if a is None or b is None:
        return False

    return abs(a - b) <= tolerance
