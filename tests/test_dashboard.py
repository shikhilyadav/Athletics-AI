"""
ATHLETIX AI — Dashboard Validation Test Suite
Unit tests for data loader, metrics, charts, components, and page rendering modules.
"""

import sys
from pathlib import Path
import pytest

# Ensure root is in path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.dashboard.data_loader import (
    load_master_df,
    load_kinematics_df,
    load_cod_df,
    load_game_tracking_df,
    load_player_play_df,
    load_oof_predictions,
    load_athletic_alpha,
    load_model_metrics,
    load_nested_cv_metrics,
    load_fdr_correlations,
    load_feature_importance,
    load_vif_analysis,
    load_dataset_inventory,
)
from src.dashboard.metrics import (
    fmt_speed,
    fmt_accel,
    fmt_time,
    fmt_ratio,
    fmt_pct,
    fmt_dist_in,
    fmt_weight_lbs,
)
from src.dashboard.charts import (
    plot_model_comparison_bars,
    plot_actual_vs_predicted,
    plot_residuals,
    plot_alpha_scatter,
    plot_alpha_position_box,
    plot_sprint_curve_distribution,
    plot_cod_apex_vs_preservation,
    plot_feature_importance,
    plot_vif_bars,
)
from src.dashboard.components import (
    render_kpi_card_v2,
    render_kpi_card,
    render_metric_card,
    render_editorial_header,
    render_section_header,
    render_status_indicator,
    render_empty_state,
    render_scientific_banner,
)


def test_data_loaders():
    """Verify all datasets load properly with verified row counts."""
    master = load_master_df()
    assert len(master) == 510, f"Expected 510 master records, got {len(master)}"
    
    kin = load_kinematics_df()
    assert len(kin) == 6310, f"Expected 6310 kinematic records, got {len(kin)}"
    
    cod = load_cod_df()
    assert len(cod) == 6310, f"Expected 6310 COD records, got {len(cod)}"
    
    game = load_game_tracking_df()
    assert len(game) == 156, f"Expected 156 game tracking records, got {len(game)}"
    
    play = load_player_play_df()
    assert len(play) == 50462, f"Expected 50462 plays, got {len(play)}"
    
    oof = load_oof_predictions()
    assert len(oof) == 149, f"Expected 149 OOF records, got {len(oof)}"
    
    alpha = load_athletic_alpha()
    assert len(alpha) == 149, f"Expected 149 alpha records, got {len(alpha)}"
    
    nested = load_nested_cv_metrics()
    assert len(nested) == 3, f"Expected 3 nested CV metrics, got {len(nested)}"
    
    fdr = load_fdr_correlations()
    assert len(fdr) == 11, f"Expected 11 FDR correlations, got {len(fdr)}"


def test_metric_formatters():
    """Verify formatting edge cases and null handling."""
    assert fmt_speed(None) == "N/A"
    assert fmt_speed(21.456) == "21.46 yd/s"
    assert fmt_accel(None) == "N/A"
    assert fmt_accel(5.213) == "5.21 yd/s²"
    assert fmt_time(None) == "N/A"
    assert fmt_time(4.381) == "4.38 s"
    assert fmt_ratio(None) == "N/A"
    assert fmt_ratio(0.8123) == "0.812"
    assert fmt_pct(None) == "N/A"
    assert fmt_pct(0.125) == "12.5%"
    assert fmt_dist_in(None) == "N/A"
    assert fmt_dist_in(33.5) == '33.5"'
    assert fmt_weight_lbs(None) == "N/A"
    assert fmt_weight_lbs(215.4) == "215 lbs"


def test_components_markup():
    """Verify reusable UI components generate expected HTML strings without error."""
    kpi_html = render_kpi_card_v2("Combine Prospects", "510", "Active Cohort", highlight_lime=True)
    assert "kpi-dark-card" in kpi_html
    assert "510" in kpi_html

    kpi_alias = render_kpi_card("In-Game Tracked", "156")
    assert "kpi-dark-card" in kpi_alias
    assert "156" in kpi_alias

    metric_html = render_metric_card("Peak Acceleration", "4.85", "yd/s²", badge_text="TOP 5%", badge_color="lime")
    assert "4.85" in metric_html
    assert "TOP 5%" in metric_html

    from src.dashboard.components import (
        render_segmented_bar,
        render_dark_ai_card,
        render_model_architecture_card,
        render_key_findings_card,
    )
    bar_html = render_segmented_bar("Sprint Burst", 94, "lime", "Peak")
    assert "94%" in bar_html

    ai_html = render_dark_ai_card("Test Insight", "Test recommendation", ["Bullet 1"])
    assert "Test Insight" in ai_html

    model_html = render_model_architecture_card()
    assert "model-arch-card" in model_html
    assert "Traditional (A)" in model_html
    assert "Sensor Only (B)" in model_html
    assert "Hybrid (C)" in model_html
    assert "0.9381" in model_html
    assert "<pre>" not in model_html
    assert "<code>" not in model_html

    findings_html = render_key_findings_card()
    assert "findings-card" in findings_html
    assert "Traditional combine testing" in findings_html
    assert "Multicollinearity prevents" in findings_html
    assert "<pre>" not in findings_html
    assert "<code>" not in findings_html


def test_charts_generation():
    """Verify all Plotly figure generators execute without error."""
    oof_df = load_oof_predictions()
    alpha_df = load_athletic_alpha()
    nested_df = load_nested_cv_metrics()
    master_df = load_master_df()
    cod_df = load_cod_df()
    feat_df = load_feature_importance()
    vif_df = load_vif_analysis()

    fig1 = plot_model_comparison_bars(nested_df, "oof_r2")
    assert fig1 is not None

    fig2 = plot_actual_vs_predicted(oof_df)
    assert fig2 is not None

    fig3 = plot_residuals(oof_df)
    assert fig3 is not None

    fig4 = plot_alpha_scatter(alpha_df)
    assert fig4 is not None

    fig5 = plot_alpha_position_box(alpha_df)
    assert fig5 is not None

    fig6 = plot_sprint_curve_distribution(master_df)
    assert fig6 is not None

    fig7 = plot_cod_apex_vs_preservation(cod_df)
    assert fig7 is not None

    fig8 = plot_feature_importance(feat_df)
    assert fig8 is not None

    fig9 = plot_vif_bars(vif_df)
    assert fig9 is not None

    # Test signature comparison studio charts
    p1 = master_df.iloc[0]
    p2 = master_df.iloc[1]
    from src.dashboard.charts import plot_radar_comparison, plot_sprint_curve_overlay
    fig10 = plot_radar_comparison(p1, p2, master_df)
    assert fig10 is not None

    fig11 = plot_sprint_curve_overlay(p1, p2)
    assert fig11 is not None

    # Test Phase 2 Biomechanical Lab charts
    from src.dashboard.charts import (
        plot_sprint_velocity_interactive,
        plot_acceleration_profile,
        plot_cod_interactive_scatter,
        plot_biomechanical_profile_radar,
        plot_cod_velocity_transitions,
    )
    fig12 = plot_sprint_velocity_interactive(p1)
    assert fig12 is not None

    fig13 = plot_acceleration_profile(p1)
    assert fig13 is not None

    fig14 = plot_cod_interactive_scatter(cod_df, highlight_nfl_id=int(p1["nfl_id"]))
    assert fig14 is not None

    fig15 = plot_biomechanical_profile_radar(p1, master_df)
    assert fig15 is not None

    p1_trials = cod_df[cod_df["nfl_id"] == int(p1["nfl_id"])]
    fig15b = plot_cod_velocity_transitions(p1_trials, str(p1["display_name"]))
    assert fig15b is not None

    from src.dashboard.charts import plot_hero_lime_trend, plot_recent_form_spline, plot_cohort_performance_trend, plot_3d_motion_analysis
    fig16 = plot_hero_lime_trend(master_df)
    assert fig16 is not None

    fig17 = plot_recent_form_spline(master_df)
    assert fig17 is not None

    fig18 = plot_cohort_performance_trend()
    assert fig18 is not None

    fig19 = plot_3d_motion_analysis()
    assert fig19 is not None


def test_views_import():
    """Verify all views import properly without dependency errors."""
    from src.dashboard.views import (
        overview,
        prospect_explorer,
        model_performance,
        athletic_alpha,
        biomechanical_lab,
        comparison_studio,
        methodology,
    )
    assert overview is not None
    assert prospect_explorer is not None
    assert model_performance is not None
    assert athletic_alpha is not None
    assert biomechanical_lab is not None
    assert comparison_studio is not None
    assert methodology is not None


def test_apptest_navigation():
    """Verify Streamlit AppTest runs all 7 dark sports intelligence pages with zero exceptions."""
    from streamlit.testing.v1 import AppTest

    pages = [
        "🏠  Research Overview",
        "🔍  Prospect Explorer",
        "📚  Model Performance",
        "📈  Athletic Alpha",
        "🏃  Biomechanical Lab",
        "👥  Player Comparison",
        "📖  Research Methodology",
    ]

    app_path = (ROOT / "src" / "dashboard" / "app.py").resolve()
    for p in pages:
        at = AppTest.from_file(str(app_path), default_timeout=30)
        at.run()
        at.sidebar.radio[0].set_value(p)
        at.run()
        assert not at.exception, f"Exception on page {p}: {at.exception}"
