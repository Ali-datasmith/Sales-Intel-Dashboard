<div align="center">

# 📊 Sales Intel Terminal

### High-Performance Sales Analytics — Built in Pure Python

*A Power BI replacement with zero licences, zero infrastructure, and zero compromise.*

<br>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Polars](https://img.shields.io/badge/Polars-1.0-CD792C?style=for-the-badge&logo=polars&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-1.0-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![Plotly](https://img.shields.io/badge/Plotly-5.22-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-059669?style=for-the-badge)
![Deploy](https://img.shields.io/badge/Deployed-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

<br>

[**Live Demo →**](https://sales-intel-dashboard-56kzx3cgrz23fdtbizputa.streamlit.app/) &nbsp;·&nbsp; [**Video Walkthrough →**](https://youtu.be/j4qpUIL95nU) &nbsp;·&nbsp; 

<br>

<!-- SCREENSHOT: Full dashboard — Overview tab loaded with sample data. Show all 4 KPI cards, Revenue by Region chart, Deals by Stage chart visible. Dark Emerald theme. -->
<img width="1366" height="768" alt="Screenshot 2026-06-14 11 13 58 PM" src="https://github.com/user-attachments/assets/4fc8e8da-a5a1-440e-9ef2-5fa49dc2f359" />


</div>

---

## Why Sales Intel Terminal?

Your sales data deserves better than a spreadsheet and a Power BI subscription.

Sales Intel Terminal is a **self-hosted, open-source analytics engine** that ingests your raw CRM export and delivers production-grade dashboards in seconds — no database, no server, no monthly fee.

Built on the fastest Python data stack available:

```
Polars 1.0  →  Rust columnar engine    →  5–10× faster than Pandas
DuckDB 1.0  →  In-process SQL          →  millisecond GROUP BY on 200K rows
Streamlit   →  Reactive UI             →  zero-config deployment
```

---

## ⚡ Performance

```
Dataset: 200,000 row CRM export · 12.2 MB CSV

┌─────────────────────────────┬──────────────┬──────────────────────┐
│ Operation                   │ Pandas Stack │ Sales Intel Terminal │
├─────────────────────────────┼──────────────┼──────────────────────┤
│ Load + clean 200K rows      │ ~45 seconds  │ < 5 seconds  ⚡      │
│ GROUP BY aggregation        │ ~8 seconds   │ < 0.1 seconds        │
│ Multi-filter re-query       │ ~12 seconds  │ instant              │
│ Memory footprint            │ ~800 MB      │ ~120 MB              │
└─────────────────────────────┴──────────────┴──────────────────────┘
```

---

## Dashboard

Four fully interactive views — each with live sidebar filters, CSV export, and glass-morphism UI.

<br>

### 📊 Sales Overview
Revenue KPIs, month-over-month growth, revenue by region, deals by stage, product breakdown, and monthly trend line — all in one view.

<!-- SCREENSHOT: Overview tab. KPI strip at top showing Total Revenue, Total Deals, Avg Deal Size, Regions, Products in Gold mono font. Revenue by Region bar chart on left, Deals by Stage on right. Monthly trend line at bottom. -->
[<img width="1366" height="768" alt="Screenshot 2026-06-14 11 15 54 PM" src="https://github.com/user-attachments/assets/140222db-2821-4d2a-a479-7f02ffb360f9" />
]

<br>

### 🗺️ Regional Performance
Rep × Region revenue density heatmap. Instantly identify your top territories, coverage gaps, and which reps are underperforming in which regions.

<!-- SCREENSHOT: Regional tab. Large heatmap centre screen showing rep names on Y axis and regions on X axis. Emerald-to-Gold color scale. Region bar and Rep bar charts below in two columns. -->
[<img width="1366" height="768" alt="Screenshot 2026-06-14 11 16 28 PM" src="https://github.com/user-attachments/assets/98c67d49-25be-4bc9-8b5a-d29fbcd3f8e1" />
]

<br>

### 🌪️ Pipeline Conversion
Stage-by-stage funnel with Emerald → Gold color gradient. Stage Health panel alongside the funnel showing per-stage deal count, % of pipeline, and status badge (WON / OK / MID / LOW).

<!-- SCREENSHOT: Funnel tab. Left 2/3 shows the Plotly funnel chart with Prospecting → Qualification → Proposal → Negotiation → Closed Won. Right 1/3 shows Stage Health cards with colored badges and mini progress bars. -->
[<img width="1366" height="768" alt="Screenshot 2026-06-14 11 16 47 PM" src="https://github.com/user-attachments/assets/73496fe2-0a73-4712-a81d-d516a24c1a5f" />
]

<br>

### 👤 Rep Performance
Individual rep scorecard grid with rank medals, Gold revenue values, deal counts, and mini progress bars relative to the top performer. Full ranked leaderboard table below.

<!-- SCREENSHOT: Rep Performance tab. 3-column grid of rep scorecard cards — each showing rep name, 🥇🥈🥉 rank, Gold revenue, deal count, and green progress bar. Full leaderboard table at bottom. -->
[<img width="1366" height="768" alt="Screenshot 2026-06-14 11 17 13 PM" src="https://github.com/user-attachments/assets/0170a93d-d62f-4c33-b223-40cf1eb84ed3" />
]

---

## 🔐 Security

Access is protected by a **single-user login gate** — the dashboard is completely inaccessible without authentication.

- Passwords stored as `sha256` hash — never plain text, anywhere
- Session-based auth via Streamlit `session_state`
- Full session wipe on logout — data, filters, and file cache all cleared
- Glass-morphism login screen with animated Emerald scanline effect

<!-- SCREENSHOT: Login screen centred on dark Emerald background. Glass card with 📊 icon, "SALES INTEL TERMINAL" title in white with green accent, username + password fields, green AUTHENTICATE button. Scanline animation visible. -->
[<img width="1366" height="768" alt="Screenshot 2026-06-14 11 17 43 PM" src="https://github.com/user-attachments/assets/a681625f-fba3-431f-978f-001e26eb425c" />
]

---

## Data Requirements

Upload any **CSV or Excel file** with these six columns — names are case-insensitive and auto-normalised:

| Column | Type | Notes |
|--------|------|-------|
| `date` | date / string | Deal or transaction date |
| `revenue` | float / int / string | Supports `$1,200.00` format — parsed automatically |
| `rep` | string | Sales representative name |
| `region` | string | Geographic region or territory |
| `product` | string | Product or service name |
| `stage` | string | `Prospecting` · `Qualification` · `Proposal` · `Negotiation` · `Closed Won` |

> Missing categorical columns are auto-filled with `"Unknown"` — the app never crashes on incomplete data.

**Example:**
```csv
date,revenue,rep,region,product,stage
2024-03-15,12500.00,Sara Ahmed,North,Enterprise Plan,Closed Won
2024-03-18,8750.00,James Okafor,West,Starter Pack,Proposal
```

No data? Hit **⬇ Download Sample CRM Data** in the sidebar — a full demo dataset loads instantly.

---

## Architecture

```
sales-intel-dashboard/
│
├── app.py            # Entry point — login gate, sidebar, routing, landing page
├── credentials.py    # Auth store  — sha256 hashing, single-user validation
├── login.py          # Auth UI     — glass-morphism login, session management
│
├── ingest.py         # The Loader        — CSV/Excel parsing & schema detection
├── transform.py      # The Sanitiser     — Polars 5-step cleaning pipeline
├── db.py             # The Engine        — DuckDB session & SQL aggregation helpers
├── metrics.py        # The Calculator    — MoM growth, variance alerts, KPI logic
├── charts.py         # The Visual Factory — Plotly chart builders (all chart types)
├── funnel.py         # The Funnel Lens   — Drop-off analysis & stage health metrics
├── filters.py        # The Control Panel — Sidebar filter widgets & FilterState
├── views.py          # The Composer      — Full page layouts, export bars, scorecards
├── theme.py          # The Stylist       — Glass-morphism CSS, Plotly template, helpers
├── utils.py          # The Toolkit       — Shared helpers & sample data generator
│
└── requirements.txt  # All dependencies — version-pinned for reproducible deploys
```

**One rule:** every file has exactly one responsibility. `views.py` never touches data. `db.py` never touches the UI. Adding a new chart means one new function in `charts.py` — nothing else changes.

### Data Flow

```
User Uploads CSV / Excel
         │
         ▼
   credentials.py    ← login gate — blocks unauthenticated access
         │
         ▼
   ingest.py         ← file parsing, schema detection, format normalisation
         │
         ▼
   transform.py      ← Polars pipeline:
         │             normalize headers → clean revenue → parse dates
         │             → fill categoricals → deduplicate
         ▼
   db.py             ← DuckDB registers Polars DataFrame (zero serialisation)
         │
         ▼
   metrics.py        ← SQL aggregations, MoM growth, KPI computation
         │
         ▼
   charts.py         ← pure Plotly Figure objects (Emerald + Gold themed)
         │
         ▼
   views.py          ← Streamlit composition — filters applied, exports rendered
```

---

## Tech Stack

| Layer | Technology | Version | Why |
|-------|-----------|---------|-----|
| UI Framework | Streamlit | 1.36 | Reactive Python UI — sidebar, tabs, session state |
| Data Engine | Polars | 1.0 | Rust columnar — 5–10× faster than Pandas at scale |
| SQL Layer | DuckDB | 1.0 | In-process SQL on DataFrames — no server, no ETL |
| Visualisation | Plotly | 5.22 | Interactive dark-mode charts, hover tooltips |
| Interop | Pandas + PyArrow | 2.2 + 14 | Polars ↔ Pandas bridge for Excel and pivot ops |
| Auth | hashlib | stdlib | sha256 — zero extra dependency |
| Runtime | Python | 3.10+ | Core language |

---

## Getting Started

### 1 — Clone

```bash
git clone https://github.com/Ali-datasmith/Sales-Intel-Dashboard.git
cd Sales-Intel-Dashboard
```

### 2 — Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows
```

### 3 — Install

```bash
pip install -r requirements.txt
```

### 4 — Run

```bash
streamlit run app.py
```

Open `http://localhost:8501` — log in and upload your CRM export.

---

## Deployment

### Streamlit Cloud (Recommended — Free)

```
1. Push repo to GitHub
2. Visit share.streamlit.io
3. Connect repo → set main file: app.py
4. Deploy
```

Zero environment variables. Zero secrets file. Runs on the free tier for datasets up to ~200K rows (1 GB RAM).

### Changing the Login Password

```bash
# Generate a new sha256 hash
python3 -c "import hashlib; print(hashlib.sha256('YourNewPassword'.encode()).hexdigest())"
```

Replace the `password_hash` value in `credentials.py` with the output.

> For team deployments: move credentials to `.streamlit/secrets.toml` and update `credentials.py` to read from `st.secrets`.

---

## Dashboard Video

<!-- VIDEO: Replace with Loom or GitHub-hosted walkthrough. Show login → upload CSV → Overview KPIs → Regional heatmap → Funnel → Rep scorecards → logout. Aim for 90–120 seconds. -->
[https://youtu.be/j4qpUIL95nU]

---

## Author

**Muhammad Ali Rajput** — Data App Developer · Python · Streamlit · Analytics Engineering
[![GitHub](https://img.shields.io/badge/GitHub-Ali--datasmith-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ali-datasmith)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Muhammad_Ali_Rajput-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/YOUR_LINKEDIN_USERNAME)


---

<div align="center">

*No BI licences. No infrastructure. No Pandas bottleneck. No public exposure.*
*Just fast, secure, open-source sales analytics.*

**[⭐ Star this repo](https://github.com/Ali-datasmith/Sales-Intel-Dashboard)** if it saved you a Power BI subscription.

</div>
