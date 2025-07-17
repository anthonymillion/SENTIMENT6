import streamlit as st
import pandas as pd
import datetime

# Define symbol groups
stocks = ["NVDA", "MSFT", "AAPL", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "AVGO", "COST", "AMD", "NFLX"]
indices = ["SP500", "QQQ", "USTECH100", "RUSSELL", "NIKKEI"]
commodities = ["GOLD", "USOIL", "BRENT", "COPPER", "SILVER", "NATGAS"]
currencies = ["USDJPY", "EURUSD", "DXY", "BTCUSD"]
volatility = ["VIX", "BONDYIELDS"]

# Expanded timeframes
timeframes = ["1s", "5s", "15s", "30s", "M1", "M2", "M3", "M4", "M10", "M15", "M30", "H6", "H7", "H8", "1H", "4H", "Daily", "Weekly", "Monthly"]

# Config
st.set_page_config(page_title="AI EdgeFinder – Horizontal Layout", layout="wide")
st.title("📊 AI EdgeFinder – Horizontal Layout")

# Timeframe selectors
main_tf = st.selectbox("Main Timeframe", timeframes, index=10, key="main_tf")
top_tf = st.selectbox("Top Movers Timeframe", timeframes, index=10, key="top_tf")

# Simulated scoring
def simulate_score(symbol, tf):
    base = (hash(symbol + tf + str(datetime.date.today())) % 9) - 4
    return round(base + (hash(tf) % 3 - 1), 2)

def classify_sentiment(score):
    if score > 1.5:
        return "🟢 Bullish"
    elif score < -1.5:
        return "🔴 Bearish"
    return "🟡 Neutral"

def score_group(symbols, tf):
    return pd.DataFrame([{
        "Symbol": sym,
        "Score": (s := simulate_score(sym, tf)),
        "Sentiment": classify_sentiment(s)
    } for sym in symbols])

# Top Movers (all stocks, all sentiment)
df_top = pd.DataFrame([{
    "Symbol": sym,
    "Score": (s := simulate_score(sym, top_tf)),
    "Sentiment": classify_sentiment(s)
} for sym in stocks])

# Display 5 categories side-by-side
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.subheader("📈 Top Movers")
    st.dataframe(df_top, use_container_width=True)

with col2:
    st.subheader("🌐 Indices")
    st.dataframe(score_group(indices, main_tf), use_container_width=True)

with col3:
    st.subheader("💰 Commodities")
    st.dataframe(score_group(commodities, main_tf), use_container_width=True)

with col4:
    st.subheader("💱 Currencies")
    st.dataframe(score_group(currencies, main_tf), use_container_width=True)

with col5:
    st.subheader("⚡ Volatility")
    st.dataframe(score_group(volatility, main_tf), use_container_width=True)
