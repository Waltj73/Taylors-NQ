# engine/named_ranges.py

"""
Taylor Named Range Manager

Loads and exposes all Excel Named Ranges from the Taylor workbook.

This allows the application to reference workbook-defined names
instead of hard-coded cell references whenever possible.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from openpyxl import load_workbook


@dataclass(slots=True)
class NamedRange:

    name: str

    destination: str

    sheet: str


class NamedRangeManager:

    def __init__(
        self,
        workbook: str | Path,
    ):

        self.path = Path(workbook)

        self.workbook = load_workbook(
            self.path,
            data_only=False,
        )

        self._ranges = self._load()

    def _load(self):

        results = {}

        for defined_name in self.workbook.defined_names.definedName:

            destinations = list(
                defined_name.destinations
            )

            if not destinations:
                continue

            sheet, destination = destinations[0]

            results[defined_name.name] = NamedRange(
                name=defined_name.name,
                destination=destination,
                sheet=sheet,
            )

        return results

    @property
    def names(self):

        return sorted(
            self._ranges.keys()
        )

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._ranges

    def get(
        self,
        name: str,
    ) -> NamedRange | None:

        return self._ranges.get(name)

    def destination(
        self,
        name: str,
    ) -> str | None:

        item = self.get(name)

        if item is None:
            return None

        return item.destination

    def sheet(
        self,
        name: str,
    ) -> str | None:

        item = self.get(name)

        if item is None:
            return None

        return item.sheet

    def as_dict(self):

        return {
            name: {
                "sheet": item.sheet,
                "destination": item.destination,
            }
            for name, item in self._ranges.items()
        }
