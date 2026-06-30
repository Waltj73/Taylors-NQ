import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Taylor Envelope Projector", layout="wide")
st.title("📐 Taylor Trading Technique: Envelope Projector")
st.caption("Formulated directly from the Timeless Dollar Book Method Logic")

ticker = st.sidebar.text_input("Asset Ticker", value="SPY").upper()

@st.cache_data(ttl=3600)
def get_taylor_data(symbol):
    # Fetch enough history to build clean rolling calculations
    df = yf.download(symbol, period="3mo")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # 1. Calculate basic raw values from video formulas
    df['Decline_Raw'] = df['High'].shift(1) - df['Low']
    df['Buying_Under_Raw'] = df['Low'].shift(1) - df['Low']
    df['Rally_Raw'] = df['High'] - df['Low'].shift(1)
    df['Buying_High_Raw'] = df['High'] - df['High'].shift(1)
    
    # 2. Extract 3-day moving averages of those raw values
    df['Avg_Decline_3d'] = df['Decline_Raw'].rolling(window=3).mean()
    df['Avg_Buying_Under_3d'] = df['Buying_Under_Raw'].rolling(window=3).mean()
    df['Avg_Rally_3d'] = df['Rally_Raw'].rolling(window=3).mean()
    df['Avg_Buying_High_3d'] = df['Buying_High_Raw'].rolling(window=3).mean()
    
    # 3. Formulate the explicit targets
    df['Target_Decline'] = df['High'] - df['Avg_Decline_3d']
    df['Target_Buying_Under'] = df['Low'] - df['Avg_Buying_Under_3d']
    df['Pivot_BO_Short'] = (((df['High'] + df['Low'] + df['Close']) / 3) * 2) - df['High']
    
    df['Target_Rally'] = df['Low'] + df['Avg_Rally_3d']
    df['Target_Buying_High'] = df['High'] + df['Avg_Buying_High_3d']
    df['Pivot_BO_Long'] = (((df['High'] + df['Low'] + df['Close']) / 3) * 2) - df['Low']
    
    return df

try:
    data = get_taylor_data(ticker)
    current_session = data.iloc[-1]
    
    st.subheader(f"Projected Zones for Next Trading Session ({ticker})")
    
    # Render Envelopes Side-by-Side
    col_sell, col_buy = st.columns(2)
    
    with col_sell:
        st.error("### 🔴 Sell Envelope (Resistance)")
        st.metric("Target Buying High (Extreme Extension)", f"${current_session['Target_Buying_High']:.2f}")
        st.metric("Target Rally Point", f"${current_session['Target_Rally']:.2f}")
        st.metric("Session Reference High", f"${current_session['High']:.2f}")
        st.metric("Pivot Breakout (Long)", f"${current_session['Pivot_BO_Long']:.2f}")
        
    with col_buy:
        st.success("### 🟢 Buy Envelope (Support)")
        st.metric("Pivot Breakout (Short)", f"${current_session['Pivot_BO_Short']:.2f}")
        st.metric("Session Reference Low", f"${current_session['Low']:.2f}")
        st.metric("Target Decline Point", f"${current_session['Target_Decline']:.2f}")
        st.metric("Target Buying Under (Extreme Dip)", f"${current_session['Target_Buying_Under']:.2f}")

    # Ledger display
    st.markdown("---")
    st.subheader("Historical Envelope Metrics Engine")
    ledger = data[['Open', 'High', 'Low', 'Close', 'Target_Rally', 'Target_Decline']].dropna()
    st.dataframe(ledger.iloc[::-1], use_container_width=True)

except Exception as e:
    st.error(f"Could not construct Taylor matrices: {e}")
