# app.py

"""
Taylor NQ
Main Application

Production entry point.
"""

from __future__ import annotations

import traceback

import streamlit as st

from config import config, ensure_directories
from engine import (
    TaylorCalculator,
    YahooData,
    YahooQuote,
    SignalEngine,
    SessionManager,
)


st.set_page_config(
    page_title=config.APP_NAME,
    layout="wide",
    initial_sidebar_state="expanded",
)

ensure_directories()


@st.cache_data(ttl=config.REFRESH_SECONDS)
def load_history():

    data = YahooData(config.SYMBOL)

    return data.latest(
        bars=250,
        interval=config.HISTORY_INTERVAL,
    )


def main():

    st.title("Taylor NQ")

    try:

        history = load_history()

        calculator = TaylorCalculator()

        calculated = calculator.calculate(history)

        latest = calculator.latest(history)

        signal = SignalEngine().evaluate(calculated)

        quote = YahooQuote(config.SYMBOL).quote()

        session = SessionManager().info()

        #
        # Header
        #

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Current Price",
            f"{quote.price:,.2f}",
        )

        c2.metric(
            "Today's High",
            f"{quote.high:,.2f}",
        )

        c3.metric(
            "Today's Low",
            f"{quote.low:,.2f}",
        )

        c4.metric(
            "Previous Close",
            f"{quote.previous_close:,.2f}",
        )

        st.divider()

        #
        # Session
        #

        s1, s2, s3 = st.columns(3)

        s1.metric(
            "Session",
            session.session.value,
        )

        s2.metric(
            "Trading Day",
            str(session.trading_day),
        )

        s3.metric(
            "Minutes Remaining",
            session.minutes_until_close,
        )

        st.divider()

        #
        # Average Buy / Sell
        #

        a1, a2 = st.columns(2)

        a1.metric(
            "Average Buy",
            f"{latest.avg_buy:,.2f}"
            if latest.avg_buy is not None
            else "-",
        )

        a2.metric(
            "Average Sell",
            f"{latest.avg_sell:,.2f}"
            if latest.avg_sell is not None
            else "-",
        )

        #
        # Pivot Levels
        #

        p1, p2 = st.columns(2)

        p1.metric(
            "Pivot Breakout High",
            f"{latest.pivot_breakout_high:,.2f}"
            if latest.pivot_breakout_high is not None
            else "-",
        )

        p2.metric(
            "Pivot Breakout Low",
            f"{latest.pivot_breakout_low:,.2f}"
            if latest.pivot_breakout_low is not None
            else "-",
        )

        st.divider()

        #
        # Signal
        #

        st.subheader("Taylor Signal")

        st.success(signal.day_type.value)

        col1, col2 = st.columns(2)

        col1.metric(
            "Above Avg Buy",
            "YES" if signal.above_avg_buy else "NO",
        )

        col2.metric(
            "Below Avg Sell",
            "YES" if signal.below_avg_sell else "NO",
        )

        st.divider()

        st.subheader("Calculation Table")

        display_columns = [
            "Open",
            "High",
            "Low",
            "Close",
            "AvgBuy",
            "AvgSell",
            "PivotBreakoutHigh",
            "PivotBreakoutLow",
            "AnticipatedHighFromLow",
            "AnticipatedHighFromHigh",
            "YesterdayHighMinusAvg",
            "YesterdayLowMinusAvg",
        ]

        st.dataframe(
            calculated[display_columns].tail(30),
            use_container_width=True,
            height=650,
        )

    except Exception:

        st.error("Application Error")

        st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
