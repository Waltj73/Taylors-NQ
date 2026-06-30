# ui/help_panel.py

"""
Taylor NQ Help Panel

Displays application information and quick reference.

Presentation only.
"""

from __future__ import annotations

import streamlit as st


class HelpPanel:

    @staticmethod
    def render():

        with st.expander("Application Help", expanded=False):

            st.markdown(
                """
### Taylor NQ

This application calculates the Taylor Trading levels using the
Taylor workbook as the source of truth.

---

### Data Source

- Live Quotes: Yahoo Finance
- Historical Data: Yahoo Finance
- Verification: Taylors NQ.xlsx

---

### Primary Levels

**Average Buy**

The average projected buying level.

**Average Sell**

The average projected selling level.

**Pivot Breakout High**

Taylor breakout resistance.

**Pivot Breakout Low**

Taylor breakout support.

---

### Day Types

🟢 **BUY DAY**

Expect buying opportunities.

🔴 **SELL DAY**

Expect selling opportunities.

🟡 **BUY / SELL DAY**

Both sides may trade.

🟠 **SELL / BUY DAY**

Early weakness followed by buying.

---

### Workbook Verification

The verification page compares every calculated value against the
Excel workbook to ensure the application matches the workbook.

---
"""
            )
