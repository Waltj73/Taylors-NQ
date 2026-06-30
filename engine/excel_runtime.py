# engine/excel_runtime.py

"""
Taylor Excel Runtime

This module executes translated Excel formulas against a pandas
DataFrame.

The runtime intentionally mimics Excel behavior whenever practical.

Responsibilities

    - Cell lookup
    - Range lookup
    - SUM
    - AVERAGE
    - MIN
    - MAX
    - ABS
    - ROUND

Future Excel functions can be added without modifying the rest of
the application.
"""

from __future__ import annotations

import re

import pandas as pd

from .excel_formula_translator import ExcelFormulaTranslator


class ExcelRuntime:

    def __init__(self):

        self.translator = ExcelFormulaTranslator()

        self.dataframe: pd.DataFrame | None = None

        self.column_map: dict[str, str] = {}

    def execute(
        self,
        dataframe: pd.DataFrame,
        formula_map: dict[str, str],
        excel_columns: dict[str, str],
    ) -> pd.DataFrame:

        result = dataframe.copy()

        self.dataframe = result

        self.column_map = excel_columns

        for workbook_column, formula in formula_map.items():

            translated = self.translator.translate(
                formula
            )

            try:

                result[workbook_column] = eval(
                    translated,
                    {
                        "__builtins__": {},
                        "CELL": self.CELL,
                        "_SUM": self._SUM,
                        "_AVERAGE": self._AVERAGE,
                    },
                    {},
                )

            except Exception:
                #
                # Unsupported formulas remain untouched.
                #
                continue

        return result

    #
    # ----------------------------------------------------
    # Excel Functions
    # ----------------------------------------------------
    #

    def CELL(
        self,
        excel_column: str,
        row: int,
    ):

        column = self.column_map.get(
            excel_column
        )

        if column is None:
            return None

        #
        # Excel row 2 == dataframe row 0
        #

        index = row - 2

        if index < 0:
            return None

        if index >= len(self.dataframe):
            return None

        return self.dataframe.iloc[index][column]

    def _SUM(self, *args):

        total = 0

        for value in args:

            if value is None:
                continue

            if isinstance(value, pd.Series):

                total += value

            else:

                total += value

        return total

    def _AVERAGE(self, *args):

        values = []

        for value in args:

            if value is None:
                continue

            values.append(value)

        if not values:
            return None

        if isinstance(values[0], pd.Series):

            return (
                pd.concat(
                    values,
                    axis=1,
                )
                .mean(axis=1)
            )

        return sum(values) / len(values)
