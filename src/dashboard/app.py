"""
ATHLETIX AI — Main Streamlit Application Shell
Premium Dark NFL Movement Intelligence Platform
Deep charcoal black (#0B0E11), graphite containers (#161B22), neon lime (#C8F45A),
modern 7-page sports analytics navigation, and stadium visuals.
"""

import sys
from pathlib import Path

# Ensure workspace root is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from src.dashboard.components import inject_custom_css, render_top_bar, render_status_indicator
from src.dashboard.views import (
    overview,
    prospect_explorer,
    model_performance,
    athletic_alpha,
    biomechanical_lab,
    comparison_studio,
    methodology,
)

# Configure Streamlit Page
st.set_page_config(
    page_title="ATHLETIX AI — NFL Movement Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Global Dark Design System CSS
inject_custom_css()

# Sidebar: Branding, 7-Page Navigation, Stadium Telemetry
with st.sidebar:
    # Stylized Neon Lime Logo & Brand Title
    st.markdown(
        """
        <div style="padding: 0.6rem 0.4rem 1.4rem 0.4rem;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 36px; height: 36px; border-radius: 10px; background: #C8F45A; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 1.35rem; color: #0B0E11; box-shadow: 0 0 14px rgba(200, 244, 90, 0.45);">
                    A
                </div>
                <div>
                    <div style="font-size: 1.25rem; font-weight: 900; color: #FFFFFF; letter-spacing: -0.03em; line-height: 1;">
                        ATHLETIX AI
                    </div>
                    <div style="font-size: 0.68rem; font-weight: 700; color: #8B949E; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 3px;">
                        NFL Movement Intelligence
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 7 Core Navigation Destinations Matching Reference
    page_selection = st.radio(
        "Navigation",
        [
            "Research Overview",
            "Prospect Explorer",
            "Model Performance",
            "Athletic Alpha",
            "Biomechanical Lab",
            "Player Comparison",
            "Research Methodology",
        ],
        index=0,
        format_func=lambda p: {
            "Research Overview": "🏠  Research Overview",
            "Prospect Explorer": "🔍  Prospect Explorer",
            "Model Performance": "📚  Model Performance",
            "Athletic Alpha": "📈  Athletic Alpha",
            "Biomechanical Lab": "🏃  Biomechanical Lab",
            "Player Comparison": "👥  Player Comparison",
            "Research Methodology": "📖  Research Methodology",
        }.get(p, p),
        label_visibility="collapsed",
    )

    st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)
    
    # Sidebar Bottom: Stadium Backdrop & Official Platform Telemetry
    st.markdown(
        """
        <div style="position: relative; border-radius: 16px; padding: 1.2rem 1rem; background: linear-gradient(180deg, rgba(22, 27, 34, 0.4) 0%, rgba(11, 14, 17, 0.95) 100%), radial-gradient(circle at top, rgba(200,244,90,0.12) 0%, transparent 70%); border: 1px solid #1E2631; overflow: hidden;">
            <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                <div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.25rem;">🛡️</span>
                        <div>
                            <div style="font-size: 0.72rem; font-weight: 800; color: #FFFFFF; text-transform: uppercase; letter-spacing: 0.08em;">
                                NFL Analytics
                            </div>
                            <div style="font-size: 0.64rem; color: #8B949E; line-height: 1.2;">
                                Sports Science Suite
                            </div>
                        </div>
                    </div>
                </div>
                <div style="font-family: monospace; font-size: 1.1rem; font-weight: 900; color: #C8F45A; letter-spacing: -1px; text-shadow: 0 0 8px rgba(200,244,90,0.6);">
                    ///
                </div>
            </div>
            <div style="margin-top: 10px; font-size: 0.68rem; color: #64748B; border-top: 1px solid #1E2631; padding-top: 8px;">
                10 Hz RFID Feeds • Big Data Bowl 2027
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Render Top Bar Identity & Navigation Pill Header
render_top_bar(active_cohort="2023 Cohort")

# Route to selected page
if page_selection == "Research Overview":
    overview.render_page()
elif page_selection == "Prospect Explorer":
    prospect_explorer.render_page()
elif page_selection == "Model Performance":
    model_performance.render_page()
elif page_selection == "Athletic Alpha":
    athletic_alpha.render_page()
elif page_selection == "Biomechanical Lab":
    biomechanical_lab.render_page()
elif page_selection == "Player Comparison":
    comparison_studio.render_page()
elif page_selection == "Research Methodology":
    methodology.render_page()
