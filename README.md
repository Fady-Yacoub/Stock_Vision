# 📈 StockVision – Stock Market Analysis System

A Streamlit web application for viewing and analyzing stock market data using Yahoo Finance.

---

## 👥 Team Structure

| Member | Role | File |
|--------|------|------|
| Member 1 | Project Lead / Backend Developer | `backend.py` |
| Member 2 | Data Processing & Analysis | `data_processing.py` |
| Member 3 | Visualization Developer | `visualization.py` |
| Member 4 | UI Developer / Tester / Docs | `app.py` |

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🔧 Features

- **Stock Search** – Enter any valid ticker symbol (AAPL, TSLA, MSFT…)
- **Time Period** – 7 days, 1 month, 3 months, 6 months, 1 year, 2 years
- **Chart Types** – Line chart or Candlestick
- **Key Metrics** – Current price, Day High/Low, 52-Week High/Low, Volume
- **Moving Averages** – MA7, MA20, MA50 overlay
- **Volume Chart** – Bar chart with green/red direction colouring
- **Historical Table** – Full OHLCV data in expandable section
- **Error Handling** – Validates symbols and handles API failures gracefully

---

## 🗂️ Project Structure

```
stock_market_app/
├── app.py              # Streamlit UI (Member 4)
├── backend.py          # API integration & validation (Member 1)
├── data_processing.py  # Data cleaning & indicators (Member 2)
├── visualization.py    # Plotly charts (Member 3)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 📦 Technologies

- **Frontend/Backend**: Streamlit
- **Language**: Python 3.10+
- **Data**: yfinance (Yahoo Finance API)
- **Processing**: Pandas, NumPy
- **Visualization**: Plotly

---

## 🧪 Testing

Test scenarios:
- ✅ Valid symbols: `AAPL`, `TSLA`, `MSFT`, `BRK.B`
- ✅ Invalid symbol: `XXXXX` → shows error message
- ✅ Empty input → shows validation error
- ✅ All time periods work
- ✅ Both chart types render correctly
