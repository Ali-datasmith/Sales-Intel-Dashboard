# Sales-Intel-Dashboard: High-Performance Sales Analytics

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Polars](https://img.shields.io/badge/Polars-0.20-CD792C?style=flat&logo=polars&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-0.10-FFF000?style=flat&logo=duckdb&logoColor=black)
![Plotly](https://img.shields.io/badge/Plotly-5.22-3F4F75?style=flat&logo=plotly&logoColor=white)

---

## Executive Summary

Most sales dashboards are bottlenecked by Pandas — slow on large datasets, memory-hungry, and row-oriented by design. **Sales-Intel-Dashboard** replaces that bottleneck with a modern analytical stack:

- **Polars** processes data in a columnar, multi-threaded Rust engine — typically **5–10× faster** than Pandas on transformation workloads and significantly more memory-efficient on files above 100K rows.
- **DuckDB** runs analytical SQL directly on in-process DataFrames — no server, no connection overhead, no ETL pipeline. It turns complex GROUP BY aggregations into millisecond operations without ever leaving Python memory.

The result is a dashboard that feels instant for the end user, deploys on Streamlit Cloud free tier without a database, and requires zero infrastructure setup from the developer.

---

## Key Features

- **Modular architecture** — 10 single-responsibility files, cleanly separated by concern (ingestion, transformation, analytics, UI)
- **CSV / Excel upload** — drag-and-drop upload with automatic schema detection; no database configuration needed
- **Revenue analytics** — filterable by region, product, and sales rep with interactive Plotly charts
- **Month-over-month growth tracking** — automated variance alerts when performance drops beyond configurable thresholds
- **Real-time funnel analysis** — stage-by-stage drop-off visualisation with conversion rate breakdowns
- **Automated data cleaning** — null handling, type coercion, date normalisation, and deduplication via Polars
- **Dark-mode UI** — branded Plotly theme with consistent colour palette across all chart types
- **Zero infrastructure** — runs entirely in-memory via DuckDB; deploys on Streamlit Cloud free tier out of the box

---

## Tech Stack

| Layer | Technology | Role |
|---|---|---|
| Frontend | Streamlit 1.35 | UI, file upload, sidebar filters, layout |
| Transformation | Polars 0.20 | High-speed columnar data cleaning |
| Analytics Engine | DuckDB 0.10 | In-memory SQL aggregations |
| Visualisation | Plotly 5.22 | Interactive dark-mode charts |
| Compatibility | Pandas 2.2 + PyArrow | Interop layer for upstream data sources |
| Runtime | Python 3.11 | Core language |

---

## Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/sales-intel-dashboard.git
cd sales-intel-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

### 5. Upload your data

On the sidebar, upload any CSV or Excel CRM export. The app auto-detects columns for date, revenue, rep, region, product, and funnel stage — no manual mapping required.

---

## Architecture Overview

```
sales-intel-dashboard/
├── app.py          # Entry point — Streamlit routing and session state
├── ingest.py       # The Loader    — CSV/Excel upload and schema detection
├── transform.py    # The Sanitiser — Polars-powered cleaning and normalisation
├── db.py           # The Engine    — DuckDB session and SQL aggregation helpers
├── metrics.py      # The Calculator — MoM growth, variance alerts, KPI computation
├── charts.py       # The Visual Factory — Plotly chart builder functions
├── funnel.py       # The Funnel Lens — Drop-off analysis and conversion charts
├── filters.py      # The Control Panel — Sidebar filter widgets and FilterState
├── views.py        # The Composer  — Full page layouts assembling all components
├── theme.py        # The Stylist   — Dark-mode palette and Plotly layout defaults
└── requirements.txt
```

### The Engine (`db.py` + `transform.py`)

Data flows from raw upload → Polars cleaning → DuckDB registration. Once registered, all aggregations run as parameterised SQL queries — no Python loops, no Pandas `groupby` overhead. The engine layer is entirely decoupled from the UI.

### The Sanitiser (`ingest.py` + `transform.py`)

Handles the messy reality of CRM exports: inconsistent date formats, mixed-type columns, duplicate rows, and missing values. Polars lazy evaluation means cleaning runs in a single optimised pass regardless of file size.

### The Visual Factory (`charts.py` + `funnel.py` + `theme.py`)

Every chart is built as a pure Plotly `Figure` object, styled once via `theme.py`, and returned to `views.py` for rendering. Adding a new chart type requires only a new function in `charts.py` — zero changes elsewhere.

---

## Deployment

This app is configured to run on **Streamlit Community Cloud** (free tier):

1. Push the repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set the main file path to `app.py`
4. Deploy — no environment variables or secrets required

Resource usage stays well within free-tier limits (1 GB RAM) for typical CRM exports up to ~200K rows.

---

## Contact & Portfolio

**Muhammad Ali Rajput**
Data App Developer · Python · Streamlit · Analytics Engineering

- GitHub: [github.com/YOUR_GITHUB_USERNAME](https://github.com/YOUR_GITHUB_USERNAME)
- LinkedIn: [linkedin.com/in/YOUR_LINKEDIN_USERNAME](https://linkedin.com/in/YOUR_LINKEDIN_USERNAME)

---

*Built with a modern Python data stack. No BI tool licences. No infrastructure. Just fast, clean, open-source analytics.*
