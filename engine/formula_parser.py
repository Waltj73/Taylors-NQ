# engine/formula_parser.py

"""
Taylor Formula Parser

Converts Excel formulas from the Taylor workbook into a structured
representation that can be analyzed, validated, and eventually
executed by the application.

This module does NOT evaluate formulas. It only parses them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


CELL_PATTERN = re.compile(r"\$?[A-Z]{1,3}\$?\d+")
RANGE_PATTERN = re.compile(r"\$?[A-Z]{1,3}\$?\d+:\$?[A-Z]{1,3}\$?\d+")


@dataclass(slots=True)
class ParsedFormula:

    original: str

    functions: list[str]

    cell_references: list[str]

    ranges: list[str]

    operators: list[str]


class FormulaParser:

    FUNCTIONS = [
        "SUM",
        "AVERAGE",
        "IF",
        "ROUND",
        "ABS",
        "MAX",
        "MIN",
        "COUNT",
        "COUNTA",
        "AND",
        "OR",
        "NOT",
    ]

    OPERATORS = [
        "+",
        "-",
        "*",
        "/",
        "^",
        "=",
        "<",
        ">",
        "<=",
        ">=",
        "<>",
    ]

    def parse(
        self,
        formula: str,
    ) -> ParsedFormula:

        if formula.startswith("="):
            formula = formula[1:]

        upper = formula.upper()

        functions = []

        for fn in self.FUNCTIONS:

            if f"{fn}(" in upper:
                functions.append(fn)

        references = CELL_PATTERN.findall(upper)

        ranges = RANGE_PATTERN.findall(upper)

        operators = []

        for op in sorted(
            self.OPERATORS,
            key=len,
            reverse=True,
        ):

            if op in upper:
                operators.append(op)

        return ParsedFormula(
            original=formula,
            functions=functions,
            cell_references=references,
            ranges=ranges,
            operators=operators,
        )

    def dependencies(
        self,
        formula: str,
    ) -> List[str]:

        return self.parse(
            formula
        ).cell_references

    def has_function(
        self,
        formula: str,
        function: str,
    ) -> bool:

        return (
            function.upper()
            in self.parse(formula).functions
        )

    def is_formula(
        self,
        value,
    ) -> bool:

        return (
            isinstance(value, str)
            and value.startswith("=")
        )
