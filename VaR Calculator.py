import numpy as np
import tkinter as tk
from tkinter import messagebox
from alpha_vantage.timeseries import TimeSeries
from config import api_key

def get_data(ticker, interval = 'daily', outputsize = 'compact'):
    timedata = TimeSeries(key = api_key, output_format = 'pandas')
    data, metadata = timedata.get_daily(symbol = ticker, outputsize = outputsize)

    closing = data[['4. close']]
    closing.columns = ['Close']
    return closing

def var_calc(data, confidence_level = 0.95):
    returns = data['Close'].pct_change().dropna()
    var = np.percentile(returns, (1 - confidence_level) * 100)
    return var

def calculate_and_display_var():
    ticker = ticker_entry.get()

    if ticker:
        try:
            stockdata = get_data(ticker)
            VaR = var_calc(stockdata)
            result_label.config(text = f"VaR (95% confidence level): {VaR:.4%}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Error", "Please input a valid ticker.")

def gui():
    root = tk.Tk()
    root.title("VaR Calculator")

    tk.Label(root, text="Enter Ticker:").pack(pady = 10)

    global ticker_entry
    ticker_entry = tk.Entry(root)
    ticker_entry.pack(pady=5)

    calculate_button = tk.Button(root, text="Calculate VaR", command = calculate_and_display_var)
    calculate_button.pack(pady = 20)

    global result_label
    result_label = tk.Label(root, text = "")
    result_label.pack(pady = 10)

    root.mainloop()

if __name__ == "__main__":
    gui()
