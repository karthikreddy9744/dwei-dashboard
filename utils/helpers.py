import datetime
import streamlit as st


def format_number(num):
    if num >= 1e7:
        return f"{num/1e7:.2f} Cr"
    elif num >= 1e5:
        return f"{num/1e5:.2f} L"
    elif num >= 1e3:
        return f"{num/1e3:.2f} K"
    return f"{num:.2f}"


def get_tier_key(tier_name):
    text = str(tier_name)
    if text.startswith("Tier I -") or text == "Tier I":
        return "tier-1"
    if text.startswith("Tier II"):
        return "tier-2"
    if text.startswith("Tier III"):
        return "tier-3"
    if text.startswith("Tier IV"):
        return "tier-4"
    if text.startswith("Tier V"):
        return "tier-5"
    return "tier-unknown"


def get_tier_color(tier_name):
    from utils.tier_colors import TIER_COLORS
    text = str(tier_name)
    for key, color in TIER_COLORS.items():
        if isinstance(key, str) and (text == key or text.startswith(f"{key} -")):
            return color
    return TIER_COLORS.get(tier_name, "#94A3B8")


def load_css():
    with open("styles/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def page_hero(title, subtitle, eyebrow="District Welfare Efficiency Index"):
    st.markdown(
        f"""
        <section class="dwei-hero">
            <div>
                <span class="hero-eyebrow">{eyebrow}</span>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, caption=None, tone="green"):
    caption_html = f"<small>{caption}</small>" if caption else ""
    tooltip = caption if caption else label
    st.markdown(
        f"""
        <div class="metric-card metric-{tone}" title="{tooltip}">
            <span>{label}</span>
            <strong>{value}</strong>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_plotly(fig, height=None):
    fig.update_layout(
        font=dict(family="Inter, -apple-system, sans-serif", color="#354252", size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=48, b=40, l=10, r=10),
        hoverlabel=dict(
            bgcolor="rgba(16, 32, 51, 0.95)",
            font_color="white",
            bordercolor="rgba(255,255,255,0.1)",
            font_family="Inter, sans-serif"
        ),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(221, 229, 232, 0.5)", zeroline=False, automargin=True)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(221, 229, 232, 0.5)", zeroline=False, automargin=True)
    if height:
        fig.update_layout(height=height)
    return fig

def notify_ready(message="Data loaded successfully."):
    st.toast(message, icon="✅")


def render_sidebar():
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-mark">D</div>
            <div>
                <strong>DWEI Dashboard</strong>
                <span>Governance-adjusted welfare analytics</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        from utils.data_loader import load_master_data
        df = load_master_data()
        st.sidebar.markdown(
            f"""
            <div class="sidebar-stat">
                <span>District coverage</span>
                <strong>{len(df)}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        pass

    st.sidebar.markdown(
        """
        <div class="sidebar-source">
            <strong>Data sources</strong>
            <span>NFHS-4 and NFHS-5</span>
            <span>SECC and Census 2011</span>
            <span>MGNREGA, VIIRS, LGD bridge</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.caption(f"Loaded: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
