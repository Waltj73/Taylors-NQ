# engine/taylor_sequence.py

"""
Taylor Sequence Engine

Maintains the rolling Taylor sequence using the workbook data.

This module does not determine BUY/SELL logic. It simply tracks the
Taylor sequence so the trading model always knows where it is within
the cycle.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import pandas as pd


class Sequence(Enum):

    DAY1 = 1
    DAY2 = 2
    DAY3 = 3


@dataclass(slots=True)
class SequenceState:

    trading_date: pd.Timestamp

    sequence: Sequence

    previous: Sequence | None

    next: Sequence


class TaylorSequence:

    def build(
        self,
        dataframe: pd.DataFrame,
    ) -> list[SequenceState]:

        states = []

        for i, (idx, _) in enumerate(dataframe.iterrows()):

            current = self._sequence(i)

            previous = (
                None
                if i == 0
                else self._sequence(i - 1)
            )

            next_day = self._sequence(i + 1)

            states.append(
                SequenceState(
                    trading_date=idx,
                    sequence=current,
                    previous=previous,
                    next=next_day,
                )
            )

        return states

    def latest(
        self,
        dataframe: pd.DataFrame,
    ) -> SequenceState:

        return self.build(dataframe)[-1]

    @staticmethod
    def _sequence(index: int) -> Sequence:

        remainder = index % 3

        if remainder == 0:
            return Sequence.DAY1

        if remainder == 1:
            return Sequence.DAY2

        return Sequence.DAY3
