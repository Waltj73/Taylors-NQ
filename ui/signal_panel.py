# ui/signal_panel.py

"""
Taylor NQ Signal Panel

Displays the current Taylor signal and trading bias.

Presentation only.
"""

from __future__ import annotations

import streamlit as st

from engine.signals import DayType, SignalResult


class SignalPanel:

    @staticmethod
    def render(signal: SignalResult):

        st.subheader("Taylor Signal")

        if signal.day_type == DayType.BUY:
            st.success("BUY DAY")

        elif signal.day_type == DayType.SELL:
            st.error("SELL DAY")

        elif signal.day_type == DayType.BUY_SELL:
            st.warning("BUY / SELL DAY")

        elif signal.day_type == DayType.SELL_BUY:
            st.warning("SELL / BUY DAY")

        else:
            st.info("UNKNOWN")

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Close",
            f"{signal.close:,.2f}",
        )

        col2.metric(
            "Average Buy",
            "-"
            if signal.avg_buy is None
            else f"{signal.avg_buy:,.2f}",
        )

        col3.metric(
            "Average Sell",
            "-"
            if signal.avg_sell is None
            else f"{signal.avg_sell:,.2f}",
        )

        if signal.bullish:
            col4.success("Bullish")

        elif signal.bearish:
            col4.error("Bearish")

        else:
            col4.info("Neutral")

        st.divider()

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

        p1, p2 = st.columns(2)

        p1.metric(
            "Pivot Breakout High",
            "-"
            if signal.pivot_high is None
            else f"{signal.pivot_high:,.2f}",
        )

        p2.metric(
            "Pivot Breakout Low",
            "-"
            if signal.pivot_low is None
            else f"{signal.pivot_low:,.2f}",
        )
