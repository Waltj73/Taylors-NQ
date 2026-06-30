# engine/workbook_pipeline.py

"""
Taylor Workbook Pipeline

This is the master pipeline that transforms live Yahoo Finance data
into a workbook-equivalent calculation model.

Pipeline

Yahoo Finance
      │
      ▼
WorkbookAdapter
      │
      ▼
WorksheetBuilder
      │
      ▼
WorkbookCompiler
      │
      ▼
ExcelRuntime
      │
      ▼
WorkbookValidator
      │
      ▼
Finished Taylor Worksheet

The goal is for the returned DataFrame to be indistinguishable from
the Excel workbook.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .excel_runtime import ExcelRuntime
from .workbook_adapter import WorkbookAdapter
from .workbook_compiler import WorkbookCompiler
from .workbook_loader import WorkbookLoader
from .workbook_parser import WorkbookParser
from .workbook_validator import WorkbookValidator
from .worksheet_builder import WorksheetBuilder


class WorkbookPipeline:

    def __init__(
        self,
        workbook: str | Path,
        sheet: str = "NQ",
    ):

        self.workbook = Path(workbook)

        self.sheet = sheet

        self.loader = WorkbookLoader(
            self.workbook
        )

        self.parser = WorkbookParser(
            self.workbook
        )

        self.adapter = WorkbookAdapter()

        self.builder = WorksheetBuilder()

        self.compiler = WorkbookCompiler(
            self.workbook,
            sheet_name=sheet,
        )

        self.runtime = ExcelRuntime()

        self.validator = WorkbookValidator()

    def run(
        self,
        yahoo_dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Execute the complete workbook pipeline.
        """

        #
        # Step 1
        #

        worksheet = self.builder.build(
            yahoo_dataframe
        )

        #
        # Step 2
        #

        formulas = self.parser.formula_map(
            self.sheet
        )

        #
        # Step 3
        #

        excel_columns = {}

        for column in self.parser.parse_sheet(
            self.sheet
        ):

            excel_columns[
                column.excel_column
            ] = column.title

        #
        # Step 4
        #

        calculated = self.runtime.execute(
            worksheet,
            formulas,
            excel_columns,
        )

        return calculated

    def verify(
        self,
        workbook_dataframe: pd.DataFrame,
        calculated_dataframe: pd.DataFrame,
    ):

        return self.validator.validate(
            workbook_dataframe,
            calculated_dataframe,
        )

    def workbook_formulas(self):

        return self.parser.formula_map(
            self.sheet
        )

    def workbook_columns(self):

        return self.parser.parse_sheet(
            self.sheet
        )

    def compiled_columns(self):

        return self.compiler.compile()
