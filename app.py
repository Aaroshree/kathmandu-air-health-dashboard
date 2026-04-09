"""
Kathmandu Air Pollution & Respiratory Health Dashboard
======================================================
Author  : Data Science Student — 3rd Semester
Data    : Open-Meteo API + Google Trends (2022-08 → 2024-12)
Run     : streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Kathmandu Air & Health Dashboard",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f1117; }


    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #c8d0e7;
        border-left: 4px solid #4c6ef5;
        padding-left: 12px;
        margin: 28px 0 14px 0;
        letter-spacing: 0.03em;
    }

    .warning-banner {
        border-radius: 10px;
        padding: 14px 20px;
        font-size: 0.9rem;
        margin-bottom: 18px;
    }
    .warning-banner.good {
        background: linear-gradient(90deg, #1a3a1a, #1a2e1a);
        border: 1px solid #2ecc71;
        color: #82e0aa;
    }
    .warning-banner.moderate {
        background: linear-gradient(90deg, #3d2e0a, #2e230a);
        border: 1px solid #f39c12;
        color: #fad7a0;
    }
    .warning-banner.unhealthy-sensitive {
        background: linear-gradient(90deg, #3d2800, #2e2000);
        border: 1px solid #e67e22;
        color: #f0b27a;
    }
    .warning-banner.unhealthy {
        background: linear-gradient(90deg, #3d1a1a, #2d1515);
        border: 1px solid #c0392b;
        color: #f1948a;
    }
    .warning-banner.very-unhealthy {
        background: linear-gradient(90deg, #2d1040, #1e0a2e);
        border: 1px solid #8e44ad;
        color: #d7bde2;
    }

    .info-box {
        background: linear-gradient(135deg, #1a2540, #1e2d50);
        border: 1px solid #2e4a7a;
        border-radius: 10px;
        padding: 14px 18px;
        color: #7fb3d3;
        font-size: 0.85rem;
        margin-top: 10px;
    }

    .forecast-notice {
        background: linear-gradient(90deg, #1e1a0a, #2a2410);
        border: 1px solid #f39c12;
        border-radius: 8px;
        padding: 10px 14px;
        color: #fad7a0;
        font-size: 0.8rem;
        margin-bottom: 12px;
    }

    [data-testid="stSidebar"] {
        background: #13161f;
        border-right: 1px solid #252a3a;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #e8ecf5;
        font-size: 0.82rem;
    }

    hr { border-color: #2e3450; margin: 22px 0; }

    div[role="radiogroup"] {
        background: #1e2130;
        border-radius: 10px;
        padding: 4px;
        gap: 2px;
        display: flex;
        flex-wrap: wrap;
    }
    div[role="radiogroup"] > label {
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 7px 18px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        cursor: pointer;
        margin: 0 !important;
        background: #2a2f45 !important;
    }
    div[role="radiogroup"] > label * {
        color: #ffffff !important;
    }
    div[role="radiogroup"] > label p,
    div[role="radiogroup"] > label span,
    div[role="radiogroup"] > label div {
        color: #ffffff !important;
    }
    div[role="radiogroup"] > label:has(input:checked) {
        background: #4c6ef5 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    div[role="radiogroup"] > label:has(input:checked) * {
        color: #ffffff !important;
    }
    div[role="radiogroup"] input[type="radio"] {
        display: none !important;
    }
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 10px;
        margin-bottom: 20px;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1e2130, #252a3a);
        border: 1px solid #2e3450;
        border-radius: 0 0 12px 12px;
        padding: 14px 16px 12px 16px;
    }
    .kpi-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #c8d0e7;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.55rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 6px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-delta {
        font-size: 0.78rem;
        color: #e8ecf5;
    }

    .footer {
        text-align: center;
        color: #c8d0e7;
        font-size: 0.75rem;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #252a3a;
    }

    /* ── Sticky tab bar ── */
    div[role="radiogroup"] {
        position: sticky;
        top: 0;
        z-index: 999;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        background: rgba(15,17,23,0.92) !important;
        border-bottom: 1px solid #2e3450;
        border-radius: 0 !important;
        padding: 6px 8px !important;
        margin: 0 -1rem;
    }

    /* ── Skeleton loader ── */
    .skeleton {
        background: linear-gradient(90deg, #1e2130 25%, #252a3a 50%, #1e2130 75%);
        background-size: 200% 100%;
        animation: shimmer 1.4s infinite;
        border-radius: 8px;
        height: 360px;
        width: 100%;
        margin-bottom: 12px;
    }
    .skeleton-kpi {
        height: 90px;
        border-radius: 8px;
    }
    .skeleton-small {
        height: 20px;
        border-radius: 4px;
        margin-bottom: 8px;
        width: 60%;
    }
    @keyframes shimmer {
        0%   { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    /* ── KPI tooltip ── */
    .kpi-card {
        position: relative;
    }
    .kpi-card .tooltip-icon {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 16px;
        height: 16px;
        background: #2e3450;
        border-radius: 50%;
        color: #8b95b0;
        font-size: 0.65rem;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: help;
        font-weight: 700;
        line-height: 1;
    }
    .kpi-card .tooltip-text {
        visibility: hidden;
        opacity: 0;
        background: #1a1f30;
        color: #c8d0e7;
        font-size: 0.75rem;
        line-height: 1.5;
        border: 1px solid #2e3450;
        border-radius: 8px;
        padding: 8px 12px;
        position: absolute;
        z-index: 9999;
        bottom: calc(100% + 8px);
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        transition: opacity 0.2s ease;
        pointer-events: none;
    }
    .kpi-card .tooltip-text::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 6px solid transparent;
        border-top-color: #2e3450;
    }
    .kpi-card:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }

    /* ── FIX 1: All Streamlit widget label text → white ── */
    /* Checkbox labels */
    div[data-testid="stCheckbox"] label,
    div[data-testid="stCheckbox"] label p,
    div[data-testid="stCheckbox"] label span,
    div[data-testid="stCheckbox"] > label > div,
    div[data-testid="stCheckbox"] > label > div > p {
        color: #ffffff !important;
    }
    /* Checkbox tick box border */
    div[data-testid="stCheckbox"] span[data-baseweb="checkbox"] div {
        border-color: #4c6ef5 !important;
    }
    /* Selectbox label */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] label p {
        color: #ffffff !important;
    }
    /* Selectbox dropdown: text inside the control */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] div {
        color: #ffffff !important;
        background-color: #1e2130 !important;
    }
    /* Multiselect label */
    div[data-testid="stMultiSelect"] label,
    div[data-testid="stMultiSelect"] label p {
        color: #ffffff !important;
    }
    /* Date input label */
    div[data-testid="stDateInput"] label,
    div[data-testid="stDateInput"] label p {
        color: #ffffff !important;
    }
    /* Slider label */
    div[data-testid="stSlider"] label,
    div[data-testid="stSlider"] label p {
        color: #ffffff !important;
    }
    /* Generic widget label fallback (covers future Streamlit versions) */
    .stWidgetLabel p,
    div[class*="stWidgetLabel"] p,
    p[class*="label"] {
        color: #ffffff !important;
    }
    /* Selectbox/dropdown option list */
    ul[data-testid="stSelectboxVirtualDropdown"] li,
    ul[data-testid="stSelectboxVirtualDropdown"] li span {
        color: #ffffff !important;
        background-color: #1e2130 !important;
    }
    /* Sidebar widget labels */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] label p,
    [data-testid="stSidebar"] .stWidgetLabel p {
        color: #e8ecf5 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS — single source of truth
# ─────────────────────────────────────────────
WHO_PM25  = 15.0
WHO_PM10  = 45.0
NEPAL_STD = 40.0

# All colors centralised here
UI_COLOR = {
    "bg":              "#0f1117",
    "card":            "#1e2130",
    "border":          "#2e3450",
    "text":            "#c8d0e7",
    "text_dim":        "#e8ecf5",
    "accent":          "#4c6ef5",
    "good":            "#2ecc71",
    "moderate":        "#f39c12",
    "unhealthy_sens":  "#e67e22",
    "unhealthy":       "#e74c3c",
    "very_unhealthy":  "#8e44ad",
    "pm10_gauge":      "#4c6ef5",
    "risk_gauge":      "#4c6ef5",
}

RISK_COLORS = {
    "Children": "#ef5675",
    "Elderly":  "#ffa600",
    "Asthma":   "#ff764a",
    "Healthy":  "#58a4b0",
}

SEASON_MAP = {
    12: "Winter",      1: "Winter",      2: "Winter",
     3: "Pre-Monsoon", 4: "Pre-Monsoon", 5: "Pre-Monsoon",
     6: "Monsoon",     7: "Monsoon",     8: "Monsoon",
     9: "Post-Monsoon",10: "Post-Monsoon",11: "Post-Monsoon",
}

SEASON_COLORS = {
    "Winter":       "#4e79d8",
    "Pre-Monsoon":  "#f28e2b",
    "Monsoon":      "#59a14f",
    "Post-Monsoon": "#e15759",
}

MONTH_ORDER = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]

# ── FIX 2: Explicit legend font added so legend text is always white ──
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,17,23,0.6)",
    font=dict(color="#ffffff", family="Inter, sans-serif", size=12),
    title_font=dict(color="#ffffff", size=14),
    xaxis=dict(gridcolor="#1e2540", zerolinecolor="#2e3450", linecolor="#2e3450",
               tickfont=dict(color="#ffffff"), title_font=dict(color="#ffffff")),
    yaxis=dict(gridcolor="#1e2540", zerolinecolor="#2e3450", linecolor="#2e3450",
               tickfont=dict(color="#ffffff"), title_font=dict(color="#ffffff")),
    legend=dict(
        bgcolor="rgba(30,33,48,0.8)",
        bordercolor="#4c6ef5",
        borderwidth=1,
        font=dict(color="#ffffff", size=12),   # ← FIX: explicit white legend text
        title_font=dict(color="#ffffff"),
    ),
    margin=dict(l=50, r=30, t=45, b=45),
)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def pm25_color(val):
    """Return (hex_color, label, css_class) for a PM2.5 value."""
    if val <= 12:   return UI_COLOR["good"],           "Good",                        "good"
    if val <= 35.4: return UI_COLOR["moderate"],       "Moderate",                    "moderate"
    if val <= 55.4: return UI_COLOR["unhealthy_sens"], "Unhealthy for Sensitive",     "unhealthy-sensitive"
    if val <= 150:  return UI_COLOR["unhealthy"],      "Unhealthy",                   "unhealthy"
    return UI_COLOR["very_unhealthy"], "Very Unhealthy", "very-unhealthy"


def rolling_mean(series: pd.Series, window: int = 7, min_periods: int = 3) -> pd.Series:
    """Unified rolling mean — single definition used everywhere."""
    return series.rolling(window, min_periods=min_periods).mean()


def skeleton_charts(n_charts: int = 2, show_kpi: bool = False) -> None:
    """Render shimmer skeleton placeholders while charts load."""
    if show_kpi:
        cols = st.columns(5)
        for col in cols:
            with col:
                st.markdown('<div class="skeleton skeleton-kpi"></div>', unsafe_allow_html=True)
        st.markdown('<div class="skeleton-small skeleton"></div>', unsafe_allow_html=True)
    if n_charts == 2:
        c1, c2 = st.columns(2)
        for col in [c1, c2]:
            with col:
                st.markdown('<div class="skeleton"></div>', unsafe_allow_html=True)
    else:
        for _ in range(n_charts):
            st.markdown('<div class="skeleton"></div>', unsafe_allow_html=True)


def safe_pearsonr(x: pd.Series, y: pd.Series):
    """Pearson r with guard for insufficient data. Returns (r, p) or (nan, nan)."""
    mask = x.notna() & y.notna()
    if mask.sum() < 10:
        return np.nan, np.nan
    return stats.pearsonr(x[mask], y[mask])


def apply_plotly_layout(fig, **overrides):
    """Apply shared Plotly layout with optional per-call overrides."""
    layout = {**PLOTLY_LAYOUT, **overrides}
    fig.update_layout(**layout)
    # ── FIX 3: Ensure all axis tick/title fonts are white after layout merge ──
    fig.update_xaxes(tickfont=dict(color="#ffffff"), title_font=dict(color="#ffffff"))
    fig.update_yaxes(tickfont=dict(color="#ffffff"), title_font=dict(color="#ffffff"))
    return fig


KPI_TOOLTIPS = {
    "Mean PM2.5":       "Average fine particulate matter (≤2.5µm) concentration. WHO safe limit is 15 µg/m³. Long-term exposure above this causes respiratory and cardiovascular disease.",
    "WHO Exceedance":   "Percentage of days where PM2.5 exceeded the WHO annual guideline of 15 µg/m³. Higher % means more days of unsafe air quality.",
    "Peak PM2.5":       "Highest single-day PM2.5 reading in the selected period. Extreme spikes are linked to crop burning, festivals, or weather inversions.",
    "Mean Health Risk": "Composite score (0–100) aggregating risk across population groups based on PM2.5 exposure. Above 50 = High Risk.",
    "Mean Cough Index": "Google Trends proxy for respiratory symptoms (cough searches). Peaks typically lag PM2.5 spikes by ~4 days.",
}

def kpi_card(label: str, value: str, delta: str, value_color: str) -> str:
    """Return an HTML KPI card string with colored top stripe, value, and hover tooltip."""
    tip = KPI_TOOLTIPS.get(label, "")
    tooltip_html = (
        f'<div class="tooltip-icon">?</div>'
        f'<div class="tooltip-text">{tip}</div>'
    ) if tip else ""
    return (
        f'<div class="kpi-card" style="border-top: 2px solid {value_color};">'
        f'{tooltip_html}'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value" style="color:{value_color};">{value}</div>'
        f'<div class="kpi-delta">{delta}</div>'
        f'</div>'
    )


# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    try:
        df = pd.read_csv("data/processed/health_risk_dataset.csv", parse_dates=["date"])
    except FileNotFoundError:
        st.error(" `data/processed/health_risk_dataset.csv` not found. "
                 "Make sure you run this from your project root directory.")
        st.stop()

    df = df.sort_values("date").reset_index(drop=True)
    df["month"]      = df["date"].dt.month
    df["year"]       = df["date"].dt.year
    df["season"]     = df["month"].map(SEASON_MAP)
    df["month_name"] = df["date"].dt.strftime("%b")
    df["week"]       = df["date"].dt.isocalendar().week.astype(int)
    df["who_exceed"] = df["pm2_5"] > WHO_PM25
    return df


@st.cache_data(show_spinner=False)
def load_forecast():
    """Load forecast CSV; fall back to synthetic data with a clear flag."""
    try:
        fc = pd.read_csv("data/processed/forecast_90day.csv", parse_dates=["date"])
        return fc, False   # (dataframe, is_synthetic)
    except FileNotFoundError:
        pass

    np.random.seed(42)
    dates  = pd.date_range("2025-04-01", periods=90, freq="D")
    base   = 37.4
    noise  = np.random.normal(0, 6, 90)
    trend  = np.linspace(0, -10, 90)
    vals   = np.clip(base + trend + noise, 12, 85)
    ci_lo  = np.clip(vals - np.linspace(4, 14, 90), 5, None)
    ci_hi  = vals + np.linspace(4, 14, 90)
    fc = pd.DataFrame({"date": dates, "forecast": vals,
                       "ci_lower": ci_lo, "ci_upper": ci_hi})
    return fc, True        # (dataframe, is_synthetic)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar(df):
    with st.sidebar:
        st.markdown(
            "<div style='font-size:0.95rem;font-weight:600;color:#c8d0e7;"
            "letter-spacing:0.04em;padding:4px 0 16px 0;'>Dashboard Controls</div>",
            unsafe_allow_html=True,
        )

        min_d, max_d = df["date"].min().date(), df["date"].max().date()
        st.markdown(
            "<div style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;"
            "color:#8b95b0;margin-bottom:6px;'>Date Range</div>",
            unsafe_allow_html=True,
        )
        date_input = st.date_input(
            "Select period",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
            label_visibility="collapsed",
        )
        if isinstance(date_input, (list, tuple)) and len(date_input) == 2:
            date_range = date_input
        else:
            st.warning("Please select both a start and end date.")
            date_range = (min_d, max_d)

        st.markdown("---")

        st.markdown(
            "<div style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;"
            "color:#8b95b0;margin-bottom:6px;'>Season Filter</div>",
            unsafe_allow_html=True,
        )
        seasons = st.multiselect(
            "Seasons",
            ["Winter", "Pre-Monsoon", "Monsoon", "Post-Monsoon"],
            default=["Winter", "Pre-Monsoon", "Monsoon", "Post-Monsoon"],
            label_visibility="collapsed",
        )
        if not seasons:
            st.warning("Select at least one season.")
            seasons = ["Winter", "Pre-Monsoon", "Monsoon", "Post-Monsoon"]

        st.markdown("---")
        st.markdown(
            "<div style='font-size:0.72rem;color:#c8d0e7;line-height:1.9;'>"
            "<div style='color:#a0aac0;text-transform:uppercase;letter-spacing:0.08em;"
            "font-size:0.68rem;margin-bottom:6px;'>About</div>"
            "Location &mdash; Kathmandu, Nepal<br>"
            "Data period &mdash; Aug 2022 to Dec 2024<br>"
            "Sources &mdash; Open-Meteo, Google Trends<br>"
            "WHO PM2.5 limit &mdash; 15 &mu;g/m&sup3;<br>"
            "Nepal NAAQS &mdash; 40 &mu;g/m&sup3;"
            "</div>",
            unsafe_allow_html=True,
        )

    return date_range, seasons


# ─────────────────────────────────────────────
# TAB 1 — OVERVIEW
# ─────────────────────────────────────────────
def tab_overview(df_f):
    if df_f.empty:
        st.warning("No data available for the selected filters.")
        return

    mean_pm25  = df_f["pm2_5"].mean()
    exceed_pct = df_f["who_exceed"].mean() * 100
    max_pm25   = df_f["pm2_5"].max()
    mean_risk  = df_f["health_risk_score"].mean() if "health_risk_score" in df_f.columns else 0
    mean_cough = df_f["cough"].mean() if "cough" in df_f.columns else 0

    color, label, css_class = pm25_color(mean_pm25)
    peak_color, peak_label, _ = pm25_color(max_pm25)

    # ── KPI row ─────────────────────────────
    risk_color  = (UI_COLOR["unhealthy"] if mean_risk >= 50
                   else UI_COLOR["moderate"] if mean_risk >= 30
                   else UI_COLOR["good"])
    cough_color = UI_COLOR["accent"]

    cards_html = (
        '<div class="kpi-grid">'
        + kpi_card("Mean PM2.5",      f"{mean_pm25:.1f} μg/m³",
                   f"{mean_pm25 - WHO_PM25:+.1f} vs WHO limit", color)
        + kpi_card("WHO Exceedance",  f"{exceed_pct:.1f}%",
                   f"{df_f['who_exceed'].sum()} days unsafe",
                   UI_COLOR["unhealthy"] if exceed_pct > 50 else UI_COLOR["moderate"])
        + kpi_card("Peak PM2.5",      f"{max_pm25:.1f} μg/m³",
                   f"Category: {peak_label}", peak_color)
        + kpi_card("Mean Health Risk", f"{mean_risk:.1f}/100",
                   "Children highest risk" if "risk_children" in df_f.columns else "—",
                   risk_color)
        + kpi_card("Mean Cough Index", f"{mean_cough:.1f}",
                   "Lag peak: Day 4", cough_color)
        + '</div>'
    )
    st.markdown(cards_html, unsafe_allow_html=True)

    # ── AQI banner ──────────────────────────
    st.markdown(f"""
<div class="warning-banner {css_class}">
 <strong>Air Quality Status for Selected Period:</strong> &nbsp;
PM2.5 = <strong>{mean_pm25:.1f} μg/m³</strong> — 
<strong>{mean_pm25/WHO_PM25:.1f}× the WHO guideline</strong>. 
Category: <strong style='color:{color}'>{label}</strong>. 
Days unsafe: <strong>{df_f['who_exceed'].sum()}</strong> of {len(df_f)}.
</div>
""", unsafe_allow_html=True)

    # ── Gauge row ───────────────────────────
    col1, col2, col3 = st.columns(3)

    def make_gauge(val, title, max_val, threshold, bar_color, unit="μg/m³"):
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=val,
            delta={"reference": threshold, "valueformat": ".1f",
                   "increasing": {"color": UI_COLOR["unhealthy"]},
                   "decreasing": {"color": UI_COLOR["good"]}},
            number={"suffix": f" {unit}", "font": {"size": 22, "color": "#ffffff"}},
            title={"text": title, "font": {"size": 13, "color": "#ffffff"}},
            gauge={
                "axis": {"range": [0, max_val], "tickcolor": "#ffffff",
                         "tickfont": {"color": "#ffffff", "size": 10}},
                "bar": {"color": bar_color, "thickness": 0.25},
                "bgcolor": UI_COLOR["card"],
                "bordercolor": UI_COLOR["border"],
                "steps": [
                    {"range": [0, threshold * 0.5],  "color": "#1a2e1a"},
                    {"range": [threshold * 0.5, threshold], "color": "#2e2e1a"},
                    {"range": [threshold, max_val],   "color": "#2e1a1a"},
                ],
                "threshold": {"line": {"color": UI_COLOR["unhealthy"], "width": 2},
                              "thickness": 0.8, "value": threshold},
            }
        ))
        apply_plotly_layout(fig, height=240)
        return fig

    pm25_gauge_color, _, _ = pm25_color(mean_pm25)
    with col1:
        st.plotly_chart(
            make_gauge(mean_pm25, "PM2.5 (Mean)", 100, WHO_PM25, pm25_gauge_color),
            use_container_width=True)
    with col2:
        st.plotly_chart(
            make_gauge(df_f["pm10"].mean(), "PM10 (Mean)", 150, WHO_PM10, UI_COLOR["pm10_gauge"]),
            use_container_width=True)
    with col3:
        st.plotly_chart(
            make_gauge(mean_risk, "Health Risk Score", 100, 50, UI_COLOR["risk_gauge"], unit="/100"),
            use_container_width=True)

    # ── PM2.5 time series ───────────────────
    st.markdown('<div class="section-header">PM2.5 Trend & WHO Thresholds</div>',
                unsafe_allow_html=True)

    ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 2])
    with ctrl1:
        chart_mode = st.radio(
            "Chart mode", ["Standard", "Compare Years"],
            horizontal=True, label_visibility="collapsed",
            key="overview_chart_mode",
        )
    with ctrl2:
        show_anomalies = st.checkbox(" Highlight anomalies (±2 SD)", value=True,
                                      key="show_anomalies")
    with ctrl3:
        overlay = st.selectbox("Overlay", ["None", "Temperature", "Wind Speed"],
                                key="overlay_select")

    # ── Standard mode ───────────────────────
    if chart_mode == "Standard":
        roll = rolling_mean(df_f["pm2_5"])
        mean_val = df_f["pm2_5"].mean()
        std_val  = df_f["pm2_5"].std()
        anomaly_mask = df_f["pm2_5"] > (mean_val + 2 * std_val)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=pd.concat([df_f["date"], df_f["date"][::-1]]),
            y=pd.concat([
                pd.Series([mean_val + 2 * std_val] * len(df_f)),
                pd.Series([mean_val - 2 * std_val] * len(df_f))[::-1],
            ]),
            fill="toself", fillcolor="rgba(76,110,245,0.07)",
            line=dict(color="rgba(0,0,0,0)"),
            name="±2 SD Band", hoverinfo="skip",
        ))

        fig.add_trace(go.Scatter(
            x=df_f["date"], y=df_f["pm2_5"], name="Daily PM2.5",
            line=dict(color=UI_COLOR["accent"], width=1), opacity=0.4, mode="lines"))
        fig.add_trace(go.Scatter(
            x=df_f["date"], y=roll, name="7-Day Rolling Avg",
            line=dict(color="#74b9ff", width=2.5)))

        if show_anomalies and anomaly_mask.any():
            df_anom = df_f[anomaly_mask]
            fig.add_trace(go.Scatter(
                x=df_anom["date"], y=df_anom["pm2_5"],
                mode="markers", name=f"Anomaly (>{mean_val + 2*std_val:.0f} μg/m³)",
                marker=dict(color=UI_COLOR["unhealthy"], size=8,
                            symbol="circle", line=dict(color="#fff", width=1)),
                hovertemplate="<b>%{x|%d %b %Y}</b><br>PM2.5: %{y:.1f} μg/m³<extra>Anomaly</extra>",
            ))
            for _, row in df_anom.iterrows():
                fig.add_vrect(
                    x0=row["date"] - pd.Timedelta(hours=12),
                    x1=row["date"] + pd.Timedelta(hours=12),
                    fillcolor="rgba(231,76,60,0.12)", line_width=0,
                )

        if overlay != "None":
            overlay_col = "temperature_2m_mean" if overlay == "Temperature" else "windspeed_10m_max"
            overlay_label = "Temp (°C)" if overlay == "Temperature" else "Wind Speed (km/h)"
            overlay_color = "#fd7e14" if overlay == "Temperature" else "#20c997"
            if overlay_col in df_f.columns:
                fig.add_trace(go.Scatter(
                    x=df_f["date"], y=df_f[overlay_col],
                    name=overlay_label,
                    line=dict(color=overlay_color, width=1.5, dash="dot"),
                    opacity=0.8,
                    yaxis="y2",
                ))
                fig.update_layout(
                    yaxis2=dict(
                        title=overlay_label,
                        overlaying="y", side="right",
                        gridcolor="rgba(0,0,0,0)",
                        tickfont=dict(color=overlay_color),
                        title_font=dict(color=overlay_color),
                    )
                )

        fig.add_hline(y=WHO_PM25, line_dash="dash",
                      line_color=UI_COLOR["good"], line_width=1.5,
                      annotation_text=f"WHO {WHO_PM25} μg/m³",
                      annotation_font_color="#ffffff",
                      annotation_bgcolor=UI_COLOR["good"],
                      annotation_bordercolor=UI_COLOR["good"])
        fig.add_hline(y=NEPAL_STD, line_dash="dot",
                      line_color=UI_COLOR["moderate"], line_width=1.5,
                      annotation_text=f"Nepal NAAQS {NEPAL_STD} μg/m³",
                      annotation_font_color="#ffffff",
                      annotation_bgcolor=UI_COLOR["moderate"],
                      annotation_bordercolor=UI_COLOR["moderate"])

        n_anom = anomaly_mask.sum()
        title = (f"Daily PM2.5 — Kathmandu"
                 + (f"  |   {n_anom} anomaly days" if show_anomalies and n_anom else ""))
        apply_plotly_layout(fig, height=400,
                            yaxis_title="PM2.5 (μg/m³)", xaxis_title="Date",
                            title=title)
        st.plotly_chart(fig, use_container_width=True)

        if show_anomalies and anomaly_mask.any():
            with st.expander(f" View {n_anom} anomaly days"):
                anom_df = df_f[anomaly_mask][["date", "pm2_5", "season"]].copy()
                anom_df["pm2_5"] = anom_df["pm2_5"].round(1)
                anom_df.columns = ["Date", "PM2.5 (μg/m³)", "Season"]
                st.dataframe(anom_df.reset_index(drop=True), use_container_width=True)

    # ── Compare Years mode ───────────────────
    else:
        YEAR_COLORS = {2022: "#4c6ef5", 2023: "#f39c12", 2024: "#2ecc71", 2025: "#e74c3c"}
        fig = go.Figure()

        years_available = sorted(df_f["year"].unique())
        for yr in years_available:
            yr_df = df_f[df_f["year"] == yr].copy()
            yr_df = yr_df.sort_values("date")
            yr_df["doy"] = yr_df["date"].dt.dayofyear
            roll_yr = rolling_mean(yr_df["pm2_5"])
            c = YEAR_COLORS.get(yr, UI_COLOR["accent"])

            fig.add_trace(go.Scatter(
                x=yr_df["doy"], y=yr_df["pm2_5"],
                name=f"{yr} daily",
                line=dict(color=c, width=1), opacity=0.25, mode="lines",
                showlegend=False,
            ))
            fig.add_trace(go.Scatter(
                x=yr_df["doy"], y=roll_yr,
                name=str(yr),
                line=dict(color=c, width=2.5),
                hovertemplate=f"<b>{yr}</b> — Day %{{x}}<br>PM2.5 (7d avg): %{{y:.1f}} μg/m³<extra></extra>",
            ))

            if show_anomalies:
                mean_yr = yr_df["pm2_5"].mean()
                std_yr  = yr_df["pm2_5"].std()
                anom_yr = yr_df[yr_df["pm2_5"] > mean_yr + 2 * std_yr]
                if not anom_yr.empty:
                    fig.add_trace(go.Scatter(
                        x=anom_yr["doy"], y=anom_yr["pm2_5"],
                        mode="markers", name=f"{yr} anomaly",
                        marker=dict(color=c, size=7, symbol="x",
                                    line=dict(color="#fff", width=1)),
                        showlegend=False,
                        hovertemplate=f"<b>{yr} anomaly</b> — Day %{{x}}<br>%{{y:.1f}} μg/m³<extra></extra>",
                    ))

        month_doys  = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
        month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                       "Jul","Aug","Sep","Oct","Nov","Dec"]
        fig.update_xaxes(
            tickvals=month_doys, ticktext=month_names,
            title_text="Month",
        )
        fig.add_hline(y=WHO_PM25, line_dash="dash",
                      line_color=UI_COLOR["good"], line_width=1.5,
                      annotation_text=f"WHO {WHO_PM25} μg/m³",
                      annotation_font_color="#ffffff",
                      annotation_bgcolor=UI_COLOR["good"],
                      annotation_bordercolor=UI_COLOR["good"])
        fig.add_hline(y=NEPAL_STD, line_dash="dot",
                      line_color=UI_COLOR["moderate"], line_width=1.5,
                      annotation_text=f"Nepal NAAQS {NEPAL_STD} μg/m³",
                      annotation_font_color="#ffffff",
                      annotation_bgcolor=UI_COLOR["moderate"],
                      annotation_bordercolor=UI_COLOR["moderate"])
        apply_plotly_layout(fig, height=420,
                            yaxis_title="PM2.5 (μg/m³)",
                            title="Year-over-Year PM2.5 Comparison — Kathmandu (7-Day Rolling Avg)")
        st.plotly_chart(fig, use_container_width=True)

        yoy = (df_f.groupby("year")["pm2_5"]
               .agg(Mean="mean", Median="median", Peak="max",
                    Days_Unsafe=lambda x: (x > WHO_PM25).sum())
               .round(1).reset_index())
        yoy.columns = ["Year", "Mean (μg/m³)", "Median", "Peak", "Days > WHO"]
        st.dataframe(yoy, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# TAB 2 — SEASONAL ANALYSIS
# ─────────────────────────────────────────────
def tab_seasonal(df_f):
    if df_f.empty:
        st.warning("No data available for the selected filters.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Monthly PM2.5 Distribution</div>',
                    unsafe_allow_html=True)
        df_plot = df_f.copy()
        df_plot["month_name"] = pd.Categorical(df_plot["month_name"],
                                               categories=MONTH_ORDER, ordered=True)
        df_sorted = df_plot.sort_values("month_name")

        fig = go.Figure()
        months_present = [m for m in MONTH_ORDER
                          if m in df_sorted["month_name"].cat.categories
                          and len(df_sorted[df_sorted["month_name"] == m]) > 0]

        if months_present:
            for m in months_present:
                sub = df_sorted[df_sorted["month_name"] == m]["pm2_5"]
                fig.add_trace(go.Box(
                    y=sub, name=m,
                    marker_color=UI_COLOR["accent"],
                    line_color="#6c8ef5",
                    fillcolor="rgba(76,110,245,0.25)",
                ))
            fig.add_hline(y=WHO_PM25, line_dash="dash",
                          line_color=UI_COLOR["good"], line_width=1.5,
                          annotation_text="WHO 15 μg/m³",
                          annotation_font_color="#ffffff",
                          annotation_bgcolor=UI_COLOR["good"])
            apply_plotly_layout(fig, height=380,
                                yaxis_title="PM2.5 (μg/m³)", showlegend=False,
                                title="Monthly Distribution of PM2.5")
        else:
            fig.add_annotation(text="No data for selected months",
                               xref="paper", yref="paper", x=0.5, y=0.5,
                               font=dict(color="#ffffff", size=14),
                               showarrow=False)
            apply_plotly_layout(fig, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Seasonal Average PM2.5</div>',
                    unsafe_allow_html=True)
        seas_avg = (df_f.groupby("season")["pm2_5"]
                    .agg(["mean", "std", "count"])
                    .reset_index())
        seas_avg.columns = ["season", "mean", "std", "n"]

        fig = go.Figure()
        for _, row in seas_avg.iterrows():
            c = SEASON_COLORS.get(row["season"], UI_COLOR["accent"])
            fig.add_trace(go.Bar(
                x=[row["season"]], y=[row["mean"]],
                error_y=dict(type="data", array=[row["std"]], color="#ffffff"),
                name=row["season"],
                marker_color=c,
                marker_line_color=c,
                text=[f'{row["mean"]:.1f} μg/m³'], textposition="outside",
                textfont=dict(color="#ffffff"),
            ))
        fig.add_hline(y=WHO_PM25, line_dash="dash",
                      line_color=UI_COLOR["good"], line_width=1.5,
                      annotation_text="WHO 15 μg/m³",
                      annotation_font_color="#ffffff",
                      annotation_bgcolor=UI_COLOR["good"])
        apply_plotly_layout(fig, height=380, showlegend=False,
                            yaxis_title="Mean PM2.5 (μg/m³)",
                            title="Seasonal PM2.5 Averages (± SD)")
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap
    st.markdown('<div class="section-header">PM2.5 Heatmap — Month × Year</div>',
                unsafe_allow_html=True)
    pivot = (df_f.groupby(["year", "month_name"])["pm2_5"]
             .mean().reset_index()
             .pivot(index="year", columns="month_name", values="pm2_5"))
    cols_present = [m for m in MONTH_ORDER if m in pivot.columns]
    pivot = pivot[cols_present]

    if not pivot.empty:
        fig = px.imshow(
            pivot,
            color_continuous_scale=[[0, "#1a3a1a"], [0.3, "#4c6ef5"],
                                     [0.6, "#f39c12"], [1, "#e74c3c"]],
            text_auto=".1f",
            aspect="auto",
        )
        fig.update_traces(textfont=dict(color="white", size=11))
        apply_plotly_layout(fig, height=260,
                            coloraxis_colorbar=dict(
                                title="PM2.5<br>(μg/m³)",
                                tickfont=dict(color="#ffffff"),
                                title_font=dict(color="#ffffff")),
                            xaxis_title="Month", yaxis_title="Year",
                            title="Average Monthly PM2.5 by Year")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data to render the heatmap for the selected filters.")

    # Correlation matrix
    st.markdown('<div class="section-header">Pollutant × Health Correlation Matrix</div>',
                unsafe_allow_html=True)
    corr_cols = ["pm2_5", "pm10", "carbon_monoxide", "nitrogen_dioxide",
                 "ozone", "temperature_2m_mean", "precipitation_sum",
                 "cough", "asthma", "health_risk_score"]
    corr_cols = [c for c in corr_cols if c in df_f.columns]

    if len(corr_cols) >= 2:
        corr = df_f[corr_cols].corr()
        fig = px.imshow(corr, color_continuous_scale="RdBu_r",
                        zmin=-1, zmax=1, text_auto=".2f")
        fig.update_traces(textfont=dict(size=10, color="#ffffff"))
        apply_plotly_layout(fig, height=420,
                            title="Pearson Correlation — Pollutants & Health Indicators")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough numeric columns available for a correlation matrix.")


# ─────────────────────────────────────────────
# TAB 3 — HEALTH RISK
# ─────────────────────────────────────────────
def tab_health(df_f):
    if df_f.empty:
        st.warning("No data available for the selected filters.")
        return

    group_col = {
        "Children": "risk_children",
        "Elderly":  "risk_elderly",
        "Asthma":   "risk_asthma",
        "Healthy":  "risk_healthy",
    }
    available_groups = {g: c for g, c in group_col.items() if c in df_f.columns}

    st.markdown('<div class="section-header">Population Risk Summary</div>',
                unsafe_allow_html=True)
    if available_groups:
        cards_html = '<div class="kpi-grid" style="grid-template-columns: repeat(' + str(len(available_groups)) + ', minmax(0,1fr));">'
        for grp, col in available_groups.items():
            mean_r = df_f[col].mean()
            max_r  = df_f[col].max()
            cards_html += kpi_card(grp, f"{mean_r:.1f}", f"Peak: {max_r:.0f}", RISK_COLORS[grp])
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)
    else:
        st.info("No group risk columns found in dataset.")

    st.markdown('<div class="section-header">Health Risk Score Over Time — All Groups</div>',
                unsafe_allow_html=True)
    fig = go.Figure()
    for grp, col in available_groups.items():
        roll = rolling_mean(df_f[col])
        fig.add_trace(go.Scatter(
            x=df_f["date"], y=roll,
            name=grp,
            line=dict(color=RISK_COLORS[grp], width=2.2),
        ))
    if available_groups:
        fig.add_hline(y=50, line_dash="dash", line_color=UI_COLOR["unhealthy"],
                      line_width=1.5, annotation_text="High Risk threshold (50)",
                      annotation_font_color="#ffffff",
                      annotation_bgcolor=UI_COLOR["unhealthy"])
    apply_plotly_layout(fig, height=380,
                        yaxis_title="Risk Score (0–100)",
                        title="7-Day Rolling Health Risk Score by Population Group")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Risk Level Distribution</div>',
                    unsafe_allow_html=True)
        if "risk_level" in df_f.columns:
            risk_counts = df_f["risk_level"].value_counts().reset_index()
            risk_counts.columns = ["level", "days"]
            color_map = {
                "Low": UI_COLOR["good"], "Moderate": UI_COLOR["moderate"],
                "High": UI_COLOR["unhealthy_sens"], "Very High": UI_COLOR["unhealthy"],
                "Hazardous": UI_COLOR["very_unhealthy"],
            }
            fig = px.pie(risk_counts, values="days", names="level",
                         color="level", color_discrete_map=color_map, hole=0.45)
            fig.update_traces(
                textinfo="percent+label",
                textfont=dict(color="white", size=12),
                marker=dict(line=dict(color="#0f1117", width=2)),
            )
            apply_plotly_layout(fig, height=360, showlegend=True,
                                title="Days by Risk Level Category")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("'risk_level' column not found in dataset.")

    with col2:
        st.markdown('<div class="section-header">Risk Score vs PM2.5</div>',
                    unsafe_allow_html=True)
        focus_col = "health_risk_score" if "health_risk_score" in df_f.columns else None
        if focus_col and len(df_f) >= 10:
            fig = px.scatter(
                df_f, x="pm2_5", y=focus_col,
                color="season",
                color_discrete_map=SEASON_COLORS,
                opacity=0.65,
                trendline="ols",
                trendline_color_override="#ffffff",
            )
            fig.add_vline(x=WHO_PM25, line_dash="dash",
                          line_color=UI_COLOR["good"], line_width=1.5)
            apply_plotly_layout(fig, height=360,
                                xaxis_title="PM2.5 (μg/m³)",
                                yaxis_title="Health Risk Score",
                                title="PM2.5 vs Overall Health Risk Score")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data for scatter plot (minimum 10 rows required).")

    st.markdown('<div class="section-header">Seasonal Risk Breakdown by Group</div>',
                unsafe_allow_html=True)
    rows = []
    for grp, col in available_groups.items():
        for seas in df_f["season"].unique():
            sub = df_f[df_f["season"] == seas][col]
            rows.append({"Group": grp, "Season": seas, "Mean Risk": sub.mean()})

    if rows:
        risk_seas = pd.DataFrame(rows)
        fig = px.bar(risk_seas, x="Season", y="Mean Risk", color="Group",
                     barmode="group", color_discrete_map=RISK_COLORS)
        fig.add_hline(y=50, line_dash="dash", line_color=UI_COLOR["unhealthy"],
                      line_width=1.5,
                      annotation_text="High Risk (50)",
                      annotation_font_color="#ffffff",
                      annotation_bgcolor=UI_COLOR["unhealthy"])
        apply_plotly_layout(fig, height=360,
                            yaxis_title="Mean Risk Score (0–100)",
                            title="Average Health Risk Score by Season and Population Group")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No group risk data available for seasonal breakdown.")


# ─────────────────────────────────────────────
# TAB 4 — FORECAST
# ─────────────────────────────────────────────
def tab_forecast(df_f):
    if df_f.empty:
        st.warning("No data available for the selected filters.")
        return

    fc, is_synthetic = load_forecast()

    if is_synthetic:
        st.markdown("""
<div class="forecast-notice">
 <strong>Note:</strong> Forecast CSV not found — displaying synthetic illustrative data 
based on SARIMAX model parameters. Run your forecast pipeline to load real predictions.
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="info-box">
<strong>SARIMAX 90-Day Forecast</strong> — Apr–Jul 2025 &nbsp;|&nbsp; 
Forecast mean: <strong>37.4 μg/m³</strong> &nbsp;|&nbsp;
All forecast days exceed WHO limit (15 μg/m³) &nbsp;|&nbsp;
Monsoon arrival expected to bring relief in late June–July.
</div>
""", unsafe_allow_html=True)

    hist_tail = df_f[["date", "pm2_5"]].tail(180)
    y_max = max(fc["ci_upper"].max(), hist_tail["pm2_5"].max()) * 0.9

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist_tail["date"], y=hist_tail["pm2_5"],
        name="Historical PM2.5",
        line=dict(color=UI_COLOR["accent"], width=2),
    ))
    fig.add_trace(go.Scatter(
        x=pd.concat([fc["date"], fc["date"][::-1]]),
        y=pd.concat([fc["ci_upper"], fc["ci_lower"][::-1]]),
        fill="toself",
        fillcolor="rgba(255,165,0,0.15)",
        line=dict(color="rgba(0,0,0,0)"),
        name="95% Confidence Interval",
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=fc["date"], y=fc["forecast"],
        name="SARIMAX Forecast",
        line=dict(color="#ffa600", width=2.5, dash="dot"),
    ))
    fig.add_hline(y=WHO_PM25, line_dash="dash",
                  line_color=UI_COLOR["good"], line_width=1.5,
                  annotation_text="WHO 15 μg/m³",
                  annotation_font_color="#ffffff",
                  annotation_bgcolor=UI_COLOR["good"])
    fig.add_hline(y=NEPAL_STD, line_dash="dot",
                  line_color=UI_COLOR["moderate"], line_width=1.5,
                  annotation_text="Nepal NAAQS 40 μg/m³",
                  annotation_font_color="#ffffff",
                  annotation_bgcolor=UI_COLOR["moderate"])
    fig.add_vline(x="2025-04-01", line_dash="dash",
                  line_color="#ffffff", line_width=1)
    fig.add_annotation(
        x="2025-04-01", y=y_max,
        text="Forecast start",
        showarrow=False,
        font=dict(color="#ffffff", size=12),
        xanchor="center",
    )
    apply_plotly_layout(fig, height=420,
                        yaxis_title="PM2.5 (μg/m³)",
                        title="SARIMAX 90-Day PM2.5 Forecast with Confidence Interval")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Monthly Forecast Summary</div>',
                    unsafe_allow_html=True)
        fc["month"] = fc["date"].dt.strftime("%B %Y")
        fc_monthly = (fc.groupby("month")
                      .agg(Mean=("forecast", "mean"),
                           Min=("ci_lower", "min"),
                           Max=("ci_upper", "max"))
                      .round(1).reset_index())
        st.dataframe(fc_monthly, use_container_width=True, hide_index=True)

    with col2:
        st.markdown('<div class="section-header">Days Above Thresholds (Forecast)</div>',
                    unsafe_allow_html=True)
        thresholds = [
            ("WHO (15 μg/m³)", 15),
            ("Nepal NAAQS (40 μg/m³)", 40),
            ("Unhealthy (55 μg/m³)", 55),
            ("Very Unhealthy (150 μg/m³)", 150),
        ]
        thresh_data = pd.DataFrame({
            "Threshold":  [t[0] for t in thresholds],
            "Days Above": [(fc["forecast"] > t[1]).sum() for t in thresholds],
            "Percentage": [f"{(fc['forecast'] > t[1]).mean()*100:.1f}%" for t in thresholds],
        })
        st.dataframe(thresh_data, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# TAB 5 — LAG CORRELATION
# ─────────────────────────────────────────────
def tab_lag(df_f):
    if df_f.empty:
        st.warning("No data available for the selected filters.")
        return

    st.markdown("""
<div class="info-box">
🔬 <strong>Lag Correlation Analysis</strong> — How many days after a PM2.5 spike do health 
outcomes peak? Your EDA found PM2.5 → Cough peaks at <strong>Day 4 (r = 0.327)</strong>. 
Explore lags 0–21 days across all health indicators below.
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col2:
        available_health = [c for c in ["cough", "asthma", "health_risk_score",
                                         "health_proxy_score"] if c in df_f.columns]
        available_pollutants = [c for c in ["pm2_5", "pm10", "nitrogen_dioxide",
                                             "carbon_monoxide", "ozone"] if c in df_f.columns]
        if not available_health or not available_pollutants:
            st.info("Required health or pollutant columns not found.")
            return

        health_indicator = st.selectbox("Health Indicator", available_health)
        pollutant        = st.selectbox("Pollutant",         available_pollutants)
        max_lag          = st.slider("Max lag (days)", 7, 30, 21)

    lags, corrs, pvals = [], [], []
    for lag in range(0, max_lag + 1):
        r, p = safe_pearsonr(df_f[pollutant].shift(lag), df_f[health_indicator])
        if not np.isnan(r):
            lags.append(lag)
            corrs.append(r)
            pvals.append(p)

    if not lags:
        st.warning("Not enough overlapping data to compute lag correlations.")
        return

    lag_df   = pd.DataFrame({"lag": lags, "r": corrs, "p": pvals})
    best_idx = lag_df["r"].idxmax()
    peak_lag = lag_df.loc[best_idx]

    with col1:
        st.markdown('<div class="section-header">Cross-Correlation: Pollutant Lag → Health Outcome</div>',
                    unsafe_allow_html=True)

        n = len(df_f)
        sig_threshold = 1.96 / np.sqrt(n) if n > 4 else 0.5

        fig = go.Figure()
        fig.add_hrect(y0=-sig_threshold, y1=sig_threshold,
                      fillcolor="rgba(255,255,255,0.05)", line_width=0,
                      annotation_text="Not significant (α=0.05)",
                      annotation_font_color="#ffffff")

        bar_colors = [UI_COLOR["unhealthy"] if r == lag_df["r"].max()
                      else UI_COLOR["accent"] for r in lag_df["r"]]
        fig.add_trace(go.Bar(
            x=lag_df["lag"], y=lag_df["r"],
            marker_color=bar_colors,
            name="Pearson r",
            text=[f"r={r:.3f}" if i == best_idx else ""
                  for i, r in enumerate(lag_df["r"])],
            textposition="outside",
            textfont=dict(color="#ffffff"),
        ))
        fig.add_vline(x=peak_lag["lag"], line_dash="dash",
                      line_color=UI_COLOR["unhealthy"], line_width=1.5,
                      annotation_text=f"Peak lag: Day {int(peak_lag['lag'])}",
                      annotation_font_color="#ffffff",
                      annotation_bgcolor=UI_COLOR["unhealthy"])
        apply_plotly_layout(fig, height=380,
                            xaxis_title="Lag (days)", yaxis_title="Pearson r",
                            title=f"Lag Correlation: {pollutant} → {health_indicator}")
        st.plotly_chart(fig, use_container_width=True)

    best_lag_val = int(peak_lag["lag"])
    st.markdown(f'<div class="section-header">Scatter at Peak Lag (Day {best_lag_val})</div>',
                unsafe_allow_html=True)

    df_lag = df_f[[pollutant, health_indicator, "season"]].copy()
    df_lag["lagged_pollutant"] = df_lag[pollutant].shift(best_lag_val)
    df_lag = df_lag.dropna(subset=["lagged_pollutant", health_indicator])

    if len(df_lag) >= 10:
        fig = px.scatter(
            df_lag, x="lagged_pollutant", y=health_indicator,
            color="season", color_discrete_map=SEASON_COLORS,
            opacity=0.6, trendline="ols", trendline_color_override="#ffffff",
            labels={
                "lagged_pollutant": f"{pollutant} (lagged {best_lag_val}d)",
                health_indicator: health_indicator,
            },
        )
        apply_plotly_layout(fig, height=360,
                            title=f"Scatter: {pollutant} (lag {best_lag_val}d) vs "
                                  f"{health_indicator} | r = {peak_lag['r']:.3f}, "
                                  f"p = {peak_lag['p']:.4f}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Only {len(df_lag)} rows remain after lag shift — "
                   "too few for a reliable scatter plot. Try a shorter lag or wider date range.")

    st.markdown('<div class="section-header">Full Lag Correlation Table</div>',
                unsafe_allow_html=True)
    lag_display = lag_df.copy()
    lag_display["significant"] = lag_display["p"] < 0.05
    lag_display = lag_display.rename(columns={
        "lag": "Lag (days)", "r": "Pearson r", "p": "p-value",
        "significant": "Significant (α=0.05)"
    })
    lag_display["Pearson r"] = lag_display["Pearson r"].round(4)
    lag_display["p-value"]   = lag_display["p-value"].round(4)
    st.dataframe(lag_display, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# TAB 6 — RAW DATA
# ─────────────────────────────────────────────
def tab_data(df_f):
    if df_f.empty:
        st.warning("No data available for the selected filters.")
        return

    st.markdown('<div class="section-header">Filtered Dataset Preview</div>',
                unsafe_allow_html=True)

    date_range_str = f"{df_f['date'].min().date()} &rarr; {df_f['date'].max().date()}"
    cards_html = (
        '<div class="kpi-grid" style="grid-template-columns: repeat(3, minmax(0,1fr));">'
        + kpi_card("Rows (filtered)", str(len(df_f)), "after date &amp; season filter", UI_COLOR["accent"])
        + kpi_card("Date range", date_range_str, "selected period", UI_COLOR["accent"])
        + kpi_card("Columns", str(len(df_f.columns)), "in dataset", UI_COLOR["accent"])
        + '</div>'
    )
    st.markdown(cards_html, unsafe_allow_html=True)

    all_cols  = df_f.columns.tolist()
    show_cols = st.multiselect("Select columns to display",
                               all_cols, default=all_cols[:10])
    if show_cols:
        st.dataframe(df_f[show_cols].reset_index(drop=True),
                     use_container_width=True, height=400)

    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download filtered CSV", data=csv,
                       file_name="filtered_data.csv", mime="text/csv")

    st.markdown('<div class="section-header">Descriptive Statistics</div>',
                unsafe_allow_html=True)
    num_cols = df_f.select_dtypes(include=np.number).columns.tolist()
    if num_cols:
        st.dataframe(df_f[num_cols].describe().round(3), use_container_width=True)
    else:
        st.info("No numeric columns to summarise.")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    st.markdown(
        "<div style='text-align:center;padding:10px 0 24px 0;'>"
        "<h1 style='color:#e8ecf5;font-size:1.9rem;font-weight:700;"
        "letter-spacing:0.02em;margin-bottom:6px;'>"
        "Kathmandu Air Pollution &amp; Respiratory Health"
        "</h1>"
        "<p style='color:#a0aac0;font-size:0.82rem;letter-spacing:0.06em;"
        "text-transform:uppercase;'>"
        "Data Science Project &nbsp;&middot;&nbsp; Aug 2022 &ndash; Dec 2024 "
        "&nbsp;&middot;&nbsp; Open-Meteo &amp; Google Trends"
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    _skeleton_ph = st.empty()
    with _skeleton_ph.container():
        skeleton_charts(n_charts=1, show_kpi=True)
        skeleton_charts(n_charts=2, show_kpi=False)
    df = load_data()
    _skeleton_ph.empty()

    date_range, seasons = render_sidebar(df)

    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    df_f = df[(df["date"] >= start) & (df["date"] <= end) & (df["season"].isin(seasons))].copy()

    if df_f.empty:
        st.warning("No data for the selected filters. Please adjust the date range or season.")
        return

    df_f["pm25_roll"] = rolling_mean(df_f["pm2_5"])

    TAB_NAMES = ["Overview", "Seasonal", "Health Risk",
                 "Forecast", "Lag Correlation", "Raw Data"]

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Overview"

    selected = st.radio(
        "tab_nav",
        TAB_NAMES,
        index=TAB_NAMES.index(st.session_state.active_tab),
        horizontal=True,
        label_visibility="collapsed",
        key="active_tab",
    )

    st.markdown("<div style='border-top:1px solid #2e3450;margin:0 0 20px 0;'></div>",
                unsafe_allow_html=True)

    _tab_ph = st.empty()
    with _tab_ph.container():
        if selected == "Overview":
            skeleton_charts(n_charts=1, show_kpi=True)
            skeleton_charts(n_charts=2)
        elif selected in ("Seasonal", "Health Risk"):
            skeleton_charts(n_charts=2)
            skeleton_charts(n_charts=1)
        else:
            skeleton_charts(n_charts=1)
    _tab_ph.empty()

    if selected == "Overview":          tab_overview(df_f)
    elif selected == "Seasonal":        tab_seasonal(df_f)
    elif selected == "Health Risk":     tab_health(df_f)
    elif selected == "Forecast":        tab_forecast(df_f)
    elif selected == "Lag Correlation": tab_lag(df_f)
    elif selected == "Raw Data":        tab_data(df_f)

    st.markdown("""
<div class="footer">
  Built with Streamlit & Plotly &nbsp;·&nbsp;
  Data: Open-Meteo API + Google Trends &nbsp;·&nbsp;
  WHO PM2.5 guideline: 15 μg/m³ &nbsp;·&nbsp;
  Nepal NAAQS: 40 μg/m³ &nbsp;·&nbsp;
  Aaroshree Gautam &nbsp;·&nbsp; Data Science
</div>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()