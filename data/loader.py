"""
Taylor Workstation
Data Loader

Version: 0.1
"""

from pathlib import Path
import pandas as pd
import yfinance as yf


class DataLoader:

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Download from Yahoo Finance
    # ---------------------------------------------------------

    def from_yahoo(
        self,
        symbol: str = "NQ=F",
        period: str = "5y",
        interval: str = "1d"
    ) -> pd.DataFrame:

        df = yf.download(
            symbol,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False
        )

        if df.empty:
            raise ValueError(f"No data returned for {symbol}")

        df.reset_index(inplace=True)

        df = df[[
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]]

        return df

    # ---------------------------------------------------------
    # Load CSV
    # ---------------------------------------------------------

    def from_csv(
        self,
        filename
    ) -> pd.DataFrame:

        filename = Path(filename)

        if not filename.exists():
            raise FileNotFoundError(filename)

        df = pd.read_csv(filename)

        return df

    # ---------------------------------------------------------
    # Save CSV
    # ---------------------------------------------------------

    def save_csv(
        self,
        df,
        filename
    ):

        filename = Path(filename)

        df.to_csv(
            filename,
            index=False
        )

    # ---------------------------------------------------------
    # Load Excel
    # ---------------------------------------------------------

    def from_excel(
        self,
        filename,
        sheet_name=0
    ):

        filename = Path(filename)

        if not filename.exists():
            raise FileNotFoundError(filename)

        return pd.read_excel(
            filename,
            sheet_name=sheet_name
        )
