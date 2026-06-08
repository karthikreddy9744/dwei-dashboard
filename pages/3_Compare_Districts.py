import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_master_data, get_state_list, get_districts_for_state, load_district_explanations
from utils.constants import FEATURES, FEATURE_NAMES_MAP
from utils.helpers import get_tier_key, load_css, page_hero, render_sidebar, style_plotly

st.set_page_config(page_title="Compare Districts | DWEI", layout="wide", initial_sidebar_state="expanded")
render_sidebar()
load_css()

page_hero(
    "Compare Districts",
    "Place any two districts side by side to see differences in structural need, implementation indicators, DWEI rank, and explanation drivers.",
    "District comparison",
)

df = load_master_data()
df['Rank'] = df['DWEI_score'].rank(ascending=False, method='min').astype(int)
expl_df = load_district_explanations()

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### District A")
    state_a = st.selectbox("State A", get_state_list(), index=0, key="sa")
    dist_a = st.selectbox("District A", get_districts_for_state(state_a), key="da")

with col_right:
    st.markdown("### District B")
    state_b = st.selectbox("State B", get_state_list(), index=min(1, len(get_state_list())-1), key="sb")
    dist_b = st.selectbox("District B", get_districts_for_state(state_b), key="db")

if state_a and dist_a and state_b and dist_b:
    data_a = df[(df['State'] == state_a) & (df['District'] == dist_a)].iloc[0]
    data_b = df[(df['State'] == state_b) & (df['District'] == dist_b)].iloc[0]

    tier_a = str(data_a['tier']) if pd.notna(data_a['tier']) else 'Unknown'
    tier_b = str(data_b['tier']) if pd.notna(data_b['tier']) else 'Unknown'
    color_a, color_b = '#1f77b4', '#d62728'
    tier_key_a, tier_key_b = get_tier_key(tier_a), get_tier_key(tier_b)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class='section-card slide-up' style='border-left: 6px solid {color_a}'>
            <h3>{dist_a}</h3>
            <div class='profile-meta'>
                <span class='tier-badge {tier_key_a}'>{tier_a}</span>
                <span class='meta-pill'>Rank {data_a['Rank']}</span>
                <span class='meta-pill'>DWEI {data_a['DWEI_score']:+.3f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='section-card slide-up' style='border-left: 6px solid {color_b}'>
            <h3>{dist_b}</h3>
            <div class='profile-meta'>
                <span class='tier-badge {tier_key_b}'>{tier_b}</span>
                <span class='meta-pill'>Rank {data_b['Rank']}</span>
                <span class='meta-pill'>DWEI {data_b['DWEI_score']:+.3f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-card slide-up'><h3>Feature Comparison</h3>", unsafe_allow_html=True)
    categories = [FEATURE_NAMES_MAP[f] for f in FEATURES]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[data_a[f] for f in FEATURES], theta=categories, fill='toself', name=dist_a, line_color=color_a
    ))
    fig.add_trace(go.Scatterpolar(
        r=[data_b[f] for f in FEATURES], theta=categories, fill='toself', name=dist_b, line_color=color_b
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, gridcolor="#E6EBF1", linecolor="#C9D3DC"),
            angularaxis=dict(gridcolor="#E6EBF1", linecolor="#C9D3DC")
        ),
        showlegend=True,
    )
    style_plotly(fig, height=540)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-card slide-up'><h3>Feature Values</h3>", unsafe_allow_html=True)
    comp_df = pd.DataFrame({
        "Feature": categories,
        f"{dist_a} Value": [data_a[f] for f in FEATURES],
        f"{dist_b} Value": [data_b[f] for f in FEATURES],
        "Diff (A - B)": [data_a[f] - data_b[f] for f in FEATURES]
    })
    st.dataframe(comp_df.style.format({
        f"{dist_a} Value": "{:.3f}",
        f"{dist_b} Value": "{:.3f}",
        "Diff (A - B)": "{:+.3f}"
    }), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # SHAP Insights Comparison
    c1, c2 = st.columns(2)
    def render_insights(dist, state):
        expl_dist = expl_df[(expl_df['State'] == state) & (expl_df['District'] == dist)]
        if not expl_dist.empty:
            expl = expl_dist.iloc[0]
            return expl
        return None

    expl_a = render_insights(dist_a, state_a)
    expl_b = render_insights(dist_b, state_b)

    with c1:
        st.markdown(f"<div class='section-card slide-up'><h3>{dist_a} Insights</h3>", unsafe_allow_html=True)
        if expl_a is not None:
            st.markdown(f"<div class='shap-box shap-strength'><h4>Strengths</h4><ul class='insight-list'><li>{expl_a.get('positive_1','')}</li><li>{expl_a.get('positive_2','')}</li><li>{expl_a.get('positive_3','')}</li></ul></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='shap-box shap-weakness'><h4>Weaknesses</h4><ul class='insight-list'><li>{expl_a.get('negative_1','')}</li><li>{expl_a.get('negative_2','')}</li><li>{expl_a.get('negative_3','')}</li></ul></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"<div class='section-card slide-up'><h3>{dist_b} Insights</h3>", unsafe_allow_html=True)
        if expl_b is not None:
            st.markdown(f"<div class='shap-box shap-strength'><h4>Strengths</h4><ul class='insight-list'><li>{expl_b.get('positive_1','')}</li><li>{expl_b.get('positive_2','')}</li><li>{expl_b.get('positive_3','')}</li></ul></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='shap-box shap-weakness'><h4>Weaknesses</h4><ul class='insight-list'><li>{expl_b.get('negative_1','')}</li><li>{expl_b.get('negative_2','')}</li><li>{expl_b.get('negative_3','')}</li></ul></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
