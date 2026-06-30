# engine/worksheet_builder.py

"""
Taylor Worksheet Builder

Builds an in-memory representation of the Taylor workbook from
Yahoo Finance data.

This module prepares the worksheet exactly as Excel expects before
the formula engine executes.

Responsibilities

    Yahoo Data
        ↓
    Workbook Adapter
        ↓
    Worksheet Builder
        ↓
    Excel Runtime
"""

from __future__ import annotations

import pandas as pd

from .workbook_adapter import WorkbookAdapter


class WorksheetBuilder:

    def __init__(self):

        self.adapter = WorkbookAdapter()

    def build(
        self,
        yahoo_dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Build a workbook-compatible worksheet.
        """

        worksheet = self.adapter.adapt(
            yahoo_dataframe
        )

        #
        # Ensure workbook column ordering.
        #

        ordered = []

        for column in self.adapter.workbook_columns():

            if column in worksheet.columns:
                ordered.append(column)

        worksheet = worksheet[ordered]

        #
        # Excel-style row numbering.
        #
        # Workbook formulas begin on row 5.
        #

        worksheet.index = range(
            5,
            len(worksheet) + 5,
        )

        worksheet.index.name = "ExcelRow"

        return worksheet

    def append(
        self,
        worksheet: pd.DataFrame,
        new_bar: pd.Series,
    ) -> pd.DataFrame:
        """
        Append a new market bar while preserving
        Excel-style row numbering.
        """

        frame = worksheet.copy()

        next_row = frame.index.max() + 1

        values = {}

        for column in frame.columns:

            values[column] = new_bar.get(
                column,
                pd.NA,
            )

        frame.loc[next_row] = values

        return frame

    @staticmethod
    def excel_row(
        worksheet: pd.DataFrame,
        row_number: int,
    ) -> pd.Series:

        return worksheet.loc[row_number]

    @staticmethod
    def latest(
        worksheet: pd.DataFrame,
    ) -> pd.Series:

        return worksheet.iloc[-1]

    @staticmethod
    def previous(
        worksheet: pd.DataFrame,
    ) -> pd.Series:

        return worksheet.iloc[-2]
