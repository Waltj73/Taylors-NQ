# engine/state.py

"""
Taylor NQ State

Application state container.

Acts as the single source of truth for the currently loaded
market data, calculations, workbook comparison, and signals.

No UI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd

from .models import (
    AppState,
    MarketSnapshot,
    SignalState,
    TaylorDay,
    TaylorProjection,
)
from .verify import VerificationResult


@dataclass(slots=True)
class RuntimeState:

    loaded: bool = False

    last_refresh: datetime | None = None

    history: pd.DataFrame | None = None

    calculations: pd.DataFrame | None = None

    workbook: pd.DataFrame | None = None

    verification: list[VerificationResult] = field(
        default_factory=list
    )

    verification_summary: dict = field(
        default_factory=dict
    )

    app: AppState | None = None


class StateManager:

    def __init__(self):

        self.state = RuntimeState()

    def update(
        self,
        *,
        history: pd.DataFrame,
        calculations: pd.DataFrame,
        workbook: pd.DataFrame | None,
        verification: list[VerificationResult],
        verification_summary: dict,
        market: MarketSnapshot,
        day: TaylorDay,
        projections: TaylorProjection,
        signal: SignalState,
    ):

        self.state.loaded = True

        self.state.last_refresh = datetime.now()

        self.state.history = history

        self.state.calculations = calculations

        self.state.workbook = workbook

        self.state.verification = verification

        self.state.verification_summary = verification_summary

        self.state.app = AppState(
            market=market,
            day=day,
            projections=projections,
            signal=signal,
        )

    def clear(self):

        self.state = RuntimeState()

    @property
    def loaded(self):

        return self.state.loaded

    @property
    def calculations(self):

        return self.state.calculations

    @property
    def workbook(self):

        return self.state.workbook

    @property
    def verification(self):

        return self.state.verification

    @property
    def summary(self):

        return self.state.verification_summary

    @property
    def app(self):

        return self.state.app

    @property
    def refresh_time(self):

        return self.state.last_refresh


state = StateManager()
