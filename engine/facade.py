# engine/facade.py

"""
Taylor Engine Facade

This is the public API for the Taylor NQ application.

Nothing outside of the engine package should know how the
workbook is built or executed.

The UI should simply do:

    engine = TaylorFacade()
    state = engine.refresh()

and render the returned state.

Everything else remains internal.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .workbook_service import WorkbookService


@dataclass(slots=True)
class EngineState:

    timestamp: datetime

    history: object

    worksheet: object

    workbook: object

    verification: object

    verification_summary: dict

    trading_plan: object


class TaylorFacade:

    def __init__(self):

        self.service = WorkbookService()

    def refresh(self) -> EngineState:

        result = self.service.refresh()

        return EngineState(
            timestamp=datetime.now(),

            history=result.history,

            worksheet=result.worksheet,

            workbook=result.workbook,

            verification=result.verification,

            verification_summary=result.summary,

            trading_plan=result.trading_plan,
        )

    def worksheet(self):

        return self.refresh().worksheet

    def workbook(self):

        return self.refresh().workbook

    def trading_plan(self):

        return self.refresh().trading_plan

    def verification(self):

        return self.refresh().verification

    def verification_summary(self):

        return self.refresh().verification_summary
