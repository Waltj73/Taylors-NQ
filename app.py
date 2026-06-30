# app.py

import streamlit as st

from data.loader import DataLoader
from engine.taylor_engine import TaylorEngine

st.set_page_config(
    page_title="Taylor Workstation",
    page_icon="📈",
    layout="wide",
)

st.title("Taylor Workstation")

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    st.header("Settings")

    symbol = st.selectbox(
        "Market",
        [
            "NQ=F",
            "ES=F",
            "YM=F",
            "RTY=F",
            "CL=F",
            "GC=F",
        ],
        index=0,
    )

    years = st.selectbox(
        "History",
        [
            "1y",
            "2y",
            "5y",
            "10y",
        ],
        index=2,
    )

    refresh = st.button(
        "Refresh Data",
        use_container_width=True,
    )

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

loader = DataLoader()

try:

    with st.spinner("Downloading market data..."):

        df = loader.from_yahoo(
            symbol=symbol,
            period=years,
            interval="1d",
        )

except Exception as e:

    st.error(str(e))
    st.stop()

# -------------------------------------------------------
# Run Taylor Engine
# -------------------------------------------------------

engine = TaylorEngine(df)

try:

    levels = engine.latest()

except Exception as e:

    st.error(str(e))
    st.stop()

# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.success(f"Latest Trading Day: {levels.date}")

# -------------------------------------------------------
# Daily OHLC
# -------------------------------------------------------

st.subheader("Current Daily Candle")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Open",
    f"{levels.open:,.2f}",
)

c2.metric(
    "High",
    f"{levels.high:,.2f}",
)

c3.metric(
    "Low",
    f"{levels.low:,.2f}",
)

c4.metric(
    "Close",
    f"{levels.close:,.2f}",
)

st.divider()

# -------------------------------------------------------
# Taylor Levels
# -------------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Sell Side")

    st.metric(
        "Projected High #1",
        f"{levels.projected_high_1:,.2f}",
    )

    st.metric(
        "Projected High #2",
        f"{levels.projected_high_2:,.2f}",
    )

    st.metric(
        "Average Sell",
        f"{levels.average_sell:,.2f}",
    )

    st.metric(
        "Breakout Buy",
        f"{levels.breakout_buy:,.2f}",
    )

with right:

    st.subheader("Buy Side")

    st.metric(
        "Projected Low #1",
        f"{levels.projected_low_1:,.2f}",
    )

    st.metric(
        "Projected Low #2",
        f"{levels.projected_low_2:,.2f}",
    )

    st.metric(
        "Average Buy",
        f"{levels.average_buy:,.2f}",
    )

    st.metric(
        "Breakout Sell",
        f"{levels.breakout_sell:,.2f}",
    )

st.divider()

st.subheader("Pivot")

st.metric(
    "Pivot",
    f"{levels.pivot:,.2f}",
)

# -------------------------------------------------------
# Raw Data
# -------------------------------------------------------

with st.expander("Daily Data"):

    st.dataframe(
        df.tail(20),
        use_container_width=True,
        hide_index=True,
    )
