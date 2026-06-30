# engine/taylor_engine.py

"""
Taylor Engine

This is the ONE engine the rest of the application should call.

Once complete, no UI component should know anything about:
    - Yahoo Finance
    - Excel
    - Workbook parsing
    - Formula execution

Everything comes through TaylorEngine.

Pipeline

Yahoo Finance
      │
      ▼
Worksheet Builder
      │
      ▼
Workbook Pipeline
      │
      ▼
Workbook Validation
      │
      ▼
Trading Plan
      │
      ▼
Dashboard
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from config import config
from .data import YahooData
from .trading_plan import TradingPlanBuilder
from .workbook import TaylorWorkbook
from .workbook_pipeline import WorkbookPipeline


@dataclass(slots=True)
class TaylorEngineResult:

    history: pd.DataFrame

    worksheet: pd.DataFrame

    workbook: pd.DataFrame | None

    verification: list | None

    trading_plan: object | None


class TaylorEngine:

    def __init__(self):

        self.market = YahooData(
            config.SYMBOL
        )

        self.pipeline = WorkbookPipeline(
            config.EXCEL_WORKBOOK,
            sheet="NQ",
        )

        self.plan = TradingPlanBuilder()

    def refresh(self) -> TaylorEngineResult:

        #
        # Download latest market history.
        #

        history = self.market.latest(
            bars=250,
            interval=config.HISTORY_INTERVAL,
        )

        #
        # Build workbook-equivalent worksheet.
        #

        worksheet = self.pipeline.run(
            history
        )

        #
        # Optional verification against workbook.
        #

        workbook = None
        verification = None

        try:

            workbook = TaylorWorkbook(
                config.EXCEL_WORKBOOK
            ).first_sheet()

            verification = (
                self.pipeline.verify(
                    workbook,
                    worksheet,
                )
            )

        except Exception:

            workbook = None
            verification = None

        #
        # Trading plan.
        #

        trading_plan = None

        try:

            trading_plan = (
                self.plan.build(
                    worksheet
                )
            )

        except Exception:

            trading_plan = None

        return TaylorEngineResult(
            history=history,
            worksheet=worksheet,
            workbook=workbook,
            verification=verification,
            trading_plan=trading_plan,
        )
