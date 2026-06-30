# engine/excel_formula_translator.py

"""
Taylor Excel Formula Translator

Converts native Excel formulas into executable pandas expressions.

This module is the bridge between the Excel workbook and the Python
runtime.  Its responsibility is ONLY translation—it does not execute
formulas.

Supported (current)

    +
    -
    *
    /
    ^
    SUM()
    AVERAGE()
    ABS()
    MIN()
    MAX()
    ROUND()

Additional Excel functions can be added without changing any other
part of the application.
"""

from __future__ import annotations

import re


class ExcelFormulaTranslator:

    CELL = re.compile(r"(?<![A-Z])([A-Z]{1,3})(\d+)")

    FUNCTIONS = {
        "SUM": "_SUM",
        "AVERAGE": "_AVERAGE",
        "ABS": "abs",
        "MIN": "min",
        "MAX": "max",
        "ROUND": "round",
    }

    def translate(
        self,
        formula: str,
    ) -> str:

        if not formula:
            return ""

        expression = formula.strip()

        if expression.startswith("="):
            expression = expression[1:]

        #
        # Excel functions
        #

        for excel, python in self.FUNCTIONS.items():

            expression = re.sub(
                rf"\b{excel}\(",
                f"{python}(",
                expression,
                flags=re.IGNORECASE,
            )

        #
        # Power
        #

        expression = expression.replace("^", "**")

        #
        # Cell references
        #
        # C5 -> CELL("C",5)
        #

        expression = self.CELL.sub(
            lambda m: (
                f'CELL("{m.group(1)}",{m.group(2)})'
            ),
            expression,
        )

        return expression

    def dependencies(
        self,
        formula: str,
    ) -> list[str]:

        refs = self.CELL.findall(formula)

        return [
            f"{c}{r}"
            for c, r in refs
        ]

    def contains_range(
        self,
        formula: str,
    ) -> bool:

        return ":" in formula

    def contains_function(
        self,
        formula: str,
    ) -> bool:

        return "(" in formula

    def supported(
        self,
        formula: str,
    ) -> bool:

        text = formula.upper()

        unsupported = [
            "OFFSET(",
            "INDIRECT(",
            "INDEX(",
            "MATCH(",
            "XLOOKUP(",
            "VLOOKUP(",
            "HLOOKUP(",
        ]

        return not any(
            fn in text
            for fn in unsupported
        )
