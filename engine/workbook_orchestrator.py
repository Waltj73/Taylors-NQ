# engine/workbook_orchestrator.py

"""
Taylor Workbook Orchestrator

This is the highest-level coordinator for the Taylor workbook.

Unlike TaylorEngine, this class is completely workbook-centric.

Responsibilities

    • Load workbook
    • Download Yahoo data
    • Build worksheet
    • Execute workbook
    • Validate workbook
    • Produce trading plan
    • Produce verification report

This is intended to become the application's primary backend.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .data import YahooData
from .trading_plan import TradingPlanBuilder
from .workbook import TaylorWorkbook
from .workbook_pipeline import WorkbookPipeline
from .workbook_diff import WorkbookDiff


@dataclass(slots=True)
class WorkbookResult:

    history: pd.DataFrame

    worksheet: pd.DataFrame

    workbook: pd.DataFrame

    trading_plan: object

    verification: list

    summary: dict


class WorkbookOrchestrator:

    def __init__(
        self,
        workbook: str | Path,
        symbol: str = "NQ=F",
        sheet: str = "NQ",
        interval: str = "1d",
    ):

        self.symbol = symbol
        self.interval = interval
        self.sheet = sheet

        self.market = YahooData(symbol)

        self.pipeline = WorkbookPipeline(
            workbook,
            sheet,
        )

        self.workbook = TaylorWorkbook(
            workbook
        )

        self.diff = WorkbookDiff()

        self.plan = TradingPlanBuilder()

    def run(
        self,
        bars: int = 250,
    ) -> WorkbookResult:

        #
        # Download market data.
        #

        history = self.market.latest(
            bars=bars,
            interval=self.interval,
        )

        #
        # Build worksheet.
        #

        worksheet = self.pipeline.run(
            history
        )

        #
        # Load workbook.
        #

        workbook = self.workbook.first_sheet()

        #
        # Verify.
        #

        verification = self.diff.compare(
            workbook,
            worksheet,
        )

        summary = self.diff.summary(
            workbook,
            worksheet,
        )

        #
        # Trading plan.
        #

        trading_plan = self.plan.build(
            worksheet
        )

        return WorkbookResult(
            history=history,
            worksheet=worksheet,
            workbook=workbook,
            trading_plan=trading_plan,
            verification=verification,
            summary=summary,
        )
