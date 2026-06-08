import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_master_data
from utils.constants import FEATURES, FEATURE_NAMES_MAP
from utils.tier_colors import TIER_COLORS
from utils.helpers import get_tier_color, load_css, metric_card, page_hero, render_sidebar, style_plotly

st.set_page_config(page_title="Tier Analysis | DWEI", layout="wide", initial_sidebar_state="expanded")
render_sidebar()
load_css()

df = load_master_data()

page_hero(
    "Tier Analysis",
    "Understand how performance clusters differ, which states dominate each tier, and what feature patterns separate districts.",
    "Cluster interpretation",
)

tiers = sorted([t for t in df['tier'].unique() if pd.notna(t)])
selected_tier = st.selectbox("Select Tier to Analyze", tiers)

tier_data = df[df['tier'] == selected_tier]
other_data = df[df['tier'] != selected_tier]

c1, c2, c3 = st.columns(3)
with c1:
    metric_card("Districts in tier", f"{len(tier_data):,}", selected_tier, "green")
with c2:
    metric_card("Average DWEI", f"{tier_data['DWEI_score'].mean():+.3f}", "Mean residual score", "teal")
with c3:
    metric_card("Share of India", f"{(len(tier_data) / len(df)) * 100:.1f}%", "Within matched sample", "gold")

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("<div class='section-card slide-up'><h3>Tier Profile vs Rest of India</h3>", unsafe_allow_html=True)
    categories = [FEATURE_NAMES_MAP[f] for f in FEATURES]
    tier_avg = [tier_data[f].mean() for f in FEATURES]
    rest_avg = [other_data[f].mean() for f in FEATURES]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=tier_avg, theta=categories, fill='toself', name=selected_tier,
        line_color=get_tier_color(selected_tier)
    ))
    fig.add_trace(go.Scatterpolar(
        r=rest_avg, theta=categories, fill='toself', name='Rest of India',
        line_color='#CCCCCC'
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, gridcolor="#E6EBF1", linecolor="#C9D3DC"),
            angularaxis=dict(gridcolor="#E6EBF1", linecolor="#C9D3DC")
        )
    )
    style_plotly(fig, height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_b:
    st.markdown("<div class='section-card slide-up'><h3>State Distribution in this Tier</h3>", unsafe_allow_html=True)
    state_counts = tier_data['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']
    fig2 = px.bar(state_counts.head(10), x='State', y='Count', color_discrete_sequence=[get_tier_color(selected_tier)])
    fig2.update_traces(marker_line_width=0)
    style_plotly(fig2, height=500)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-card slide-up'><h3>All Tiers Comparison</h3>", unsafe_allow_html=True)
all_tiers_avg = df.groupby('tier')['DWEI_score'].mean().reset_index().sort_values(by='tier')
fig3 = px.bar(all_tiers_avg, x='tier', y='DWEI_score', color='tier', color_discrete_map=TIER_COLORS)
fig3.update_traces(marker_line_width=0)
style_plotly(fig3, height=430)
st.plotly_chart(fig3, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-card slide-up'><h3>Tier Characteristics</h3>", unsafe_allow_html=True)
tier_strengths = []
for f in FEATURES:
    if tier_data[f].mean() > df[f].mean():
        tier_strengths.append(FEATURE_NAMES_MAP[f])
if tier_strengths:
    st.markdown(f"Districts in **{selected_tier}** generally perform **above** the national average in: {', '.join(tier_strengths[:4])}.")
else:
    st.markdown(f"Districts in **{selected_tier}** generally trail the national average across most dimensions.")
st.markdown("</div>", unsafe_allow_html=True)
