import streamlit as st
import pandas as pd
import pickle
import networkx as nx
import numpy as np
import plotly.graph_objects as go
import time

# PAGE CONFIG
st.set_page_config(layout="wide", page_title="MSI · Market Structure Intelligence")

# FONTS
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Chakra+Petch:wght@400;700&family=Teko:wght@400;600&display=swap" rel="stylesheet">
            """, unsafe_allow_html=True)

# GLOBAL CSS
st.html("""<style>

html, body, [data-testid="stAppViewContainer"] {
    background-color: #020408 !important;
    color: #e8f4f8 !important;
    overflow: hidden !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 60% 40% at 65% 45%, rgba(0,100,255,0.04) 0%, transparent 70%),
        radial-gradient(ellipse 40% 60% at 30% 60%, rgba(0,255,100,0.03) 0%, transparent 70%),
        #020408 !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed; inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.07) 2px, rgba(0,0,0,0.07) 4px);
    pointer-events: none; z-index: 9999;
}

[data-testid="stHeader"] { background: transparent !important; display: none !important; }
[data-testid="stMainBlockContainer"] { padding-top: 8px !important; padding-bottom: 0 !important; }
[data-testid="stMain"] { overflow: hidden !important; }
.block-container { padding-top: 0.5rem !important; padding-bottom: 0 !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: rgba(4,12,20,0.97) !important;
    border-right: 1px solid rgba(0,170,255,0.15) !important;
}
[data-testid="stSidebar"] * { color: #e8f4f8 !important; }
[data-testid="stSidebar"] h1 {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 10px !important; letter-spacing: 0.22em !important;
    color: #00e5ff !important; text-transform: uppercase !important;
    border-bottom: 1px solid rgba(0,170,255,0.2) !important;
    padding-bottom: 8px !important; margin-bottom: 12px !important;
}
[data-testid="stSlider"] label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 10px !important; color: #4a7a8a !important;
}
[data-testid="stSidebar"] button {
    background: transparent !important;
    border: 1px solid rgba(0,229,255,0.25) !important;
    color: #00e5ff !important;
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 8px !important; letter-spacing: 0.12em !important;
    border-radius: 0 !important; width: 100% !important; margin-bottom: 4px !important;
}
[data-testid="stSidebar"] button:hover {
    background: rgba(0,229,255,0.07) !important;
    border-color: #00e5ff !important;
    box-shadow: 0 0 10px rgba(0,229,255,0.18) !important;
}
[data-testid="stDataFrame"] { border: 1px solid rgba(0,170,255,0.12) !important; }
[data-testid="stDataFrame"] * {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 9px !important; background-color: transparent !important; color: #7ab8c8 !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(6,18,30,0.92) !important;
    border: 1px solid rgba(0,170,255,0.1) !important;
    padding: 8px 12px !important; position: relative !important; overflow: hidden !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Chakra Petch', sans-serif !important; font-size: 7px !important;
    letter-spacing: 0.16em !important; color: #4a7a8a !important; text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Teko', sans-serif !important; font-size: 22px !important;
    font-weight: 900 !important; letter-spacing: -0.02em !important;
}
[data-testid="stMetricDelta"] { font-family: 'Share Tech Mono', monospace !important; font-size: 8px !important; }
.stress-val [data-testid="stMetricValue"] { color: #ff3a3a !important; text-shadow: 0 0 16px rgba(255,58,58,0.5) !important; }
.corr-val   [data-testid="stMetricValue"] { color: #f5c518 !important; text-shadow: 0 0 16px rgba(245,197,24,0.5) !important; }
.vol-val    [data-testid="stMetricValue"] { color: #00e5ff !important; text-shadow: 0 0 16px rgba(0,229,255,0.5) !important; }

[data-testid="stHorizontalBlock"] { gap: 6px !important; }
[data-testid="stColumn"] { padding: 0 !important; }
div.element-container { margin-bottom: 0 !important; margin-top: 0 !important; }

.msi-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 4px 0 8px 0; border-bottom: 1px solid rgba(0,170,255,0.12); margin-bottom: 8px;
}
.msi-logo { font-family:'Chakra Petch', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.22em; color: #00e5ff; text-transform: uppercase; }
.msi-logo span { color: #4a7a8a; font-weight: 400; }
.msi-live { display: flex; align-items: center; gap: 5px; font-family: 'Chakra Petch', sans-serif; font-size: 8px; color: #00ff88; }
.live-dot { width: 5px; height: 5px; border-radius: 50%; background: #00ff88; box-shadow: 0 0 6px #00ff88; animation: blink 1.5s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.msi-date { font-family: 'Share Tech Mono', monospace; font-size: 11px; color: #7ab8c8; border: 1px solid rgba(0,170,255,0.2); padding: 3px 10px; }

.sec-lbl {
    font-family: 'Chakra Petch', sans-serif; font-size: 8px; letter-spacing: 0.2em;
    color: #4a7a8a; text-transform: uppercase; display: flex; align-items: center;
    gap: 8px; margin-bottom: 4px; margin-top: 2px;
}
.sec-lbl::after { content: ''; flex: 1; height: 1px; background: rgba(0,170,255,0.12); }

.info-panel { background: rgba(4,12,20,0.95); border: 1px solid rgba(0,170,255,0.1); padding: 10px 9px; }
.panel-title { font-family: 'Chakra Petch', sans-serif; font-size: 7.5px; letter-spacing: 0.18em; color: #4a7a8a; text-transform: uppercase; padding-bottom: 4px; border-bottom: 1px solid rgba(0,170,255,0.1); margin-bottom: 5px; }
.cent-item { margin-bottom: 3px; }
.cent-row { display: flex; justify-content: space-between; }
.cent-name { font-family: 'Share Tech Mono', monospace; font-size: 10px; color: #7ab8c8; }
.cent-score { font-family: 'Share Tech Mono', monospace; font-size: 9px; color: #00e5ff; }
.cent-bar { width: 100%; height: 2px; background: rgba(0,170,255,0.1); border-radius: 1px; margin-top: 2px; margin-bottom: 3px; }
.cent-fill { height: 100%; border-radius: 1px; background: #00e5ff; box-shadow: 0 0 3px #00e5ff; }
.legend-item { display: flex; align-items: flex-start; gap: 6px; margin-bottom: 4px; }
.legend-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; margin-top: 2px; }
.legend-text { font-family: 'Share Tech Mono', monospace; font-size: 8.5px; color: #a0c8d8; line-height: 1.4; }
.signal-text { font-family: 'Share Tech Mono', monospace; font-size: 8.5px; color: #a0c8d8; line-height: 1.8; }

.chart-header { display: flex; align-items: center; gap: 10px; margin-bottom: 3px; margin-top: 3px; }
.chart-title { font-family: 'Chakra Petch', sans-serif; font-size: 10px; letter-spacing: 0.18em; color: #4a7a8a; text-transform: uppercase; }
.chart-val { font-family: 'Share Tech Mono', monospace; font-size: 11px; color: #00ff88; }

/* Pulsing live dot - bigger */
.live-dot {
    width: 8px !important;
    height: 8px !important;
    box-shadow: 0 0 10px #00ff88, 0 0 20px #00ff88 !important;
}

/* Metric card number glow pulse */
[data-testid="stMetricValue"] {
    animation: glow-pulse 1.5s ease-in-out infinite;
}
@keyframes glow-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.55; }
}
        
#MainMenu, footer { visibility: hidden; }
</style>""")

# SESSION STATE
if "play" not in st.session_state:
    st.session_state.play = False

# LOAD DATA
returns = pd.read_csv("data/daily_returns.csv", index_col=0, parse_dates=True)
with open("data/rolling_corr.pkl", "rb") as f:
    rolling_corr = pickle.load(f)
dates = list(rolling_corr.keys())

# SIDEBAR
st.sidebar.title("Market Controls")
selected_date = st.sidebar.select_slider(
    "Select Date", options=dates,
    value=dates[st.session_state.get("date_index", len(dates) - 1)]
    if "date_index" in st.session_state else dates[-1]
)
col_a, col_b = st.sidebar.columns(2)
with col_a:
    if st.button("⏵ Autoplay", key="ap"): st.session_state.play = True
with col_b:
    if st.button("⏸ Pause", key="pa"): st.session_state.play = False

latest_returns = returns.loc[selected_date].sort_values(ascending=False)
ticker_flags = {
    "AAPL": "🇺🇸", "MSFT": "🇺🇸", "NVDA": "🇺🇸", "AMZN": "🇺🇸",
    "META": "🇺🇸", "TSLA": "🇺🇸", "JPM": "🇺🇸",
    "ASML": "🇳🇱", "SAP": "🇩🇪", "MC.PA": "🇫🇷", "NESN.SW": "🇨🇭",
    "BABA": "🇨🇳", "JD": "🇨🇳", "TCEHY": "🇨🇳",
    "TCS.NS": "🇮🇳", "RELIANCE.NS": "🇮🇳", "HDFCBANK.NS": "🇮🇳",
    "6758.T": "🇯🇵", "7203.T": "🇯🇵", "005930.KS": "🇰🇷"
}
latest_returns.index = [f"{ticker_flags.get(t, '')} {t}" for t in latest_returns.index]
st.sidebar.markdown('<div style="font-family:Orbitron,monospace;font-size:7px;letter-spacing:0.18em;color:#4a7a8a;text-transform:uppercase;margin-top:10px;margin-bottom:6px;">Global Ranking</div>', unsafe_allow_html=True)
st.sidebar.dataframe(
    latest_returns.rename("Return").to_frame(),
    use_container_width=True, height=320
)

# AUTOPLAY
if st.session_state.play:
    current_index = dates.index(selected_date)
    if current_index < len(dates) - 1:
        st.session_state.date_index = current_index + 1
        time.sleep(0.15)
        st.rerun()
    else:
        st.session_state.play = False

# COMPUTE
corr = rolling_corr[selected_date]
distance_matrix = np.sqrt(2 * (1 - corr))
avg_corr = corr.values[np.triu_indices_from(corr.values, 1)].mean()
volatility = returns.loc[:selected_date].tail(60).std().mean()
stress_index = avg_corr * volatility

# BUILD GRAPH
G_full = nx.Graph()
for i in range(len(distance_matrix.columns)):
    for j in range(i + 1, len(distance_matrix.columns)):
        s1 = distance_matrix.columns[i]
        s2 = distance_matrix.columns[j]
        G_full.add_edge(s1, s2, weight=distance_matrix.iloc[i, j])
G = nx.minimum_spanning_tree(G_full, weight='weight')
centrality = nx.eigenvector_centrality(G, max_iter=1000)
pos = nx.kamada_kawai_layout(G)

# HEADER
date_str = pd.Timestamp(selected_date).strftime("%Y-%m-%d")
st.markdown(f"""
<div class="msi-header">
    <div class="msi-logo"> Market Structure Intelligence</div>
    <div class="msi-date">{date_str}</div>
    <div class="msi-live"><div class="live-dot"></div>LIVE</div>
</div>""", unsafe_allow_html=True)

# METRICS
stress_label = "↑ HIGH TENSION" if stress_index > 0.01 else "↓ Low tension regime"
corr_label   = "↑ High cohesion" if avg_corr > 0.5 else "↔ Moderate cohesion"
vol_label    = "↑ Elevated vol"  if volatility > 0.02 else "↓ Compressed vol"

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="stress-val">', unsafe_allow_html=True)
    st.metric("⬡  Market Stress Index", round(stress_index, 4), delta=stress_label)
    st.markdown('</div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="corr-val">', unsafe_allow_html=True)
    st.metric("⬡  Average Correlation", round(avg_corr, 3), delta=corr_label)
    st.markdown('</div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="vol-val">', unsafe_allow_html=True)
    st.metric("⬡  Average Volatility", round(volatility, 4), delta=vol_label)
    st.markdown('</div>', unsafe_allow_html=True)

# NETWORK + INFO PANEL
net_col, info_col = st.columns([2.5, 1])

with net_col:
    st.markdown('<div class="sec-lbl">Structural Dependency Network</div>', unsafe_allow_html=True)

    max_cent = max(centrality.values())
    def node_color(c):
        r = c / max_cent if max_cent > 0 else 0
        if r < 0.4:   return "#00ff88"
        elif r < 0.7: return "#f5c518"
        else:         return "#ff3a3a"

    edge_traces = []
    for u, v, d in G.edges(data=True):
        x0, y0 = pos[u]; x1, y1 = pos[v]
        w = d.get('weight', 1)
        alpha = max(0.1, 1 - w * 0.5)
        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None], mode='lines',
            line=dict(width=1.0, color=f"rgba(0,170,255,{alpha:.2f})"),
            hoverinfo='none', showlegend=False
        ))

    nx_, ny_, nt_, nc_, ns_, nh_ = [], [], [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        nx_.append(x); ny_.append(y); nt_.append(node)
        c = centrality[node]
        nc_.append(node_color(c))
        ns_.append(10 + c * 100)
        ret = latest_returns.get(node, 0)
        nh_.append(f"<b>{node}</b><br>Centrality: {c:.4f}<br>Return: {ret:+.4f}<br>Degree: {G.degree(node)}")

    glow = go.Scatter(
        x=nx_, y=ny_, mode='markers',
        marker=dict(size=[s * 1.7 for s in ns_], color=nc_, opacity=0.1, line=dict(width=0)),
        hoverinfo='none', showlegend=False
    )
    nodes_trace = go.Scatter(
        x=nx_, y=ny_, mode='markers+text',
        text=nt_, textposition='middle center',
        textfont=dict(family='Share Tech Mono', size=8, color='#e8f4f8'),
        marker=dict(size=ns_, color=nc_, opacity=0.88, line=dict(width=1.2, color='rgba(255,255,255,0.15)')),
        hovertext=nh_, hoverinfo='text',
        hoverlabel=dict(bgcolor='rgba(4,12,24,0.95)', bordercolor='rgba(0,229,255,0.5)', font=dict(family='Share Tech Mono', size=10, color='#e8f4f8')),
        showlegend=False
    )

    net_fig = go.Figure(data=edge_traces + [glow, nodes_trace])
    net_fig.update_layout(
        paper_bgcolor='rgba(2,6,14,1)', plot_bgcolor='rgba(2,6,14,1)',
        margin=dict(l=8, r=8, t=8, b=8), height=320,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showline=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showline=False, scaleanchor='x'),
        font=dict(family='Share Tech Mono', color='#7ab8c8'), hoverdistance=25,
    )

    st.plotly_chart(net_fig, use_container_width=True, config={"displayModeBar": "hover"})

with info_col:
    sorted_cent = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    max_c = sorted_cent[0][1] if sorted_cent else 1
    colors = ["#00aaff", "#00ff88", "#f5c518", "#ff3a3a", "#aa44ff"]

    cent_rows = ""
    for i, (name, score) in enumerate(sorted_cent):
        pct = int((score / max_c) * 100)
        initials = name.replace(".NS", "").replace(".SW", "").replace(".PA", "").replace(".T", "").replace(".KS", "")[:2]
        bg_color = colors[i % len(colors)]
        logo_html = (
            f'<span style="display:inline-flex;align-items:center;justify-content:center;'
            f'width:16px;height:16px;border-radius:50%;background:{bg_color};'
            f'font-size:7px;font-weight:700;color:#020408;margin-right:5px;'
            f'vertical-align:middle;flex-shrink:0;">{initials}</span>'
        )
        cent_rows += (
            '<div class="cent-item">'
            '<div class="cent-row">'
            f'<span class="cent-name">{logo_html}{name}</span>'
            f'<span class="cent-score">{score:.3f}</span>'
            '</div>'
            f'<div class="cent-bar"><div class="cent-fill" style="width:{pct}%"></div></div>'
            '</div>'
        )

    if stress_index > 0.015:
        signal_color = "#ff3a3a"
        signal_text = "Network highly interconnected. Contagion pathways active. Diversification breaking down."
        signal_cta = "Elevated systemic risk"
    elif stress_index > 0.008:
        signal_color = "#f5c518"
        signal_text = "Correlation clusters forming. Bridge nodes under pressure. Monitor central hubs closely."
        signal_cta = "Moderate systemic risk"
    else:
        signal_color = "#00ff88"
        signal_text = "Markets structurally relaxed. Weak cross-asset coupling. Diversification effective."
        signal_cta = "Minimal systemic risk"

    
    cent_html = (
        '<div class="info-panel">'
        '<div class="panel-title">Top Centrality</div>'
        + cent_rows +
        '<div class="panel-title" style="margin-top:10px;">Node Legend</div>'
        '<div class="legend-item"><div class="legend-dot" style="background:#00ff88;box-shadow:0 0 5px #00ff88"></div><div class="legend-text">Low centrality<br>peripheral</div></div>'
        '<div class="legend-item"><div class="legend-dot" style="background:#f5c518;box-shadow:0 0 5px #f5c518"></div><div class="legend-text">Mid centrality<br>bridge node</div></div>'
        '<div class="legend-item"><div class="legend-dot" style="background:#ff3a3a;box-shadow:0 0 5px #ff3a3a"></div><div class="legend-text">High centrality<br>systemic hub</div></div>'
        '<div class="legend-item"><div class="legend-dot" style="background:rgba(0,170,255,0.3);border:1px solid #00aaff"></div><div class="legend-text">MST edge<br>weight=distance</div></div>'
        '<div class="panel-title" style="margin-top:10px;">Structure Signal</div>'
        f'<div class="signal-text">{signal_text}<br><br>'
        f'<span style="color:{signal_color}">→ {signal_cta}</span></div>'
        '</div>'
    )

    st.markdown(cent_html, unsafe_allow_html=True)


# CHART
market_return = returns.mean(axis=1).cumsum()
current_val = market_return.loc[selected_date] if selected_date in market_return.index else market_return.iloc[-1]
cumul_pct = f"{current_val * 100:+.1f}%"

st.markdown(f'''<div class="chart-header">
    <div class="chart-title">Cumulative Market Return</div>
    <div class="chart-val">{cumul_pct}</div>
</div>''', unsafe_allow_html=True)

chart_fig = go.Figure()
chart_fig.add_trace(go.Scatter(
    x=market_return.index, y=market_return.values,
    fill='tozeroy', fillcolor='rgba(0,255,136,0.06)',
    line=dict(color='rgba(0,255,136,0)', width=0),
    hoverinfo='none', showlegend=False
))
chart_fig.add_trace(go.Scatter(
    x=market_return.index, y=market_return.values,
    mode='lines', line=dict(color='#00ff88', width=1.6),
    hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Return: %{y:.4f}<extra></extra>',
    hoverlabel=dict(bgcolor='rgba(4,12,24,0.95)', bordercolor='rgba(0,255,136,0.5)', font=dict(family='Share Tech Mono', size=10, color='#e8f4f8')),
    showlegend=False
))
chart_fig.add_vline(x=selected_date, line_width=1, line_dash="dash", line_color="rgba(0,229,255,0.35)")
chart_fig.update_layout(
    paper_bgcolor='rgba(4,10,20,1)', plot_bgcolor='rgba(4,10,20,1)',
    height=120, margin=dict(l=36, r=12, t=4, b=24),
    xaxis=dict(showgrid=True, gridcolor='rgba(0,170,255,0.06)', zeroline=False, tickfont=dict(family='Share Tech Mono', size=8, color='#4a7a8a'), showline=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(0,170,255,0.06)', zeroline=True, zerolinecolor='rgba(0,170,255,0.12)', zerolinewidth=1, tickfont=dict(family='Share Tech Mono', size=8, color='#4a7a8a'), showline=False),
    hovermode='x unified',
)
st.plotly_chart(chart_fig, use_container_width=True, config={"displayModeBar": "hover"})
