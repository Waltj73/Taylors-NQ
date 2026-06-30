from __future__ import annotations

import time
from datetime import datetime

import pandas as pd
import streamlit as st

from config import config
from engine.service import TaylorService
from engine.version import version
from ui.footer import Footer
from ui.help_panel import HelpPanel


# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="Taylor NQ",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----------------------------------------------------------
# Session State
# ----------------------------------------------------------

if "service" not in st.session_state:
    st.session_state.service = TaylorService()

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = None

if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = True

if "refresh_seconds" not in st.session_state:
    st.session_state.refresh_seconds = 30

if "state" not in st.session_state:
    st.session_state.state = None

service = st.session_state.service


# ----------------------------------------------------------
# Sidebar
# ----------------------------------------------------------

with st.sidebar:

    st.title("Taylor NQ")
    st.caption(f"Version {version.VERSION}")

    st.divider()

    st.session_state.auto_refresh = st.checkbox(
        "Auto Refresh",
        value=st.session_state.auto_refresh,
    )

    st.session_state.refresh_seconds = st.slider(
        "Refresh Interval (Seconds)",
        min_value=5,
        max_value=300,
        value=st.session_state.refresh_seconds,
        step=5,
    )

    st.divider()

    if st.button(
        "Refresh Now",
        use_container_width=True,
    ):
        st.session_state.last_refresh = None
        st.rerun()

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Trading Plan",
            "Workbook",
            "Verification",
            "Raw Data",
            "Help",
        ],
    )


# ----------------------------------------------------------
# Refresh Data
# ----------------------------------------------------------

refresh_required = False

if st.session_state.last_refresh is None:
    refresh_required = True

elif st.session_state.auto_refresh:

    elapsed = (
        datetime.now()
        - st.session_state.last_refresh
    ).total_seconds()

    refresh_required = (
        elapsed >= st.session_state.refresh_seconds
    )

if refresh_required:

    with st.spinner("Loading market data..."):
        state = service.refresh()

    st.session_state.state = state
    st.session_state.last_refresh = datetime.now()

else:

    state = st.session_state.state


# ----------------------------------------------------------
# Header
# ----------------------------------------------------------

st.title("Taylor Trading Model")

left, right = st.columns([3, 1])

with left:
    st.caption(f"Symbol: {config.SYMBOL}")

with right:

    if st.session_state.last_refresh:
        st.caption(
            "Last Refresh: "
            + st.session_state.last_refresh.strftime("%H:%M:%S")
        )

st.divider()
# ----------------------------------------------------------
# Dashboard
# ----------------------------------------------------------

if page == "Dashboard":

    latest = state.calculations.iloc[-1]

    st.subheader("Today's Market")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Current Price",
            f"{latest['Close']:,.2f}",
        )

    with m2:
        st.metric(
            "Average Buy",
            f"{latest['AverageBuy']:,.2f}",
        )

    with m3:
        st.metric(
            "Average Sell",
            f"{latest['AverageSell']:,.2f}",
        )

    with m4:
        st.metric(
            "Today's Range",
            f"{latest['High'] - latest['Low']:.2f}",
        )

    st.divider()

    left, right = st.columns([1, 1])

    with left:

        st.subheader("Taylor Levels")

        levels = pd.DataFrame(
            {
                "Level": [
                    "Buying High",
                    "Buying Low",
                    "Average Buy",
                    "Average Sell",
                    "Breakout High",
                    "Breakout Low",
                    "Projected High",
                    "Projected High (From Low)",
                ],
                "Value": [
                    latest["BuyingHigh"],
                    latest["BuyingLow"],
                    latest["AverageBuy"],
                    latest["AverageSell"],
                    latest["TomorrowBreakoutHigh"],
                    latest["TomorrowBreakoutLow"],
                    latest["TomorrowAnticipatedHighFromHigh"],
                    latest["TomorrowAnticipatedHighFromLow"],
                ],
            }
        )

        st.dataframe(
            levels,
            use_container_width=True,
            hide_index=True,
        )

    with right:

        st.subheader("Recent Close")

        chart = state.history.tail(100)

        st.line_chart(chart["Close"])

    st.divider()

    st.subheader("Latest Taylor Calculation")

    st.dataframe(
        latest.to_frame().T,
        use_container_width=True,
        hide_index=True,
    )
    # ----------------------------------------------------------
# Trading Plan
# ----------------------------------------------------------

elif page == "Trading Plan":

    latest = state.calculations.iloc[-1]

    st.subheader("Today's Taylor Trading Plan")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Average Buy",
            f"{latest['AverageBuy']:,.2f}",
        )

        st.metric(
            "Buying High",
            f"{latest['BuyingHigh']:,.2f}",
        )

        st.metric(
            "Buying Low",
            f"{latest['BuyingLow']:,.2f}",
        )

        st.metric(
            "Breakout Low",
            f"{latest['TomorrowBreakoutLow']:,.2f}",
        )

        st.metric(
            "Yesterday Low Minus Avg",
            f"{latest['YesterdayLowMinusAverage']:,.2f}",
        )

    with c2:

        st.metric(
            "Average Sell",
            f"{latest['AverageSell']:,.2f}",
        )

        st.metric(
            "Today's High",
            f"{latest['TodaysHigh']:,.2f}",
        )

        st.metric(
            "Today's Low",
            f"{latest['TodaysLow']:,.2f}",
        )

        st.metric(
            "Breakout High",
            f"{latest['TomorrowBreakoutHigh']:,.2f}",
        )

        st.metric(
            "Yesterday High Minus Avg",
            f"{latest['YesterdayHighMinusAverage']:,.2f}",
        )

    st.divider()

    st.subheader("Projected Levels")

    projections = pd.DataFrame(
        {
            "Description": [
                "Tomorrow Anticipated High (From High)",
                "Tomorrow Anticipated High (From Low)",
                "Tomorrow Breakout High",
                "Tomorrow Breakout Low",
                "Average Buy",
                "Average Sell",
            ],
            "Value": [
                latest["TomorrowAnticipatedHighFromHigh"],
                latest["TomorrowAnticipatedHighFromLow"],
                latest["TomorrowBreakoutHigh"],
                latest["TomorrowBreakoutLow"],
                latest["AverageBuy"],
                latest["AverageSell"],
            ],
        }
    )

    st.dataframe(
        projections,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Latest Calculation Row")

    st.dataframe(
        latest.to_frame().T,
        use_container_width=True,
        hide_index=True,
    )
    # ----------------------------------------------------------
# Workbook
# ----------------------------------------------------------

elif page == "Workbook":

    st.subheader("Taylor Workbook")

    if state.workbook is None:

        st.error("Workbook could not be loaded.")

    else:

        st.dataframe(
            state.workbook,
            use_container_width=True,
            height=700,
        )


# ----------------------------------------------------------
# Verification
# ----------------------------------------------------------

elif page == "Verification":

    st.subheader("Workbook Verification")

    if state.summary is None:

        st.warning("Verification unavailable.")

    else:

        a, b, c = st.columns(3)

        a.metric(
            "Cells",
            state.summary["cells"],
        )

        b.metric(
            "Matched",
            state.summary["matched"],
        )

        c.metric(
            "Accuracy",
            f"{state.summary['accuracy']:.2f}%"
        )

        st.divider()

        if state.verification:

            verify = pd.DataFrame(
                [vars(x) for x in state.verification]
            )

            st.dataframe(
                verify,
                use_container_width=True,
                height=650,
            )

        else:

            st.success(
                "Workbook matches calculation engine."
            )


# ----------------------------------------------------------
# Raw Data
# ----------------------------------------------------------

elif page == "Raw Data":

    st.subheader("Historical Data")

    st.dataframe(
        state.history,
        use_container_width=True,
        height=300,
    )

    st.divider()

    st.subheader("Calculated Taylor Worksheet")

    st.dataframe(
        state.calculations,
        use_container_width=True,
        height=650,
    )


# ----------------------------------------------------------
# Help
# ----------------------------------------------------------

elif page == "Help":

    HelpPanel.render()


# ----------------------------------------------------------
# Footer
# ----------------------------------------------------------

Footer.render()


# ----------------------------------------------------------
# Auto Refresh
# ----------------------------------------------------------

if st.session_state.auto_refresh:

    time.sleep(1)

    st.rerun()
