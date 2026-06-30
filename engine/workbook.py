# engine/workbook.py

"""
Taylor NQ Workbook Loader

Loads the Taylor Excel workbook and exposes worksheets as pandas
DataFrames. This module is used to verify that the application's
calculations match the workbook exactly.

No UI.
No Yahoo Finance.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class WorkbookError(Exception):
    """Workbook could not be loaded."""


class TaylorWorkbook:

    def __init__(self, workbook: str | Path):

        self.path = Path(workbook)

        if not self.path.exists():
            raise WorkbookError(
                f"Workbook not found: {self.path}"
            )

        self.excel = pd.ExcelFile(
            self.path,
            engine="openpyxl",
        )

    @property
    def sheets(self):

        return self.excel.sheet_names

    def load_sheet(
        self,
        sheet: str | int = 0,
    ) -> pd.DataFrame:

        return pd.read_excel(
            self.path,
            sheet_name=sheet,
            engine="openpyxl",
        )

    def load_all(self):

        return {
            name: self.load_sheet(name)
            for name in self.sheets
        }

    def first_sheet(self):

        return self.load_sheet(self.sheets[0])

    def last_sheet(self):

        return self.load_sheet(self.sheets[-1])

    def sheet_exists(
        self,
        name: str,
    ) -> bool:

        return name in self.sheets

    def columns(
        self,
        sheet: str | int = 0,
    ):

        return list(
            self.load_sheet(sheet).columns
        )

    def row_count(
        self,
        sheet: str | int = 0,
    ):

        return len(
            self.load_sheet(sheet)
        )

    def compare_columns(
        self,
        dataframe: pd.DataFrame,
        sheet: str | int = 0,
    ):

        workbook_columns = set(
            self.columns(sheet)
        )

        dataframe_columns = set(
            dataframe.columns
        )

        return {
            "missing_from_dataframe": sorted(
                workbook_columns - dataframe_columns
            ),
            "extra_in_dataframe": sorted(
                dataframe_columns - workbook_columns
            ),
        }
