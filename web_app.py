import streamlit as st
import subprocess
import time
import os

st.set_page_config(page_title="AI Trading Bot", layout="wide")

# Simple password protection - use env var for security
PASSWORD = os.getenv("TRADING_BOT_PASSWORD", "tradingbot2026")  # Set env var for production

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter password:", type="password")
    if st.button("Login"):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()

st.title("AI Trading Bot Dashboard")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Run Bot", "Backtest", "Optimizer"]
)

# Liquidity source selector
liquidity_source = st.sidebar.selectbox(
    "Liquidity Source",
    ["ASIAN", "DAILY", "WEEKLY", "CUSTOM"],
    index=0
)

# Save to session state
st.session_state.liquidity_source = liquidity_source

# keep a reference to the bot process in session state so we can stop it later
if 'bot_process' not in st.session_state:
    st.session_state.bot_process = None

if page == "Dashboard":

    st.header("Bot Status")

    # Show current session
    try:
        from main_bot import get_current_session
        session, _ = get_current_session()
        st.write(f"**Current Session**: {session}")
    except:
        st.write("**Current Session**: Unknown")

    st.write("**Strategy**")
    st.markdown("""- Asian Range
- Liquidity Sweep
- Retest Entry
- H4 Bias Filter""")

    st.write("**Pairs**")
    st.markdown("""EURUSD
XAUUSD
NAS100
BTCUSD""")

    # Recent Liquidity Monitoring
    st.subheader("Recent Liquidity Analysis")
    try:
        from recent_liquidity_detector import get_recent_liquidity_summary

        symbols = ["EURUSD", "XAUUSD", "NAS100", "BTCUSD"]
        liquidity_data = []

        for symbol in symbols:
            try:
                summary = get_recent_liquidity_summary(symbol)
                liquidity_data.append({
                    'Symbol': symbol,
                    'Volume Clusters': summary.get('volume_clusters_count', 0),
                    'Rejection Signals': summary.get('rejection_signals_count', 0),
                    'Traditional High': summary.get('traditional_high', 'N/A'),
                    'Traditional Low': summary.get('traditional_low', 'N/A'),
                    'Last Update': summary.get('last_update', 'N/A')
                })
            except Exception as e:
                liquidity_data.append({
                    'Symbol': symbol,
                    'Volume Clusters': 'Error',
                    'Rejection Signals': 'Error',
                    'Traditional High': 'N/A',
                    'Traditional Low': 'N/A',
                    'Last Update': str(e)
                })

        if PANDAS_AVAILABLE:
            import pandas as pd
            df_liquidity = pd.DataFrame(liquidity_data)
            st.dataframe(df_liquidity)
        else:
            st.json(liquidity_data)

        # Order Flow Analysis
        st.subheader("Order Flow Analysis")
        for symbol in symbols:
            try:
                summary = get_recent_liquidity_summary(symbol)
                order_flow = summary.get('order_flow_imbalance')
                if order_flow:
                    st.write(f"**{symbol}**: {order_flow['description']} (Strength: {order_flow['strength']:.2f})")
                else:
                    st.write(f"**{symbol}**: No significant order flow imbalance")
            except:
                st.write(f"**{symbol}**: Unable to analyze order flow")

    except Exception as e:
        st.error(f"Error loading liquidity data: {e}")

    # show recent trades if log exists
    try:
        try:
            import pandas as pd
            PANDAS_AVAILABLE = True
        except ImportError:
            PANDAS_AVAILABLE = False

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Refresh Trades"):
                st.rerun()
        with col2:
            if st.button("Clear Trade Log"):
                if os.path.exists("trade_log.csv"):
                    os.remove("trade_log.csv")
                    st.success("Trade log cleared")
                    st.rerun()
        if os.path.exists("trade_log.csv"):
            if PANDAS_AVAILABLE:
                df = pd.read_csv("trade_log.csv", header=None,
                                 names=["time","symbol","direction","entry","sl","tp","volume"])
                st.subheader("Recent trades")
                st.dataframe(df.tail(20))
            else:
                st.subheader("Recent trades")
                st.info("Pandas not available - cannot display trade log in table format")
                with open("trade_log.csv", "r") as f:
                    lines = f.readlines()[-20:]  # Last 20 lines
                    st.text("".join(lines))
        else:
            st.info("No trade log available yet.")
    except Exception as e:
        st.error(f"Error loading trade log: {e}")

    # Show weekly performance if available
    try:
        if os.path.exists("weekly_performance.txt"):
            with open("weekly_performance.txt", "r") as f:
                perf = f.read()
            st.subheader("Weekly Performance Summary")
            st.text(perf)
    except Exception as e:
        st.error(f"Error loading performance summary: {e}")

if page == "Run Bot":

    st.header("Trading Bot Control")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Start Trading Bot"):
            if st.session_state.bot_process is None or st.session_state.bot_process.poll() is not None:
                with open("bot_log.txt", "w") as f:
                    f.write("")  # clear log
                env = os.environ.copy()
                env["LIQUIDITY_SOURCE"] = st.session_state.liquidity_source
                st.session_state.bot_process = subprocess.Popen(["python", "main_bot.py"],
                                                               stdout=open("bot_log.txt", "a"),
                                                               stderr=subprocess.STDOUT,
                                                               text=True,
                                                               env=env)
                st.success("Bot started")
            else:
                st.warning("Bot already running")
    with col2:
        if st.button("Stop Trading Bot"):
            proc = st.session_state.bot_process
            if proc is not None and proc.poll() is None:
                proc.terminate()
                st.success("Bot stopped")
            else:
                st.info("Bot is not running")
    with col3:
        if st.button("Refresh Bot Output"):
            st.rerun()

    # show output log from file
    try:
        if os.path.exists("bot_log.txt"):
            with open("bot_log.txt", "r") as f:
                logs = f.read()
            st.text_area("Bot output", logs, height=200)
        else:
            st.info("Bot log not available yet.")
    except Exception as e:
        st.error(f"Error reading bot log: {e}")

    # Clear log button
    if st.button("Clear Bot Log"):
        if os.path.exists("bot_log.txt"):
            with open("bot_log.txt", "w") as f:
                f.write("")
            st.success("Bot log cleared")
            st.rerun()

if page == "Backtest":

    st.header("Run Strategy Backtest")

    if st.button("Run Backtest"):
        with st.spinner("Running backtest..."):
            result = subprocess.run(["python", "backtester.py"], capture_output=True, text=True)
        st.text_area("Backtest output", result.stdout + result.stderr, height=300)

if page == "Optimizer":

    st.header("Run AI Optimizer")

    if st.button("Run Optimization"):
        with st.spinner("Running AI optimization..."):
            result = subprocess.run(["python", "optimizer.py"], capture_output=True, text=True)
        st.text_area("Optimizer output", result.stdout + result.stderr, height=300)

        # Show results if available
        try:
            try:
                import pandas as pd
                PANDAS_AVAILABLE = True
            except ImportError:
                PANDAS_AVAILABLE = False

            if os.path.exists("optimization_results.csv"):
                if PANDAS_AVAILABLE:
                    df = pd.read_csv("optimization_results.csv")
                    st.subheader("Optimization Trials")
                    st.dataframe(df)
                else:
                    st.subheader("Optimization Trials")
                    st.info("Pandas not available - cannot display optimization results in table format")
                    with open("optimization_results.csv", "r") as f:
                        content = f.read()
                        st.text(content[:2000])  # Limit display
        except Exception as e:
            st.error(f"Error loading optimization results: {e}")