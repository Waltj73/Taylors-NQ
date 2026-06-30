# ui/price_panel.py

"""
Taylor NQ Price Panel

Displays the current market snapshot.

Presentation only.
"""

from __future__ import annotations

import streamlit as st

from engine.yahoo import Quote


class PricePanel:

    @staticmethod
    def render(quote: Quote):

        st.subheader("Market Snapshot")

        row1 = st.columns(5)

        row1[0].metric(
            "Last",
            f"{quote.price:,.2f}",
        )

        row1[1].metric(
            "Open",
            f"{quote.open:,.2f}",
        )

        row1[2].metric(
            "High",
            f"{quote.high:,.2f}",
        )

        row1[3].metric(
            "Low",
            f"{quote.low:,.2f}",
        )

        row1[4].metric(
            "Previous Close",
            f"{quote.previous_close:,.2f}",
        )

        row2 = st.columns(2)

        row2[0].metric(
            "Today's Range",
            f"{quote.high - quote.low:,.2f}",
        )

        row2[1].metric(
            "Volume",
            f"{quote.volume:,.0f}",
        )
