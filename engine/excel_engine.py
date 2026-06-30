# engine/excel_engine.py

"""
Taylor Excel Engine

THIS is the engine that should ultimately replace calculations.py.

Its responsibility is simple:

    1. Load Yahoo Finance OHLC data.
    2. Populate the workbook input columns.
    3. Execute the EXACT workbook formulas.
    4. Return a dataframe identical to Excel.

No approximations.
No rewritten math.
No alternate formulas.

The workbook is the source of truth.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .workbook_parser import WorkbookParser
from .workbook_runtime import WorkbookRuntime


class TaylorExcelEngine:

    def __init__(
        self,
        workbook: str | Path,
        sheet: str = "NQ",
    ):

        self.workbook = Path(workbook)

        self.sheet = sheet

        self.runtime = WorkbookRuntime(
            workbook=self.workbook,
            sheet=sheet,
        )

        self.parser = WorkbookParser(
            workbook=self.workbook,
        )

    def calculate(
        self,
        yahoo_dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Primary entry point.

        Parameters
        ----------
        yahoo_dataframe

            DataFrame containing

                Open
                High
                Low
                Close

        Returns
        -------
        DataFrame

            Workbook calculations.
        """

        #
        # Copy so we never mutate source data.
        #

        dataframe = yahoo_dataframe.copy()

        #
        # Normalize names to match workbook.
        #

        dataframe = dataframe.rename(
            columns={
                "Open": "Open",
                "High": "High",
                "Low": "Low",
                "Close": "Close",
            }
        )

        #
        # Execute workbook.
        #

        return self.runtime.calculate(
            dataframe
        )

    def execution_order(self):

        return self.runtime.execution_order()

    def workbook_columns(self):

        return self.runtime.workbook_columns()

    def workbook_formulas(self):

        return self.runtime.workbook_formulas()
