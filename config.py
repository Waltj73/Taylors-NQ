# config.py

"""
Application configuration for the Taylor NQ application.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

ENGINE_DIR = BASE_DIR / "engine"

ASSETS_DIR = BASE_DIR / "assets"

DATA_DIR = BASE_DIR / "data"

LOG_DIR = BASE_DIR / "logs"

CACHE_DIR = BASE_DIR / "cache"

ICON_FILE = ASSETS_DIR / "icon.ico"

EXCEL_REFERENCE = DATA_DIR / "Taylors NQ.xlsx"


@dataclass(frozen=True)
class AppConfig:

    #
    # Application
    #

    APP_NAME: str = "Taylor NQ"

    VERSION: str = "1.0.0"

    REFRESH_SECONDS: int = 5

    #
    # Market
    #

    SYMBOL: str = "NQ=F"

    HISTORY_PERIOD: str = "2y"

    HISTORY_INTERVAL: str = "1d"

    INTRADAY_INTERVAL: str = "1m"

    #
    # Display
    #

    PRICE_DECIMALS: int = 2

    LEVEL_DECIMALS: int = 2

    #
    # Files
    #

    EXCEL_WORKBOOK: Path = EXCEL_REFERENCE

    CACHE_FOLDER: Path = CACHE_DIR

    LOG_FOLDER: Path = LOG_DIR

    ASSET_FOLDER: Path = ASSETS_DIR

    #
    # Colors
    #

    BUY_COLOR: str = "#00C853"

    SELL_COLOR: str = "#D50000"

    NEUTRAL_COLOR: str = "#757575"

    BACKGROUND: str = "#111111"

    PANEL: str = "#1E1E1E"

    TEXT: str = "#FFFFFF"

    WARNING: str = "#FFA000"

    #
    # Fonts
    #

    FONT: str = "Segoe UI"

    FONT_SIZE: int = 11

    TITLE_SIZE: int = 18

    HEADER_SIZE: int = 14

    #
    # Window
    #

    WINDOW_TITLE: str = "Taylor NQ"

    WINDOW_WIDTH: int = 1450

    WINDOW_HEIGHT: int = 900

    SIDEBAR_WIDTH: int = 300


config = AppConfig()


def ensure_directories() -> None:

    for directory in (
        DATA_DIR,
        CACHE_DIR,
        LOG_DIR,
        ASSETS_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)
