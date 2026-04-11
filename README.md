# 🌫️ Kathmandu Air Pollution & Respiratory Health Dashboard

> An end-to-end data science project analyzing air pollution trends in Kathmandu, Nepal, and their relationship with respiratory health outcomes — from raw API data to an interactive Streamlit dashboard.

**Author:** Aaroshree Gautam · Data Science Student  
**Data Period:** August 2022 – December 2024  
**Status:** 🟡 In Progress (forecast pipeline uses real SARIMAX model; forecast CSV export in development)

---

## 📖 Table of Contents

- [Project Overview](#-project-overview)
- [Key Findings](#-key-findings)
- [Dashboard Features](#-dashboard-features)
- [Project Structure](#-project-structure)
- [Data Sources & Pipeline](#-data-sources--pipeline)
- [Methodology](#-methodology)
- [How to Run](#-how-to-run)
- [Requirements](#-requirements)
- [Known Limitations](#-known-limitations)

---

## 🔍 Project Overview

Kathmandu is one of South Asia's most polluted cities, regularly exceeding WHO air quality guidelines by several times. This project investigates:

- **How bad is the air?** Quantifying PM2.5 and other pollutants against WHO and Nepal NAAQS standards.
- **When is it worst?** Identifying seasonal and monthly pollution patterns driven by Kathmandu's unique geography and monsoon climate.
- **Does pollution cause health symptoms?** Using lag correlation analysis to find the delay between pollution spikes and respiratory health search trends.
- **Who is most at risk?** Building a composite Health Risk Score for four distinct population groups.
- **What comes next?** Forecasting PM2.5 levels 90 days into the future using a SARIMAX time series model.

---

## 📊 Key Findings

### Air Quality
- Kathmandu's **mean PM2.5 is ~31.4 μg/m³** — more than **2× the WHO safe limit** of 15 μg/m³.
- **88.4% of days** exceed the WHO guideline; the city has virtually no safe-air days.
- The **worst month is December** (mean ~50 μg/m³); the **only relative relief comes in July** during the monsoon.
- Peak single-day reading: **119.2 μg/m³** — nearly 8× the WHO limit.

### Pollution-Health Lag
- PM2.5 today most strongly predicts **cough-related Google searches 4 days later** (Pearson r = 0.327).
- Asthma searches show a longer delayed response, peaking around **day 13** — consistent with chronic inflammatory buildup.
- Carbon monoxide is the single strongest same-day predictor of cough (r = 0.41), pointing to traffic and biomass burning as key drivers.

### Health Risk Score
- The composite Health Risk Score averages **42.3/100** — placing Kathmandu in the "High" risk category on a typical day.
- **Children are the most at-risk group** (mean score 52.9/100, max 85.4/100).
- Over **91% of days** fall into High or Moderate risk categories.
- Even healthy adults have **zero truly low-risk days** over the 2.5-year study period.

### Forecasting
- A SARIMAX model (with weather regressors) forecasts **Apr–Jul 2026 mean PM2.5 at ~37.4 μg/m³**.
- All 90 forecast days are projected to exceed the WHO limit.
- Monsoon onset (late June/July) is expected to bring some natural relief.

---

## 🖥️ Dashboard Features

The Streamlit app (`app.py`) provides an interactive, dark-themed dashboard with six analytical tabs:

| Tab | What It Shows |
|-----|---------------|
| **Overview** | KPI cards, AQI status banner, PM2.5 & PM10 gauges, time series with anomaly detection, year-over-year comparison |
| **Seasonal** | Monthly PM2.5 box plots, seasonal bar chart, year × month heatmap, pollutant–health correlation matrix |
| **Health Risk** | Population risk scores (Children, Elderly, Asthma, Healthy), risk level distribution pie chart, PM2.5 vs. risk scatter, seasonal group breakdown |
| **Forecast** | SARIMAX 90-day PM2.5 forecast with confidence intervals, monthly summary table, threshold exceedance counts |
| **Lag Correlation** | Interactive lag explorer (0–30 days), peak-lag scatter plot, full correlation table with significance flags |
| **Raw Data** | Filterable data table, column selector, CSV download, descriptive statistics |

**Sidebar controls** allow filtering by date range and season (Winter / Pre-Monsoon / Monsoon / Post-Monsoon) across all tabs.

---

## 📁 Project Structure

```
kathmandu-air-health/
│
├── app.py                        # Streamlit dashboard (main entry point)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── notebooks/
│   ├── 01_data_acquisition.ipynb     # API data fetching (Open-Meteo + Google Trends)
│   ├── 02_data_cleaning.ipynb        # Cleaning, resampling, merging into master dataset
│   ├── 03_eda_correlation.ipynb      # EDA, seasonal analysis, lag correlation
│   ├── 04_forecasting.ipynb          # SARIMAX model training, evaluation, 90-day forecast
│   └── 05_health_risk_score.ipynb    # Composite Health Risk Score construction
│
└── data/
    ├── raw/
    │   ├── kathmandu_airquality.csv  # Hourly air quality from Open-Meteo
    │   ├── kathmandu_weather.csv     # Daily weather from Open-Meteo
    │   └── nepal_health_trends.csv   # Weekly Google Trends (cough, asthma)
    └── processed/
        ├── master_dataset.csv        # Cleaned, merged daily dataset
        ├── health_risk_dataset.csv   # Master dataset + all risk score columns
        └── forecast_90day.csv        # SARIMAX forecast output (generated by notebook 04)
```

> **Note:** The `data/` directory is not committed to version control. Run the notebooks in order to generate all required files before launching the dashboard.

---

## 🌐 Data Sources & Pipeline

| Source | Variables | Resolution | Notes |
|--------|-----------|------------|-------|
| [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api) | PM2.5, PM10, CO, NO₂, O₃, Dust, UV Index | Hourly | Free, no API key required |
| [Open-Meteo Weather API](https://open-meteo.com/en/docs) | Temperature, Precipitation, Wind Speed, Humidity | Daily | Free, no API key required |
| [Google Trends (via pytrends)](https://pypi.org/project/pytrends/) | "cough", "asthma" search interest | Weekly | Nepal region; used as health proxy |

**Date range:** 2020–2024 attempted; effective data starts **August 4, 2022** (limited by Open-Meteo air quality availability for Kathmandu).  
**Location:** Kathmandu, Nepal — lat: 27.7172, lon: 85.3240

### Pipeline execution order

Run the notebooks sequentially — each one produces files that the next depends on:

```
01_data_acquisition  →  data/raw/*.csv
02_data_cleaning     →  data/processed/master_dataset.csv
03_eda_correlation   →  (analysis only, no output files)
04_forecasting       →  data/processed/forecast_90day.csv
05_health_risk_score →  data/processed/health_risk_dataset.csv   ← required by app.py
```

---

## 🔬 Methodology

### Data Cleaning (Notebook 02)
- Dropped rows where PM2.5 was null (the primary target variable).
- Resampled hourly air quality data to **daily averages**.
- Aligned all three datasets to a common date range (Aug 2022 – Dec 2024).
- Forward-filled weekly Google Trends data to daily frequency using `merge_asof`.
- Dropped the "breathing problem" Trends column (contained all zeros).

### Exploratory Analysis (Notebook 03)
- Compared all pollutants against WHO and Nepal NAAQS benchmarks.
- Mapped seasonal patterns using Kathmandu's four climatological seasons.
- Computed Pearson correlation across pollutants, weather, and health proxies.
- Ran **lag correlation analysis** (0–14 days) to find the biological delay between pollution exposure and symptom onset.

### Health Risk Score (Notebook 05)

A composite score (0–100) built from four weighted components:

| Component | Weight | Variables Used |
|-----------|--------|----------------|
| PM2.5 Score | 40% | PM2.5 mapped to WHO/AQI breakpoints |
| Multi-Pollutant Score | 25% | NO₂ (40%), CO (30%), O₃ (30%) normalized |
| Weather Score | 20% | Temperature inversion risk, humidity, wind relief |
| Health Proxy Score | 15% | Google Trends cough (60%) + asthma (40%) |

Population-specific scores are derived by applying sensitivity multipliers:
- **Children** — 1.25× base score (most sensitive due to developing lungs)
- **Elderly** — Reweighted with higher weather component
- **Asthma patients** — Extra weight on ozone and PM2.5
- **Healthy adults** — Baseline composite score

Risk levels: Low (<20) · Moderate (20–40) · High (40–60) · Very High (60–80) · Hazardous (>80)

### Forecasting (Notebook 04)

Model: **SARIMAX(1,1,1)(1,1,1,7)** — SARIMA with weekly seasonality and weather exogenous regressors.

| Parameter | Value | Meaning |
|-----------|-------|---------|
| p=1, d=1, q=1 | Non-seasonal AR, differencing, MA | Accounts for trend and short-term autocorrelation |
| P=1, D=1, Q=1 | Seasonal AR, differencing, MA | Captures weekly pollution cycles |
| s=7 | Seasonal period | Weekly cycle |
| Exogenous | Temperature, Precipitation, Wind Speed, Humidity | Weather-driven pollution dynamics |

- **Training set:** August 2022 – October 2024 (~821 days)
- **Holdout set:** November – December 2024 (~60 days)
- **Holdout MAE:** 28.82 μg/m³ (note: holdout period was anomalously polluted at mean 61.4 μg/m³ vs training mean 29.2 μg/m³)
- A bridge weather regression (Linear Regression: weather → PM2.5) fills the 2025 gap to enable a forward forecast.

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/kathmandu-air-health.git
cd kathmandu-air-health
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

For the notebooks, you will also need:

```bash
pip install requests pytrends statsmodels scikit-learn jupyter
```

### 4. Generate the data (first time only)

Open and run the notebooks **in order** from your project root:

```bash
jupyter notebook
```

Run `01_data_acquisition.ipynb` → `02_data_cleaning.ipynb` → `04_forecasting.ipynb` → `05_health_risk_score.ipynb`

This will populate the `data/raw/` and `data/processed/` directories.

### 5. Launch the dashboard

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

> **Shortcut:** If you just want to explore the dashboard without running the full pipeline, the app will fall back to synthetic forecast data automatically if `forecast_90day.csv` is missing — but `health_risk_dataset.csv` is required.

---

## 📦 Requirements

**Dashboard (`requirements.txt`):**

```
streamlit
pandas
numpy
plotly
scipy
```

**Notebooks (additional):**

```
requests
pytrends
statsmodels
scikit-learn
jupyter
matplotlib
seaborn
```

Tested on Python 3.10+. No API keys are required for any data source.

---

## ⚠️ Known Limitations

- **Google Trends is a proxy, not clinical data.** Search volumes reflect public awareness and internet access as much as actual health outcomes. Results should be interpreted with appropriate caution.
- **Air quality data starts August 2022.** Open-Meteo's historical air quality coverage for Kathmandu coordinates is limited before this date, restricting the study period to ~2.4 years.
- **Forecast bridge uses a simplified regression.** The 2025 PM2.5 bridge (used to extend the SARIMAX training window) is estimated from weather variables alone via linear regression (R² ≈ low-moderate). This introduces uncertainty in the 90-day forward forecast.
- **High holdout MAPE (43.9%).** November–December 2024 was an exceptionally polluted period (~2× the training mean). The model's forecast of ~34 μg/m³ represents a normal winter level, not a failure — but users should treat point forecasts as indicative rather than precise.
- **No ground-truth health data.** Hospital admissions, clinic visits, or clinical respiratory metrics were not available. Google Trends search interest is used as a behavioural proxy only.
- **Single location.** All analysis is specific to central Kathmandu. Pollution levels vary significantly across the valley.

---

## 📄 License

This project is for educational and research purposes. Data is sourced from Open-Meteo (CC BY 4.0) and Google Trends (subject to Google's Terms of Service).