# ui/sidebar.py

"""
Taylor NQ Sidebar

Application controls and summary panel.
"""

from __future__ import annotations

import streamlit as st

from engine.session import SessionInfo
from engine.signals import SignalResult
from engine.calculations import TaylorLevels
from engine.yahoo import Quote


class Sidebar:

    @staticmethod
    def render(
        *,
        quote: Quote,
        session: SessionInfo,
        signal: SignalResult,
        levels: TaylorLevels,
    ):

        sb = st.sidebar

        sb.title("Taylor NQ")

        sb.markdown("---")

        sb.subheader("Market")

        sb.write(f"**Symbol:** {quote.symbol}")
        sb.write(f"**Price:** {quote.price:,.2f}")
        sb.write(f"**Open:** {quote.open:,.2f}")
        sb.write(f"**High:** {quote.high:,.2f}")
        sb.write(f"**Low:** {quote.low:,.2f}")
        sb.write(f"**Prev Close:** {quote.previous_close:,.2f}")

        sb.markdown("---")

        sb.subheader("Trading Session")

        sb.write(f"**Session:** {session.session.value}")
        sb.write(f"**Trading Day:** {session.trading_day}")
        sb.write(f"**Minutes Remaining:** {session.minutes_until_close}")

        sb.markdown("---")

        sb.subheader("Taylor Signal")

        if signal.day_type.value.startswith("BUY"):
            sb.success(signal.day_type.value)
        elif signal.day_type.value.startswith("SELL"):
            sb.error(signal.day_type.value)
        else:
            sb.warning(signal.day_type.value)

        sb.markdown("---")

        sb.subheader("Primary Levels")

        Sidebar.level("Average Buy", levels.avg_buy)
        Sidebar.level("Average Sell", levels.avg_sell)
        Sidebar.level("Pivot High", levels.pivot_breakout_high)
        Sidebar.level("Pivot Low", levels.pivot_breakout_low)

        sb.markdown("---")

        sb.subheader("Calculated Levels")

        Sidebar.level(
            "Anticipated High (Low)",
            levels.anticipated_high_from_low,
        )

        Sidebar.level(
            "Anticipated High (High)",
            levels.anticipated_high_from_high,
        )

        Sidebar.level(
            "Yesterday High Avg",
            levels.yesterday_high_minus_avg,
        )

        Sidebar.level(
            "Yesterday Low Avg",
            levels.yesterday_low_minus_avg,
        )

        sb.markdown("---")

        sb.caption("Taylor NQ")

    @staticmethod
    def level(name: str, value):

        if value is None:
            st.sidebar.write(f"**{name}:** —")
        else:
            st.sidebar.write(f"**{name}:** {value:,.2f}")
