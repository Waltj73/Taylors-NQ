# ui/footer.py

"""
Taylor NQ Footer

Application footer.

Presentation only.
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from engine.version import version


class Footer:

    @staticmethod
    def render():

        st.divider()

        left, center, right = st.columns(3)

        with left:
            st.caption(
                f"{version.APP_NAME} v{version.VERSION}"
            )

        with center:
            st.caption(
                datetime.now().strftime(
                    "%A, %B %d, %Y  %I:%M:%S %p"
                )
            )

        with right:
            st.caption(
                version.COPYRIGHT
            )
