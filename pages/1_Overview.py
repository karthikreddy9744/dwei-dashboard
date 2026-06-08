import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import json
from utils.data_loader import load_verified_geodata, load_audit_summary
from utils.tier_colors import TIER_COLORS
from utils.helpers import load_css, metric_card, page_hero, render_sidebar, style_plotly

st.set_page_config(page_title="Overview | DWEI", layout="wide", initial_sidebar_state="expanded")
render_sidebar()
load_css()

page_hero(
    "National DWEI Snapshot",
    "Scan district-level welfare efficiency across India, then move from national tiers into state and district action.",
    "National overview",
)

# Load audit summary and verified data
audit = load_audit_summary()
gdf = load_verified_geodata()

# Display audit summary
if audit:
    with st.expander("Map Audit Summary", expanded=False):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            metric_card("Total Districts", f"{audit.get('total_master_districts', 0):,}", "Master data")
        with col2:
            metric_card("Matched", f"{audit.get('matched', 0):,}", "Successfully geocoded")
        with col3:
            metric_card("Unmatched", f"{audit.get('unmatched', 0):,}", "Need manual review")
        with col4:
            metric_card("Match Rate", f"{audit.get('match_rate', 0):.1f}%", "Geocoding accuracy")

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        status = audit.get('validation_status', 'UNKNOWN')
        status_color = "#10b981" if status == "PASS" else "#f59e0b"
        st.markdown(
            f"<div style='padding: 14px 18px; background: {status_color}20; border-radius: 12px; color: {status_color}; font-size: 0.95rem;'>Validation Status: <strong>{status}</strong></div>",
            unsafe_allow_html=True,
        )

if gdf is None or len(gdf) == 0:
    st.error("Verified geodata not available. Please run the validation script first.")
else:
    tier_text = gdf["tier"].astype(str)

    # Key metrics section
    st.markdown("<div class='section-card slide-up'><h3>Key Metrics</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    # Consistent spacing across sections
    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    with col1:
        metric_card("Matched Districts", f"{len(gdf):,}", "Analytical sample")
    with col2:
        metric_card("Average DWEI", f"{gdf['DWEI_score'].mean():+.2f}", "National residual score")
    with col3:
        metric_card("Tier I Districts", f"{tier_text.str.startswith('Tier I').sum():,}", "High efficiency outliers")
    with col4:
        metric_card("Tier V Districts", f"{tier_text.str.startswith('Tier V').sum():,}", "Priority support group")
    st.markdown("</div>", unsafe_allow_html=True)

    # National map section
    st.markdown("<div class='section-card slide-up'><h3>National Distribution Map</h3>", unsafe_allow_html=True)
    map_mode = st.selectbox(
        "Select map view",
        ["Tier Choropleth", "DWEI Score Choropleth", "Women's Participation", "Avg Days per Household", "Person-Days per Household", "Wage Timeliness"],
        index=0,
    )
    with st.spinner("Rendering national district map..."):
        color_col = 'tier'
        color_map = TIER_COLORS
        color_continuous = None
        range_color = None
        title = "DWEI Tiers Across Indian Districts"

        if map_mode == "DWEI Score Choropleth":
            color_col = 'DWEI_score'
            color_map = None
            color_continuous = 'Teal'
            range_color = [gdf['DWEI_score'].quantile(0.05), gdf['DWEI_score'].quantile(0.95)]
            title = "DWEI Score Across Indian Districts"
        elif map_mode == "Women's Participation":
            color_col = 'women_pct'
            color_map = None
            color_continuous = 'Purples'
            title = "Women's Participation in MGNREGA"
        elif map_mode == "Avg Days per Household":
            color_col = 'avg_days_per_hh'
            color_map = None
            color_continuous = 'Blues'
            title = "Average Work Days per Household"
        elif map_mode == "Person-Days per Household":
            color_col = 'persondays_per_hh'
            color_map = None
            color_continuous = 'Greens'
            title = "Person-Days per Household"
        elif map_mode == "Wage Timeliness":
            color_col = 'wage_timeliness_pct'
            color_map = None
            color_continuous = 'Oranges'
            title = "Wage Timeliness Percentage"

        fig_map = px.choropleth(
            gdf,
            geojson=gdf.__geo_interface__,
            featureidkey="properties.ID_2",
            locations="ID_2",
            color=color_col,
            color_discrete_map=color_map,
            color_continuous_scale=color_continuous,
            range_color=range_color,
            hover_name='District',
            hover_data={
                'ID_2': False,
                'State': True,
                'tier': True,
                'DWEI_score': ':.3f',
                'rank': True,
                'positive_1': True,
                'negative_1': True
            },
            title=title
        )
        style_plotly(fig_map, height=750)
        fig_map.update_geos(fitbounds="locations", visible=False, projection_type="mercator")
        fig_map.update_layout(
            margin={"r": 40, "t": 80, "l": 40, "b": 40},
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                bgcolor="rgba(255,255,255,0.98)",
                bordercolor="#DDE5E8",
                borderwidth=1,
                itemclick="toggleothers",
                itemdoubleclick="toggle"
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Two-column charts section
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("<div class='section-card slide-up'><h3>Tier Distribution</h3>", unsafe_allow_html=True)
        tier_counts = gdf['tier'].value_counts().reset_index()
        tier_counts.columns = ['Tier', 'Count']
        tier_counts = tier_counts.sort_values(by='Tier')
        fig_bar = px.bar(tier_counts, x='Tier', y='Count', color='Tier', color_discrete_map=TIER_COLORS, text='Count')
        fig_bar.update_traces(textposition="outside", marker_line_width=0)
        style_plotly(fig_bar, height=480)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='section-card slide-up'><h3>DWEI Score Distribution</h3>", unsafe_allow_html=True)
        fig_hist = px.histogram(
            gdf,
            x='DWEI_score',
            nbins=46,
            color_discrete_sequence=['#0D7C80'],
            labels={"DWEI_score": "DWEI score"},
        )
        fig_hist.add_vline(x=0, line_dash="dash", line_color="#C88412", annotation_text="Expected performance")
        style_plotly(fig_hist, height=480)
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
