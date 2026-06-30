# engine/verify.py

"""
Taylor NQ Workbook Verification Engine

Compares application calculations against the Excel workbook.

No UI.
No Yahoo Finance.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(slots=True)
class VerificationResult:

    column: str

    workbook_value: float | None

    calculated_value: float | None

    difference: float | None

    passed: bool


class WorkbookVerifier:

    def __init__(
        self,
        tolerance: float = 0.01,
    ):

        self.tolerance = tolerance

    def verify_last_row(
        self,
        workbook: pd.DataFrame,
        calculated: pd.DataFrame,
    ) -> list[VerificationResult]:

        results = []

        common = [
            c
            for c in workbook.columns
            if c in calculated.columns
        ]

        wb = workbook.iloc[-1]
        calc = calculated.iloc[-1]

        for column in common:

            w = self._number(wb[column])
            c = self._number(calc[column])

            if w is None or c is None:

                results.append(
                    VerificationResult(
                        column=column,
                        workbook_value=w,
                        calculated_value=c,
                        difference=None,
                        passed=w == c,
                    )
                )

                continue

            diff = abs(w - c)

            results.append(
                VerificationResult(
                    column=column,
                    workbook_value=w,
                    calculated_value=c,
                    difference=diff,
                    passed=diff <= self.tolerance,
                )
            )

        return results

    def summary(
        self,
        workbook: pd.DataFrame,
        calculated: pd.DataFrame,
    ):

        results = self.verify_last_row(
            workbook,
            calculated,
        )

        passed = sum(r.passed for r in results)

        failed = len(results) - passed

        return {
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "percent": (
                0
                if len(results) == 0
                else passed / len(results) * 100
            ),
        }

    @staticmethod
    def _number(value):

        if pd.isna(value):
            return None

        try:
            return float(value)
        except Exception:
            return None
