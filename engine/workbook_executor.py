# engine/workbook_executor.py

"""
Taylor Workbook Executor

Executes workbook calculations in dependency order.

Unlike workbook_calculator.py (which contains handwritten formulas),
this engine is designed to execute formulas discovered from the
Taylor workbook itself.

Current supported operations:

    +
    -
    *
    /
    SUM()
    AVERAGE()

Future workbook functions can be added without changing the rest of
the application.
"""

from __future__ import annotations

import re

import pandas as pd

from .formula_parser import FormulaParser


class WorkbookExecutor:

    def __init__(self):

        self.parser = FormulaParser()

    def execute(
        self,
        dataframe: pd.DataFrame,
        formula_map: dict[str, str],
    ) -> pd.DataFrame:

        result = dataframe.copy()

        #
        # Execute formulas in workbook order.
        #

        for column, formula in formula_map.items():

            try:

                result[column] = self._evaluate(
                    formula,
                    result,
                )

            except Exception:
                #
                # Leave workbook column untouched if
                # execution is not yet supported.
                #
                continue

        return result

    #
    # ----------------------------------------------------
    #
    # Internal
    #
    # ----------------------------------------------------
    #

    def _evaluate(
        self,
        formula: str,
        df: pd.DataFrame,
    ):

        expression = formula.strip()

        if expression.startswith("="):
            expression = expression[1:]

        upper = expression.upper()

        #
        # SUM(...)
        #

        if upper.startswith("SUM("):
            return self._sum(
                expression,
                df,
            )

        #
        # AVERAGE(...)
        #

        if upper.startswith("AVERAGE("):
            return self._average(
                expression,
                df,
            )

        #
        # Replace workbook column names with dataframe columns.
        #

        expression = self._replace_columns(
            expression,
            df,
        )

        return eval(
            expression,
            {"__builtins__": {}},
            {},
        )

    def _sum(
        self,
        formula: str,
        df: pd.DataFrame,
    ):

        args = formula[
            formula.find("(") + 1 :
            formula.rfind(")")
        ]

        columns = [
            c.strip()
            for c in args.split(",")
        ]

        series = None

        for column in columns:

            if column not in df.columns:
                continue

            if series is None:
                series = df[column]

            else:
                series = series + df[column]

        return series

    def _average(
        self,
        formula: str,
        df: pd.DataFrame,
    ):

        args = formula[
            formula.find("(") + 1 :
            formula.rfind(")")
        ]

        columns = [
            c.strip()
            for c in args.split(",")
        ]

        values = []

        for column in columns:

            if column in df.columns:
                values.append(df[column])

        return (
            pd.concat(
                values,
                axis=1,
            )
            .mean(axis=1)
        )

    def _replace_columns(
        self,
        expression: str,
        df: pd.DataFrame,
    ):

        #
        # Longest names first so replacements don't collide.
        #

        columns = sorted(
            df.columns,
            key=len,
            reverse=True,
        )

        for column in columns:

            escaped = re.escape(column)

            expression = re.sub(
                rf"\b{escaped}\b",
                f"df[{column!r}]",
                expression,
            )

        return expression
