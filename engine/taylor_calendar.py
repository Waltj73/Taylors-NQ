# engine/taylor_calendar.py

"""
Taylor Calendar

Implements the Taylor Trading three-day cycle.

Day 1 -> Buy Day
Day 2 -> Sell Day
Day 3 -> Short Sell Day

The sequence repeats continuously while allowing manual overrides
from the workbook if desired.

No UI.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum


class TaylorCycle(Enum):

    BUY = 1

    SELL = 2

    SHORT_SELL = 3


@dataclass(slots=True)
class CalendarDay:

    trading_day: date

    cycle_day: TaylorCycle

    sequence: int


class TaylorCalendar:

    def __init__(
        self,
        anchor_date: date,
        anchor_cycle: TaylorCycle = TaylorCycle.BUY,
    ):

        self.anchor_date = anchor_date
        self.anchor_cycle = anchor_cycle

    def cycle_for(
        self,
        trading_day: date,
    ) -> CalendarDay:

        delta = (trading_day - self.anchor_date).days

        offset = delta % 3

        if self.anchor_cycle == TaylorCycle.BUY:

            mapping = [
                TaylorCycle.BUY,
                TaylorCycle.SELL,
                TaylorCycle.SHORT_SELL,
            ]

        elif self.anchor_cycle == TaylorCycle.SELL:

            mapping = [
                TaylorCycle.SELL,
                TaylorCycle.SHORT_SELL,
                TaylorCycle.BUY,
            ]

        else:

            mapping = [
                TaylorCycle.SHORT_SELL,
                TaylorCycle.BUY,
                TaylorCycle.SELL,
            ]

        return CalendarDay(
            trading_day=trading_day,
            cycle_day=mapping[offset],
            sequence=offset + 1,
        )

    def next_day(
        self,
        trading_day: date,
    ) -> CalendarDay:

        return self.cycle_for(
            trading_day + timedelta(days=1)
        )

    def previous_day(
        self,
        trading_day: date,
    ) -> CalendarDay:

        return self.cycle_for(
            trading_day - timedelta(days=1)
        )
