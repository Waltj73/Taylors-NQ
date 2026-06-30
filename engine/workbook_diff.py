# engine/workbook_diff.py

"""
Taylor Workbook Difference Engine

Performs a full row-by-row, column-by-column comparison between the
Excel workbook and the application's calculated output.

Unlike workbook_validator.py, this module is designed to generate
a detailed reconciliation report showing every mismatch.

No UI.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class Difference:

    row: int

    column: str

    workbook: object

    calculated: object

    delta: float | None

    match: bool


class WorkbookDiff:

    def __init__(
        self,
        tolerance: float = 0.01,
    ):

        self.tolerance = tolerance

    def compare(
        self,
        workbook: pd.DataFrame,
        calculated: pd.DataFrame,
    ) -> list[Difference]:

        differences: list[Difference] = []

        common = [
            c
            for c in workbook.columns
            if c in calculated.columns
        ]

        rows = min(
            len(workbook),
            len(calculated),
        )

        for row in range(rows):

            wb = workbook.iloc[row]

            calc = calculated.iloc[row]

            for column in common:

                left = wb[column]
                right = calc[column]

                if self._equal(left, right):

                    differences.append(
                        Difference(
                            row=row,
                            column=column,
                            workbook=left,
                            calculated=right,
                            delta=self._delta(
                                left,
                                right,
                            ),
                            match=True,
                        )
                    )

                else:

                    differences.append(
                        Difference(
                            row=row,
                            column=column,
                            workbook=left,
                            calculated=right,
                            delta=self._delta(
                                left,
                                right,
                            ),
                            match=False,
                        )
                    )

        return differences

    def mismatches(
        self,
        workbook: pd.DataFrame,
        calculated: pd.DataFrame,
    ) -> list[Difference]:

        return [
            d
            for d in self.compare(
                workbook,
                calculated,
            )
            if not d.match
        ]

    def matches(
        self,
        workbook: pd.DataFrame,
        calculated: pd.DataFrame,
    ) -> list[Difference]:

        return [
            d
            for d in self.compare(
                workbook,
                calculated,
            )
            if d.match
        ]

    def summary(
        self,
        workbook: pd.DataFrame,
        calculated: pd.DataFrame,
    ):

        comparison = self.compare(
            workbook,
            calculated,
        )

        total = len(comparison)

        matched = sum(
            d.match
            for d in comparison
        )

        failed = total - matched

        return {
            "cells": total,
            "matched": matched,
            "failed": failed,
            "accuracy": (
                0.0
                if total == 0
                else matched / total * 100.0
            ),
        }

    def _equal(
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

    @staticmethod
    def _delta(
        left,
        right,
    ):

        try:

            return (
                float(right)
                - float(left)
            )

        except Exception:

            return None
