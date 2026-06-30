# ui/workbook_panel.py

"""
Taylor NQ Workbook Verification Panel

Displays the calculated values beside the Excel workbook values
to verify that the application matches the Taylor workbook.

Presentation only.
"""

from __future__ import annotations

import streamlit as st
import pandas as pd


class WorkbookPanel:

    @staticmethod
    def render(
        calculated: pd.DataFrame,
        workbook: pd.DataFrame | None = None,
    ):

        st.subheader("Workbook Verification")

        if workbook is None:

            st.info(
                "No workbook loaded.\n\n"
                "Place Taylors NQ.xlsx inside the data folder "
                "to enable workbook comparison."
            )

            return

        left, right = st.columns(2)

        with left:

            st.markdown("### Excel Workbook")

            st.dataframe(
                workbook.tail(25),
                use_container_width=True,
                height=650,
            )

        with right:

            st.markdown("### Application")

            st.dataframe(
                calculated.tail(25),
                use_container_width=True,
                height=650,
            )
