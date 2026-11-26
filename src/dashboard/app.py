"""
ATHLETIX AI — Main Streamlit Application Shell
Commercial sports SaaS research platform for the NFL Big Data Bowl 2027.
Minimalist light-grey (#ECEFEC), rounded white containers (#FFFFFF),
electric lime highlights (#C8F45A), deep black typography (#171917),
and 6-page core sports science navigation.
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
    methodology,
)

# Configure Streamlit Page
st.set_page_config(
    page_title="ATHLETIX AI — NFL Movement Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Global Design System CSS
inject_custom_css()

# Sidebar: Branding, Research Controls, Navigation
with st.sidebar:
    # ATHLETIX AI Brand Header
    st.markdown(
        """
        <div style="padding: 0.6rem 0.5rem 1.2rem 0.5rem;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 32px; height: 32px; border-radius: 8px; background: #C8F45A; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; color: #171917;">⚡</div>
                <div>
                    <div style="font-size: 1.18rem; font-weight: 800; color: #171917; letter-spacing: -0.03em; line-height: 1;">ATHLETIX AI</div>
                    <div style="font-size: 0.70rem; font-weight: 600; color: #858B86; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 2px;">Sports Science SaaS</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Research Cohort Selector
    cohort_selection = st.selectbox(
        "Research Cohort",
        [
            "Primary Cohort (149 • Scrimmage ≥50)",
            "Combine Attendees (510 • All Prospects)",
            "2023 Game Tracked (156 • Scrimmage & ST)",
            "Route Separation (51 • Skill Sub-Cohort)",
        ],
        index=0,
        help="Select empirical cohort subset for tracking cross-analysis.",
    )
    st.session_state["active_cohort"] = cohort_selection

    # Global Search Control
    search_query = st.text_input(
        "Search Prospect",
        placeholder="Filter by name, position...",
        label_visibility="collapsed",
    )
    if search_query:
        st.session_state["global_search"] = search_query

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # Six Navigation Destinations
    page_selection = st.radio(
        "Navigation",
        [
            "1. Research Overview",
            "2. Prospect Explorer",
            "3. Model Performance",
            "4. Athletic Alpha",
            "5. Biomechanical Lab",
            "6. Research Methodology",
        ],
        index=0,
    )

    st.markdown("---")
    
    # Status Indicator
    render_status_indicator("10 Hz RFID Feeds", is_active=True, badge="ONLINE")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="padding: 0.5rem 0.65rem; background: #F5F7F5; border-radius: 14px; border: 1px solid #E5E7E5; font-size: 0.75rem; color: #5B615C; line-height: 1.6;">
            <strong style="color: #171917;">Research Architecture:</strong><br>
            • Primary Cohort: <strong>149</strong> Players<br>
            • Game Tracked: <strong>156</strong> Players<br>
            • Combine Attendees: <strong>510</strong><br>
            • Sensor Frequency: <strong>10 Hz</strong><br>
            • Empirical Status: Verified
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("NFL Big Data Bowl 2027 • Official Submission")

# Extract short cohort label for Top Bar
short_cohort = cohort_selection.split(" (")[0] + " • " + cohort_selection.split(" • ")[-1].replace(")", "") if " • " in cohort_selection else cohort_selection

# Render Top Bar Identity & Navigation Pill Header
render_top_bar(active_cohort=short_cohort)

# Route to selected page
if "1. Research Overview" in page_selection:
    overview.render_page()
elif "2. Prospect Explorer" in page_selection:
    prospect_explorer.render_page()
elif "3. Model Performance" in page_selection:
    model_performance.render_page()
elif "4. Athletic Alpha" in page_selection:
    athletic_alpha.render_page()
elif "5. Biomechanical Lab" in page_selection:
    biomechanical_lab.render_page()
elif "6. Research Methodology" in page_selection:
    methodology.render_page()
