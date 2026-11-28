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

        /* Design System Variables - Design 2: Next-Gen Motion Intelligence */
        :root {
            --bg-app: #080C14;
            --bg-sidebar: #06090F;
            --card-bg: #0F172A;
            --card-bg-elevated: #131D31;
            --card-border: #1E293B;
            --card-border-highlight: #38BDF8;
            --accent-blue: #38BDF8;
            --accent-cyan: #22D3EE;
            --accent-violet: #8B5CF6;
            --accent-gradient: linear-gradient(135deg, #06B6D4 0%, #3B82F6 50%, #8B5CF6 100%);
            --accent-cyan-dim: rgba(34, 211, 238, 0.15);
            --accent-cyan-glow: rgba(34, 211, 238, 0.25);
            --accent-blue-glow: rgba(56, 189, 248, 0.25);
            --accent-lime: #C8F45A;
            --text-primary: #FFFFFF;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            --card-radius: 18px;
            --pill-radius: 9999px;
            --shadow-card: 0 10px 25px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.4);
            --shadow-glow: 0 0 25px rgba(56, 189, 248, 0.22);
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

        /* Sidebar Styling (Deep Navy & Graphite) */
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
            background-color: #0F172A !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stRadio"] label[data-checked="true"],
        div[data-testid="stRadio"] label:has(input:checked) {
            background: linear-gradient(135deg, #06B6D4 0%, #2563EB 100%) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            box-shadow: 0 4px 18px rgba(37, 99, 235, 0.45) !important;
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
            background: #0F172A;
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
            background: #1E293B;
            color: var(--text-secondary);
            font-size: 0.72rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 6px;
            border: 1px solid #334155;
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
            background: #0F172A;
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
            background: #0F172A;
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
            background-color: var(--accent-cyan);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-cyan);
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
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
            border: 1px solid var(--accent-cyan) !important;
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
            border-color: #38BDF8;
            transform: translateY(-2px);
        }

        .kpi-dark-card-active {
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.16) 0%, rgba(15, 23, 42, 0.95) 100%);
            border: 1.5px solid var(--accent-cyan);
            box-shadow: 0 0 22px rgba(34, 211, 238, 0.28);
        }

        .kpi-dark-icon-wrap {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: #1E293B;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            color: #FFFFFF;
            flex-shrink: 0;
        }

        .kpi-dark-icon-wrap-cyan, .kpi-dark-icon-wrap-lime {
            background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%);
            color: #FFFFFF;
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

        .pill-badge-cyan {
            background-color: rgba(34, 211, 238, 0.16);
            color: #22D3EE;
            border: 1px solid rgba(34, 211, 238, 0.35);
        }

        .pill-badge-blue {
            background-color: rgba(56, 189, 248, 0.16);
            color: #38BDF8;
            border: 1px solid rgba(56, 189, 248, 0.35);
        }

        .pill-badge-violet {
            background-color: rgba(139, 92, 246, 0.16);
            color: #A78BFA;
            border: 1px solid rgba(139, 92, 246, 0.35);
        }

        .pill-badge-lime {
            background-color: var(--accent-cyan);
            color: #080C14;
        }

        .pill-badge-dark {
            background-color: #1E293B;
            color: #FFFFFF;
            border: 1px solid var(--card-border);
        }

        .pill-badge-grey {
            background-color: #1E293B;
            color: var(--text-secondary);
        }

        /* Bottom Feature Cards with Background Graphics */
        .hero-cta-motion {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 60%, #8B5CF6 100%);
            color: #FFFFFF !important;
            font-weight: 800;
            font-size: 0.88rem;
            padding: 10px 24px;
            border-radius: var(--pill-radius);
            text-decoration: none;
            box-shadow: 0 4px 20px rgba(56, 189, 248, 0.40);
            transition: all 0.2s ease;
        }

        .hero-cta-motion:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(56, 189, 248, 0.55);
        }

        .hero-cta-lime {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 60%, #8B5CF6 100%);
            color: #FFFFFF !important;
            font-weight: 800;
            font-size: 0.88rem;
            padding: 10px 22px;
            border-radius: var(--pill-radius);
            text-decoration: none;
            box-shadow: 0 4px 16px rgba(56, 189, 248, 0.35);
            transition: all 0.2s ease;
        }

        .hero-cta-lime:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.50);
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

        /* Biomechanical Prospect Card Layout (Design 2) */
        .bio-prospect-card {
            background: #0F172A;
            border: 1px solid #1E293B;
            border-radius: 18px;
            padding: 1.3rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        }

        .bio-prospect-header {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 1.1rem;
            padding-bottom: 0.9rem;
            border-bottom: 1px solid #1E293B;
        }

        .bio-avatar-circle {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #131D31 0%, #0F172A 100%);
            border: 2px solid #22D3EE;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            box-shadow: 0 0 14px rgba(34, 211, 238, 0.35);
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
            color: #94A3B8;
            margin-top: 2px;
        }

        .bio-kpi-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 7px 0;
            border-bottom: 1px solid rgba(30, 41, 59, 0.7);
            font-size: 0.82rem;
        }

        .bio-kpi-row:last-child {
            border-bottom: none;
        }

        .bio-kpi-label {
            color: #94A3B8;
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

        /* Model Architecture Comparison Card & Table (Design 2) */
        .model-arch-card {
            background: #0F172A;
            border: 1px solid #1E293B;
            border-radius: 18px;
            padding: 1.4rem;
            min-height: 335px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .model-arch-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 1.1rem;
        }

        .model-arch-title {
            font-size: 1.08rem;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.02em;
        }

        .model-arch-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 8px;
            font-size: 0.88rem;
        }

        .model-arch-th-left {
            color: #8B949E;
            text-transform: uppercase;
            font-size: 0.72rem;
            letter-spacing: 0.06em;
            text-align: left;
            padding: 0 10px 8px 10px;
        }

        .model-arch-th-right {
            color: #8B949E;
            text-transform: uppercase;
            font-size: 0.72rem;
            letter-spacing: 0.06em;
            text-align: right;
            padding: 0 10px 8px 10px;
        }

        .model-row-featured {
            background: rgba(34, 211, 238, 0.16);
            border: 1.5px solid #22D3EE;
            color: #FFFFFF;
            font-weight: 700;
        }

        .model-row-normal {
            background: rgba(255, 255, 255, 0.02);
            color: #D1D5DB;
        }

        /* Key Research Findings Checklist Card (Design 2) */
        .findings-card {
            background: #0F172A;
            border: 1px solid #1E293B;
            border-radius: 18px;
            padding: 1.4rem;
            min-height: 335px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        }

        .findings-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 1.2rem;
        }

        .findings-title {
            font-size: 1.08rem;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.02em;
        }

        .findings-list {
            display: flex;
            flex-direction: column;
            gap: 13px;
            font-size: 0.88rem;
            color: #D1D5DB;
            line-height: 1.45;
        }

        .findings-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }

        .findings-check {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.72rem;
            font-weight: 900;
            flex-shrink: 0;
            margin-top: 1px;
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
    """Render dark KPI card matching Design 2 Next-Gen Motion Intelligence without markdown code block triggering."""
    active_class = "kpi-dark-card-active" if highlight_lime else "kpi-dark-card"
    icon_wrap_class = "kpi-dark-icon-wrap-cyan" if highlight_lime else "kpi-dark-icon-wrap"
    
    icon_map = {
        "Combine Prospects": "👥",
        "In-Game Tracked": "🏃",
        "Research Cohort": "📚",
        "Route Separation": "🔬",
        "Drill Trials": "🏋️",
        "Tracking Frames": "💾",
        "Evaluated 40yd Sprints": "⏱️",
        "R² ≥ 0.98 (Exceptional)": "⭐",
        "R² ≥ 0.95 (High Fit)": "🎯",
        "Skipped / DNP 40yd": "⚠️",
        "Mean Apex Speed": "⚡",
        "Speed Preservation Ratio": "🔄",
        "Speed Preservation": "🔄",
        "Peak Angular Velocity": "📐",
        "Tracked COD Trials": "📊",
        "Turning Efficiency Index": "📈",
        "Mean Peak Accel (a_max)": "🚀",
        "Mean Peak Accel": "🚀",
        "Initial Drive (a_init)": "⚡",
        "Initial Drive": "⚡",
        "Braking Deceleration": "🛑",
        "Max Deceleration": "🛑",
        "Mean Positive Jerk": "📈",
        "Mean Pos Jerk": "📈",
    }
    icon = icon_map.get(label, "⚡")
    val_color = '#22D3EE' if highlight_lime else '#FFFFFF'
    sub_html = f'<div style="font-size: 0.70rem; color: #94A3B8; margin-top: 2px;">{subtext}</div>' if subtext else ''
    
    html = (
        f'<div class="{active_class}">'
        f'<div class="{icon_wrap_class}">{icon}</div>'
        '<div>'
        f'<div class="kpi-dark-num" style="color: {val_color};">{value}</div>'
        f'<div class="kpi-dark-label">{label}</div>'
        f'{sub_html}'
        '</div>'
        '</div>'
    )
    return html


def render_kpi_card(label: str, value: str, subtext: str = "", highlight_lime: bool = False):
    """Alias for render_kpi_card_v2."""
    return render_kpi_card_v2(label, value, subtext, highlight_lime)


def render_metric_card(title: str, value: str, unit: str = "", badge_text: str = "", badge_color: str = "cyan", subtext: str = ""):
    """Render compact metric card in Design 2 dark styling without markdown indentation issues."""
    color_map = {
        "cyan": ("rgba(34, 211, 238, 0.16)", "#22D3EE", "#22D3EE"),
        "blue": ("rgba(56, 189, 248, 0.16)", "#38BDF8", "#38BDF8"),
        "violet": ("rgba(167, 139, 250, 0.16)", "#A78BFA", "#A78BFA"),
        "lime": ("rgba(34, 211, 238, 0.16)", "#22D3EE", "#22D3EE"),
        "dark": ("#1E293B", "#94A3B8", "#334155"),
        "grey": ("#131D31", "#94A3B8", "#1E293B"),
        "red": ("rgba(239, 68, 68, 0.16)", "#EF4444", "#EF4444"),
    }
    bg, fg, border = color_map.get(badge_color, ("#1E293B", "#94A3B8", "#334155"))
    badge_html = f'<span style="background:{bg}; color:{fg}; border:1px solid {border}; font-size:0.68rem; font-weight:800; padding:2px 8px; border-radius:9999px;">{badge_text}</span>' if badge_text else ''
    unit_html = f'<span style="font-size:0.80rem; font-weight:600; color:#94A3B8; margin-left:4px;">{unit}</span>' if unit else ''
    subtext_html = f'<div style="font-size:0.74rem; color:#94A3B8; margin-top:4px;">{subtext}</div>' if subtext else ''
    
    html = (
        '<div style="background:#0F172A; border:1px solid #1E293B; border-radius:14px; padding:0.95rem 1.15rem; box-shadow:0 4px 14px rgba(0,0,0,0.3);">'
        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">'
        f'<span style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#94A3B8;">{title}</span>'
        f'{badge_html}'
        '</div>'
        '<div style="display:flex; align-items:baseline;">'
        f'<span style="font-size:1.55rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.03em;">{value}</span>'
        f'{unit_html}'
        '</div>'
        f'{subtext_html}'
        '</div>'
    )
    return html


def render_scientific_banner(title: str, text: str):
    """Render scientific boundary card with Design 2 cyan accent bar without markdown indentation issues."""
    html = (
        '<div style="background: #0F172A; border-left: 4px solid #22D3EE; border-top: 1px solid #1E293B; border-right: 1px solid #1E293B; border-bottom: 1px solid #1E293B; border-radius: 0 14px 14px 0; padding: 1.1rem 1.4rem; margin-bottom: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">'
        '<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">'
        '<span style="font-size: 1.1rem; color: #22D3EE;">🛡️</span>'
        f'<strong style="font-size: 0.92rem; color: #FFFFFF; letter-spacing: -0.01em;">{title}</strong>'
        '</div>'
        f'<div style="font-size: 0.84rem; color: #94A3B8; line-height: 1.6;">{text}</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_feature_card(title: str, subtitle: str, icon: str, badge: str = "", bg_image_url: str = ""):
    """Render bottom feature card matching Design 2 with photo background and circular arrow."""
    badge_html = f'<span style="background:rgba(34,211,238,0.18); color:#22D3EE; border:1px solid #22D3EE; font-size:0.68rem; font-weight:700; padding:2px 8px; border-radius:9999px;">{badge}</span>' if badge else ''
    bg_style = f"background-image: linear-gradient(180deg, rgba(15,23,42,0.7) 0%, rgba(8,12,20,0.95) 100%), url('{bg_image_url}');" if bg_image_url else "background: #0F172A;"
    
    html = (
        f'<div class="feature-hero-card" style="{bg_style}">'
        '<div class="feature-card-content">'
        f'<div class="feature-card-icon-pill">{icon}</div>'
        '<div class="feature-card-title-row">'
        f'<span class="feature-card-title">{title}</span>'
        f'{badge_html}'
        '</div>'
        f'<div class="feature-card-desc">{subtitle}</div>'
        '</div>'
        '<div class="feature-card-arrow-btn">➔</div>'
        '</div>'
    )
    return html


def render_section_header(title: str, subtitle: str = "", badge: str = ""):
    """Render clean dark section header without markdown indentation issues."""
    badge_html = f'<span class="pill-badge pill-badge-cyan">{badge}</span>' if badge else ''
    subtitle_html = f'<div style="font-size: 0.84rem; color: #94A3B8; margin-top: 2px;">{subtitle}</div>' if subtitle else ''
    html = (
        '<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1.2rem; margin-bottom: 1.0rem;">'
        '<div>'
        f'<h2 style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; margin: 0;">{title}</h2>'
        f'{subtitle_html}'
        '</div>'
        f'{badge_html}'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


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


def render_model_architecture_card(models: Optional[List[Dict[str, Any]]] = None, note: str = "") -> str:
    """Render the Model Architecture Comparison card without triggering markdown code block parsing."""
    if models is None:
        models = [
            {"name": "Traditional (A)", "r2": "0.9381", "rmse": "0.3843", "is_featured": True},
            {"name": "Sensor Only (B)", "r2": "0.9184", "rmse": "0.4411", "is_featured": False},
            {"name": "Hybrid (C)", "r2": "0.9311", "rmse": "0.4053", "is_featured": False},
        ]
    if not note:
        note = '<span style="color: #22D3EE; font-weight: 700;">Paired Test:</span> Model A vs Model C ΔRMSE = +0.0210 yd/s (t = -2.74, p = 0.0069).'

    rows = []
    for m in models:
        if m.get("is_featured"):
            row = (
                '<tr class="model-row-featured">'
                f'<td style="padding: 10px; border-top-left-radius: 12px; border-bottom-left-radius: 12px; color: #22D3EE; font-weight: 800;">{m["name"]}</td>'
                f'<td style="text-align: right; padding: 10px; color: #22D3EE; font-weight: 800;">{m["r2"]}</td>'
                f'<td style="text-align: right; padding: 10px; border-top-right-radius: 12px; border-bottom-right-radius: 12px; color: #22D3EE; font-weight: 800;">{m["rmse"]}</td>'
                '</tr>'
            )
        else:
            row = (
                '<tr class="model-row-normal">'
                f'<td style="padding: 10px; border-top-left-radius: 12px; border-bottom-left-radius: 12px;">{m["name"]}</td>'
                f'<td style="text-align: right; padding: 10px;">{m["r2"]}</td>'
                f'<td style="text-align: right; padding: 10px; border-top-right-radius: 12px; border-bottom-right-radius: 12px;">{m["rmse"]}</td>'
                '</tr>'
            )
        rows.append(row)
    tbody = "".join(rows)

    html = (
        '<div class="model-arch-card">'
        '<div>'
        '<div class="model-arch-header">'
        '<span style="font-size: 1.1rem; color: #8B5CF6;">📚</span>'
        '<span class="model-arch-title">Model Architecture Comparison</span>'
        '</div>'
        '<table class="model-arch-table">'
        '<thead>'
        '<tr>'
        '<th class="model-arch-th-left">Model</th>'
        '<th class="model-arch-th-right">R² (OOF)</th>'
        '<th class="model-arch-th-right">RMSE (yd/s)</th>'
        '</tr>'
        '</thead>'
        f'<tbody>{tbody}</tbody>'
        '</table>'
        '</div>'
        f'<div style="font-size: 0.74rem; color: #94A3B8; margin-top: 14px; line-height: 1.45;">{note}</div>'
        '</div>'
    )
    return html


def render_key_findings_card(findings: Optional[List[Tuple[str, str, str]]] = None) -> str:
    """Render the Key Research Findings checklist card without triggering markdown code block parsing."""
    if findings is None:
        findings = [
            ("✓", "#22D3EE", "Traditional combine testing remains the dominant baseline predictor."),
            ("✓", "#38BDF8", "10 Hz sensor kinematics add non-linear agility & deceleration context."),
            ("✓", "#8B5CF6", "Athletic Alpha isolates unmodeled regular-season speed translation."),
            ("✓", "#22D3EE", "Multicollinearity prevents sensor features from displacing stopwatches."),
        ]

    items = []
    for icon, bg, text in findings:
        color = "#080C14" if bg != "#8B5CF6" else "#FFFFFF"
        item = (
            '<div class="findings-item">'
            f'<span class="findings-check" style="background: {bg}; color: {color};">{icon}</span>'
            f'<span>{text}</span>'
            '</div>'
        )
        items.append(item)
    items_body = "".join(items)

    html = (
        '<div class="findings-card">'
        '<div class="findings-header">'
        '<span style="font-size: 1.1rem; color: #22D3EE;">🎯</span>'
        '<span class="findings-title">Key Research Findings</span>'
        '</div>'
        f'<div class="findings-list">{items_body}</div>'
        '</div>'
    )
    return html

