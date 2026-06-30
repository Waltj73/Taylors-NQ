# engine/workbook_compiler.py

"""
Taylor Workbook Compiler

Compiles the Excel workbook into an internal calculation model.

Pipeline

Workbook
    ↓
Parser
    ↓
Formula Registry
    ↓
Dependency Graph
    ↓
Execution Order
    ↓
Compiled Workbook

This module does not execute formulas. It prepares them for execution.
"""

from __future__ import annotations

from dataclasses import dataclass

from .calculation_graph import CalculationGraph
from .workbook_parser import WorkbookParser


@dataclass(slots=True)
class CompiledColumn:

    name: str

    formula: str | None

    execution_order: int

    dependencies: list[str]


class WorkbookCompiler:

    def __init__(
        self,
        workbook_path,
        sheet_name: str = "NQ",
    ):

        self.parser = WorkbookParser(
            workbook_path
        )

        self.graph = CalculationGraph()

        self.sheet_name = sheet_name

    def compile(self):

        columns = self.parser.parse_sheet(
            self.sheet_name
        )

        graph = self.graph.build(columns)

        order = self.graph.execution_order(
            columns
        )

        compiled = []

        for index, column in enumerate(order):

            node = graph[column]

            compiled.append(
                CompiledColumn(
                    name=node.column,
                    formula=node.formula,
                    execution_order=index,
                    dependencies=node.dependencies,
                )
            )

        return compiled

    def print_execution_order(self):

        compiled = self.compile()

        for item in compiled:

            print(
                f"{item.execution_order:03d}  "
                f"{item.name:<40}  "
                f"{item.dependencies}"
            )
