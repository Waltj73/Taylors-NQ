# engine/workbook_validator.py

"""
Taylor Workbook Validator

Performs validation against the source Excel workbook.

The purpose of this class is to guarantee that every calculated
Taylor value matches the workbook before the application is used
for live trading.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class ValidationError:

    row: int

    column: str

    workbook: float | str | None

    application: float | str | None

    difference: float | None


class WorkbookValidator:

    def __init__(
        self,
        tolerance: float = 0.01,
    ):

        self.tolerance = tolerance

    def validate(
        self,
        workbook: pd.DataFrame,
        calculated: pd.DataFrame,
    ) -> list[ValidationError]:

        errors: list[ValidationError] = []

        common = [
            c
            for c in workbook.columns
            if c in calculated.columns
        ]

        rows = min(
            len(workbook),
            len(calculated),
        )

        for r in range(rows):

            wb = workbook.iloc[r]

            calc = calculated.iloc[r]

            for column in common:

                left = self._value(
                    wb[column]
                )

                right = self._value(
                    calc[column]
                )

                if left is None and right is None:
                    continue

                if left is None or right is None:

                    errors.append(
                        ValidationError(
                            row=r,
                            column=column,
                            workbook=left,
                            application=right,
                            difference=None,
                        )
                    )

                    continue

                difference = abs(
                    left - right
                )

                if difference > self.tolerance:

                    errors.append(
                        ValidationError(
                            row=r,
                            column=column,
                            workbook=left,
                            application=right,
                            difference=difference,
                        )
                    )

        return errors

    def passed(
        self,
        workbook: pd.DataFrame,
        calculated: pd.DataFrame,
    ) -> bool:

        return (
            len(
                self.validate(
                    workbook,
                    calculated,
                )
            )
            == 0
        )

    @staticmethod
    def _value(value):

        try:

            if pd.isna(value):
                return None

            return float(value)

        except Exception:

            return None
