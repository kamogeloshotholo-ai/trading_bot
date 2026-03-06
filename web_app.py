import streamlit as st
import subprocess

st.set_page_config(page_title="AI Trading Bot", layout="wide")

st.title("AI Trading Bot Dashboard")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Run Bot", "Backtest", "Optimizer"]
)

if page == "Dashboard":

    st.header("Bot Status")

    st.write("Strategy:")
    st.write("- Asian Range")
    st.write("- Liquidity Sweep")
    st.write("- Retest Entry")
    st.write("- H4 Bias Filter")

    st.write("Pairs:")
    st.write("EURUSD")
    st.write("XAUUSD")
    st.write("NAS100")

if page == "Run Bot":

    st.header("Trading Bot Control")

    if st.button("Start Trading Bot"):
        subprocess.Popen(["python", "main_bot.py"])
        st.success("Bot started")

if page == "Backtest":

    st.header("Run Strategy Backtest")

    if st.button("Run Backtest"):
        subprocess.run(["python", "backtester.py"])
        st.success("Backtest finished")

if page == "Optimizer":

    st.header("Run AI Optimizer")

    if st.button("Run Optimization"):
        subprocess.run(["python", "optimizer.py"])
        st.success("Optimization complete")