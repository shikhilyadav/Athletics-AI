# ATHLETIX AI — Reproducibility & Execution Guide

**Competition:** NFL Big Data Bowl 2027  
**Platform:** Windows 10/11, Python 3.10–3.14  
**Hardware Requirement:** 8 GB RAM minimum, multi-core CPU  

---

## 1. Quick Start: Launching the Dashboard

The interactive research dashboard runs locally using Streamlit.

### Launch Command:
```powershell
streamlit run src/dashboard/app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

---

## 2. Environment Setup & Dependencies

### Step 1: Clone Repository
```powershell
git clone https://github.com/shikhilyadav/Athletics-AI.git
cd "Athletics ai"
```

### Step 2: Install Required Packages
```powershell
pip install -r requirements.txt
```

Core dependencies verified:
- `polars>=0.20.0`
- `pandas>=2.0.0`
- `scikit-learn>=1.3.0`
- `scipy>=1.10.0`
- `plotly>=5.18.0`
- `streamlit>=1.30.0`
- `pytest>=7.4.0`

---

## 3. Complete End-to-End Execution Pipeline

To reproduce all artifacts from raw competition data:

### Step 1: Dataset Audit (Phase 1)
```powershell
python -m src.data.dataset_audit
```
*Discovers and audits the 7 raw CSV files in `data/raw/` and generates `reports/actual_dataset_inventory.csv`.*

### Step 2: Feature Engineering (Phase 2)
```powershell
python -m src.features.run_feature_pipeline
```
*Extracts kinematics, mono-exponential sprint curves, change-of-direction metrics, and game aggregations. Saves 5 Parquet files to `data/processed/`.*

### Step 3: Statistical Modeling (Phase 3)
```powershell
python -m src.models.run_phase3_experiments
```
*Runs 10-repeat 5-fold cross-validation across Models A, B, and C. Saves OOF predictions and Athletic Alpha residuals to `models/saved/`.*

### Step 4: Independent Statistical Audit (Phase 3.1)
```powershell
python -m src.models.audit_phase3_experiments
```
*Runs leakage checks, 2,000-iteration player bootstrap, nested CV hyperparameter tuning, confounding regressions, and FDR corrections. Saves outputs to `models/saved/phase3_1_audit/`.*

### Step 5: Run Automated Test Suite
```powershell
python -m pytest tests/ -v
```
*Executes all 9 unit tests covering kinematics, sprint curve fitting, snap eligibility, data loaders, formatters, and chart generators.*

---

## 4. Repository Directory Structure

```
Athletics ai/
├── data/
│   ├── raw/                           <- 7 original competition CSV files (566 MB)
│   └── processed/                     <- 5 optimized Parquet datasets
├── models/
│   └── saved/                         <- OOF predictions, metrics, Athletic Alpha CSVs
│       └── phase3_1_audit/            <- Nested CV metrics, FDR tables
├── notebooks/                         <- 6 exploratory and modeling Jupyter notebooks
├── reports/                           <- Comprehensive markdown research reports
│   └── phase3_1_audit/                <- 8 independent statistical audit reports
├── src/
│   ├── data/                          <- Dataset auditing and discovery scripts
│   ├── features/                      <- Kinematics, COD, sprint curves, aggregators
│   ├── models/                        <- Cross-validation, nested CV, audit scripts
│   └── dashboard/                     <- Production Streamlit platform
│       ├── app.py                     <- Application entry point
│       ├── data_loader.py             <- Cached data access layer
│       ├── metrics.py                 <- Unit formatters and statistical helpers
│       ├── components.py              <- Custom white & green CSS and UI cards
│       ├── charts.py                  <- Consistent Plotly chart generators
│       └── pages/                     <- 6 modular application pages
├── tests/                             <- Pytest automated test suites
├── requirements.txt                   <- Pinned dependency specification
└── README.md                          <- Main project documentation
```
