# ui/theme.py

"""
Taylor NQ Theme

Centralized styling for the Streamlit application.
"""

from __future__ import annotations

import streamlit as st


PRIMARY = "#1976D2"
SUCCESS = "#2E7D32"
DANGER = "#C62828"
WARNING = "#ED6C02"

BACKGROUND = "#0E1117"
CARD = "#1B1F24"
BORDER = "#30363D"
TEXT = "#FAFAFA"
SUBTEXT = "#A8B3C2"


def apply():

    st.markdown(
        f"""
<style>

html, body, [class*="css"] {{
    background-color: {BACKGROUND};
}}

[data-testid="stAppViewContainer"] {{
    background-color: {BACKGROUND};
}}

[data-testid="stHeader"] {{
    background-color: {BACKGROUND};
}}

[data-testid="stSidebar"] {{
    background-color: {CARD};
}}

div[data-testid="metric-container"] {{
    background-color: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 14px;
}}

div[data-testid="metric-container"] label {{
    color: {SUBTEXT};
}}

div[data-testid="metric-container"] div {{
    color: {TEXT};
}}

table {{
    border-collapse: collapse;
}}

thead tr {{
    background: {CARD};
}}

thead th {{
    color: white !important;
    font-weight: 700 !important;
}}

section[data-testid="stSidebar"] * {{
    color: white;
}}

hr {{
    border-color: {BORDER};
}}

.block-container {{
    padding-top: 1rem;
    padding-bottom: 1rem;
}}

</style>
""",
        unsafe_allow_html=True,
    )
