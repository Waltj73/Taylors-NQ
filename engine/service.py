# engine/service.py

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from config import config

from engine.calculations import TaylorCalculator
from engine.data import YahooData
from engine.workbook import TaylorWorkbook
from engine.verify import WorkbookVerifier


@dataclass(slots=True)
class TaylorState:

    history: pd.DataFrame

    calculations: pd.DataFrame

    workbook: pd.DataFrame | None

    verification: list | None

    summary: dict | None


class TaylorService:

    def __init__(self):

        self.market = YahooData(
            config.SYMBOL
        )

        self.calculator = TaylorCalculator()

        self.verifier = WorkbookVerifier()

    def refresh(self):

        #
        # Download latest market history.
        #

        history = self.market.latest(
            bars=250,
            interval=config.HISTORY_INTERVAL,
        )

        #
        # Perform workbook calculations.
        #

        calculations = self.calculator.calculate(
            history
        )

        workbook = None
        verification = None
        summary = None

        try:

            workbook = TaylorWorkbook(
                config.EXCEL_WORKBOOK
            ).first_sheet()

            verification = (
                self.verifier.verify_last_row(
                    workbook,
                    calculations,
                )
            )

            summary = (
                self.verifier.summary(
                    workbook,
                    calculations,
                )
            )

        except Exception:

            pass

        return TaylorState(

            history=history,

            calculations=calculations,

            workbook=workbook,

            verification=verification,

            summary=summary,
        )
