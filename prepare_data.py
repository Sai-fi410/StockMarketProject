import pandas as pd

returns = pd.read_csv("data/daily_returns.csv", index_col=0, parse_dates=True)

window = 60  # 60-day rolling window

rolling_corr = {}

for date in returns.index[window:]:
    subset = returns.loc[:date].tail(window)
    corr = subset.corr()
    rolling_corr[date] = corr

import pickle
with open("data/rolling_corr.pkl", "wb") as f:
    pickle.dump(rolling_corr, f)
