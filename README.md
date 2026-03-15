# Market Structure Intelligence (MSI)

An interactive financial network analysis dashboard that visualizes structural relationships between global assets over time using rolling correlations and graph theory.

## What it does

Instead of tracking prices, MSI tracks **structure** — how assets are connected, how central each one is, and whether the market is clustering or dispersing. At any point in time the dashboard answers:

- How interconnected are assets right now?
- Which assets are structurally central (systemic hubs)?
- Is the market under stress or relaxed?
- Is contagion risk increasing or decreasing?

## How it works

1. **Rolling Correlation** — computes 30–60 day rolling correlation windows across all assets
2. **Distance Transformation** — converts correlation to distance using `sqrt(2 × (1 - correlation))`
3. **Minimum Spanning Tree** — filters the full network to its structural backbone, removing noise
4. **Eigenvector Centrality** — ranks assets by structural importance within the network
5. **Market Stress Index** — computes `avg_correlation × avg_volatility` as a measure of systemic tension

## Tech Stack

- **Python** — core language
- **Pandas** — data processing and rolling computations
- **NetworkX** — graph construction, MST filtering, centrality
- **SciPy** — Kamada–Kawai layout optimization
- **Plotly** — interactive network visualization
- **Streamlit** — dashboard interface

## Dataset

20 global assets across US, Europe, Asia, and India — covering tech, finance, luxury, and emerging markets. Daily returns from 2020 to 2025.

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
StockMarketProject/
├── app.py                  # Main Streamlit dashboard
├── data_fetch.py           # Data download pipeline
├── prepare_data.py         # Returns computation and preprocessing
├── metrics.py              # Stress index and metric calculations
├── network_graph.py        # Graph construction and MST logic
├── data/
│   ├── daily_returns.csv   # Time-indexed asset return series
│   ├── rolling_corr.pkl    # Precomputed rolling correlation matrices
│   └── correlation_matrix.csv
└── requirements.txt
```
