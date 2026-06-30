# engine/reconciliation.py

"""
Taylor Workbook Reconciliation Engine

This module produces a reconciliation report between the source
Excel workbook and the application's calculated values.

Unlike WorkbookDiff, this engine groups mismatches by row and
column, making it much easier to diagnose why a calculation differs
from Excel.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass(slots=True)
class CellMismatch:

    row: int

    column: str

    workbook_value: object

    application_value: object

    difference: float | None


@dataclass(slots=True)
class RowReconciliation:

    row: int

    mismatches: list[CellMismatch] = field(
        default_factory=list
    )


class ReconciliationEngine:

    def __init__(
        self,
        tolerance: float = 0.01,
    ):

        self.tolerance = tolerance

    def reconcile(
        self,
        workbook: pd.DataFrame,
        application: pd.DataFrame,
    ) -> list[RowReconciliation]:

        common = [
            c
            for c in workbook.columns
            if c in application.columns
        ]

        rows = min(
            len(workbook),
            len(application),
        )

        report = []

        for row in range(rows):

            reconciliation = RowReconciliation(
                row=row
            )

            wb = workbook.iloc[row]
            app = application.iloc[row]

            for column in common:

                left = wb[column]
                right = app[column]

                if self._matches(
                    left,
                    right,
                ):
                    continue

                reconciliation.mismatches.append(
                    CellMismatch(
                        row=row,
                        column=column,
                        workbook_value=left,
                        application_value=right,
                        difference=self._difference(
                            left,
                            right,
                        ),
                    )
                )

            if reconciliation.mismatches:

                report.append(
                    reconciliation
                )

        return report

    def passed(
        self,
        workbook: pd.DataFrame,
        application: pd.DataFrame,
    ) -> bool:

        return (
            len(
                self.reconcile(
                    workbook,
                    application,
                )
            )
            == 0
        )

    @staticmethod
    def _difference(
        left,
        right,
    ):

        try:

            return float(right) - float(left)

        except Exception:

            return None

    def _matches(
        self,
        left,
        right,
    ) -> bool:

        if pd.isna(left) and pd.isna(right):
            return True

        try:

            return (
                abs(
                    float(left)
                    - float(right)
                )
                <= self.tolerance
            )

        except Exception:

            return str(left) == str(right)
