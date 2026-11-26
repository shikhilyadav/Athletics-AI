"""
ATHLETIX AI — Premium Sports Analytics Design System & Component Library
Phase 1 Design Foundation:
Minimalist light grey (#ECEFEC), large rounded white cards (#FFFFFF), electric lime (#C8F45A),
deep graphite black (#171917), black pill controls, and editorial typography.
"""

import streamlit as st
from typing import List, Optional


def inject_custom_css():
    """Inject the complete premium sports analytics design system into Streamlit."""
    st.markdown(
        """
        <style>
        /* Import Google Fonts: Plus Jakarta Sans, Inter, JetBrains Mono */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

        /* Design System Variables */
        :root {
            --bg-app: #ECEFEC;
            --card-bg: #FFFFFF;
            --card-dark: #171917;
            --accent-lime: #C8F45A;
            --accent-lime-hover: #b8e64b;
            --accent-lime-dark: #8CCB42;
            --text-primary: #171917;
            --text-secondary: #858B86;
            --text-muted: #A3A8A4;
            --border-light: #E5E7E5;
            --border-subtle: #EEEEEE;
            --card-radius: 22px;
            --pill-radius: 9999px;
            --shadow-card: 0 4px 20px -2px rgba(23, 25, 23, 0.04), 0 2px 6px -1px rgba(23, 25, 23, 0.02);
            --shadow-elevated: 0 12px 32px -4px rgba(23, 25, 23, 0.08);
        }

        /* App Background & Base Typography */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: var(--bg-app) !important;
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
        }

        /* Main content container */
        .main .block-container {
            max-width: 1400px;
            padding-top: 1.2rem;
            padding-bottom: 3.5rem;
            padding-left: 2.2rem;
            padding-right: 2.2rem;
        }

        /* Completely remove default Streamlit header, footer, multipage nav */
        #MainMenu, footer, header {
            visibility: hidden !important;
            display: none !important;
        }

        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNavItems"],
        [data-testid="stSidebarNavSeparator"],
        section[data-testid="stSidebar"] > div:first-child > div:first-child > ul:first-child,
        ul[data-testid="stSidebarNavItems"] {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
            overflow: hidden !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid var(--border-light) !important;
            box-shadow: 2px 0 12px rgba(0,0,0,0.02) !important;
            width: 290px !important;
        }

        /* Radio Navigation in Sidebar */
        div[data-testid="stRadio"] > div {
            gap: 6px !important;
        }

        div[data-testid="stRadio"] label {
            background-color: transparent !important;
            border-radius: var(--pill-radius) !important;
            padding: 10px 16px !important;
            margin: 0 !important;
            font-size: 0.90rem !important;
            font-weight: 600 !important;
            color: var(--text-secondary) !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            border: 1px solid transparent !important;
            cursor: pointer !important;
        }

        div[data-testid="stRadio"] label:hover {
            background-color: #F5F7F5 !important;
            color: var(--text-primary) !important;
        }

        div[data-testid="stRadio"] label[data-checked="true"],
        div[data-testid="stRadio"] label:has(input:checked) {
            background-color: var(--accent-lime) !important;
            color: var(--text-primary) !important;
            font-weight: 700 !important;
            box-shadow: 0 2px 8px rgba(200, 244, 90, 0.35) !important;
        }

        /* Hide radio circle dots for modern pill button look */
        div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }

        /* Top Bar Container */
        .top-bar-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #FFFFFF;
            border: 1px solid var(--border-light);
            border-radius: var(--card-radius);
            padding: 0.85rem 1.6rem;
            margin-bottom: 1.8rem;
            box-shadow: var(--shadow-card);
        }

        .top-bar-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .top-bar-logo-icon {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            background-color: var(--accent-lime);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--text-primary);
        }

        .top-bar-brand-title {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: var(--text-primary);
            line-height: 1;
        }

        .top-bar-brand-sub {
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-secondary);
            margin-top: 2px;
        }

        .top-bar-pills {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .top-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: var(--pill-radius);
            font-size: 0.78rem;
            font-weight: 600;
            background-color: #F5F7F5;
            color: var(--text-primary);
            border: 1px solid var(--border-light);
        }

        .top-pill-lime {
            background-color: var(--accent-lime);
            color: var(--text-primary);
            border-color: #b5e446;
        }

        .top-pill-dark {
            background-color: var(--card-dark);
            color: #FFFFFF;
            border-color: #2a2d2a;
        }

        /* Large Editorial Page Header */
        .editorial-header {
            margin-bottom: 2rem;
        }

        .editorial-title {
            font-size: 2.35rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            color: var(--text-primary);
            margin: 0;
            line-height: 1.15;
        }

        .editorial-subtitle {
            font-size: 1.02rem;
            font-weight: 400;
            color: var(--text-secondary);
            margin-top: 0.4rem;
            margin-bottom: 0;
        }

        /* Section Headers */
        .section-header-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 1.8rem;
            margin-bottom: 1.1rem;
        }

        .section-header-title {
            font-size: 1.28rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-primary);
            margin: 0;
        }

        .section-header-subtitle {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 2px;
        }

        /* Card Containers */
        .athletix-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-light);
            border-radius: var(--card-radius);
            padding: 1.6rem 1.8rem;
            box-shadow: var(--shadow-card);
            margin-bottom: 1.5rem;
        }

        .athletix-card-dark {
            background-color: var(--card-dark);
            border: 1px solid #282B28;
            border-radius: var(--card-radius);
            padding: 1.8rem 2rem;
            color: #FFFFFF;
            box-shadow: var(--shadow-elevated);
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
        }

        .athletix-card-lime {
            background-color: var(--accent-lime);
            border: 1px solid #B8E64B;
            border-radius: var(--card-radius);
            padding: 1.8rem 2rem;
            color: var(--text-primary);
            box-shadow: 0 8px 24px -4px rgba(200, 244, 90, 0.4);
            margin-bottom: 1.5rem;
        }

        /* Chart Wrapper */
        .chart-container-box {
            background: #FFFFFF;
            border: 1px solid var(--border-light);
            border-radius: var(--card-radius);
            padding: 1.5rem 1.6rem;
            box-shadow: var(--shadow-card);
            margin-bottom: 1.5rem;
        }

        .chart-header-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }

        .chart-title-text {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.01em;
        }

        .chart-caption-text {
            font-size: 0.78rem;
            color: var(--text-secondary);
            margin-top: 2px;
        }

        /* Modern KPI Cards */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            margin-bottom: 1.6rem;
        }

        .kpi-card-v2 {
            background: #FFFFFF;
            border: 1px solid var(--border-light);
            border-radius: 18px;
            padding: 1.25rem 1.4rem;
            box-shadow: var(--shadow-card);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .kpi-card-v2:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px -2px rgba(23, 25, 23, 0.06);
        }

        .kpi-label-v2 {
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-secondary);
            margin-bottom: 0.4rem;
        }

        .kpi-value-v2 {
            font-size: 1.95rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            color: var(--text-primary);
            line-height: 1.1;
        }

        .kpi-subtext-v2 {
            font-size: 0.76rem;
            font-weight: 500;
            color: var(--text-secondary);
            margin-top: 0.45rem;
        }

        /* Metric Card (Compact) */
        .metric-card-box {
            background: #FFFFFF;
            border: 1px solid var(--border-light);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            box-shadow: var(--shadow-card);
        }

        .metric-card-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.4rem;
        }

        .metric-card-title {
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-secondary);
        }

        .metric-card-value {
            font-size: 1.65rem;
            font-weight: 800;
            color: var(--text-primary);
            letter-spacing: -0.03em;
        }

        .metric-card-unit {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-left: 4px;
        }

        /* Pill Buttons & Badges */
        .pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 12px;
            border-radius: var(--pill-radius);
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        .pill-badge-lime {
            background-color: var(--accent-lime);
            color: var(--text-primary);
        }

        .pill-badge-dark {
            background-color: var(--card-dark);
            color: #FFFFFF;
        }

        .pill-badge-grey {
            background-color: #ECEFEC;
            color: var(--text-secondary);
        }

        .pill-badge-red {
            background-color: #FFEAE8;
            color: #D32F2F;
        }

        /* Status Indicator */
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: var(--pill-radius);
            font-size: 0.75rem;
            font-weight: 600;
            background: #F5F7F5;
            border: 1px solid var(--border-light);
            color: var(--text-primary);
        }

        .status-dot-active {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #8CCB42;
            box-shadow: 0 0 6px #8CCB42;
        }

        .status-dot-inactive {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #A3A8A4;
        }

        /* Empty State */
        .empty-state-box {
            text-align: center;
            padding: 3rem 2rem;
            background: #FFFFFF;
            border: 1px dashed var(--border-light);
            border-radius: var(--card-radius);
            margin: 1.5rem 0;
        }

        .empty-state-icon {
            font-size: 2.4rem;
            margin-bottom: 0.8rem;
        }

        .empty-state-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.3rem;
        }

        .empty-state-msg {
            font-size: 0.86rem;
            color: var(--text-secondary);
            max-width: 400px;
            margin: 0 auto;
        }

        /* Scientific Disclaimer Banner */
        .scientific-banner {
            background-color: #FFFFFF;
            border-left: 5px solid var(--text-primary);
            border-radius: 14px;
            padding: 1.1rem 1.4rem;
            margin: 1.4rem 0;
            box-shadow: var(--shadow-card);
            font-size: 0.88rem;
            color: var(--text-primary);
            line-height: 1.55;
        }

        /* Streamlit Tabs Customization */
        div[data-testid="stTabs"] button[role="tab"] {
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            color: var(--text-secondary) !important;
            padding: 8px 18px !important;
            border-radius: var(--pill-radius) !important;
            background-color: transparent !important;
            border: 1px solid transparent !important;
            margin-right: 6px !important;
            transition: all 0.2s ease !important;
        }

        div[data-testid="stTabs"] button[role="tab"]:hover {
            color: var(--text-primary) !important;
            background-color: #FFFFFF !important;
        }

        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            background-color: var(--card-dark) !important;
            color: #FFFFFF !important;
            border: 1px solid var(--card-dark) !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }

        div[data-testid="stTabs"] div[data-baseweb="tab-highlight"] {
            display: none !important;
        }

        div[data-testid="stTabs"] div[data-baseweb="tab-border"] {
            display: none !important;
        }

        /* Dataframe styling */
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border-light) !important;
            border-radius: 16px !important;
            overflow: hidden !important;
            background: #FFFFFF !important;
            box-shadow: var(--shadow-card) !important;
        }

        /* Inputs and Selectbox styling */
        div[data-testid="stTextInput"] input,
        div[data-testid="stSelectbox"] > div {
            border-radius: 12px !important;
            border: 1px solid var(--border-light) !important;
            background-color: #FFFFFF !important;
            font-size: 0.88rem !important;
            color: var(--text-primary) !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: var(--accent-lime-dark) !important;
            box-shadow: 0 0 0 2px rgba(200, 244, 90, 0.4) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_bar(active_cohort: str = "149 Scrimmage Cohort"):
    """Render top identity navigation bar with logo, research cohort badge, and controls."""
    st.markdown(
        f"""
        <div class="top-bar-container">
            <div class="top-bar-brand">
                <div class="top-bar-logo-icon">⚡</div>
                <div>
                    <div class="top-bar-brand-title">ATHLETIX AI</div>
                    <div class="top-bar-brand-sub">NFL Movement Intelligence • Big Data Bowl 2027</div>
                </div>
            </div>
            <div class="top-bar-pills">
                <span class="top-pill top-pill-lime">● {active_cohort}</span>
                <span class="top-pill top-pill-dark">10 Hz RFID Feeds</span>
                <span class="top-pill">🔔 0 Alerts</span>
                <span class="top-pill" style="font-weight: 700;">👤 Scouting Lab</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_editorial_header(title: str, subtitle: str, tag: str = ""):
    """Render a clean editorial-style page title and subtitle."""
    tag_html = f'<span class="pill-badge pill-badge-lime" style="margin-bottom: 8px;">{tag}</span><br>' if tag else ''
    st.markdown(
        f"""
        <div class="editorial-header">
            {tag_html}
            <h1 class="editorial-title">{title}</h1>
            <p class="editorial-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str = "", badge: str = ""):
    """Render a clean section header with optional subtitle and badge."""
    badge_html = f'<span class="pill-badge pill-badge-lime">{badge}</span>' if badge else ''
    subtitle_html = f'<div class="section-header-subtitle">{subtitle}</div>' if subtitle else ''
    st.markdown(
        f"""
        <div class="section-header-container">
            <div>
                <h2 class="section-header-title">{title}</h2>
                {subtitle_html}
            </div>
            {badge_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card_v2(label: str, value: str, subtext: str = "", highlight_lime: bool = False):
    """Render high-clarity minimalist KPI card."""
    border_style = "border-color: #B8E64B; background-color: #FAFDF5;" if highlight_lime else ""
    val_color = "color: #171917;"
    return f"""
    <div class="kpi-card-v2" style="{border_style}">
        <div class="kpi-label-v2">{label}</div>
        <div class="kpi-value-v2" style="{val_color}">{value}</div>
        {f'<div class="kpi-subtext-v2">{subtext}</div>' if subtext else ''}
    </div>
    """


def render_kpi_card(label: str, value: str, subtext: str = "", highlight_lime: bool = False):
    """Alias for render_kpi_card_v2."""
    return render_kpi_card_v2(label, value, subtext, highlight_lime)


def render_metric_card(title: str, value: str, unit: str = "", badge_text: str = "", badge_color: str = "lime", subtext: str = ""):
    """Render a compact metric card with title, value, unit, and badge."""
    badge_class = f"pill-badge-{badge_color}" if badge_color in ["lime", "dark", "grey", "red"] else "pill-badge-lime"
    badge_html = f'<span class="pill-badge {badge_class}">{badge_text}</span>' if badge_text else ''
    subtext_html = f'<div style="font-size: 0.74rem; color: #858B86; margin-top: 4px;">{subtext}</div>' if subtext else ''
    return f"""
    <div class="metric-card-box">
        <div class="metric-card-top">
            <span class="metric-card-title">{title}</span>
            {badge_html}
        </div>
        <div style="display: flex; align-items: baseline;">
            <span class="metric-card-value">{value}</span>
            {f'<span class="metric-card-unit">{unit}</span>' if unit else ''}
        </div>
        {subtext_html}
    </div>
    """


def render_chart_container(fig, title: str = "", caption: str = ""):
    """Render a Plotly chart inside a styled card container."""
    header_html = ""
    if title or caption:
        header_html = f"""
        <div class="chart-header-row">
            <div>
                {f'<div class="chart-title-text">{title}</div>' if title else ''}
                {f'<div class="chart-caption-text">{caption}</div>' if caption else ''}
            </div>
        </div>
        """
        st.markdown(f'<div class="chart-container-box">{header_html}', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_player_selector(player_options: List[str], default_index: int = 0, key: str = "player_selector", label: str = "Select Prospect"):
    """Render standardized prospect dropdown selector."""
    return st.selectbox(
        label,
        options=player_options,
        index=default_index if 0 <= default_index < len(player_options) else 0,
        key=key,
    )


def render_search_filter_bar(search_key: str = "filter_search", placeholder: str = "Search prospects, positions, colleges..."):
    """Render standardized search bar."""
    return st.text_input(
        "Search",
        placeholder=placeholder,
        key=search_key,
        label_visibility="collapsed",
    )


def render_status_indicator(status_text: str, is_active: bool = True, badge: str = "ONLINE"):
    """Render status pill with green/grey glowing dot."""
    dot_class = "status-dot-active" if is_active else "status-dot-inactive"
    st.markdown(
        f"""
        <div class="status-pill">
            <span class="{dot_class}"></span>
            <span>{status_text}</span>
            <span class="pill-badge pill-badge-lime" style="font-size: 0.68rem; padding: 2px 8px; margin-left: 4px;">{badge}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(title: str = "No Records Found", message: str = "Try adjusting your filters or search terms.", icon: str = "🔍"):
    """Render empty state card when search or filters return zero items."""
    st.markdown(
        f"""
        <div class="empty-state-box">
            <div class="empty-state-icon">{icon}</div>
            <div class="empty-state-title">{title}</div>
            <div class="empty-state-msg">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_scientific_banner(title: str, text: str):
    """Render scientific boundary card in minimal editorial style."""
    st.markdown(
        f"""
        <div class="scientific-banner">
            <div style="font-weight: 800; font-size: 0.92rem; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px;">
                🔬 {title}
            </div>
            <div>{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
