# engine/data.py

"""
Yahoo Finance data provider for the Taylor NQ application.

This module is responsible ONLY for downloading and preparing price data.
No calculations belong here.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

import pandas as pd
import yfinance as yf


DEFAULT_SYMBOL = "NQ=F"


class YahooDataError(Exception):
    """Raised when Yahoo Finance fails to return usable data."""


class YahooData:

    def __init__(self, symbol: str = DEFAULT_SYMBOL):
        self.symbol = symbol

    def history(
        self,
        period: str = "6mo",
        interval: str = "1d",
    ) -> pd.DataFrame:

        df = yf.download(
            tickers=self.symbol,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False,
            threads=False,
        )

        return self._prepare(df)

    def between(
        self,
        start: str | datetime,
        end: str | datetime,
        interval: str = "1d",
    ) -> pd.DataFrame:

        df = yf.download(
            tickers=self.symbol,
            start=start,
            end=end,
            interval=interval,
            auto_adjust=False,
            progress=False,
            threads=False,
        )

        return self._prepare(df)

    def latest(
        self,
        bars: int = 100,
        interval: str = "1d",
    ) -> pd.DataFrame:

        lookup = {
            "1m": "7d",
            "2m": "60d",
            "5m": "60d",
            "15m": "60d",
            "30m": "60d",
            "60m": "730d",
            "90m": "730d",
            "1h": "730d",
            "1d": "2y",
            "1wk": "10y",
            "1mo": "20y",
        }

        period = lookup.get(interval, "2y")

        df = self.history(
            period=period,
            interval=interval,
        )

        return df.tail(bars)

    @staticmethod
    def _prepare(df: pd.DataFrame) -> pd.DataFrame:

        if df is None or df.empty:
            raise YahooDataError(
                "Yahoo Finance returned no data."
            )

        #
        # Flatten MultiIndex columns if present
        #
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        keep = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
        ]

        df = df[keep].copy()

        df = df.dropna()

        df.index = pd.to_datetime(df.index)

        df = df.sort_index()

        df = df.astype(
            {
                "Open": float,
                "High": float,
                "Low": float,
                "Close": float,
                "Volume": float,
            }
        )

        return df

    def current_price(self) -> float:

        df = self.latest(
            bars=1,
            interval="1m",
        )

        return float(df.iloc[-1]["Close"])

    def previous_close(self) -> float:

        df = self.latest(
            bars=2,
            interval="1d",
        )

        return float(df.iloc[-2]["Close"])

    def current_bar(
        self,
        interval: str = "1d",
    ) -> pd.Series:

        df = self.latest(
            bars=1,
            interval=interval,
        )

        return df.iloc[-1]

    def last_bar(
        self,
        interval: str = "1d",
    ) -> pd.Series:

        df = self.latest(
            bars=2,
            interval=interval,
        )

        return df.iloc[-2]
