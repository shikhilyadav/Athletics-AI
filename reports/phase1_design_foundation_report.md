# ATHLETIX AI — Phase 1: Design Foundation Report
**Project:** ATHLETIX AI — NFL Movement Intelligence & Scouting Science  
**Phase:** Phase 1 Design Foundation (Complete UI/UX Transformation)  
**Date:** November 2026  
**Status:** Complete & Validated (Awaiting User Review)

---

## 1. Executive Summary & Design Vision

In accordance with the visual reference guidelines and user specifications, the ATHLETIX AI design architecture has been completely transformed from conventional dark/academic templates into a **commercial sports analytics and biomechanical SaaS platform**. 

The new interface embraces:
1. **Minimalist Light-Grey Canvas (`#ECEFEC`):** High contrast, reduced eye strain, and editorial clarity.
2. **Elevated White Containers (`#FFFFFF`):** High border-radius (22px), soft multi-layer ambient drop shadows, and razor-thin borders (`#E5E7E5`).
3. **Electric Lime Brand Highlights (`#C8F45A` & `#8CCB42`):** Used deliberately for active states, key performance metrics, and top-tier kinematic badges.
4. **Deep Graphite Typography (`#171917`):** Powered by Plus Jakarta Sans and Inter, providing strong visual hierarchy from 38px editorial headlines down to 11px uppercase technical labels.
5. **Streamlined Application Shell:** A slim vertical sidebar with branding, empirical cohort selector, global search, and 6 core navigation destinations, complemented by a persistent top bar with notification and analyst controls.

---

## 2. Centralized Design Tokens

The global design tokens are declared centrally in `src/dashboard/components.py` and injected across the entire application runtime:

| Token Name | Value | Purpose |
| :--- | :--- | :--- |
| `--bg-app` | `#ECEFEC` | Main application background |
| `--card-bg` | `#FFFFFF` | Primary card and chart container surface |
| `--card-dark` | `#171917` | Dark feature card surface & active tab highlights |
| `--accent-lime` | `#C8F45A` | Electric lime primary accent (active nav, badges, top KPIs) |
| `--accent-lime-dark` | `#8CCB42` | Forest lime secondary accent & glowing active status indicator |
| `--text-primary` | `#171917` | High-contrast editorial titles, values, and primary labels |
| `--text-secondary` | `#858B86` | Secondary labels, descriptions, and metadata |
| `--border-light` | `#E5E7E5` | Clean 1px structural container borders |
| `--card-radius` | `22px` | Modern rounded corner radius for cards and containers |
| `--pill-radius` | `9999px` | Fully rounded pill buttons, badges, and navigation items |
| `--shadow-card` | `0 4px 20px -2px rgba(23, 25, 23, 0.04)` | Subtle elevation shadow |

---

## 3. Global Application Shell Architecture

### 3.1 Slim Vertical Sidebar
- **Brand Header:** High-impact electric lime `⚡` badge with bold `ATHLETIX AI` logotype and `SPORTS SCIENCE SAAS` classification.
- **Research Cohort Selector:** Dropdown selector allowing instant switching between empirical subsets:
  - `Primary Cohort (149 • Scrimmage ≥50)`
  - `Combine Attendees (510 • All Prospects)`
  - `2023 Game Tracked (156 • Scrimmage & ST)`
  - `Route Separation (51 • Skill Sub-Cohort)`
- **Global Search Control:** Text input for real-time prospect and position queries.
- **Six Core Navigation Destinations:**
  1. `1. Research Overview`
  2. `2. Prospect Explorer`
  3. `3. Model Performance`
  4. `4. Athletic Alpha`
  5. `5. Biomechanical Lab`
  6. `6. Research Methodology`
- **Active Navigation Pill Style:** Pill-shaped items with smooth transitions, highlighted in `#C8F45A` with `#171917` bold typography upon selection.
- **System Telemetry & Status:** Glowing green 10 Hz RFID active status indicator and verified cohort architecture summary box.

### 3.2 Persistent Top Identity Bar
- **Branding Subtitle:** `NFL Movement Intelligence • Big Data Bowl 2027`.
- **Dynamic Cohort Indicator:** Reflects the selected active cohort directly from application state (`● 149 Scrimmage Cohort`).
- **Telemetry Feeds Pill:** `10 Hz RFID Feeds`.
- **Notification & Profile Controls:** `🔔 0 Alerts` and `👤 Scouting Lab` profile badge.

### 3.3 Elimination of Duplicate Navigation
- All Streamlit automatic multipage sidebar items (`[data-testid="stSidebarNav"]`) are forcefully suppressed and hidden via CSS and `.streamlit/config.toml` (`showSidebarNavigation = false`).

---

## 4. Reusable UI Component Library (`src/dashboard/components.py`)

A comprehensive library of 10 modular UI components was authored to guarantee visual consistency:

1. **`render_top_bar(active_cohort)`**: Top identity bar with dynamic cohort indicators, feed status, notifications, and profile pills.
2. **`render_editorial_header(title, subtitle, tag)`**: Large 38px editorial page title with secondary text and optional lime classification badge.
3. **`render_section_header(title, subtitle, badge)`**: Clean section divider and title for page sub-modules.
4. **`render_kpi_card_v2(label, value, subtext, highlight_lime)`**: High-contrast numerical summary card with hover micro-elevation.
5. **`render_metric_card(title, value, unit, badge_text, badge_color, subtext)`**: Compact technical card for athlete metrics and kinematics.
6. **`render_chart_container(fig, title, caption)`**: Card container enclosing Plotly figures with title and caption.
7. **`render_player_selector(player_options, default_index, key, label)`**: Standardized prospect dropdown selectbox.
8. **`render_search_filter_bar(search_key, placeholder)`**: Clean text input bar for filtering and queries.
9. **`render_status_indicator(status_text, is_active, badge)`**: System status pill with glowing green/grey dot.
10. **`render_empty_state(title, message, icon)`**: Informative fallback view when filters return zero prospects.
11. **`render_scientific_banner(title, text)`**: Dark-bordered methodological caution card to safeguard empirical boundaries.

---

## 5. Verification & Test Suite Results

All automated tests were updated and executed:
- **`tests/test_dashboard.py`**:
  - `test_data_loaders`: PASSED (510 combine, 156 game, 149 OOF/alpha, 50,462 plays)
  - `test_metric_formatters`: PASSED
  - `test_components_markup`: PASSED (KPI cards, metric cards, badges)
  - `test_charts_generation`: PASSED (9 figures generated with Plotly)
  - `test_views_import`: PASSED (all 6 views imported cleanly)
  - `test_apptest_navigation`: PASSED (Simulated AppTest navigation across all 6 pages with 0 exceptions)
- **Full Test Suite (`pytest tests/ -v`)**:
  - **12 passed in 8.57s** (100% pass rate).
- **Live Local Server**: Active and running at `http://localhost:8501`.

---

## 6. Scope Boundaries & Next Phase Authorization

As instructed:
- **Phase 1 Scope Respected:** Design foundation, design tokens, global shell, navigation, and reusable components are complete.
- **Scope Deferrals:** Detailed redesign of individual analytical views and implementation of the Player Comparison Studio are strictly deferred to Phase 2.
- **Empirical Boundaries Preserved:** No models were retrained, no metrics fabricated, and Model A baseline superiority is rigorously maintained.

**Next Step:** Awaiting user review and authorization to proceed to Phase 2.
