"""
ATHLETIX AI — Premium Dark Sports Performance Intelligence Design System
Faithful implementation of the NFL Movement Intelligence visual reference:
Deep charcoal black (#0B0E11), graphite surfaces (#161B22), neon lime highlights (#C8F45A),
crisp white typography (#FFFFFF), stadium-inspired visuals, and modern sidebar navigation.
"""

import streamlit as st
from typing import List, Optional, Dict, Any


def inject_custom_css():
    """Inject the complete premium dark sports intelligence design system into Streamlit."""
    st.markdown(
        """
        <style>
        /* Import Google Fonts: Plus Jakarta Sans, Inter, JetBrains Mono */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

        /* Design System Variables */
        :root {
            --bg-app: #0B0E11;
            --bg-sidebar: #0B0E11;
            --card-bg: #161B22;
            --card-bg-elevated: #1B222D;
            --card-border: #242D38;
            --card-border-highlight: #C8F45A;
            --accent-lime: #C8F45A;
            --accent-lime-hover: #D6F972;
            --accent-lime-dim: rgba(200, 244, 90, 0.15);
            --accent-lime-glow: rgba(200, 244, 90, 0.25);
            --text-primary: #FFFFFF;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            --card-radius: 18px;
            --pill-radius: 9999px;
            --shadow-card: 0 8px 24px -2px rgba(0, 0, 0, 0.45);
            --shadow-glow: 0 0 20px rgba(200, 244, 90, 0.20);
        }

        /* App Background & Base Typography */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: var(--bg-app) !important;
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
        }

        /* Main content container */
        .main .block-container {
            max-width: 1480px;
            padding-top: 1.0rem;
            padding-bottom: 3.5rem;
            padding-left: 2.0rem;
            padding-right: 2.0rem;
        }

        /* Remove default Streamlit header, footer, multipage nav */
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

        /* Sidebar Styling (Deep Charcoal Black) */
        section[data-testid="stSidebar"] {
            background-color: var(--bg-sidebar) !important;
            border-right: 1px solid var(--card-border) !important;
            width: 280px !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            gap: 0.6rem !important;
        }

        /* Radio Navigation in Sidebar */
        div[data-testid="stRadio"] > div {
            gap: 6px !important;
        }

        div[data-testid="stRadio"] label {
            background-color: transparent !important;
            border-radius: 12px !important;
            padding: 10px 14px !important;
            margin: 0 !important;
            font-size: 0.90rem !important;
            font-weight: 600 !important;
            color: var(--text-secondary) !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            border: 1px solid transparent !important;
            cursor: pointer !important;
        }

        div[data-testid="stRadio"] label:hover {
            background-color: #141A22 !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stRadio"] label[data-checked="true"],
        div[data-testid="stRadio"] label:has(input:checked) {
            background-color: var(--accent-lime) !important;
            color: #0B0E11 !important;
            font-weight: 800 !important;
            box-shadow: 0 2px 14px rgba(200, 244, 90, 0.35) !important;
        }

        /* Hide radio circle dots for modern pill button look */
        div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }

        /* Top Bar Container */
        .top-bar-dark {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.8rem;
            gap: 16px;
        }

        .search-box-container {
            display: flex;
            align-items: center;
            background: #161B22;
            border: 1px solid var(--card-border);
            border-radius: var(--pill-radius);
            padding: 8px 18px;
            width: 440px;
            gap: 10px;
        }

        .search-box-icon {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        .search-box-text {
            color: var(--text-muted);
            font-size: 0.86rem;
            font-weight: 500;
            flex-grow: 1;
        }

        .search-kbd-badge {
            background: #242D38;
            color: var(--text-secondary);
            font-size: 0.72rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 6px;
            border: 1px solid #333D4B;
        }

        .top-bar-controls {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .cohort-dropdown-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #161B22;
            border: 1px solid var(--card-border);
            border-radius: var(--pill-radius);
            padding: 8px 16px;
            font-size: 0.84rem;
            font-weight: 600;
            color: #FFFFFF;
        }

        .icon-circle-btn {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #161B22;
            border: 1px solid var(--card-border);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF;
            font-size: 1.05rem;
            position: relative;
        }

        .notification-dot {
            position: absolute;
            top: 9px;
            right: 9px;
            width: 7px;
            height: 7px;
            background-color: var(--accent-lime);
            border-radius: 50%;
            box-shadow: 0 0 6px var(--accent-lime);
        }

        /* Card Containers */
        .athletix-card, .dark-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--card-radius);
            padding: 1.4rem 1.6rem;
            box-shadow: var(--shadow-card);
            margin-bottom: 1.3rem;
            position: relative;
        }

        .dark-card-highlight {
            background: linear-gradient(135deg, rgba(200, 244, 90, 0.08) 0%, rgba(22, 27, 34, 0.95) 100%) !important;
            border: 1px solid var(--accent-lime) !important;
            box-shadow: var(--shadow-glow) !important;
        }

        /* KPI Cards Grid */
        .kpi-dark-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 14px;
            margin-bottom: 1.6rem;
        }

        @media (max-width: 1200px) {
            .kpi-dark-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }

        @media (max-width: 768px) {
            .kpi-dark-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        .kpi-dark-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.1rem 1.2rem;
            display: flex;
            align-items: center;
            gap: 14px;
            box-shadow: var(--shadow-card);
            transition: all 0.2s ease;
        }

        .kpi-dark-card:hover {
            border-color: #384556;
            transform: translateY(-2px);
        }

        .kpi-dark-card-active {
            background: linear-gradient(135deg, rgba(200, 244, 90, 0.14) 0%, rgba(22, 27, 34, 0.95) 100%);
            border: 1.5px solid var(--accent-lime);
            box-shadow: 0 0 18px rgba(200, 244, 90, 0.20);
        }

        .kpi-dark-icon-wrap {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: #1F2732;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            color: #FFFFFF;
            flex-shrink: 0;
        }

        .kpi-dark-icon-wrap-lime {
            background: var(--accent-lime);
            color: #0B0E11;
        }

        .kpi-dark-num {
            font-size: 1.7rem;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.03em;
            line-height: 1.1;
        }

        .kpi-dark-label {
            font-size: 0.74rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-top: 2px;
        }

        /* Pill Buttons & Badges */
        .pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 12px;
            border-radius: var(--pill-radius);
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        .pill-badge-lime {
            background-color: var(--accent-lime);
            color: #0B0E11;
        }

        .pill-badge-dark {
            background-color: #1F2732;
            color: #FFFFFF;
            border: 1px solid var(--card-border);
        }

        .pill-badge-grey {
            background-color: #242D38;
            color: var(--text-secondary);
        }

        /* Bottom Feature Cards with Background Graphics */
        .hero-cta-lime {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--accent-lime);
            color: #0B0E11 !important;
            font-weight: 800;
            font-size: 0.88rem;
            padding: 10px 22px;
            border-radius: var(--pill-radius);
            text-decoration: none;
            box-shadow: 0 4px 16px rgba(200, 244, 90, 0.35);
            transition: all 0.2s ease;
        }

        .hero-cta-lime:hover {
            background: var(--accent-lime-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(200, 244, 90, 0.45);
        }

        .hero-cta-dark {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #1F2732;
            color: #FFFFFF !important;
            font-weight: 700;
            font-size: 0.88rem;
            padding: 10px 22px;
            border-radius: var(--pill-radius);
            border: 1px solid var(--card-border);
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .hero-cta-dark:hover {
            background: #283340;
            color: var(--accent-lime) !important;
            border-color: #3B4758;
        }

        /* Movement Intelligence Right Widget */
        .movement-intel-card {
            background: #161B22;
            border: 1px solid var(--card-border);
            border-radius: 18px;
            padding: 1.15rem 1.35rem;
            width: 255px;
            box-shadow: var(--shadow-card);
        }

        .movement-intel-title {
            font-size: 0.92rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 0.75rem;
            letter-spacing: -0.01em;
        }

        .movement-intel-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 10px;
            border-radius: 10px;
            background: #11151A;
            margin-bottom: 6px;
            border: 1px solid #1C232B;
            transition: all 0.15s ease;
        }

        .movement-intel-item:hover {
            border-color: var(--accent-lime);
            background: #141A22;
        }

        .movement-intel-icon {
            width: 26px;
            height: 26px;
            border-radius: 8px;
            background: rgba(200, 244, 90, 0.12);
            color: var(--accent-lime);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.90rem;
        }

        .movement-intel-text {
            font-size: 0.78rem;
            font-weight: 600;
            color: #E2E8F0;
        }

        /* Biomechanical Prospect Card Layout */
        .bio-prospect-card {
            background: #161B22;
            border: 1px solid var(--card-border);
            border-radius: 18px;
            padding: 1.3rem;
            box-shadow: var(--shadow-card);
        }

        .bio-prospect-header {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 1.1rem;
            padding-bottom: 0.9rem;
            border-bottom: 1px solid #242D38;
        }

        .bio-avatar-circle {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #242D38 0%, #161B22 100%);
            border: 2px solid var(--accent-lime);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            box-shadow: 0 0 12px rgba(200, 244, 90, 0.25);
            flex-shrink: 0;
        }

        .bio-prospect-name {
            font-size: 1.05rem;
            font-weight: 800;
            color: #FFFFFF;
            line-height: 1.2;
        }

        .bio-prospect-meta {
            font-size: 0.76rem;
            color: var(--text-secondary);
            margin-top: 2px;
        }

        .bio-kpi-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 7px 0;
            border-bottom: 1px solid rgba(36, 45, 56, 0.6);
            font-size: 0.82rem;
        }

        .bio-kpi-row:last-child {
            border-bottom: none;
        }

        .bio-kpi-label {
            color: var(--text-secondary);
            font-weight: 500;
        }

        .bio-kpi-val {
            color: #FFFFFF;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }

        .feature-card-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 1.4rem;
        }

        @media (max-width: 900px) {
            .feature-card-grid {
                grid-template-columns: 1fr;
            }
        }

        .feature-hero-card {
            background: #161B22;
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 1.5rem 1.6rem;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 180px;
            box-shadow: var(--shadow-card);
            transition: all 0.2s ease;
        }

        .feature-hero-card:hover {
            border-color: var(--accent-lime);
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), 0 0 15px rgba(200, 244, 90, 0.15);
        }

        .feature-card-bg-overlay {
            position: absolute;
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
            background-size: cover;
            background-position: center;
            opacity: 0.22;
            pointer-events: none;
        }

        .feature-card-content {
            position: relative;
            z-index: 2;
        }

        .feature-card-icon-pill {
            width: 38px;
            height: 38px;
            border-radius: 12px;
            background: var(--accent-lime);
            color: #0B0E11;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            margin-bottom: 0.9rem;
        }

        .feature-card-title-row {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 0.35rem;
        }

        .feature-card-title {
            font-size: 1.18rem;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.02em;
        }

        .feature-card-desc {
            font-size: 0.84rem;
            color: var(--text-secondary);
            line-height: 1.45;
            max-width: 90%;
        }

        .feature-card-arrow-btn {
            position: absolute;
            bottom: 1.4rem;
            right: 1.4rem;
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: #FFFFFF;
            color: #0B0E11;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.95rem;
            font-weight: 800;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            z-index: 2;
        }

        /* Scientific Banner (Dark Mode) */
        .scientific-banner {
            background-color: #161B22;
            border-left: 4px solid var(--accent-lime);
            border-top: 1px solid var(--card-border);
            border-right: 1px solid var(--card-border);
            border-bottom: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 1.1rem 1.4rem;
            margin: 1.4rem 0;
            box-shadow: var(--shadow-card);
            font-size: 0.88rem;
            color: #FFFFFF;
            line-height: 1.55;
        }

        /* Streamlit Tabs Customization (Dark Mode) */
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
            color: #FFFFFF !important;
            background-color: #1A222C !important;
        }

        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            background-color: var(--accent-lime) !important;
            color: #0B0E11 !important;
            font-weight: 800 !important;
            border: 1px solid var(--accent-lime) !important;
            box-shadow: 0 2px 10px rgba(200, 244, 90, 0.3) !important;
        }

        div[data-testid="stTabs"] div[data-baseweb="tab-highlight"],
        div[data-testid="stTabs"] div[data-baseweb="tab-border"] {
            display: none !important;
        }

        /* Streamlit Inputs & Selectboxes Dark Styling */
        div[data-testid="stTextInput"] input,
        div[data-testid="stSelectbox"] > div {
            border-radius: 12px !important;
            border: 1px solid var(--card-border) !important;
            background-color: #161B22 !important;
            font-size: 0.88rem !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: var(--accent-lime) !important;
            box-shadow: 0 0 0 2px rgba(200, 244, 90, 0.25) !important;
        }

        /* Dataframe styling in Dark Mode */
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--card-border) !important;
            border-radius: 14px !important;
            overflow: hidden !important;
            background: #161B22 !important;
            box-shadow: var(--shadow-card) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_chart_container(title: str, subtitle: str = ""):
    """Render chart header inside dark card."""
    sub_html = f'<div style="font-size: 0.82rem; color: #94A3B8; margin-top: 2px;">{subtitle}</div>' if subtitle else ''
    return f"""
    <div style="margin-bottom: 0.8rem;">
        <div style="font-size: 1.05rem; font-weight: 800; color: #FFFFFF;">{title}</div>
        {sub_html}
    </div>
    """


def render_top_bar(active_cohort: str = "2023 Cohort"):
    """Render the exact top navigation bar matching the visual reference image."""
    st.markdown(
        f"""
        <div class="top-bar-dark">
            <div class="search-box-container">
                <span class="search-box-icon">🔍</span>
                <span class="search-box-text">Search prospects, metrics, or studies...</span>
                <span class="search-kbd-badge">Ctrl + K</span>
            </div>
            <div class="top-bar-controls">
                <div class="cohort-dropdown-pill">
                    <span>📅</span>
                    <span>{active_cohort}</span>
                    <span style="font-size: 0.72rem; color: #94A3B8;">▼</span>
                </div>
                <div class="icon-circle-btn">
                    <span>🔔</span>
                    <span class="notification-dot"></span>
                </div>
                <div class="icon-circle-btn" style="background: #1F2732; border-color: #333D4B;">
                    <span>👤</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_editorial_header(title: str, subtitle: str, tag: str = "RESEARCH OVERVIEW"):
    """Render hero editorial title and subtitle matching the reference typography."""
    st.markdown(
        f"""
        <div style="margin-bottom: 1.8rem; position: relative;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-size: 0.78rem; font-weight: 800; color: #C8F45A; text-transform: uppercase; letter-spacing: 0.10em; margin-bottom: 8px;">
                        {tag}
                    </div>
                    <h1 style="font-size: 2.7rem; font-weight: 900; letter-spacing: -0.04em; color: #FFFFFF; line-height: 1.15; margin: 0;">
                        {title}
                    </h1>
                    <p style="font-size: 1.05rem; color: #94A3B8; margin-top: 8px; margin-bottom: 0; max-width: 680px; line-height: 1.5;">
                        {subtitle}
                    </p>
                </div>
                <div style="text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; color: #64748B; letter-spacing: 0.16em; line-height: 1.8; padding-top: 10px;">
                    MOVEMENT<br>
                    BIOMECHANICS<br>
                    PERFORMANCE<br>
                    INTELLIGENCE
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card_header(title: str, subtitle: str = "", action_text: str = "Details ↗", dark_action: bool = False):
    """Render card header with title and action badge."""
    sub_html = f'<div style="font-size: 0.78rem; color: #94A3B8; margin-top: 2px;">{subtitle}</div>' if subtitle else ''
    return f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <div>
            <div style="font-size: 1.12rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">{title}</div>
            {sub_html}
        </div>
        <div style="font-size: 0.76rem; font-weight: 700; color: #C8F45A; background: rgba(200, 244, 90, 0.12); padding: 4px 12px; border-radius: 9999px; border: 1px solid rgba(200, 244, 90, 0.25);">
            {action_text}
        </div>
    </div>
    """


def render_kpi_card_v2(label: str, value: str, subtext: str = "", highlight_lime: bool = False):
    """Render dark KPI card matching the 6-grid layout in the visual reference."""
    active_class = "kpi-dark-card-active" if highlight_lime else "kpi-dark-card"
    icon_wrap_class = "kpi-dark-icon-wrap-lime" if highlight_lime else "kpi-dark-icon-wrap"
    
    icon_map = {
        "Combine Prospects": "👥",
        "In-Game Tracked": "🏃",
        "Research Cohort": "📚",
        "Route Separation": "🔬",
        "Drill Trials": "🏋️",
        "Tracking Frames": "💾",
    }
    icon = icon_map.get(label, "⚡")
    
    return f"""
    <div class="{active_class}">
        <div class="{icon_wrap_class}">{icon}</div>
        <div>
            <div class="kpi-dark-num">{value}</div>
            <div class="kpi-dark-label">{label}</div>
        </div>
    </div>
    """


def render_kpi_card(label: str, value: str, subtext: str = "", highlight_lime: bool = False):
    """Alias for render_kpi_card_v2."""
    return render_kpi_card_v2(label, value, subtext, highlight_lime)


def render_metric_card(title: str, value: str, unit: str = "", badge_text: str = "", badge_color: str = "lime", subtext: str = ""):
    """Render compact metric card in dark styling."""
    badge_bg = "var(--accent-lime)" if badge_color == "lime" else "#1F2732"
    badge_txt = "#0B0E11" if badge_color == "lime" else "#FFFFFF"
    badge_html = f'<span style="background:{badge_bg}; color:{badge_txt}; font-size:0.68rem; font-weight:800; padding:2px 8px; border-radius:9999px;">{badge_text}</span>' if badge_text else ''
    subtext_html = f'<div style="font-size:0.74rem; color:#8B949E; margin-top:4px;">{subtext}</div>' if subtext else ''
    
    return f"""
    <div style="background:#161B22; border:1px solid #242D38; border-radius:14px; padding:0.95rem 1.15rem; box-shadow:0 4px 14px rgba(0,0,0,0.3);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
            <span style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#94A3B8;">{title}</span>
            {badge_html}
        </div>
        <div style="display:flex; align-items:baseline;">
            <span style="font-size:1.55rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.03em;">{value}</span>
            {f'<span style="font-size:0.80rem; font-weight:600; color:#94A3B8; margin-left:4px;">{unit}</span>' if unit else ''}
        </div>
        {subtext_html}
    </div>
    """


def render_scientific_banner(title: str, text: str):
    """Render scientific boundary card with neon lime accent bar in dark styling."""
    st.markdown(
        f"""
        <div class="scientific-banner">
            <div style="font-weight: 800; font-size: 0.90rem; text-transform: uppercase; letter-spacing: 0.05em; color: #C8F45A; margin-bottom: 4px;">
                🔬 {title}
            </div>
            <div style="color: #D1D5DB; font-size: 0.88rem; line-height: 1.55;">
                {text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_card(title: str, subtitle: str, icon: str, badge: str = "", bg_image_url: str = ""):
    """Render bottom feature card matching Visual Reference 4 with photo background and circular arrow."""
    badge_html = f'<span style="background:rgba(200,244,90,0.18); color:#C8F45A; border:1px solid rgba(200,244,90,0.35); font-size:0.68rem; font-weight:700; padding:2px 8px; border-radius:9999px;">{badge}</span>' if badge else ''
    
    bg_style = f"background-image: linear-gradient(180deg, rgba(22,27,34,0.7) 0%, rgba(22,27,34,0.95) 100%), url('{bg_image_url}');" if bg_image_url else "background: #161B22;"
    
    return f"""
    <div class="feature-hero-card" style="{bg_style}">
        <div class="feature-card-content">
            <div class="feature-card-icon-pill">{icon}</div>
            <div class="feature-card-title-row">
                <span class="feature-card-title">{title}</span>
                {badge_html}
            </div>
            <div class="feature-card-desc">{subtitle}</div>
        </div>
        <div class="feature-card-arrow-btn">➔</div>
    </div>
    """


def render_section_header(title: str, subtitle: str = "", badge: str = ""):
    """Render clean dark section header."""
    badge_html = f'<span class="pill-badge pill-badge-lime">{badge}</span>' if badge else ''
    subtitle_html = f'<div style="font-size: 0.84rem; color: #94A3B8; margin-top: 2px;">{subtitle}</div>' if subtitle else ''
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1.6rem; margin-bottom: 1.0rem;">
            <div>
                <h2 style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; margin: 0;">{title}</h2>
                {subtitle_html}
            </div>
            {badge_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_indicator(status_text: str, is_active: bool = True, badge: str = "ONLINE"):
    """Render glowing online status pill in sidebar."""
    st.markdown(
        f"""
        <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 9999px; background: #161B22; border: 1px solid #242D38; font-size: 0.76rem; color: #FFFFFF;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background-color: #C8F45A; box-shadow: 0 0 8px #C8F45A;"></span>
            <span>{status_text}</span>
            <span style="background: rgba(200, 244, 90, 0.2); color: #C8F45A; font-size: 0.68rem; font-weight: 800; padding: 2px 8px; border-radius: 9999px; margin-left: 4px;">{badge}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_segmented_bar(label: str, percent: int, bar_type: str = "lime", sublabel: str = ""):
    """Render dark segmented progress bar."""
    sub_html = f'<span style="font-size: 0.74rem; color: #94A3B8; font-weight: 500;">{sublabel}</span>' if sublabel else ''
    bar_color = "var(--accent-lime)" if bar_type == "lime" else ("#F59E0B" if bar_type == "amber" else "#3B82F6")
    return f"""
    <div style="margin-bottom: 0.9rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.35rem;">
            <span>{label} {sub_html}</span>
            <span style="color: #FFFFFF;">{percent}%</span>
        </div>
        <div style="height: 8px; background: #242D38; border-radius: 9999px; overflow: hidden;">
            <div style="width: {min(max(percent, 0), 100)}%; height: 100%; background: {bar_color}; border-radius: 9999px;"></div>
        </div>
    </div>
    """


def render_dark_ai_card(title: str, recommendation: str, bullets: Optional[List[str]] = None, tag: str = "AI SCOUT SUGGESTION"):
    """Render dark AI intelligence card."""
    bullets_html = ""
    if bullets:
        bullets_items = "".join([f"<li style='margin-bottom: 4px;'>{b}</li>" for b in bullets])
        bullets_html = f"<ul style='padding-left: 18px; margin-top: 8px; font-size: 0.82rem; color: #94A3B8;'>{bullets_items}</ul>"

    return f"""
    <div style="background: #161B22; border: 1px solid #242D38; border-radius: 18px; padding: 1.4rem; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
            <span class="pill-badge pill-badge-lime" style="font-size: 0.70rem;">{tag}</span>
            <span style="font-size: 0.85rem; color: #64748B;">↗</span>
        </div>
        <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; line-height: 1.25; margin-bottom: 0.5rem;">
            {title}
        </div>
        <div style="font-size: 0.85rem; color: #D1D5DB; line-height: 1.55;">
            {recommendation}
        </div>
        {bullets_html}
    </div>
    """


def render_empty_state(title: str = "No Records Found", message: str = "Try adjusting your filters or search terms.", icon: str = "🔍"):
    """Render empty state card in dark styling."""
    st.markdown(
        f"""
        <div style="text-align: center; padding: 3rem 2rem; background: #161B22; border: 1px dashed #242D38; border-radius: 18px; margin: 1.5rem 0;">
            <div style="font-size: 2.4rem; margin-bottom: 0.8rem;">{icon}</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.3rem;">{title}</div>
            <div style="font-size: 0.86rem; color: #94A3B8; max-width: 400px; margin: 0 auto;">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
