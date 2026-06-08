import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_master_data, get_state_list, get_districts_for_state, load_district_explanations
from utils.constants import FEATURES, FEATURE_NAMES_MAP
from utils.helpers import get_tier_color, get_tier_key, load_css, page_hero, render_sidebar, style_plotly

st.set_page_config(page_title="District Explorer | DWEI", layout="wide", initial_sidebar_state="expanded")
render_sidebar()
load_css()

df = load_master_data()
df['Rank'] = df['DWEI_score'].rank(ascending=False, method='min').astype(int)
expl_df = load_district_explanations()

national_avg = df[FEATURES].mean()

page_hero(
    "District Explorer",
    "Open a district profile, compare its baseline conditions to the national average, and read the strongest SHAP-backed drivers.",
    "District deep dive",
)

col_s, col_d = st.columns(2)
with col_s:
    states = get_state_list()
    state = st.selectbox("Select State", states)
with col_d:
    districts = get_districts_for_state(state)
    district = st.selectbox("Select District", districts)

if state and district:
    dist_data = df[(df['State'] == state) & (df['District'] == district)]
    if not dist_data.empty:
        dist_data = dist_data.iloc[0]
        tier = dist_data['tier']
        tier_str = str(tier) if pd.notna(tier) else 'Unknown'
        color = get_tier_color(tier)
        tier_key = get_tier_key(tier)
        
        st.markdown(f"""
        <div class='section-card profile-card fade-in' style='border-left: 6px solid {color};'>
            <div>
                <h2>{district}, {state}</h2>
                <div class='profile-meta'>
                    <span class='tier-badge {tier_key}'>{tier_str}</span>
                    <span class='meta-pill'>Rank {dist_data['Rank']} of {len(df)}</span>
                    <span class='meta-pill'>DWEI {dist_data['DWEI_score']:+.3f}</span>
                </div>
            </div>
            <div class='metric-card metric-teal' style='min-width: 210px; box-shadow: none;'>
                <span>Governance value-add</span>
                <strong>{dist_data['DWEI_score']:+.2f}</strong>
                <small>Actual improvement minus expected improvement</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("<div class='section-card slide-up'><h3>Feature vs National Average</h3>", unsafe_allow_html=True)
            categories = [FEATURE_NAMES_MAP[f] for f in FEATURES]
            dist_vals = [dist_data[f] for f in FEATURES]
            nat_vals = [national_avg[f] for f in FEATURES]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=dist_vals, theta=categories, fill='toself', name='District',
                line_color=color
            ))
            fig.add_trace(go.Scatterpolar(
                r=nat_vals, theta=categories, fill='toself', name='National Average',
                line_color='#666666'
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, gridcolor="#E6EBF1", linecolor="#C9D3DC"),
                    angularaxis=dict(gridcolor="#E6EBF1", linecolor="#C9D3DC")
                ),
                showlegend=True,
            )
            style_plotly(fig, height=520)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='section-card slide-up'><h3>Human Explanation</h3>", unsafe_allow_html=True)
            expl_dist = expl_df[(expl_df['State'] == state) & (expl_df['District'] == district)]
            if not expl_dist.empty:
                expl = expl_dist.iloc[0]
                st.markdown(
                    f"<div class='shap-box shap-strength'><h4>Top Strengths</h4><ul class='insight-list'><li>{expl.get('positive_1', 'N/A')}</li><li>{expl.get('positive_2', 'N/A')}</li><li>{expl.get('positive_3', 'N/A')}</li></ul></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div class='shap-box shap-weakness'><h4>Top Weaknesses</h4><ul class='insight-list'><li>{expl.get('negative_1', 'N/A')}</li><li>{expl.get('negative_2', 'N/A')}</li><li>{expl.get('negative_3', 'N/A')}</li></ul></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.info("No text explanation available for this district.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card slide-up'><h3>Feature Breakdown</h3>", unsafe_allow_html=True)
        table_df = pd.DataFrame({
            "Feature": categories,
            "District Value": dist_vals,
            "National Avg": nat_vals,
            "Difference": [d - n for d, n in zip(dist_vals, nat_vals)]
        })
        st.dataframe(table_df.style.format({
            "District Value": "{:.3f}",
            "National Avg": "{:.3f}",
            "Difference": "{:+.3f}"
        }), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("District data not found.")
