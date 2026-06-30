# engine/yahoo.py

"""
Yahoo Finance live quote interface for the Taylor NQ application.

This module is responsible ONLY for retrieving current market data.
It performs no calculations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import yfinance as yf


DEFAULT_SYMBOL = "NQ=F"


class YahooQuoteError(Exception):
    pass


@dataclass(slots=True)
class Quote:

    symbol: str

    price: float

    open: float

    high: float

    low: float

    previous_close: float

    volume: float

    timestamp: datetime


class YahooQuote:

    def __init__(self, symbol: str = DEFAULT_SYMBOL):

        self.symbol = symbol

    def quote(self) -> Quote:

        ticker = yf.Ticker(self.symbol)

        #
        # Fast Info
        #

        fast = ticker.fast_info

        price = self._first(
            fast,
            "lastPrice",
            "regularMarketPrice",
        )

        previous_close = self._first(
            fast,
            "previousClose",
            "regularMarketPreviousClose",
        )

        day_high = self._first(
            fast,
            "dayHigh",
            "regularMarketDayHigh",
        )

        day_low = self._first(
            fast,
            "dayLow",
            "regularMarketDayLow",
        )

        day_open = self._first(
            fast,
            "open",
            "regularMarketOpen",
        )

        volume = self._first(
            fast,
            "lastVolume",
            "regularMarketVolume",
        )

        #
        # Fallback if Yahoo omits open
        #

        if day_open is None:

            hist = ticker.history(
                period="1d",
                interval="1m",
            )

            if hist.empty:
                raise YahooQuoteError(
                    "Unable to retrieve live quote."
                )

            day_open = float(hist.iloc[0]["Open"])

            if price is None:
                price = float(hist.iloc[-1]["Close"])

            if day_high is None:
                day_high = float(hist["High"].max())

            if day_low is None:
                day_low = float(hist["Low"].min())

            if volume is None:
                volume = float(hist["Volume"].sum())

        if price is None:
            raise YahooQuoteError(
                "Yahoo Finance returned no last price."
            )

        return Quote(
            symbol=self.symbol,
            price=float(price),
            open=float(day_open),
            high=float(day_high),
            low=float(day_low),
            previous_close=float(previous_close),
            volume=float(volume),
            timestamp=datetime.now(),
        )

    def last_price(self) -> float:
        return self.quote().price

    def high(self) -> float:
        return self.quote().high

    def low(self) -> float:
        return self.quote().low

    def open(self) -> float:
        return self.quote().open

    def previous_close(self) -> float:
        return self.quote().previous_close

    def volume(self) -> float:
        return self.quote().volume

    @staticmethod
    def _first(obj, *keys):

        for key in keys:

            try:

                value = obj[key]

                if value is not None:
                    return value

            except Exception:
                pass

        return None
