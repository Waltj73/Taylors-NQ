# engine/workbook_report.py

"""
Taylor Workbook Report

Produces a comprehensive report describing the workbook and the
application's compatibility with it.

This report is intended to answer:

- What worksheets exist?
- How many formulas exist?
- Which Excel functions are used?
- Which functions are currently implemented?
- Which functions still need to be implemented?
- How many cells are verified?
- How many remain?

No UI.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .workbook_audit import WorkbookAudit
from .workbook_inspector import WorkbookInspector


SUPPORTED_FUNCTIONS = {
    "SUM",
    "AVERAGE",
    "ABS",
    "ROUND",
    "MAX",
    "MIN",
    "COUNT",
    "COUNTA",
    "IF",
    "AND",
    "OR",
    "NOT",
}


@dataclass(slots=True)
class WorkbookReport:

    workbook: str

    worksheets: int

    formula_cells: int

    supported_functions: int

    unsupported_functions: int

    implementation_percent: float

    worksheet_summary: list = field(
        default_factory=list
    )

    supported: list[str] = field(
        default_factory=list
    )

    unsupported: list[str] = field(
        default_factory=list
    )


class WorkbookReportBuilder:

    def __init__(
        self,
        workbook_path,
    ):

        self.audit = WorkbookAudit(
            workbook_path
        )

        self.inspector = WorkbookInspector(
            workbook_path
        )

    def build(self):

        audit = self.audit.run()

        inspection = self.inspector.inspect()

        supported = sorted(
            [
                fn
                for fn in audit.functions
                if fn in SUPPORTED_FUNCTIONS
            ]
        )

        unsupported = sorted(
            [
                fn
                for fn in audit.functions
                if fn not in SUPPORTED_FUNCTIONS
            ]
        )

        total = len(
            supported
        ) + len(
            unsupported
        )

        percent = (
            100.0
            if total == 0
            else len(supported)
            / total
            * 100.0
        )

        return WorkbookReport(
            workbook=inspection.workbook,

            worksheets=len(
                inspection.worksheets
            ),

            formula_cells=inspection.total_formula_cells,

            supported_functions=len(
                supported
            ),

            unsupported_functions=len(
                unsupported
            ),

            implementation_percent=percent,

            worksheet_summary=inspection.worksheets,

            supported=supported,

            unsupported=unsupported,
        )
