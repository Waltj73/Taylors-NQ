# engine/service.py

"""
Taylor NQ Service Layer

Central application service used by the UI. Handles loading,
refreshing, verification, and exposes a single object to the
presentation layer.

No Streamlit code.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from config import config
from .loader import Loader
from .verify import WorkbookVerifier


@dataclass(slots=True)
class ServiceResult:

    history: pd.DataFrame

    calculations: pd.DataFrame

    levels: object

    signal: object

    quote: object

    session: object

    workbook: pd.DataFrame | None

    verification: list | None

    summary: dict | None


class TaylorService:

    def __init__(self):

        self.loader = Loader()

        self.verifier = WorkbookVerifier()

    def refresh(self) -> ServiceResult:

        data = self.loader.load()

        verification = None
        summary = None

        if data.workbook is not None:

            try:

                verification = self.verifier.verify_last_row(
                    workbook=data.workbook,
                    calculated=data.calculations,
                )

                summary = self.verifier.summary(
                    workbook=data.workbook,
                    calculated=data.calculations,
                )

            except Exception:

                verification = None
                summary = None

        return ServiceResult(
            history=data.history,
            calculations=data.calculations,
            levels=data.levels,
            signal=data.signal,
            quote=data.quote,
            session=data.session,
            workbook=data.workbook,
            verification=verification,
            summary=summary,
        )
