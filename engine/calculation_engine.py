# engine/calculation_engine.py

"""
Taylor Calculation Engine

This is the central calculation engine for the application.

Unlike workbook_calculator.py, this engine executes workbook
calculations in dependency order using the calculation graph.

Eventually this will become the ONLY calculation engine used by
the application.
"""

from __future__ import annotations

import pandas as pd

from .calculation_graph import CalculationGraph
from .workbook_executor import WorkbookExecutor
from .workbook_parser import WorkbookParser


class CalculationEngine:

    def __init__(
        self,
        workbook_path,
        sheet_name: str = "NQ",
    ):

        self.parser = WorkbookParser(
            workbook_path
        )

        self.executor = WorkbookExecutor()

        self.graph = CalculationGraph()

        self.sheet_name = sheet_name

    def calculate(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        #
        # Parse workbook
        #

        columns = self.parser.parse_sheet(
            self.sheet_name
        )

        #
        # Determine execution order
        #

        execution_order = (
            self.graph.execution_order(
                columns
            )
        )

        #
        # Workbook formulas
        #

        formula_lookup = {
            c.title: c.formula
            for c in columns
            if c.formula
        }

        #
        # Execute formulas
        #

        result = dataframe.copy()

        for column in execution_order:

            formula = formula_lookup.get(
                column
            )

            if formula is None:
                continue

            try:

                value = self.executor._evaluate(
                    formula,
                    result,
                )

                result[column] = value

            except Exception:

                #
                # Unsupported workbook functions
                # are skipped until implemented.
                #

                continue

        return result

    def formula_map(self):

        return self.parser.formula_map(
            self.sheet_name
        )

    def execution_order(self):

        columns = self.parser.parse_sheet(
            self.sheet_name
        )

        return self.graph.execution_order(
            columns
        )

    def workbook_columns(self):

        return self.parser.parse_sheet(
            self.sheet_name
        )
