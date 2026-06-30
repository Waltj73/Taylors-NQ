# engine/calculation_graph.py

"""
Taylor Calculation Graph

Builds the calculation dependency graph using workbook columns
instead of hard-coded execution order.

The purpose of this module is to determine exactly which workbook
columns depend on other workbook columns before calculations are
performed.

This is one of the final pieces needed before replacing the
handwritten calculator with a workbook-driven calculator.
"""

from __future__ import annotations

from dataclasses import dataclass

from .formula_parser import FormulaParser
from .workbook_parser import WorkbookColumn


@dataclass(slots=True)
class CalculationNode:

    column: str

    formula: str | None

    dependencies: list[str]


class CalculationGraph:

    def __init__(self):

        self.parser = FormulaParser()

    def build(
        self,
        columns: list[WorkbookColumn],
    ) -> dict[str, CalculationNode]:

        #
        # Map Excel column letters -> workbook titles
        #

        excel_lookup = {
            c.excel_column: c.title
            for c in columns
        }

        graph = {}

        for column in columns:

            dependencies = []

            if column.formula:

                refs = self.parser.dependencies(
                    column.formula
                )

                #
                # Convert A12 -> A -> Workbook Column
                #

                for ref in refs:

                    letter = "".join(
                        ch
                        for ch in ref
                        if ch.isalpha()
                    )

                    if letter in excel_lookup:

                        title = excel_lookup[
                            letter
                        ]

                        if (
                            title
                            not in dependencies
                        ):
                            dependencies.append(
                                title
                            )

            graph[column.title] = CalculationNode(
                column=column.title,
                formula=column.formula,
                dependencies=dependencies,
            )

        return graph

    def execution_order(
        self,
        columns: list[WorkbookColumn],
    ) -> list[str]:

        graph = self.build(columns)

        ordered = []

        visited = set()

        def visit(node: str):

            if node in visited:
                return

            visited.add(node)

            current = graph[node]

            for dependency in current.dependencies:

                if dependency in graph:

                    visit(dependency)

            ordered.append(node)

        for node in graph:

            visit(node)

        return ordered
