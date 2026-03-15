## Market Structure Intelligence (MSI)


> A temporal structural map of global market dependency — built with graph theory, rolling correlations, and network science.

**Live Demo → [Open Dashboard](https://stockmarketproject-dstdrf4h7jqflsc2tsjaku.streamlit.app/)**

---

## What This Is

Most financial dashboards show you **prices**. This one shows you **structure**.

MSI answers a different set of questions:

- Which assets are structurally central to the global market right now?
- How tightly are markets clustering together?
- Is systemic risk building up or dispersing?
- If one asset collapses, which others are most exposed?

This is not a price tracker. It is a **structural intelligence system** — a tool that maps the hidden skeleton of market interdependency at any point in time between 2020 and 2025.

---

## The Concept

### Why Structure Matters

When markets are calm, assets move independently. When stress builds, they start moving together — correlations rise, the network tightens, and diversification breaks down. The moment this happens, a shock to one asset can propagate to all others.

This phenomenon — called **contagion** — is invisible on a price chart. It only becomes visible when you model the market as a **network**.

MSI tracks this structural change over time, date by date, so you can watch contagion risk build and dissolve in real time.

---

## How It Works — Step by Step

### Step 1 — Daily Returns
The system starts with daily percentage returns for 20 global assets from 2020 to 2025. Returns, not prices — because returns capture how assets **move**, not just where they are.

### Step 2 — Rolling Correlation
For each date, a 30 to 60 day rolling window is used to compute a **correlation matrix** — a snapshot of how every asset is moving relative to every other asset at that moment in time. This creates thousands of time-evolving correlation snapshots stored in `rolling_corr.pkl`.

### Step 3 — Distance Transformation
Correlation is converted to **distance** using:

```
distance = sqrt(2 × (1 - correlation))
```

Why? Because correlation is not a proper distance metric — it doesn't satisfy the triangle inequality. This transformation converts it into one, making it usable for graph construction. Assets that are highly correlated end up with small distances between them. Assets that move independently end up far apart.

### Step 4 — Minimum Spanning Tree (MST)
From the full distance matrix, a **Minimum Spanning Tree** is extracted using Kruskal's algorithm. The MST keeps only the most essential connections — the ones that form the structural backbone of the market — while discarding redundant edges.

This is the key insight of the system: the MST reveals the true skeleton of market dependency, stripped of noise.

### Step 5 — Eigenvector Centrality
For each node in the MST, **eigenvector centrality** is computed. This measures not just how many connections a node has, but how important those connections are. A node connected to other highly central nodes scores higher. In market terms — a high centrality asset is a **systemic hub**. Its movement influences everything around it.

### Step 6 — Market Stress Index
The stress index is computed as:

```
Stress Index = Average Correlation × Average Volatility
```

This combines two dimensions of risk — **how correlated** assets are (structural risk) and **how volatile** they are (magnitude risk). A high stress index means markets are both moving violently and moving together — the worst possible combination for a diversified portfolio.

### Step 7 — Kamada-Kawai Layout
The network is visualized using the **Kamada-Kawai layout algorithm**, which positions nodes based on their graph-theoretic distances. Assets that are structurally close appear physically close on screen. Assets that are structurally independent appear far apart. The layout is not arbitrary — it is a direct visual representation of market structure.

---

## What Everything on Screen Means

### Metric Cards
| Metric | What It Means |
|--------|--------------|
| **Market Stress Index** | Overall systemic tension. High = markets are correlated AND volatile simultaneously. Low = calm, diversified structure. |
| **Average Correlation** | How synchronized asset movements are. Above 0.5 = dangerous clustering. Below 0.3 = healthy independence. |
| **Average Volatility** | Mean daily return volatility across all assets. Rising volatility amplifies stress. |

### Network Graph — Node Colors
| Color | Meaning |
|-------|---------|
|  Green | Low eigenvector centrality — peripheral node, limited systemic influence |
|  Yellow | Medium centrality — bridge node, connects clusters, monitor closely |
|  Red | High centrality — systemic hub, most influential, highest contagion risk |

### Network Graph — Edge Weight
Edges represent MST connections. Thicker, brighter edges indicate stronger correlation (shorter distance) between two assets. A tightly clustered graph with many bright edges = high structural stress.

### Top Centrality Panel
Lists the 5 most structurally important assets at the selected date. These are the nodes whose movement has the highest potential to cascade through the network.

### Structure Signal
A real-time interpretation of current market structure:
- **Low stress** — MST is dispersed, assets are structurally independent, diversification is working
- **Moderate stress** — clusters forming, bridge nodes under pressure, early warning signal
- **High stress** — network highly interconnected, contagion pathways active, diversification breaking down

### Cumulative Return Chart
Shows the equal-weighted portfolio return from the start of the dataset. The vertical dashed line marks the currently selected date, letting you correlate structural conditions with actual market performance.

---

## Asset Universe — 20 Global Companies

| Ticker | Company | Country | Sector |
|--------|---------|---------|--------|
| AAPL | Apple | 🇺🇸 USA | Technology |
| MSFT | Microsoft | 🇺🇸 USA | Technology |
| NVDA | NVIDIA | 🇺🇸 USA | Semiconductors |
| AMZN | Amazon | 🇺🇸 USA | E-commerce / Cloud |
| META | Meta Platforms | 🇺🇸 USA | Social Media |
| TSLA | Tesla | 🇺🇸 USA | Electric Vehicles |
| JPM | JPMorgan Chase | 🇺🇸 USA | Banking |
| ASML | ASML Holding | 🇳🇱 Netherlands | Semiconductors |
| SAP | SAP SE | 🇩🇪 Germany | Enterprise Software |
| MC.PA | LVMH | 🇫🇷 France | Luxury Goods |
| NESN.SW | Nestlé | 🇨🇭 Switzerland | Consumer Goods |
| BABA | Alibaba | 🇨🇳 China | E-commerce |
| JD | JD.com | 🇨🇳 China | E-commerce |
| TCEHY | Tencent | 🇨🇳 China | Technology |
| TCS.NS | Tata Consultancy Services | 🇮🇳 India | IT Services |
| RELIANCE.NS | Reliance Industries | 🇮🇳 India | Conglomerate |
| HDFCBANK.NS | HDFC Bank | 🇮🇳 India | Banking |
| 6758.T | Sony Group | 🇯🇵 Japan | Electronics |
| 7203.T | Toyota Motor | 🇯🇵 Japan | Automotive |
| 005930.KS | Samsung Electronics | 🇰🇷 South Korea | Semiconductors |

---
Tech Stack

| Tool | Role |
|------|------|
| **Python** | Core language |
| **Pandas** | Data processing, rolling correlation computation |
| **NetworkX** | Graph construction, MST extraction, eigenvector centrality |
| **SciPy** | Kamada-Kawai layout optimization |
| **Plotly** | Interactive network visualization and charts |
| **Streamlit** | Dashboard interface and deployment |

---

Project Structure
StockMarketProject/
├── app.py                  # Main Streamlit dashboard
├── data_fetch.py           # Data download pipeline
├── prepare_data.py         # Returns computation and preprocessing
├── metrics.py              # Stress index and metric calculations
├── network_graph.py        # Graph construction and MST logic
├── requirements.txt        # Python dependencies
└── data/
    ├── daily_returns.csv        # Time-indexed daily return series
    ├── rolling_corr.pkl         # Precomputed rolling correlation matrices
    └── correlation_matrix.csv   # Static correlation reference
<<<<<<< HEAD


---

## Running Locally

```bash
git clone https://github.com/Sai-fi410/StockMarketProject.git
cd StockMarketProject
pip install -r requirements.txt
streamlit run app.py
```

---

## Key Insight

> Markets do not fail because of price. They fail because of structure. When the network tightens and centrality concentrates, the system becomes brittle. MSI makes that brittleness visible — before it becomes a crisis.
>>>>>>> 3e0f506 (Update README)
