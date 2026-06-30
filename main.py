# main.py

"""
Taylor NQ

Application launcher.

Run with:

    streamlit run main.py
"""

from __future__ import annotations

import streamlit as st

from config import config, ensure_directories
from engine import (
    YahooData,
    YahooQuote,
    TaylorCalculator,
    SignalEngine,
    SessionManager,
)
from ui.dashboard import Dashboard
from ui.theme import apply


st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply()

ensure_directories()


@st.cache_data(ttl=config.REFRESH_SECONDS)
def load_data():

    return YahooData(config.SYMBOL).latest(
        bars=250,
        interval=config.HISTORY_INTERVAL,
    )


def run():

    history = load_data()

    calculator = TaylorCalculator()

    calculations = calculator.calculate(history)

    levels = calculator.latest(history)

    signal = SignalEngine().evaluate(calculations)

    quote = YahooQuote(config.SYMBOL).quote()

    session = SessionManager().info()

    Dashboard.render(
        quote=quote,
        session=session,
        levels=levels,
        signal=signal,
        calculations=calculations,
    )


if __name__ == "__main__":
    run()
