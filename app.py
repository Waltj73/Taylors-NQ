import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="Taylor Envelope Projector", layout="wide")
st.title("📐 Taylor Trading Technique: Futures Envelope Projector")
st.caption("Simplified Framework for Core Support & Resistance Targets")

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
    df = yf.download(symbol, period="3mo", group_by="ticker", auto_adjust=True)
    
    if isinstance(df.columns, pd.MultiIndex):
        if symbol in df.columns.levels[0]:
            df = df[symbol]
        else:
            df.columns = df.columns.get_level_values(0)
            
    if df.empty:
        return df
        
    df = df.dropna(subset=['High', 'Low', 'Close'])
    
    # Core mathematical swing calculations (Taylor rules)
    df['Decline_Raw'] = df['High'].shift(1) - df['Low']
    df['Buying_Under_Raw'] = df['Low'].shift(1) - df['Low']
    df['Rally_Raw'] = df['High'] - df['Low'].shift(1)
    df['Buying_High_Raw'] = df['High'] - df['High'].shift(1)
    
    df['Avg_Decline_3d'] = df['Decline_Raw'].rolling(window=3).mean()
    df['Avg_Buying_Under_3d'] = df['Buying_Under_Raw'].rolling(window=3).mean()
    df['Avg_Rally_3d'] = df['Rally_Raw'].rolling(window=3).mean()
    df['Avg_Buying_High_3d'] = df['Buying_High_Raw'].rolling(window=3).mean()
    
    # Dynamic chart boundaries
    df['Envelope_Low'] = df['High'] - df['Avg_Decline_3d']
    df['Extreme_Dip_Target'] = df['Low'] - df['Avg_Buying_Under_3d']
    df['Break_Below_Trigger'] = (((df['High'] + df['Low'] + df['Close']) / 3) * 2) - df['High']
    
    df['Envelope_High'] = df['Low'] + df['Avg_Rally_3d']
    df['Extreme_Extension_Target'] = df['High'] + df['Avg_Buying_High_3d']
    df['Break_Above_Trigger'] = (((df['High'] + df['Low'] + df['Close']) / 3) * 2) - df['Low']
    
    return df

try:
    data = get_taylor_data(ticker)
    
    if data.empty:
        st.error(f"Could not pull data for {ticker}. The exchange might be closed, or the ticker format changed.")
        st.stop()
        
    current_session = data.iloc[-1]
    
    # --- SETUP STREAMLIT TABS ---
    tab1, tab2 = st.tabs(["📊 Main Dashboard", "📥 Export Spreadsheet Data"])

    # ==================== TAB 1: MAIN DASHBOARD ====================
    with tab1:
        st.subheader(f"Projected Boundaries for Next Session: **{selected_label}**")
        
        # --- METRICS DISPLAY ---
        col_sell, col_buy = st.columns(2)
        
        with col_sell:
            st.error("### 🔴 Resistance Ceilings (Look to Short / Exit Longs)")
            st.metric("Envelope High (Main Target)", f"{current_session['Envelope_High']:.2f}")
            st.metric("Break-Above Trigger (Trend Extension Point)", f"{current_session['Break_Above_Trigger']:.2f}")
            st.metric("Extreme Extension Target", f"{current_session['Extreme_Extension_Target']:.2f}")
            st.metric("Prior Session High (Reference)", f"{current_session['High']:.2f}")
            
        with col_buy:
            st.success("### 🟢 Support Floors (Look to Buy / Exit Shorts)")
            st.metric("Break-Below Trigger (Trend Breakdown Point)", f"{current_session['Break_Below_Trigger']:.2f}")
            st.metric("Extreme Dip Target", f"{current_session['Extreme_Dip_Target']:.2f}")
            st.metric("Envelope Low (Main Target)", f"{current_session['Envelope_Low']:.2f}")
            st.metric("Prior Session Low (Reference)", f"{current_session['Low']:.2f}")

        # --- INTERACTIVE PLOTLY CHART OVERLAY ---
        st.markdown("---")
        st.subheader("Visual Envelope Map Overlay")
        
        chart_df = data.tail(15)
        
        fig = go.Figure(data=[go.Candlestick(
            x=chart_df.index.strftime('%Y-%m-%d'),
            open=chart_df['Open'], high=chart_df['High'],
            low=chart_df['Low'], close=chart_df['Close'],
            name="Price"
        )])
        
        # Resistance lines
        fig.add_hline(y=current_session['Envelope_High'], line_dash="dash", line_color="darkred", 
                      annotation_text="Envelope High", annotation_position="top left")
        fig.add_hline(y=current_session['Break_Above_Trigger'], line_dash="dot", line_color="red", 
                      annotation_text="Break-Above Trigger")
        fig.add_hline(y=current_session['High'], line_dash="solid", line_color="orange", 
                      annotation_text="Prior Session High")
                      
        # Support lines
        fig.add_hline(y=current_session['Low'], line_dash="solid", line_color="blue", 
                      annotation_text="Prior Session Low")
        fig.add_hline(y=current_session['Break_Below_Trigger'], line_dash="dot", line_color="teal", 
                      annotation_text="Break-Below Trigger")
        fig.add_hline(y=current_session['Envelope_Low'], line_dash="dash", line_color="green", 
                      annotation_text="Envelope Low", annotation_position="bottom left")
        
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            height=600,
            yaxis_title="Price",
            xaxis_title="Date",
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    # ==================== TAB 2: EXPORT SPREADSHEET DATA ====================
    with tab2:
        st.subheader("📥 Download Historical Data")
        st.write("This table contains clean OHLC values matched with Taylor's targets. Click the button below to download the CSV for your spreadsheet templates.")
        
        # Format the ledger to be perfectly ready for spreadsheets
        export_df = data[['Open', 'High', 'Low', 'Close', 'Envelope_High', 'Envelope_Low']].dropna()
        export_df.index.name = 'Date'
        
        # Create CSV download button
        csv_data = export_df.to_csv().encode('utf-8')
        st.download_button(
            label=f"📥 Download {ticker}_taylor_data.csv",
            data=csv_data,
            file_name=f"{ticker}_taylor_history.csv",
            mime="text/csv"
        )
        
        # Display scannable data preview (newest dates on top)
        st.markdown("### Preview Data Ledger")
        st.dataframe(export_df.iloc[::-1], use_container_width=True)

except Exception as e:
    st.error(f"Critical execution fault: {e}")
