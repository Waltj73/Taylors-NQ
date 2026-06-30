# engine/workbook_runtime.py

"""
Taylor Workbook Runtime

Coordinates the workbook-driven calculation pipeline.

Execution Flow

Excel Workbook
      │
      ▼
WorkbookParser
      │
      ▼
CalculationGraph
      │
      ▼
WorkbookCompiler
      │
      ▼
WorkbookExecutor
      │
      ▼
Calculated DataFrame

This is the runtime entry point for workbook-based calculations.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .calculation_engine import CalculationEngine
from .workbook_parser import WorkbookParser
from .workbook_compiler import WorkbookCompiler
from .workbook_validator import WorkbookValidator


class WorkbookRuntime:

    def __init__(
        self,
        workbook: str | Path,
        sheet: str = "NQ",
    ):

        self.workbook = Path(workbook)

        self.sheet = sheet

        self.parser = WorkbookParser(
            self.workbook
        )

        self.compiler = WorkbookCompiler(
            self.workbook,
            sheet_name=sheet,
        )

        self.engine = CalculationEngine(
            self.workbook,
            sheet_name=sheet,
        )

        self.validator = WorkbookValidator()

    def calculate(
        self,
        market_data: pd.DataFrame,
    ) -> pd.DataFrame:

        return self.engine.calculate(
            market_data
        )

    def validate(
        self,
        workbook_dataframe: pd.DataFrame,
        calculated_dataframe: pd.DataFrame,
    ):

        return self.validator.validate(
            workbook_dataframe,
            calculated_dataframe,
        )

    def compile(self):

        return self.compiler.compile()

    def workbook_columns(self):

        return self.parser.parse_sheet(
            self.sheet
        )

    def workbook_formulas(self):

        return self.parser.formula_map(
            self.sheet
        )

    def execution_order(self):

        compiled = self.compile()

        return [
            column.name
            for column in sorted(
                compiled,
                key=lambda x: x.execution_order,
            )
        )
