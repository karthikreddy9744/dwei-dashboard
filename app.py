import streamlit as st
from utils.helpers import load_css, metric_card, page_hero, render_sidebar, notify_ready
from utils.data_loader import load_master_data

st.set_page_config(
    page_title="DWEI Dashboard | District Welfare Efficiency Index",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()
load_css()

if "loaded" not in st.session_state:
    notify_ready("DWEI Dashboard Initialized")
    st.session_state["loaded"] = True

page_hero(
    "District Welfare Efficiency Index",
    "A governance-adjusted analytics dashboard that separates structural advantage from actual welfare performance across Indian districts.",
    "DWEI policy command center",
)

df = load_master_data()
ranked = df.assign(Rank=df["DWEI_score"].rank(ascending=False, method="min").astype(int))
tier_text = df["tier"].astype(str)

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("Districts analyzed", f"{len(df):,}", "Matched through LGD bridge", "green")
with col2:
    metric_card("States covered", f"{df['State'].nunique():,}", "National comparison layer", "blue")
with col3:
    metric_card("Average DWEI", f"{df['DWEI_score'].mean():+.2f}", "Residual welfare performance", "teal")
with col4:
    metric_card("Tier V focus", f"{tier_text.str.startswith('Tier V').sum():,}", "Special challenge districts", "red")

st.markdown(
    """
    <div class="section-card slide-up">
        <h3>What this dashboard answers</h3>
        <p>DWEI does not simply ask which districts have the best raw outcomes. It asks which districts outperform or underperform what their baseline structural conditions would predict.</p>
        <div class="pipeline-steps">
            <div class="pipeline-step"><span>01</span><strong>Need Layer</strong><p>Female literacy, SC/ST share, agriculture dependence, poverty, night lights.</p></div>
            <div class="pipeline-step"><span>02</span><strong>Welfare Change</strong><p>NFHS improvements adjusted against district starting conditions.</p></div>
            <div class="pipeline-step"><span>03</span><strong>Policy Insight</strong><p>Tiers, district comparison, and SHAP explanations for action planning.</p></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2)
with c1:
    top = ranked.nsmallest(5, "Rank")[["Rank", "State", "District", "DWEI_score", "tier"]]
    st.markdown("<div class='section-card'><h3>Highest Governance Efficiency</h3>", unsafe_allow_html=True)
    st.dataframe(top, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    focus = ranked.nlargest(5, "Rank")[["Rank", "State", "District", "DWEI_score", "tier"]]
    st.markdown("<div class='section-card'><h3>Priority Review Districts</h3>", unsafe_allow_html=True)
    st.dataframe(focus, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
