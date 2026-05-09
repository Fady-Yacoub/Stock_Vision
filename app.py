"""
Stock Market Analysis System
Main entry point – Streamlit UI (Member 4 responsibilities)
"""

import streamlit as st
from datetime import datetime

# Page config must come first
st.set_page_config(
    page_title="StockVision · Market Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Dark background */
.stApp {
    background: #0a0e1a;
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f1629 !important;
    border-right: 1px solid #1e2d4a;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #111827 0%, #1a2540 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 8px 0;
}

.metric-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 6px;
}

.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 28px;
    font-weight: 600;
    color: #f1f5f9;
}

.metric-value.positive { color: #10b981; }
.metric-value.negative { color: #ef4444; }

.metric-delta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    margin-top: 4px;
}

.delta-pos { color: #10b981; }
.delta-neg { color: #ef4444; }

/* Section headers */
.section-header {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3b82f6;
    margin: 24px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2d4a;
}

/* Info badges */
.badge {
    display: inline-block;
    background: #1e3a5f;
    color: #60a5fa;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin: 2px;
}

/* Stock header */
.stock-header {
    background: linear-gradient(135deg, #0f1629 0%, #1a2540 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
}

.stock-name {
    font-size: 32px;
    font-weight: 700;
    color: #f8fafc;
}

.stock-symbol {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    color: #3b82f6;
    background: #1e3a5f;
    padding: 3px 10px;
    border-radius: 6px;
    margin-left: 10px;
}

/* Error box */
.error-box {
    background: #1f0f0f;
    border: 1px solid #7f1d1d;
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 16px 20px;
    color: #fca5a5;
    margin: 16px 0;
}

/* Stremlit element overrides */
div[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 16px;
}
</style>
""", unsafe_allow_html=True)

# ── Imports ─────────────────────────────────────────────────────────────────
from backend import fetch_stock_data, validate_symbol
from data_processing import process_stock_data, compute_indicators
from visualization import (
    plot_price_trend,
    plot_candlestick,
    plot_volume,
    plot_moving_averages,
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:10px 0 20px 0;'>
        <div style='font-size:22px;font-weight:700;color:#f1f5f9;'>📈 StockVision</div>
        <div style='font-size:11px;color:#64748b;letter-spacing:1.5px;text-transform:uppercase;margin-top:4px;'>Market Analysis System</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Search</div>', unsafe_allow_html=True)

    symbol_input = st.text_input(
        "Stock Symbol",
        value="AAPL",
        placeholder="e.g. AAPL, TSLA, AMZN",
        help="Enter a valid stock ticker symbol",
    ).strip().upper()

    period = st.selectbox(
        "Time Period",
        options=["7d", "1mo", "3mo", "6mo", "1y", "2y"],
        index=1,
        format_func=lambda x: {
            "7d": "7 Days", "1mo": "1 Month", "3mo": "3 Months",
            "6mo": "6 Months", "1y": "1 Year", "2y": "2 Years"
        }[x],
    )

    chart_type = st.selectbox(
        "Chart Type",
        options=["Line Chart", "Candlestick"],
        index=0,
    )

    show_volume   = st.checkbox("Show Volume",          value=True)
    show_ma       = st.checkbox("Show Moving Averages", value=True)

    analyze_btn = st.button("🔍  Analyze", use_container_width=True, type="primary")

    st.markdown('<div class="section-header">Popular Symbols</div>', unsafe_allow_html=True)
    popular = ["AAPL","MSFT","GOOGL","AMZN","TSLA","META","NVDA","NFLX"]
    cols = st.columns(2)
    for i, sym in enumerate(popular):
        if cols[i % 2].button(sym, key=f"pop_{sym}", use_container_width=True):
            symbol_input = sym
            analyze_btn  = True

    st.markdown(f"""
    <div style='margin-top:auto;padding-top:20px;font-size:11px;color:#334155;'>
        Data via Yahoo Finance · {datetime.now().strftime("%b %d, %Y")}
    </div>
    """, unsafe_allow_html=True)

# ── Main area ────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:10px 0 4px 0;'>
    <h1 style='font-size:28px;font-weight:700;color:#f1f5f9;margin:0;'>
        Stock Market Analysis
    </h1>
    <p style='color:#64748b;font-size:14px;margin-top:4px;'>
        Real-time data · Interactive charts · Key indicators
    </p>
</div>
""", unsafe_allow_html=True)

# ── Trigger on first load or button press ────────────────────────────────────
if "last_symbol" not in st.session_state:
    st.session_state.last_symbol = ""
    analyze_btn = True            # auto-load AAPL on first visit

if analyze_btn or symbol_input != st.session_state.last_symbol:
    st.session_state.last_symbol = symbol_input

    if not symbol_input:
        st.markdown('<div class="error-box">⚠️ Please enter a stock symbol.</div>',
                    unsafe_allow_html=True)
        st.stop()

    # Validate
    is_valid, err_msg = validate_symbol(symbol_input)
    if not is_valid:
        st.markdown(f'<div class="error-box">⚠️ {err_msg}</div>',
                    unsafe_allow_html=True)
        st.stop()

    # Fetch data
    with st.spinner(f"Fetching data for **{symbol_input}** …"):
        raw_data, info, fetch_error = fetch_stock_data(symbol_input, period)

    if fetch_error:
        st.markdown(f'<div class="error-box">⚠️ {fetch_error}</div>',
                    unsafe_allow_html=True)
        st.stop()

    # Process
    df, proc_error = process_stock_data(raw_data)
    if proc_error:
        st.markdown(f'<div class="error-box">⚠️ {proc_error}</div>',
                    unsafe_allow_html=True)
        st.stop()

    df = compute_indicators(df)

    # ── Stock header ────────────────────────────────────────────────────────
    name        = info.get("longName", symbol_input)
    sector      = info.get("sector", "N/A")
    industry    = info.get("industry", "N/A")
    currency    = info.get("currency", "USD")
    current     = info.get("currentPrice") or info.get("regularMarketPrice") or df["Close"].iloc[-1]
    prev_close  = info.get("previousClose") or df["Close"].iloc[-2] if len(df) > 1 else current
    change      = current - prev_close
    change_pct  = (change / prev_close * 100) if prev_close else 0
    sign        = "+" if change >= 0 else ""
    clr_class   = "positive" if change >= 0 else "negative"
    arrow       = "▲" if change >= 0 else "▼"

    st.markdown(f"""
    <div class="stock-header">
        <div style='display:flex;align-items:center;gap:12px;flex-wrap:wrap;'>
            <span class="stock-name">{name}</span>
            <span class="stock-symbol">{symbol_input}</span>
        </div>
        <div style='margin-top:6px;'>
            <span class="badge">{sector}</span>
            <span class="badge">{industry}</span>
            <span class="badge">{currency}</span>
        </div>
        <div style='margin-top:16px;display:flex;align-items:flex-end;gap:16px;flex-wrap:wrap;'>
            <div class="metric-value {clr_class}" style='font-size:40px;'>{currency} {current:,.2f}</div>
            <div class="metric-delta {'delta-pos' if change >= 0 else 'delta-neg'}" style='font-size:18px;margin-bottom:6px;'>
                {arrow} {sign}{change:.2f} ({sign}{change_pct:.2f}%)
            </div>
        </div>
        <div style='font-size:11px;color:#64748b;margin-top:4px;'>
            Previous close: {prev_close:,.2f} · Period: {period}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Key metrics row ─────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        ("Day High",  info.get("dayHigh")  or df["High"].iloc[-1],  None),
        ("Day Low",   info.get("dayLow")   or df["Low"].iloc[-1],   None),
        ("52W High",  info.get("fiftyTwoWeekHigh") or df["High"].max(), None),
        ("52W Low",   info.get("fiftyTwoWeekLow")  or df["Low"].min(),  None),
        ("Volume",    info.get("volume")   or df["Volume"].iloc[-1] if "Volume" in df.columns else "N/A", None),
    ]
    for col, (label, val, _) in zip([c1,c2,c3,c4,c5], metrics):
        with col:
            if isinstance(val, float):
                st.metric(label, f"{val:,.2f}")
            elif isinstance(val, int):
                st.metric(label, f"{val:,}")
            else:
                st.metric(label, str(val))

    # ── Price chart ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Price Trend</div>', unsafe_allow_html=True)

    if chart_type == "Candlestick":
        fig = plot_candlestick(df, symbol_input)
    else:
        fig = plot_price_trend(df, symbol_input)

    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

    # ── Moving averages ──────────────────────────────────────────────────────
    if show_ma:
        st.markdown('<div class="section-header">Moving Averages</div>', unsafe_allow_html=True)
        fig_ma = plot_moving_averages(df, symbol_input)
        st.plotly_chart(fig_ma, use_container_width=True, config={"displaylogo": False})

    # ── Volume chart ─────────────────────────────────────────────────────────
    if show_volume and "Volume" in df.columns:
        st.markdown('<div class="section-header">Trading Volume</div>', unsafe_allow_html=True)
        fig_vol = plot_volume(df, symbol_input)
        st.plotly_chart(fig_vol, use_container_width=True, config={"displaylogo": False})

    # ── Historical data table ────────────────────────────────────────────────
    with st.expander("📋  Historical Data Table"):
        display_df = df.copy()
        display_df.index = display_df.index.strftime("%Y-%m-%d")
        numeric_cols = display_df.select_dtypes(include="number").columns
        st.dataframe(
            display_df[numeric_cols].style.format("{:.2f}"),
            use_container_width=True,
        )

else:
    # Landing state
    st.markdown("""
    <div style='text-align:center;padding:80px 20px;'>
        <div style='font-size:64px;margin-bottom:16px;'>📈</div>
        <div style='font-size:22px;font-weight:600;color:#f1f5f9;margin-bottom:8px;'>
            Enter a stock symbol to get started
        </div>
        <div style='font-size:14px;color:#64748b;'>
            Try AAPL, TSLA, MSFT, AMZN, GOOGL or any valid ticker
        </div>
    </div>
    """, unsafe_allow_html=True)
