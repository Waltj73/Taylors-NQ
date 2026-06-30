# engine/dependency_graph.py

"""
Taylor Dependency Graph

Builds the dependency graph for every workbook formula.

This allows the workbook execution engine to determine the correct
order of calculation automatically instead of relying on manually
coded sequencing.
"""

from __future__ import annotations

from dataclasses import dataclass

from .formula_registry import FormulaRegistry
from .formula_parser import FormulaParser


@dataclass(slots=True)
class Dependency:

    cell: str

    depends_on: list[str]


class DependencyGraph:

    def __init__(self):

        self.parser = FormulaParser()

    def build(
        self,
        registry: FormulaRegistry,
        sheet: str = "NQ",
    ) -> dict[str, Dependency]:

        graph = {}

        for item in registry.sheet(sheet):

            deps = self.parser.dependencies(
                item.formula
            )

            graph[item.address] = Dependency(
                cell=item.address,
                depends_on=deps,
            )

        return graph

    def execution_order(
        self,
        registry: FormulaRegistry,
        sheet: str = "NQ",
    ) -> list[str]:

        graph = self.build(
            registry,
            sheet,
        )

        ordered = []

        visited = set()

        def visit(node: str):

            if node in visited:
                return

            visited.add(node)

            dependency = graph.get(node)

            if dependency:

                for dep in dependency.depends_on:

                    if dep in graph:

                        visit(dep)

            ordered.append(node)

        for node in graph:

            visit(node)

        return ordered
