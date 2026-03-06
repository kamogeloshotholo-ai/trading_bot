import customtkinter as ctk
import subprocess
import MetaTrader5 as mt5

# ---------------- SETTINGS ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- MT5 CONNECTION ----------------

mt5.initialize()

bot_process = None

# ---------------- APP WINDOW ----------------

app = ctk.CTk()
app.geometry("900x600")
app.title("AI Trading Bot Platform")

# ---------------- LOGIN SCREEN ----------------

login_frame = ctk.CTkFrame(app)
login_frame.pack(fill="both", expand=True)

title = ctk.CTkLabel(login_frame, text="AI Trading Bot Platform", font=("Arial", 30))
title.pack(pady=40)

username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username")
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*")
password_entry.pack(pady=10)

# ---------------- DASHBOARD ----------------

dashboard_frame = ctk.CTkFrame(app)

header = ctk.CTkLabel(dashboard_frame, text="Trading Dashboard", font=("Arial", 28))
header.pack(pady=20)

# -------- ACCOUNT INFO --------

account = mt5.account_info()

balance_label = ctk.CTkLabel(dashboard_frame, text=f"Balance: ${account.balance}")
balance_label.pack()

equity_label = ctk.CTkLabel(dashboard_frame, text=f"Equity: ${account.equity}")
equity_label.pack()

profit_label = ctk.CTkLabel(dashboard_frame, text=f"Floating Profit: ${account.profit}")
profit_label.pack(pady=10)

# -------- BOT STATUS --------

status_label = ctk.CTkLabel(dashboard_frame, text="Bot Status: STOPPED")
status_label.pack(pady=10)

# -------- START BOT --------

def start_bot():
    global bot_process

    if bot_process is None:
        bot_process = subprocess.Popen(["python", "main_bot.py"])
        status_label.configure(text="Bot Status: RUNNING")

# -------- STOP BOT --------

def stop_bot():
    global bot_process

    if bot_process:
        bot_process.terminate()
        bot_process = None
        status_label.configure(text="Bot Status: STOPPED")

# -------- BOT BUTTONS --------

start_button = ctk.CTkButton(dashboard_frame, text="Start Bot", command=start_bot)
start_button.pack(pady=10)

stop_button = ctk.CTkButton(dashboard_frame, text="Stop Bot", command=stop_bot)
stop_button.pack(pady=10)

# -------- TRADE LOG --------

trade_title = ctk.CTkLabel(dashboard_frame, text="Recent Trades", font=("Arial", 20))
trade_title.pack(pady=20)

trade_log = ctk.CTkTextbox(dashboard_frame, height=200, width=600)
trade_log.pack()

trade_log.insert("end", "No trades yet...\n")

# ---------------- LOGIN FUNCTION ----------------

def login():

    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "1234":

        login_frame.pack_forget()
        dashboard_frame.pack(fill="both", expand=True)

    else:
        print("Invalid Login")

# -------- LOGIN BUTTON --------

login_button = ctk.CTkButton(login_frame, text="Login", command=login)
login_button.pack(pady=20)

# ---------------- RUN APP ----------------

app.mainloop()