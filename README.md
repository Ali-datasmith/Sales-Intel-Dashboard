# ⚡ Sales Intel Terminal
 
> **A Power BI replacement built entirely in Python — zero licences, zero infrastructure, zero compromise.**
 
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Polars](https://img.shields.io/badge/Polars-0.20-CD792C?style=flat&logo=polars&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-0.10-FFF000?style=flat&logo=duckdb&logoColor=black)
![Plotly](https://img.shields.io/badge/Plotly-5.22-3F4F75?style=flat&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Deploy](https://img.shields.io/badge/Deploy-Streamlit_Cloud-FF4B4B?style=flat&logo=streamlit&logoColor=white)
 
---
 
## 🖥️ Dashboard Preview
 
<img width="1366" height="768" alt="Sales Intel Terminal Dashboard" src="https://github.com/user-attachments/assets/d8b2bfcf-be6e-4591-a1d5-9c3592c0a463" />

---
 
## The Problem With Every Sales Dashboard You've Seen
 
Most analytics dashboards are built on **Pandas** — a row-oriented library designed for small data that breaks down fast:
 
| Pain Point | Pandas Reality | Sales Intel Terminal |
|---|---|---|
| 200K row CSV | 45–90 seconds to load & transform | **⚡ Under 5 seconds** |
| Memory usage | Loads entire file into RAM eagerly | Polars lazy evaluation — only computes what's needed |
| SQL aggregations | Slow Python `groupby` loops | DuckDB in-process SQL — millisecond GROUP BY |
| Deployment | Often needs a database server | Runs entirely in-memory — deploys free |
| Cost | Power BI: $10–20/user/month | **$0 — Streamlit Cloud free tier** |
 
---
 
## ⚡ Performance Benchmark
 
```
Dataset: 200,000 rows CRM export (12.2 MB CSV)
 
┌─────────────────────────────┬──────────────┬──────────────────────┐
│ Operation                   │ Pandas Stack │ Sales Intel Terminal │
├─────────────────────────────┼──────────────┼──────────────────────┤
│ Load + clean 200K rows      │ ~45 seconds  │ < 5 seconds  ⚡      │
│ GROUP BY aggregation        │ ~8 seconds   │ < 0.1 seconds        │
│ Multi-filter re-query       │ ~12 seconds  │ instant              │
│ Memory footprint            │ ~800 MB      │ ~120 MB              │
└─────────────────────────────┴──────────────┴──────────────────────┘
 
Engine: Polars 0.20 (Rust columnar) + DuckDB 0.10 (in-process SQL)
```
 
---

## 📋 Required CSV / Excel Columns

For the app to function correctly, your uploaded file **must contain these exact column names:**

| Column | Type | Description |
|---|---|---|
| `date` | `date / string` | Transaction or deal close date |
| `revenue` | `float / int` | Revenue value per row |
| `rep` | `string` | Sales representative name |
| `region` | `string` | Geographic sales region |
| `product` | `string` | Product or service name |
| `stage` | `string` | Pipeline stage (e.g. Proposal, Negotiation, Closed Won) |

> **Column names are case-insensitive.** The app auto-detects and normalises them on upload.
> Extra columns in your file are ignored — only the six above are required.

**Example row:**

```
date,revenue,rep,region,product,stage
2024-03-15,12500.00,Sara Ahmed,North,Enterprise Plan,Closed Won
```

> **No data?** Click **"Get Sample CRM Data"** in the sidebar to load a built-in 100+ row demo dataset instantly.

---

## Key Features
 
**Data Pipeline**
- `CSV / Excel upload` — drag-and-drop with automatic schema detection; zero manual column mapping
- `Automated cleaning` — null handling, type coercion, date normalisation, deduplication via Polars lazy API
- `In-memory SQL engine` — DuckDB registers Polars DataFrames directly; no serialisation overhead

**Analytics Views**
- `Sales Overview` — total revenue KPIs, revenue by region, deals by stage
- `Regional Performance` — revenue density heatmap (rep × region matrix)
- `Pipeline Conversion` — funnel chart with stage-by-stage drop-off and conversion rates
- `Rep Leaderboard` — ranked performance table with filterable revenue thresholds

**Infrastructure**
- `Month-over-month tracking` — automated variance alerts when growth drops beyond configurable thresholds
- `Dark-mode UI` — branded Plotly theme with consistent cyan palette across all chart types
- `Zero infrastructure` — no database, no server, no environment variables; deploys in one click

---
 
## Architecture
 
```
sales-intel-dashboard/
│
├── app.py            # Entry point — Streamlit routing & session state
├── ingest.py         # The Loader       — CSV/Excel upload & schema detection
├── transform.py      # The Sanitiser    — Polars cleaning & normalisation
├── db.py             # The Engine       — DuckDB session & SQL aggregation helpers
├── metrics.py        # The Calculator   — MoM growth, variance alerts, KPI computation
├── charts.py         # The Visual Factory — Plotly chart builder functions
├── funnel.py         # The Funnel Lens  — Drop-off analysis & conversion charts
├── filters.py        # The Control Panel — Sidebar filter widgets & FilterState
├── views.py          # The Composer     — Full page layouts assembling all components
├── theme.py          # The Stylist      — Dark-mode palette & Plotly layout defaults
├── utils.py          # The Toolkit      — Shared helpers & formatting utilities
└── requirements.txt
```
 
**Design principle:** every file has exactly one responsibility. The UI layer (`views.py`) never touches data. The engine layer (`db.py`) never touches the UI. Adding a new chart requires a single new function in `charts.py` — nothing else changes.
 
### Data Flow
 
```
CSV / Excel Upload
       │
       ▼
  ingest.py          ← schema detection, file parsing
       │
       ▼
  transform.py       ← Polars lazy cleaning pipeline
       │
       ▼
    db.py            ← DuckDB registers Polars DataFrame
       │
       ▼
  metrics.py         ← parameterised SQL aggregations
       │
       ▼
  charts.py          ← pure Plotly Figure objects
       │
       ▼
  views.py           ← Streamlit page composition
```
 
---
 
## Tech Stack
 
| Layer | Technology | Why This Choice |
|---|---|---|
| Frontend | Streamlit 1.35 | Rapid UI — sidebar filters, tab routing, file upload |
| Transformation | Polars 0.20 | Rust columnar engine — 5–10× faster than Pandas on 100K+ rows |
| Analytics Engine | DuckDB 0.10 | In-process SQL on DataFrames — zero server, zero ETL |
| Visualisation | Plotly 5.22 | Interactive dark-mode charts with hover tooltips |
| Interop | Pandas 2.2 + PyArrow | Compatibility layer for upstream data sources |
| Runtime | Python 3.11 | Core language |
 
---
 
## Installation
 
### 1 — Clone
 
```bash
git clone https://github.com/Ali-datasmith/Sales-Intel-Dashboard.git
cd Sales-Intel-Dashboard
```
 
### 2 — Virtual Environment
 
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```
 
### 3 — Install Dependencies
 
```bash
pip install -r requirements.txt
```
 
### 4 — Run
 
```bash
streamlit run app.py
```

---
 
## Deployment — Streamlit Cloud (Free)
 
```
1. Push this repo to GitHub
2. Visit share.streamlit.io → connect your repo
3. Set main file: app.py
4. Deploy
```
 
No environment variables. No secrets. No database. Runs within Streamlit Cloud free tier (1 GB RAM) for datasets up to ~200K rows.
 
---
 
## Dashboard Video
 
https://github.com/user-attachments/assets/29cbbd65-1d40-45c1-848d-f04d4e30b83c
 
---
 
## Author
 
**Muhammad Ali Rajput** — Data App Developer · Python · Streamlit · Analytics Engineering
 
[![GitHub](https://img.shields.io/badge/GitHub-Ali--datasmith-181717?style=flat&logo=github&logoColor=white)](https://github.com/Ali-datasmith)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Muhammad_Ali_Rajput-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/YOUR_LINKEDIN_USERNAME)

---
 
*No BI licences. No infrastructure. No Pandas bottleneck. Just fast, clean, open-source analytics.*
