# ui/statusbar.py

"""
Taylor NQ Status Bar

Displays live application status information.

No calculations.
No Yahoo downloads.
No business logic.
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from engine.session import SessionInfo


class StatusBar:

    @staticmethod
    def render(session: SessionInfo):

        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        c1.info(
            f"Session: {session.session.value}"
        )

        c2.info(
            f"Trading Day: {session.trading_day}"
        )

        c3.info(
            f"Updated: {datetime.now().strftime('%H:%M:%S')}"
        )

        if session.is_open:
            c4.success("MARKET OPEN")
        else:
            c4.error("MARKET CLOSED")
