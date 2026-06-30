# engine/workbook_service.py

"""
Taylor Workbook Service

This is the façade used by the UI.

The UI should never communicate directly with:

    - YahooData
    - WorkbookPipeline
    - WorkbookParser
    - WorkbookRuntime
    - WorkbookDiff
    - WorkbookValidator

Everything flows through WorkbookService.

This should become the only backend object referenced by Streamlit.
"""

from __future__ import annotations

from pathlib import Path

from config import config

from .workbook_orchestrator import WorkbookOrchestrator


class WorkbookService:

    def __init__(self):

        self.orchestrator = WorkbookOrchestrator(
            workbook=config.EXCEL_WORKBOOK,
            symbol=config.SYMBOL,
            sheet="NQ",
            interval=config.HISTORY_INTERVAL,
        )

    def refresh(self):

        return self.orchestrator.run()

    def worksheet(self):

        return self.refresh().worksheet

    def workbook(self):

        return self.refresh().workbook

    def verification(self):

        return self.refresh().verification

    def verification_summary(self):

        return self.refresh().summary

    def trading_plan(self):

        return self.refresh().trading_plan

    def market_history(self):

        return self.refresh().history

    @staticmethod
    def workbook_path() -> Path:

        return config.EXCEL_WORKBOOK

    @staticmethod
    def symbol() -> str:

        return config.SYMBOL
