import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="Taylor Envelope Projector", layout="wide")
st.title("📐 Taylor Trading Technique: Futures Envelope Projector")
st.caption("Formulated directly from the Timeless Dollar Book Method Logic")

# --- TICKER DICTIONARY MAP ---
FUTURES_MAP = {
    "MNQ (Micro Nasdaq)": "MNQ=F",
    "MES (Micro S&P 500)": "MES=F",
    "MGC (Micro Gold)": "MGC=F",
    "NQ (Mini Nasdaq)": "NQ=F",
    "ES (Mini S&P 500)": "ES=F"
}

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("Market Selection")
selected_label = st.sidebar.selectbox("Choose a Contract:", list(FUTURES_MAP.keys()))
ticker = FUTURES_MAP[selected_label]

# --- TAYLOR ENGINE DATA PROCESSING ---
@st.cache_data(ttl=3600)
def get_taylor_data(symbol):
    # Fetch 3 months of daily data to generate clean 3-day rolling calculations
    df = yf.download(symbol, period="3mo")
    
    # Flatten any multi-index columns from newer yfinance versions
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    if df.empty:
        return df
    
    # 1. Calculate raw swing metrics from consecutive daily bars
    df['Decline_Raw'] = df['High'].shift(1) - df['Low']
    df['Buying_Under_Raw'] = df['Low'].shift(1) - df['Low']
    df['Rally_Raw'] = df['High'] - df['Low'].shift(1)
    df['Buying_High_Raw'] = df['High'] - df['High'].shift(1)
    
    # 2. Smooth out using Taylor's core 3-day moving average rule
    df['Avg_Decline_3d'] = df['Decline_Raw'].rolling(window=3).mean()
    df['Avg_Buying_Under_3d'] = df['Buying_Under_Raw'].rolling(window=3).mean()
    df['Avg_Rally_3d'] = df['Rally_Raw'].rolling(window=3).mean()
    df['Avg_Buying_High_3d'] = df['Buying_High_Raw'].rolling(window=3).mean()
    
    # 3. Calculate dynamic Support (Buy Envelope) and Resistance (Sell Envelope) boundaries
    df['Target_Decline'] = df['High'] - df['Avg_Decline_3d']
    df['Target_Buying_Under'] = df['Low'] - df['Avg_Buying_Under_3d']
    df['Pivot_BO_Short'] = (((df['High'] + df['Low'] + df['Close']) / 3) * 2) - df['High']
    
    df['Target_Rally'] = df['Low'] + df['Avg_Rally_3d']
    df['Target_Buying_High'] = df['High'] + df['Avg_Buying_High_3d']
    df['Pivot_BO_Long'] = (((df['High'] + df['Low'] + df['Close']) / 3) * 2) - df['Low']
    
    return df

try:
    # Build out engine data
    data = get_taylor_data(ticker)
    
    if data.empty:
        st.error(f"Could not pull data for {ticker}. The exchange might be closed, or the ticker format changed.")
        st.stop()
        
    current_session = data.iloc[-1]
    
    st.subheader(f"Projected Boundaries for Next Session: **{selected_label}**")
    
    # --- METRICS DISPLAY (SIDE BY SIDE) ---
    col_sell, col_buy = st.columns(2)
    
    with col_sell:
        st.error("### 🔴 Sell Envelope (Resistance Ceiling)")
        st.metric("Target Rally Point (Absolute Peak)", f"{current_session['Target_Rally']:.2f}")
        st.metric("Pivot Breakout Long (Tipping Point)", f"{current_session['Pivot_BO_Long']:.2f}")
        st.metric("Target Buying High (Extreme Extension)", f"{current_session['Target_Buying_High']:.2f}")
        st.metric("Session Reference High (Prior High)", f"{current_session['High']:.2f}")
        
    with col_buy:
        st.success("### 🟢 Buy Envelope (Support Floor)")
        st.metric("Pivot Breakout Short (Breakdown Point)", f"{current_session['Pivot_BO_Short']:.2f}")
        st.metric("Target Buying Under (Extreme Dip)", f"{current_session['Target_Buying_Under']:.2f}")
        st.metric("Target Decline Point", f"{current_session['Target_Decline']:.2f}")
        st.metric("Session Reference Low (Absolute Floor)", f"{current_session['Low']:.2f}")

    # --- INTERACTIVE PLOTLY CHART OVERLAY ---
    st.markdown("---")
    st.subheader("📊 Visual Envelope Map Overlay")
    
    # Slice the last 15 periods so the lines are readable and not crammed
    chart_df = data.tail(15)
    
    fig = go.Figure(data=[go.Candlestick(
        x=chart_df.index.strftime('%Y-%m-%d'),
        open=chart_df['Open'], high=chart_df['High'],
        low=chart_df['Low'], close=chart_df['Close'],
        name="Price candles"
    )])
    
    # Resistance lines projected horizontally across the session
    fig.add_hline(y=current_session['Target_Rally'], line_dash="dash", line_color="darkred", 
                  annotation_text="Envelope Peak (Target Rally)", annotation_position="top left")
    fig.add_hline(y=current_session['Pivot_BO_Long'], line_dash="dot", line_color="red", 
                  annotation_text="Pivot Breakout (Long)")
    fig.add_hline(y=current_session['High'], line_dash="solid", line_color="orange", 
                  annotation_text="Session Reference High")
                  
    # Support lines projected horizontally across the session
    fig.add_hline(y=current_session['Low'], line_dash="solid", line_color="blue", 
                  annotation_text="Session Reference Low")
    fig.add_hline(y=current_session['Pivot_BO_Short'], line_dash="dot", line_color="teal", 
                  annotation_text="Pivot Breakout (Short)")
    fig.add_hline(y=current_session['Target_Decline'], line_dash="dash", line_color="green", 
                  annotation_text="Target Decline Support", annotation_position="bottom left")
    
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        height=650,
        yaxis_title="Price Index Points",
        xaxis_title="Date Tracker",
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # --- HISTORICAL ENGINE LEDGER ---
    st.markdown("---")
    st.subheader("📋 The 'Book Method' Calculation Ledger")
    ledger_df = data[['Open', 'High', 'Low', 'Close', 'Target_Rally', 'Target_Decline']].dropna()
    st.dataframe(ledger_df.iloc[::-1], use_container_width=True)

except Exception as e:
    st.error(f"Critical execution block fault: {e}")
