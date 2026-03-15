import yfinance as yf
import pandas as pd
import numpy as np

#Configuration 

TICKERS = [
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "TSLA", "JPM",
    "BABA", "TCEHY", "JD",
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS",
    "ASML", "SAP", "NESN.SW", "MC.PA",
    "7203.T", "6758.T",
    "005930.KS"
]

START_DATE = "2020-01-01"
END_DATE = "2025-12-31"
INTERVAL = "1d"

# Data Download

print("Downloading data...")

data = yf.download(
    TICKERS,
    start=START_DATE,
    end=END_DATE,
    interval=INTERVAL,
    group_by="ticker",
    auto_adjust=False,
    threads=True
)

print("Download complete.")

# Data Cleaning

if not data.empty:
    data = data.dropna(how="all")
    data = data.ffill()
else:
    print("Warning: Download returned empty dataset.")

# Save to CSV

output_path = "data/global_top20_2020_2025.csv"
data.to_csv(output_path)

print(f"Data saved to {output_path}")
print("Data Layer Build Complete.")