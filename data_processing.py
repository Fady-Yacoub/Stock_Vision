"""
data_processing.py – Member 2: Data Processing & Analysis
Responsibilities:
  - Clean and structure stock data with Pandas
  - Extract required fields (Open, Close, High, Low, Volume)
  - Compute indicators: Moving Averages, Daily Change, VWAP
"""

import pandas as pd
import numpy as np


# ── Processing ───────────────────────────────────────────────────────────────

def process_stock_data(raw_df: pd.DataFrame) -> tuple[pd.DataFrame | None, str | None]:
    """
    Clean and structure the raw yFinance DataFrame.

    Returns
    -------
    df    : pd.DataFrame  (cleaned, columns: Open High Low Close Volume)
    error : str | None
    """
    if raw_df is None or raw_df.empty:
        return None, "No data to process."

    try:
        df = raw_df.copy()

        # ── Normalise column names ────────────────────────────────────────────
        df.columns = [c.strip().title() for c in df.columns]

        # Keep only OHLCV columns that exist
        desired = ["Open", "High", "Low", "Close", "Volume"]
        available = [c for c in desired if c in df.columns]

        if "Close" not in available:
            return None, "Dataset does not contain a 'Close' price column."

        df = df[available]

        # ── Drop timezone from index (Streamlit/Plotly friendly) ─────────────
        if hasattr(df.index, "tz") and df.index.tz is not None:
            df.index = df.index.tz_localize(None)

        # ── Drop rows where Close is NaN ──────────────────────────────────────
        df = df.dropna(subset=["Close"])

        # ── Sort chronologically ──────────────────────────────────────────────
        df = df.sort_index()

        return df, None

    except Exception as exc:
        return None, f"Data processing error: {exc}"


# ── Indicators ───────────────────────────────────────────────────────────────

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute common technical indicators and append them as new columns.

    Added columns
    -------------
    MA7         : 7-day simple moving average
    MA20        : 20-day simple moving average
    MA50        : 50-day simple moving average
    Daily_Change: absolute day-over-day close change
    Daily_Pct   : percentage day-over-day close change
    Cum_Return  : cumulative return from first data point (%)
    VWAP        : volume-weighted average price (if Volume exists)
    """
    df = df.copy()

    close = df["Close"]

    # Moving averages
    df["MA7"]  = close.rolling(window=7,  min_periods=1).mean()
    df["MA20"] = close.rolling(window=20, min_periods=1).mean()
    df["MA50"] = close.rolling(window=50, min_periods=1).mean()

    # Daily change
    df["Daily_Change"] = close.diff()
    df["Daily_Pct"]    = close.pct_change() * 100

    # Cumulative return (%)
    first_price = close.iloc[0]
    df["Cum_Return"] = ((close - first_price) / first_price) * 100

    # VWAP (requires Volume)
    if "Volume" in df.columns:
        typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
        df["VWAP"] = (typical_price * df["Volume"]).cumsum() / df["Volume"].cumsum()

    return df
