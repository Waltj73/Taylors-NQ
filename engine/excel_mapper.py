# engine/excel_mapper.py

"""
Taylor NQ Excel Mapper

Maps workbook columns to internal application columns so the
verification engine can compare calculations regardless of
worksheet formatting.

No UI.
No Yahoo Finance.
"""

from __future__ import annotations

import pandas as pd


class ExcelMapper:

    def __init__(self):

        self.mapping = {}

    def learn(
        self,
        workbook: pd.DataFrame,
    ):

        self.mapping.clear()

        for column in workbook.columns:

            normalized = self.normalize(column)

            self.mapping[normalized] = column

    def workbook_column(
        self,
        internal_name: str,
    ) -> str | None:

        return self.mapping.get(
            self.normalize(internal_name)
        )

    def translate(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        rename = {}

        for internal, workbook in self.mapping.items():

            if workbook in dataframe.columns:
                rename[workbook] = internal

        return dataframe.rename(columns=rename)

    @staticmethod
    def normalize(text: str) -> str:

        return (
            str(text)
            .strip()
            .lower()
            .replace(" ", "")
            .replace("_", "")
            .replace("-", "")
            .replace("/", "")
            .replace("(", "")
            .replace(")", "")
            .replace(".", "")
        )
