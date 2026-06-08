import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_master_data, load_shap_values
from utils.constants import FEATURES, FEATURE_NAMES_MAP
from utils.helpers import load_css, page_hero, render_sidebar, style_plotly
from utils.tier_colors import TIER_COLORS

st.set_page_config(page_title="National Insights | DWEI", layout="wide", initial_sidebar_state="expanded")
render_sidebar()
load_css()

page_hero(
    "National Insights",
    "Explore macro patterns, feature importance, and policy signals behind district welfare efficiency.",
    "Model interpretation",
)

df = load_master_data()
shap_df = load_shap_values()

st.markdown("<div class='section-card slide-up'><h3>Global Feature Importance</h3>", unsafe_allow_html=True)
shap_cols = [c for c in shap_df.columns if c != 'District' and c != 'State' and c != 'tier']
try:
    numeric_shap = shap_df.select_dtypes(include=[np.number])
    mean_shap = numeric_shap.abs().mean().sort_values(ascending=True)
    valid_cols = [c for c in mean_shap.index if c in FEATURES]
    if valid_cols:
        mean_shap = mean_shap[valid_cols]
        labels = [FEATURE_NAMES_MAP.get(c, c) for c in mean_shap.index]
        fig_shap = px.bar(x=mean_shap.values, y=labels, orientation='h', 
                          title='Mean absolute SHAP value',
                          color_discrete_sequence=['#295C8A'])
        fig_shap.update_traces(marker_line_width=0)
        style_plotly(fig_shap, height=430)
        st.plotly_chart(fig_shap, use_container_width=True)
    else:
        st.info("SHAP columns do not exactly match expected features.")
except Exception:
    st.warning("Could not render global SHAP importance.")
st.markdown("</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='section-card slide-up'><h3>Feature Explorer</h3>", unsafe_allow_html=True)
    selected_feature = st.selectbox("Select Feature to analyze", FEATURES, format_func=lambda x: FEATURE_NAMES_MAP[x])
    fig_scatter = px.scatter(df, x=selected_feature, y='DWEI_score', color='tier', 
                             hover_name='District', hover_data=['State'],
                             labels={selected_feature: FEATURE_NAMES_MAP[selected_feature], 'DWEI_score': 'DWEI Score'},
                             title=f"{FEATURE_NAMES_MAP[selected_feature]} vs DWEI Score",
                             color_discrete_map=TIER_COLORS)
    fig_scatter.update_traces(marker=dict(size=8, opacity=0.78, line=dict(width=0)))
    fig_scatter.add_hline(y=0, line_dash="dash", line_color="#C88412")
    style_plotly(fig_scatter, height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section-card slide-up'><h3>Correlation Heatmap</h3>", unsafe_allow_html=True)
    corr_df = df[FEATURES + ['DWEI_score']].corr()
    fig_corr = px.imshow(corr_df, 
                         x=[FEATURE_NAMES_MAP.get(c, c) for c in corr_df.columns],
                         y=[FEATURE_NAMES_MAP.get(c, c) for c in corr_df.columns],
                         color_continuous_scale='RdBu_r',
                         zmin=-1,
                         zmax=1)
    style_plotly(fig_corr, height=500)
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class='section-card slide-up'>
        <h3>Key Governance Insights</h3>
        <div class='shap-box'>
            <ul class='insight-list'>
                <li><strong>Multidimensional welfare:</strong> DWEI reads economic context together with health, infrastructure, and implementation capacity.</li>
                <li><strong>Implementation matters:</strong> MGNREGA indicators such as wage timeliness and persondays help identify districts converting need into support.</li>
                <li><strong>Baseline adjustment changes the story:</strong> High raw welfare is not automatically high efficiency; the index highlights value added after structural conditions are considered.</li>
            </ul>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
