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

        self.market = YahooData(config.SYMBOL)

        self.calculator = TaylorCalculator()

        self.verifier = WorkbookVerifier()

    def refresh(self) -> TaylorState:

        # --------------------------------------------------
        # Download latest market data
        # --------------------------------------------------

        history = self.market.latest(
            bars=250,
            interval=config.HISTORY_INTERVAL,
        )

        # --------------------------------------------------
        # Perform Taylor calculations
        # --------------------------------------------------

        calculations = self.calculator.calculate(history)

        workbook = None
        verification = None
        summary = None

        # --------------------------------------------------
        # Load workbook and verify calculations
        # --------------------------------------------------

        try:

            workbook = TaylorWorkbook(
                config.EXCEL_WORKBOOK
            ).first_sheet()

            verification = self.verifier.verify_last_row(
                workbook,
                calculations,
            )

            summary = self.verifier.summary(
                workbook,
                calculations,
            )

        except Exception as e:

            print("\n" + "=" * 70)
            print("TAYLOR WORKBOOK ERROR")
            print("=" * 70)
            print(type(e).__name__)
            print(e)
            print("=" * 70 + "\n")

            # Leave workbook-related values as None so
            # the rest of the application can still run.
            workbook = None
            verification = None
            summary = None

        return TaylorState(
            history=history,
            calculations=calculations,
            workbook=workbook,
            verification=verification,
            summary=summary,
        )
