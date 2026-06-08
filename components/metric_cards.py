import streamlit as st

def render_metric(label, value, delta=None):
    st.metric(label=label, value=value, delta=delta)
