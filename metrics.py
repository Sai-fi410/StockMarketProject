import pandas as pd
import numpy as np

# Load Dataset (Multi-Index Header)
file_path = "data/global_top20_2020_2025.csv"

data = pd.read_csv(
    file_path,
    header=[0, 1],  
    index_col=0,
    parse_dates=True
)
print("Dataset loaded successfully.")

# Extract Adjusted Close
adj_close = data.xs("Adj Close", axis=1, level=1)
print("Adjusted Close extracted.")

# Compute Daily Returns
daily_returns = adj_close.pct_change().dropna()
print("Daily returns computed.")

# Save Returns
daily_returns.to_csv("data/daily_returns.csv")
print("Daily returns saved.")

# Compute Mean Daily Returns
mean_returns = daily_returns.mean()
print("\nMean Daily Returns:")
print(mean_returns)

# Compute Correlation Matrix
correlation_matrix = daily_returns.corr()
print("\nCorrelation Matrix:")
print(correlation_matrix)

correlation_matrix.to_csv("data/correlation_matrix.csv")

print("Correlation matrix saved.")
