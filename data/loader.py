"""
Taylor Workstation
Data Loader

Version: 0.2
"""

from pathlib import Path

import pandas as pd
import yfinance as yf


class DataLoader:

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Download Daily Data
    # ---------------------------------------------------------

    def from_yahoo(
        self,
        symbol="NQ=F",
        period="5y",
        interval="1d"
    ) -> pd.DataFrame:

        df = yf.download(
            symbol,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False,
            group_by="column",
            multi_level_index=False,
        )

        if df.empty:
            raise ValueError(f"No data returned for {symbol}")

        # Flatten MultiIndex if Yahoo returns one
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()

        # Keep only the columns we need
        required = [
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
        ]

        df = df[required]

        # Make sure numeric columns are numeric
        numeric_cols = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna()

        return df

    # ---------------------------------------------------------
    # Load CSV
    # ---------------------------------------------------------

    def from_csv(self, filename):

        filename = Path(filename)

        if not filename.exists():
            raise FileNotFoundError(filename)

        return pd.read_csv(filename)

    # ---------------------------------------------------------
    # Save CSV
    # ---------------------------------------------------------

    def save_csv(self, df, filename):

        filename = Path(filename)

        df.to_csv(
            filename,
            index=False,
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
            sheet_name=sheet_name,
        )
