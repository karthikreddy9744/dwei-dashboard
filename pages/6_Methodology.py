import streamlit as st
from utils.helpers import load_css, page_hero, render_sidebar

st.set_page_config(page_title="Methodology | DWEI", layout="wide", initial_sidebar_state="expanded")
render_sidebar()
load_css()

page_hero(
    "Methodology",
    "Transparent documentation of the data sources, LGD merge, DWEI residualization, clustering, and explainability layer.",
    "Research pipeline",
)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        <div class='section-card slide-up'>
            <h3>Data Sources</h3>
            <div class='pipeline-steps'>
                <div class='pipeline-step'><span>NFHS</span><strong>NFHS-4 and NFHS-5</strong><p>Health, nutrition, sanitation, clean fuel, immunization, and institutional delivery changes.</p></div>
                <div class='pipeline-step'><span>Baseline</span><strong>SECC and Census 2011</strong><p>District need layer: literacy, social composition, agriculture dependence, and poverty.</p></div>
                <div class='pipeline-step'><span>Implementation</span><strong>MGNREGA and VIIRS</strong><p>Wage timeliness, women participation, persondays, and night-light economic proxy.</p></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='section-card slide-up'>
            <h3>Pipeline & Architecture</h3>
            <div class='pipeline-steps'>
                <div class='pipeline-step'><span>01</span><strong>Clean and Bridge</strong><p>Normalize source data, handle missing values, and align districts through LGD mapping.</p></div>
                <div class='pipeline-step'><span>02</span><strong>Estimate Expected Welfare</strong><p>Use baseline structural conditions to model expected NFHS improvement.</p></div>
                <div class='pipeline-step'><span>03</span><strong>Create DWEI</strong><p>Average standardized residuals: actual improvement minus expected improvement.</p></div>
                <div class='pipeline-step'><span>04</span><strong>Cluster Tiers</strong><p>K-Means creates five policy tiers from district efficiency patterns.</p></div>
                <div class='pipeline-step'><span>05</span><strong>Classify Tiers</strong><p>XGBoost learns non-linear boundaries among the tier groups.</p></div>
                <div class='pipeline-step'><span>06</span><strong>Explain Locally</strong><p>SHAP surfaces district-specific drivers and drags for policy review.</p></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown("<div class='section-card slide-up'><h3>Limitations</h3>", unsafe_allow_html=True)
    st.markdown("""
    - **Temporal Mismatch:** Census 2011 data acts as a baseline, but some ground realities may have shifted.
    - **Data Granularity:** Aggregated to district level; intra-district variance is hidden.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card slide-up'><h3>Future Scope</h3>", unsafe_allow_html=True)
    st.markdown("""
    - **Block-Level Analytics:** Expanding bridging to sub-district levels.
    - **Time-Series SHAP:** Tracking how explanation drivers change year-over-year.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-card slide-up'><h3>DWEI & Modeling Details</h3>", unsafe_allow_html=True)
st.info("""
**DWEI Generation:** Created by residualizing welfare improvements against baseline socio-economic structures, generating a "Value Add" concept for governance.

**K-Means Tiers:** 
- Tier I: High Performance
- Tier V: Special Challenge Districts

**XGBoost & SHAP:** An XGBoost classifier learns the tier assignment boundaries. TreeSHAP provides exact, additive feature attributions to explain *why* any single district fell into its respective tier.
""")
st.markdown("</div>", unsafe_allow_html=True)
