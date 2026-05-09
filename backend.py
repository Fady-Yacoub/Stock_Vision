"""
backend.py – Member 1: Project Lead / Backend Developer
Responsibilities:
  - yFinance API integration
  - Stock symbol validation
  - Data fetching (current + historical)
  - Error handling
"""

import re
import yfinance as yf


# ── Validation ───────────────────────────────────────────────────────────────

def validate_symbol(symbol: str) -> tuple[bool, str]:
    """
    Validate that a stock symbol looks reasonable before hitting the API.
    Returns (is_valid: bool, error_message: str).
    """
    if not symbol:
        return False, "Stock symbol cannot be empty."

    # Basic format check: 1–5 uppercase letters (optionally with . or -)
    if not re.match(r"^[A-Z]{1,5}([.\-][A-Z]{1,3})?$", symbol):
        return False, (
            f"'{symbol}' doesn't look like a valid ticker symbol. "
            "Examples: AAPL, TSLA, BRK.B"
        )

    return True, ""


# ── Fetch ────────────────────────────────────────────────────────────────────

def fetch_stock_data(symbol: str, period: str = "1mo") -> tuple:
    """
    Fetch historical OHLCV data and company info via yFinance.

    Returns
    -------
    raw_data : pd.DataFrame | None
    info     : dict
    error    : str | None
    """
    try:
        ticker = yf.Ticker(symbol)

        # Fetch historical data
        hist = ticker.history(period=period)

        if hist is None or (hasattr(hist, "empty") and hist.empty):
            return None, {}, (
                f"No data found for symbol '{symbol}'. "
                "It may be delisted, misspelled, or not available on Yahoo Finance."
            )

        # Fetch company info (best-effort – don't fail if unavailable)
        try:
            info = ticker.info or {}
        except Exception:
            info = {}

        # If info looks empty/invalid (common with some tickers), try fast_info
        if not info.get("longName"):
            try:
                fi = ticker.fast_info
                info.setdefault("longName",             symbol)
                info.setdefault("currentPrice",         getattr(fi, "last_price",      None))
                info.setdefault("previousClose",        getattr(fi, "previous_close",  None))
                info.setdefault("dayHigh",              getattr(fi, "day_high",        None))
                info.setdefault("dayLow",               getattr(fi, "day_low",         None))
                info.setdefault("fiftyTwoWeekHigh",     getattr(fi, "year_high",       None))
                info.setdefault("fiftyTwoWeekLow",      getattr(fi, "year_low",        None))
                info.setdefault("volume",               getattr(fi, "last_volume",     None))
            except Exception:
                pass

        return hist, info, None

    except Exception as exc:
        return None, {}, f"Failed to fetch data for '{symbol}': {exc}"
