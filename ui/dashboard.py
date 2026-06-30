# ui/dashboard.py

"""
Taylor NQ Dashboard

Responsible only for rendering the Streamlit interface.

No calculations.
No Yahoo downloads.
No business logic.
"""

from __future__ import annotations

import streamlit as st
import pandas as pd

from engine.signals import SignalResult
from engine.calculations import TaylorLevels
from engine.session import SessionInfo
from engine.yahoo import Quote


class Dashboard:

    @staticmethod
    def render(
        *,
        quote: Quote,
        session: SessionInfo,
        levels: TaylorLevels,
        signal: SignalResult,
        calculations: pd.DataFrame,
    ) -> None:

        Dashboard._header(quote)
        Dashboard._session(session)
        Dashboard._levels(levels)
        Dashboard._signal(signal)
        Dashboard._table(calculations)

    @staticmethod
    def _header(quote: Quote):

        st.title("Taylor NQ")

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Price",
            f"{quote.price:,.2f}",
        )

        c2.metric(
            "Open",
            f"{quote.open:,.2f}",
        )

        c3.metric(
            "High",
            f"{quote.high:,.2f}",
        )

        c4.metric(
            "Low",
            f"{quote.low:,.2f}",
        )

        c5.metric(
            "Prev Close",
            f"{quote.previous_close:,.2f}",
        )

        st.divider()

    @staticmethod
    def _session(session: SessionInfo):

        st.subheader("Trading Session")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Session",
            session.session.value,
        )

        c2.metric(
            "Trading Day",
            str(session.trading_day),
        )

        c3.metric(
            "Minutes Open",
            session.minutes_since_open,
        )

        c4.metric(
            "Minutes Remaining",
            session.minutes_until_close,
        )

        st.divider()

    @staticmethod
    def _levels(levels: TaylorLevels):

        st.subheader("Taylor Levels")

        r1 = st.columns(4)

        r1[0].metric(
            "Avg Buy",
            Dashboard._fmt(levels.avg_buy),
        )

        r1[1].metric(
            "Avg Sell",
            Dashboard._fmt(levels.avg_sell),
        )

        r1[2].metric(
            "Pivot High",
            Dashboard._fmt(levels.pivot_breakout_high),
        )

        r1[3].metric(
            "Pivot Low",
            Dashboard._fmt(levels.pivot_breakout_low),
        )

        r2 = st.columns(4)

        r2[0].metric(
            "Ant. High (Low)",
            Dashboard._fmt(levels.anticipated_high_from_low),
        )

        r2[1].metric(
            "Ant. High (High)",
            Dashboard._fmt(levels.anticipated_high_from_high),
        )

        r2[2].metric(
            "Yesterday High Avg",
            Dashboard._fmt(levels.yesterday_high_minus_avg),
        )

        r2[3].metric(
            "Yesterday Low Avg",
            Dashboard._fmt(levels.yesterday_low_minus_avg),
        )

        st.divider()

    @staticmethod
    def _signal(signal: SignalResult):

        st.subheader("Taylor Signal")

        color = "green"

        if signal.day_type.value.startswith("SELL"):
            color = "red"

        st.markdown(
            f"## :{color}[{signal.day_type.value}]"
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Above Avg Buy",
            "YES" if signal.above_avg_buy else "NO",
        )

        c2.metric(
            "Below Avg Sell",
            "YES" if signal.below_avg_sell else "NO",
        )

        st.divider()

    @staticmethod
    def _table(df: pd.DataFrame):

        st.subheader("Taylor Calculation Table")

        st.dataframe(
            df,
            use_container_width=True,
            height=650,
        )

    @staticmethod
    def _fmt(value):

        if value is None:
            return "-"

        return f"{value:,.2f}"
