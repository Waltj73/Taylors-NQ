# ui/levels_panel.py

"""
Taylor NQ Levels Panel

Displays all calculated Taylor levels in a structured layout.

No calculations.
No data downloads.
No business logic.
"""

from __future__ import annotations

import streamlit as st

from engine.calculations import TaylorLevels


class LevelsPanel:

    @staticmethod
    def render(levels: TaylorLevels):

        st.subheader("Taylor Price Levels")

        col1, col2, col3 = st.columns(3)

        #
        # BUY LEVELS
        #

        with col1:

            st.markdown("### 🟢 Buy Levels")

            LevelsPanel.metric(
                "Average Buy",
                levels.avg_buy,
            )

            LevelsPanel.metric(
                "Pivot Breakout Low",
                levels.pivot_breakout_low,
            )

            LevelsPanel.metric(
                "Buying Low",
                levels.buying_low,
            )

            LevelsPanel.metric(
                "Buying Low Avg",
                levels.buying_low_avg,
            )

            LevelsPanel.metric(
                "Yesterday Low Avg",
                levels.yesterday_low_minus_avg,
            )

        #
        # SELL LEVELS
        #

        with col2:

            st.markdown("### 🔴 Sell Levels")

            LevelsPanel.metric(
                "Average Sell",
                levels.avg_sell,
            )

            LevelsPanel.metric(
                "Pivot Breakout High",
                levels.pivot_breakout_high,
            )

            LevelsPanel.metric(
                "Buying High",
                levels.buying_high,
            )

            LevelsPanel.metric(
                "Buying High Avg",
                levels.buying_high_avg,
            )

            LevelsPanel.metric(
                "Yesterday High Avg",
                levels.yesterday_high_minus_avg,
            )

        #
        # PROJECTED LEVELS
        #

        with col3:

            st.markdown("### 🔵 Projected")

            LevelsPanel.metric(
                "Rally",
                levels.rally,
            )

            LevelsPanel.metric(
                "Rally Avg",
                levels.rally_avg,
            )

            LevelsPanel.metric(
                "Decline",
                levels.decline,
            )

            LevelsPanel.metric(
                "Decline Avg",
                levels.decline_avg,
            )

            LevelsPanel.metric(
                "Projected High (Low)",
                levels.anticipated_high_from_low,
            )

            LevelsPanel.metric(
                "Projected High (High)",
                levels.anticipated_high_from_high,
            )

    @staticmethod
    def metric(label: str, value):

        if value is None:
            st.metric(label, "-")
        else:
            st.metric(label, f"{value:,.2f}")
