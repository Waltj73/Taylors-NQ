import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="Taylor Envelope Projector", layout="wide")
st.title("📐 Taylor Trading Technique: Futures Envelope Projector")
st.caption("Matches the verified Taylor Calculator formula: Support/Resistance = average of 4 sub-targets")

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

    # --- Core mathematical swing calculations (Taylor rules) ---
    df['Decline_Raw'] = df['High'].shift(1) - df['Low']
    df['Buying_Under_Raw'] = df['Low'].shift(1) - df['Low']
    df['Rally_Raw'] = df['High'] - df['Low'].shift(1)
    df['Buying_High_Raw'] = df['High'] - df['High'].shift(1)

    df['Avg_Decline_3d'] = df['Decline_Raw'].rolling(window=3).mean()
    df['Avg_Buying_Under_3d'] = df['Buying_Under_Raw'].rolling(window=3).mean()
    df['Avg_Rally_3d'] = df['Rally_Raw'].rolling(window=3).mean()
    df['Avg_Buying_High_3d'] = df['Buying_High_Raw'].rolling(window=3).mean()

    # --- The 3 sub-targets per side (each one verified to match the spreadsheet) ---
    df['Envelope_Low'] = df['High'] - df['Avg_Decline_3d']
    df['Extreme_Dip_Target'] = df['Low'] - df['Avg_Buying_Under_3d']
    df['Break_Below_Trigger'] = (((df['High'] + df['Low'] + df['Close']) / 3) * 2) - df['High']

    df['Envelope_High'] = df['Low'] + df['Avg_Rally_3d']
    df['Extreme_Extension_Target'] = df['High'] + df['Avg_Buying_High_3d']
    df['Break_Above_Trigger'] = (((df['High'] + df['Low'] + df['Close']) / 3) * 2) - df['Low']

    # --- THE REAL TAYLOR SUPPORT/RESISTANCE NUMBERS ---
    # Verified against the live spreadsheet: each side is the average of its
    # 3 derived sub-targets PLUS today's raw High/Low.
    df['Support_Target'] = (
        df['Break_Below_Trigger'] + df['Envelope_Low'] + df['Extreme_Dip_Target'] + df['Low']
    ) / 4

    df['Resistance_Target'] = (
        df['Break_Above_Trigger'] + df['Envelope_High'] + df['Extreme_Extension_Target'] + df['High']
    ) / 4

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

        # --- PRIMARY TAYLOR TARGETS (matches spreadsheet) ---
        col_res, col_sup = st.columns(2)
        with col_res:
            st.error("### 🔴 Taylor Resistance Target")
            st.metric("Resistance (avg of 4 components)", f"{current_session['Resistance_Target']:.2f}")
        with col_sup:
            st.success("### 🟢 Taylor Support Target")
            st.metric("Support (avg of 4 components)", f"{current_session['Support_Target']:.2f}")

        st.markdown("---")
        st.caption("Component breakdown (each verified individually against the spreadsheet):")

        col_sell, col_buy = st.columns(2)

        with col_sell:
            st.markdown("**Resistance components**")
            st.metric("Envelope High", f"{current_session['Envelope_High']:.2f}")
            st.metric("Break-Above Trigger", f"{current_session['Break_Above_Trigger']:.2f}")
            st.metric("Extreme Extension Target", f"{current_session['Extreme_Extension_Target']:.2f}")
            st.metric("Prior Session High", f"{current_session['High']:.2f}")

        with col_buy:
            st.markdown("**Support components**")
            st.metric("Break-Below Trigger", f"{current_session['Break_Below_Trigger']:.2f}")
            st.metric("Extreme Dip Target", f"{current_session['Extreme_Dip_Target']:.2f}")
            st.metric("Envelope Low", f"{current_session['Envelope_Low']:.2f}")
            st.metric("Prior Session Low", f"{current_session['Low']:.2f}")

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

        # Primary Taylor targets (bold solid lines)
        fig.add_hline(y=current_session['Resistance_Target'], line_dash="solid", line_color="darkred",
                      line_width=3, annotation_text="Taylor Resistance", annotation_position="top left")
        fig.add_hline(y=current_session['Support_Target'], line_dash="solid", line_color="darkgreen",
                      line_width=3, annotation_text="Taylor Support", annotation_position="bottom left")

        # Component lines (thinner, dashed/dotted for reference)
        fig.add_hline(y=current_session['Envelope_High'], line_dash="dash", line_color="red",
                      annotation_text="Envelope High")
        fig.add_hline(y=current_session['Break_Above_Trigger'], line_dash="dot", line_color="red",
                      annotation_text="Break-Above Trigger")
        fig.add_hline(y=current_session['High'], line_dash="solid", line_color="orange", line_width=1,
                      annotation_text="Prior Session High")

        fig.add_hline(y=current_session['Low'], line_dash="solid", line_color="blue", line_width=1,
                      annotation_text="Prior Session Low")
        fig.add_hline(y=current_session['Break_Below_Trigger'], line_dash="dot", line_color="teal",
                      annotation_text="Break-Below Trigger")
        fig.add_hline(y=current_session['Envelope_Low'], line_dash="dash", line_color="green",
                      annotation_text="Envelope Low")

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

        export_df = data[[
            'Open', 'High', 'Low', 'Close',
            'Resistance_Target', 'Support_Target',
            'Envelope_High', 'Envelope_Low'
        ]].dropna()
        export_df.index.name = 'Date'

        csv_data = export_df.to_csv().encode('utf-8')
        st.download_button(
            label=f"📥 Download {ticker}_taylor_data.csv",
            data=csv_data,
            file_name=f"{ticker}_taylor_history.csv",
            mime="text/csv"
        )

        st.markdown("### Preview Data Ledger")
        st.dataframe(export_df.iloc[::-1], use_container_width=True)

except Exception as e:
    st.error(f"Critical execution fault: {e}")
