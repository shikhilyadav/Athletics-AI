# ATHLETIX AI ⚡🏈
> **Beyond Speed. Understanding Athletic Potential.**

ATHLETIX AI is an advanced, competition-oriented sports analytics and machine learning research platform developed for the **NFL Big Data Bowl**. The project bridges pre-draft athletic evaluation and professional on-field performance by integrating high-frequency (10 Hz) RFID sensor tracking from the NFL Scouting Combine with regular-season Next Gen Stats (NGS) player tracking data.

---

## 🎯 Primary Research Question

> **"Can advanced movement analytics identify NFL prospects whose athletic potential is underestimated by traditional Combine measurements?"**

Traditional NFL draft evaluation relies heavily on discrete, stopwatch-measured Combine benchmarks—such as the 40-yard dash, short shuttle, and vertical jump. While these metrics capture isolated, static athletic ceilings in shorts and t-shirts, they frequently obscure continuous micro-movement capabilities:
* Acceleration burst latency ($\text{time-to-}a_{\max}$)
* Rate of force development (jerk: $\frac{da}{dt}$)
* Biomechanical change-of-direction (COD) apex velocity maintenance
* Deceleration-to-reacceleration transition efficiency
* Functional in-game speed translation relative to straight-line track speed

ATHLETIX AI tests the hypothesis that continuous sensor tracking reveals an **"Athletic Alpha"**—a latent athletic capability that explains why certain prospects outperform their draft capital and traditional testing expectations once on an NFL field.

---

## 🏛️ Technical Architecture

```mermaid
flowchart TD
    subgraph Raw Data Ingestion
        A1["Combine Sensor Tracking<br/>(10 Hz RFID Coordinate Feeds)"]
        A2["Traditional Combine Metrics<br/>(40yd, 10/20 Splits, Jumps, Anthropometry)"]
        A3["NFL Next Gen Stats Tracking<br/>(10 Hz Regular Season Gameplay)"]
        A4["Contextual Meta Tables<br/>(games.csv, plays.csv, players.csv)"]
    end

    subgraph Data Harmonization & Entity Resolution
        B1["Coordinate Normalization<br/>(Direction of play, 120x53.3 yd grid)"]
        B2["Player Entity Matching<br/>(nflId, smartabase_id, college, draft year)"]
        B3["10 Hz Temporal Alignment<br/>(Event sync: ball_snap, drill_start)"]
    end

    subgraph Feature Engineering Engine
        C1["Kinematic Features<br/>(Peak Speed, Peak Accel, Jerk, Burst Latency)"]
        C2["COD & Agility Metrics<br/>(Apex Speed, Decel Capacity, Transition Ratio)"]
        C3["Asymptotic Velocity Modeling<br/>v(t) = v_max * (1 - exp(-t/tau))"]
        C4["Functional Game Speed Aggregation<br/>(95th/99th %ile in-game velocity, pursuit accel)"]
    end

    subgraph Analytical & Modeling Core
        D1["Baseline Model (Ridge/ElasticNet)<br/>Traditional Metrics -> Game Athleticism"]
        D2["Prospective Model (XGBoost/LightGBM)<br/>Continuous Sensor Features -> Game Athleticism"]
        D3["Residual Evaluation Engine<br/>Athletic Alpha = Actual - Expected(Traditional)"]
    end

    subgraph Explainability & Validation
        E1["SHAP Value Decomposition<br/>(TreeSHAP, Waterfall, Dependence Plots)"]
        E2["Statistical Validation<br/>(Quantile Regression, Bland-Altman, P-Values)"]
        E3["Confounding Bias Controls<br/>(Snap Count Filters, Scheme Context)"]
    end

    subgraph Presentation & UI Layer
        F1["Interactive Streamlit Analytics Dashboard"]
        F2["Plotly Biomechanical Trajectory Visualizer"]
        F3["Prospect Athletic Potential Scorecards"]
    end

    A1 & A2 & A3 & A4 --> B1 & B2 & B3
    B1 & B2 & B3 --> C1 & C2 & C3 & C4
    C1 & C2 & C3 & C4 --> D1 & D2
    D1 & D2 --> D3
    D3 --> E1 & E2 & E3
    E1 & E2 & E3 --> F1 & F2 & F3
```

---

## 🔬 Core Research Principles

1. **Strict Empirical Grounding**: No fabricated datasets, synthetic player records, or hallucinated numbers. All modeling operates on official competition datasets.
2. **Causal Discipline**: High statistical correlation between sensor traits and in-game performance does not establish standalone causation. All findings are contextualized with scheme, role, and usage parameters.
3. **Prospective Validation**: Models are evaluated using temporal group cross-validation (splitting by draft class/season) to eliminate look-ahead leakage.

---

## 📁 Scalable Project Structure

```
athletics-ai/
├── data/
│   ├── raw/                       # Raw competition datasets (gitignored)
│   │   ├── combine_tracking/      # High-frequency Combine RFID drill tracking
│   │   ├── combine_traditional/   # Traditional stopwatch and jump records
│   │   ├── nfl_ngs_tracking/      # Regular season week-by-week tracking
│   │   └── context/               # games.csv, plays.csv, players.csv
│   ├── processed/                 # Feature-engineered parquet matrices
│   └── external/                  # Supplemental benchmark datasets
├── notebooks/                     # Exploratory Data Analysis & Research Notebooks
│   ├── 01_data_exploration_combine.ipynb
│   ├── 02_data_exploration_ngs_tracking.ipynb
│   ├── 03_feature_engineering_movement.ipynb
│   └── 04_statistical_modeling_and_shap.ipynb
├── src/                           # Production-grade Python package
│   ├── __init__.py
│   ├── config.py                  # Global paths, constants, field geometry
│   ├── data/                      # Ingestion, validation, entity resolution
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── matching.py
│   │   └── preprocessor.py
│   ├── features/                  # Biomechanical feature engineering
│   │   ├── __init__.py
│   │   ├── kinematics.py
│   │   ├── cod_metrics.py
│   │   └── tracking_aggregators.py
│   ├── models/                    # Baseline, predictive, and residual models
│   │   ├── __init__.py
│   │   ├── baseline.py
│   │   ├── prospective_model.py
│   │   ├── residual_evaluator.py
│   │   └── explainability.py
│   └── visualization/             # Plotly trajectories and research charts
│       ├── __init__.py
│       ├── trajectory_plots.py
│       └── metric_eval_plots.py
├── dashboard/                     # Interactive Streamlit application
│   ├── app.py
│   └── components/
├── tests/                         # Automated unit & integration tests
├── DATASET_GUIDE.md               # Detailed schema & download instructions
├── RESEARCH_METHODOLOGY.md        # Comprehensive mathematical & statistical formulation
├── requirements.txt               # Pinned Python dependencies
└── README.md                      # Project documentation
```

---

## 🛠️ Technology Stack

| Domain | Tools / Libraries |
| :--- | :--- |
| **Language & Environment** | Python 3.10+, JupyterLab |
| **Data Engineering** | Pandas, Polars, PyArrow, NumPy, SciPy |
| **Statistical Modeling** | Statsmodels, Scikit-learn |
| **Machine Learning** | XGBoost, LightGBM |
| **Model Interpretability** | SHAP (TreeSHAP) |
| **Interactive UI & Visuals** | Streamlit, Plotly, Seaborn, Matplotlib |
| **Spatial Geometry** | Shapely, GeoPandas |

---

## 🚀 Setup & Installation

### 1. Clone & Set Up Python Environment
```bash
# Clone the repository
git clone https://github.com/your-org/athletix-ai.git
cd athletix-ai

# Create virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Dataset Acquisition
Follow the step-by-step instructions in [DATASET_GUIDE.md](DATASET_GUIDE.md) to place official competition files into `data/raw/`.

### 3. Verify Setup
Run dataset verification:
```python
from src.data.loader import DataLoader
loader = DataLoader()
status = loader.check_dataset_availability()
print(status)
```

---

## 📚 Documentation Links
* [DATASET_GUIDE.md](DATASET_GUIDE.md) — Comprehensive schema, column dictionary, and download instructions.
* [RESEARCH_METHODOLOGY.md](RESEARCH_METHODOLOGY.md) — Mathematical formulations, kinematic derivations, and validation design.
