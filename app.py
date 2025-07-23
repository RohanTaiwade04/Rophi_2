import streamlit as st
import yfinance as yf
import pandas as pd
import random
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="ROPHI ANALYTICS")

# Title
from PIL import Image

# Load local image
image = Image.open(r"C:\Users\Rohan\PycharmProjects\Stock_Prediction\image\image.png")

# Display header section
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image(image, width=190)
with col2:
    st.markdown("""
        <div style='text-align: center; padding: 10px 0 0 0;'>
            <h1 style='font-size: 3em; margin-bottom: 0;'>📈 ROPHI ANALYTICS</h1>
            <p style='font-size: 1.3em; color: gray;'>Compare, Analyze, Succeed – All in One Place.</p>
        </div>
    """, unsafe_allow_html=True)


# Sidebar: Select stock details
st.sidebar.header("Select Stocks to Compare")

# Define stock options
stock_options = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN",
    "Google (GOOGL)": "GOOGL",
    "Tesla (TSLA)": "TSLA",
    "Reliance (RELIANCE.BO)": "RELIANCE.BO",
    "Infosys (INFY.BO)": "INFY.BO",
    "TCS (TCS.BO)": "TCS.BO",
    "HDFC Bank (HDFCBANK.BO)": "HDFCBANK.BO",
    "ICICI Bank (ICICIBANK.BO)": "ICICIBANK.BO",
    "Other (manual entry)": "OTHER"
}

# First stock input
ticker1_name = st.sidebar.selectbox("1️⃣ Select First Stock", list(stock_options.keys()), index=0)
ticker1 = st.sidebar.text_input("Enter First Ticker (if Other)", value="AAPL" if ticker1_name != "Other (manual entry)" else "")
if ticker1_name != "Other (manual entry)":
    ticker1 = stock_options[ticker1_name]

# Second stock input
ticker2_name = st.sidebar.selectbox("2️⃣ Select Second Stock", list(stock_options.keys()), index=1)
ticker2 = st.sidebar.text_input("Enter Second Ticker (if Other)", value="MSFT" if ticker2_name != "Other (manual entry)" else "")
if ticker2_name != "Other (manual entry)":
    ticker2 = stock_options[ticker2_name]

# Date input
start_date = st.sidebar.date_input("📅 Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("📅 End Date", pd.to_datetime("2025-01-28"))

# Currency map for 20+ countries
currency_map = {
    ".BO": "₹", ".NS": "₹", ".TO": "C$", ".V": "C$", ".L": "£", ".AX": "A$",
    ".HK": "HK$", ".T": "¥", ".SS": "¥", ".SZ": "¥", ".KS": "₩", ".KQ": "₩",
    ".TW": "NT$", ".PA": "€", ".F": "€", ".DE": "€", ".ST": "kr", ".HE": "€",
    ".AS": "€", ".MX": "MX$", ".SA": "R$", ".IS": "₺", ".NZ": "NZ$", ".SG": "S$",
    ".BKK": "฿", ".JO": "R", ".IR": "€", ".PL": "zł"
}

# Get currency symbol based on ticker suffix
def get_currency_symbol(ticker):
    for suffix, symbol in currency_map.items():
        if ticker.endswith(suffix):
            return symbol
    return "$"  # Default to USD

# Load data function
@st.cache_data
def load_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df = df[['Close']]
    df.rename(columns={'Close': ticker}, inplace=True)
    return df

# Load and combine data
data1 = load_data(ticker1, start_date, end_date)
data2 = load_data(ticker2, start_date, end_date)
combined_data = pd.concat([data1, data2], axis=1).dropna()

# Show data
st.subheader(f"📋 Closing Price Data for {ticker1} and {ticker2}")
st.dataframe(combined_data.tail())

# Plot interactive line chart
st.subheader("📈 Stock Comparison: Closing Prices")
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=combined_data.index,
    y=combined_data[ticker1],
    mode='lines',
    name=ticker1,
    hovertemplate='Date: %{x}<br>' + ticker1 + ' Price: %{y:.2f}'
))

fig.add_trace(go.Scatter(
    x=combined_data.index,
    y=combined_data[ticker2],
    mode='lines',
    name=ticker2,
    hovertemplate='Date: %{x}<br>' + ticker2 + ' Price: %{y:.2f}'
))

fig.update_layout(
    title=f"{ticker1} vs {ticker2} - Closing Price Comparison",
    xaxis_title="Date",
    yaxis_title=f"Price ({get_currency_symbol(ticker1)}/{get_currency_symbol(ticker2)})",
    template='plotly_white',
    hovermode='x unified'
)
st.plotly_chart(fig, use_container_width=True)

# Basic Analysis
st.subheader("📊 Basic Analysis")
for ticker in [ticker1, ticker2]:
    if ticker in combined_data:
        st.markdown(f"**🔍 {ticker} Analysis**")
        avg = combined_data[ticker].mean()
        vol = combined_data[ticker].std()
        ret = combined_data[ticker].pct_change().mean() * 100
        currency_symbol = get_currency_symbol(ticker)
        st.write(f"• Average Closing Price: {currency_symbol}{avg:.2f}")
        st.write(f"• Volatility (Standard Deviation): {currency_symbol}{vol:.2f}")
        st.write(f"• Average Daily Return: {ret:.2f}%")

# Beginner Tips
tips = [
    "💡 Compare multiple stocks before investing.",
    "📚 Use historical trends but don’t rely on them solely.",
    "📈 Diversification reduces risk.",
    "🕒 Stay invested for the long term.",
    "🔍 Use tools like P/E ratio and volume to guide decisions."
]
st.sidebar.markdown("## 👶 Beginner Tip")
st.sidebar.info(random.choice(tips))

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: gray; font-size: 0.9em;">
        🙏 Thank you for using <b>ROPHI ANALYTICS</b> — We hope it helped you make smarter investment decisions! 📊
    </div>
""", unsafe_allow_html=True)

