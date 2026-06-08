FEATURES = [
    "female_literacy_pct", 
    "scst_pct", 
    "agri_worker_pct", 
    "poverty_log", 
    "night_lights_log", 
    "wage_timeliness_pct", 
    "avg_days_per_hh", 
    "women_pct", 
    "persondays_per_hh"
]

FEATURE_NAMES_MAP = {
    "female_literacy_pct": "Female Literacy (%)",
    "scst_pct": "SC/ST Population (%)",
    "agri_worker_pct": "Agri Workers (%)",
    "poverty_log": "Poverty (Log)",
    "night_lights_log": "Night Lights (Log)",
    "wage_timeliness_pct": "Wage Timeliness (%)",
    "avg_days_per_hh": "Avg Days per HH",
    "women_pct": "Women Participation (%)",
    "persondays_per_hh": "Persondays per HH"
}

PATHS = {
    "master_data": "data/master/master_final.parquet",
    "shap_values": "shap_values/shap_values.parquet",
    "district_explanations": "shap_values/district_explanations.parquet",
    "geojson": "geojson/india_districts_simplified.geojson"
}
