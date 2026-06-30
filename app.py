import streamlit as st

from data.loader import DataLoader
from engine.taylor_engine import TaylorEngine

st.set_page_config(
    page_title="Taylor Workstation",
    layout="wide"
)

st.title("Taylor Workstation")

loader = DataLoader()

df = loader.from_yahoo()

engine = TaylorEngine(df)

levels = engine.latest()

st.divider()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Open",
    f"{levels.open:.2f}"
)

c2.metric(
    "High",
    f"{levels.high:.2f}"
)

c3.metric(
    "Low",
    f"{levels.low:.2f}"
)

c4.metric(
    "Close",
    f"{levels.close:.2f}"
)

st.divider()

c1, c2 = st.columns(2)

with c1:

    st.subheader("Projected Highs")

    st.metric(
        "Projection 1",
        f"{levels.projected_high_1:.2f}"
    )

    st.metric(
        "Projection 2",
        f"{levels.projected_high_2:.2f}"
    )

    st.metric(
        "Average Sell",
        f"{levels.average_sell:.2f}"
    )

with c2:

    st.subheader("Projected Lows")

    st.metric(
        "Projection 1",
        f"{levels.projected_low_1:.2f}"
    )

    st.metric(
        "Projection 2",
        f"{levels.projected_low_2:.2f}"
    )

    st.metric(
        "Average Buy",
        f"{levels.average_buy:.2f}"
    )

st.divider()

c1, c2 = st.columns(2)

c1.metric(
    "Breakout Buy",
    f"{levels.breakout_buy:.2f}"
)

c2.metric(
    "Breakout Sell",
    f"{levels.breakout_sell:.2f}"
)

st.divider()

st.metric(
    "Pivot",
    f"{levels.pivot:.2f}"
)
