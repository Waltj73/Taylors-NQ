# ui/table_panel.py

"""
Taylor NQ Table Panel

Displays the complete Taylor calculation table.

Presentation only.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


class TablePanel:

    DEFAULT_COLUMNS = [
        "Open",
        "High",
        "Low",
        "Close",
        "Rally",
        "RallyAvg3",
        "AnticipatedHighFromLow",
        "BuyingHigh",
        "BuyingHighAvg3",
        "AnticipatedHighFromHigh",
        "PivotBreakoutHigh",
        "AvgSell",
        "Decline",
        "DeclineAvg3",
        "YesterdayHighMinusAvg",
        "BuyingLow",
        "BuyingLowAvg3",
        "YesterdayLowMinusAvg",
        "PivotBreakoutLow",
        "AvgBuy",
    ]

    @classmethod
    def render(
        cls,
        dataframe: pd.DataFrame,
    ) -> None:

        st.subheader("Taylor Calculation Table")

        available = [
            c
            for c in cls.DEFAULT_COLUMNS
            if c in dataframe.columns
        ]

        table = dataframe[available].copy()

        table = table.round(2)

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=False,
            height=700,
        )
