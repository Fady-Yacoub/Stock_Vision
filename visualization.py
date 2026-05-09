"""
visualization.py – Member 3: Visualization Developer
Responsibilities:
  - Stock trend charts (line, candlestick)
  - Volume bar chart
  - Moving averages overlay
  - Interactive Plotly figures with consistent dark theme
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


# ── Theme constants ───────────────────────────────────────────────────────────

DARK_BG        = "#0a0e1a"
CARD_BG        = "#0f1629"
GRID_COLOR     = "#1e2d4a"
TEXT_COLOR     = "#94a3b8"
ACCENT_BLUE    = "#3b82f6"
ACCENT_GREEN   = "#10b981"
ACCENT_RED     = "#ef4444"
ACCENT_YELLOW  = "#f59e0b"
ACCENT_PURPLE  = "#8b5cf6"

MA_COLORS = {
    "MA7":  "#f59e0b",   # amber
    "MA20": "#8b5cf6",   # purple
    "MA50": "#06b6d4",   # cyan
}

_LAYOUT_BASE = dict(
    paper_bgcolor = DARK_BG,
    plot_bgcolor  = CARD_BG,
    font          = dict(family="JetBrains Mono, monospace", color=TEXT_COLOR, size=11),
    margin        = dict(l=10, r=10, t=40, b=10),
    legend        = dict(
        bgcolor     = "#111827",
        bordercolor = GRID_COLOR,
        borderwidth = 1,
        font        = dict(size=11),
    ),
    xaxis = dict(
        gridcolor    = GRID_COLOR,
        showgrid     = True,
        zeroline     = False,
        tickfont     = dict(color=TEXT_COLOR),
        rangeslider  = dict(visible=False),
    ),
    yaxis = dict(
        gridcolor = GRID_COLOR,
        showgrid  = True,
        zeroline  = False,
        tickfont  = dict(color=TEXT_COLOR),
    ),
    hovermode = "x unified",
)


def _apply_base(fig: go.Figure, title: str = "") -> go.Figure:
    layout = dict(_LAYOUT_BASE)
    if title:
        layout["title"] = dict(
            text     = title,
            font     = dict(size=14, color="#e2e8f0"),
            x        = 0.01,
            xanchor  = "left",
        )
    fig.update_layout(**layout)
    return fig


# ── 1. Line chart ─────────────────────────────────────────────────────────────

def plot_price_trend(df: pd.DataFrame, symbol: str) -> go.Figure:
    """
    Gradient-filled area line chart of closing price.
    """
    close = df["Close"]
    is_up = close.iloc[-1] >= close.iloc[0]
    line_color = ACCENT_GREEN if is_up else ACCENT_RED
    fill_color = "rgba(16,185,129,0.15)" if is_up else "rgba(239,68,68,0.15)"

    fig = go.Figure()

    # Filled area
    fig.add_trace(go.Scatter(
        x     = df.index,
        y     = close,
        mode  = "lines",
        name  = "Close",
        line  = dict(color=line_color, width=2),
        fill  = "tozeroy",
        fillcolor = fill_color,
        hovertemplate = "%{x|%b %d, %Y}<br>Close: <b>%{y:.2f}</b><extra></extra>",
    ))

    _apply_base(fig, f"{symbol} – Closing Price")
    fig.update_layout(height=420)
    return fig


# ── 2. Candlestick chart ──────────────────────────────────────────────────────

def plot_candlestick(df: pd.DataFrame, symbol: str) -> go.Figure:
    """
    OHLC candlestick chart with custom green/red candles.
    """
    if not all(c in df.columns for c in ["Open", "High", "Low", "Close"]):
        # Fall back to line chart
        return plot_price_trend(df, symbol)

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x     = df.index,
        open  = df["Open"],
        high  = df["High"],
        low   = df["Low"],
        close = df["Close"],
        name  = "OHLC",
        increasing = dict(line=dict(color=ACCENT_GREEN), fillcolor="rgba(16,185,129,0.7)"),
        decreasing = dict(line=dict(color=ACCENT_RED),   fillcolor="rgba(239,68,68,0.7)"),
    ))

    _apply_base(fig, f"{symbol} – Candlestick")
    fig.update_layout(height=420)
    fig.update_xaxes(rangeslider_visible=False)
    return fig


# ── 3. Volume bar chart ───────────────────────────────────────────────────────

def plot_volume(df: pd.DataFrame, symbol: str) -> go.Figure:
    """
    Volume bars coloured green/red based on price direction.
    """
    if "Volume" not in df.columns:
        return go.Figure()

    # Colour each bar by price direction
    price_up = df["Close"].diff().fillna(0) >= 0
    colors   = [ACCENT_GREEN if up else ACCENT_RED for up in price_up]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x         = df.index,
        y         = df["Volume"],
        name      = "Volume",
        marker    = dict(color=colors, opacity=0.8),
        hovertemplate = "%{x|%b %d, %Y}<br>Volume: <b>%{y:,}</b><extra></extra>",
    ))

    _apply_base(fig, f"{symbol} – Trading Volume")
    fig.update_layout(height=260)
    return fig


# ── 4. Moving averages overlay ────────────────────────────────────────────────

def plot_moving_averages(df: pd.DataFrame, symbol: str) -> go.Figure:
    """
    Close price + MA7, MA20, MA50 overlaid.
    """
    fig = go.Figure()

    # Closing price (thin, muted)
    fig.add_trace(go.Scatter(
        x     = df.index,
        y     = df["Close"],
        mode  = "lines",
        name  = "Close",
        line  = dict(color="#334155", width=1.5),
        hovertemplate = "%{x|%b %d}<br>Close: <b>%{y:.2f}</b><extra></extra>",
    ))

    # MA overlays
    for ma, color in MA_COLORS.items():
        if ma in df.columns:
            fig.add_trace(go.Scatter(
                x     = df.index,
                y     = df[ma],
                mode  = "lines",
                name  = ma,
                line  = dict(color=color, width=1.8),
                hovertemplate = f"{ma}: <b>%{{y:.2f}}</b><extra></extra>",
            ))

    _apply_base(fig, f"{symbol} – Moving Averages")
    fig.update_layout(height=360)
    return fig
