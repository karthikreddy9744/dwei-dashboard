import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from utils.constants import PATHS


def _read_table(path, fallback=None):
    try:
        return pd.read_parquet(path)
    except (ImportError, FileNotFoundError):
        if fallback:
            return pd.read_csv(fallback)
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_master_data():
    return _read_table(PATHS["master_data"], "data/master/master_clustered.csv")


@st.cache_data(show_spinner=False)
def load_shap_values():
    return _read_table(PATHS["shap_values"])


@st.cache_data(show_spinner=False)
def load_district_explanations():
    return _read_table(PATHS["district_explanations"], "shap_values/district_explanations.csv")


@st.cache_data(show_spinner=False)
def load_geojson():
    with open(PATHS["geojson"], "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_verified_geodata():
    try:
        return gpd.read_parquet("data/processed/verified_dwei_geodata.parquet")
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_audit_summary():
    try:
        with open("data/validation/map_audit_summary.json", "r") as f:
            return json.load(f)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def get_state_list():
    df = load_master_data()
    return sorted(df['State'].unique().tolist())


@st.cache_data(show_spinner=False)
def get_districts_for_state(state):
    df = load_master_data()
    return sorted(df[df['State'] == state]['District'].unique().tolist())


@st.cache_resource
def load_xgboost_model():
    import joblib
    try:
        return joblib.load(PATHS.get("xgboost_model", "models/xgboost_tier_classifier.pkl"))
    except Exception:
        return None
