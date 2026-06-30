# engine/loader.py

"""
Taylor NQ Loader

Coordinates loading of market data, workbook data, calculations,
and signal generation.

This is the central orchestration layer used by the UI.

No presentation logic.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from config import config
from .calculations import TaylorCalculator, TaylorLevels
from .data import YahooData
from .signals import SignalEngine, SignalResult
from .session import SessionInfo, SessionManager
from .workbook import TaylorWorkbook
from .yahoo import Quote, YahooQuote


@dataclass(slots=True)
class ApplicationData:

    history: pd.DataFrame

    calculations: pd.DataFrame

    levels: TaylorLevels

    signal: SignalResult

    quote: Quote

    session: SessionInfo

    workbook: pd.DataFrame | None


class Loader:

    def __init__(self):

        self.market = YahooData(config.SYMBOL)

        self.quote = YahooQuote(config.SYMBOL)

        self.calculator = TaylorCalculator()

        self.signal = SignalEngine()

        self.session = SessionManager()

    def load(self) -> ApplicationData:

        #
        # Historical data
        #

        history = self.market.latest(
            bars=250,
            interval=config.HISTORY_INTERVAL,
        )

        #
        # Calculations
        #

        calculations = self.calculator.calculate(
            history
        )

        levels = self.calculator.latest(
            history
        )

        signal = self.signal.evaluate(
            calculations
        )

        #
        # Live Quote
        #

        quote = self.quote.quote()

        #
        # Session
        #

        session = self.session.info()

        #
        # Workbook (optional)
        #

        workbook = None

        try:

            workbook = TaylorWorkbook(
                config.EXCEL_WORKBOOK
            ).first_sheet()

        except Exception:
            pass

        return ApplicationData(
            history=history,
            calculations=calculations,
            levels=levels,
            signal=signal,
            quote=quote,
            session=session,
            workbook=workbook,
        )
