# engine/version.py

"""
Taylor NQ Version Information
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Version:

    APP_NAME: str = "Taylor NQ"

    VERSION: str = "1.0.0"

    BUILD: str = "001"

    AUTHOR: str = "Walt Johnson"

    DESCRIPTION: str = (
        "Taylor Trading Model for Nasdaq Futures"
    )

    COPYRIGHT: str = (
        f"© {datetime.now().year} Walt Johnson"
    )


version = Version()
