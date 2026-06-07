# DWEI Project Architecture

## Project Overview

The District Welfare Efficiency Index (DWEI) Project is a district-level governance analytics framework designed to evaluate welfare performance relative to structural constraints.

Traditional rankings often reward districts with favorable socioeconomic conditions. The DWEI framework instead attempts to answer:

> Which districts achieve welfare improvements beyond what would normally be expected given their structural conditions?

The project integrates:

- Census / SHRUG socioeconomic indicators
- SECC poverty estimates
- VIIRS Nightlight economic proxies
- MGNREGS implementation indicators
- NFHS welfare outcomes

into a unified analytical pipeline.

The architecture follows a sequential multi-stage workflow where outputs from one stage become inputs for the next stage.

---

# High-Level Pipeline

```text
RAW DATA SOURCES
       │
       ▼
NOTEBOOK 01
Data Cleaning & Feature Engineering
       │
       ▼
INTERIM DATASETS
       │
       ▼
NOTEBOOK 02
District Harmonization & Master Dataset Creation
       |
       |
       V
master_base
       │
       ▼
MASTER DATASET
       │
       ▼
NOTEBOOK 03
DWEI Construction
         
       │
       ▼
 master_mgnregs
       │
       ▼
DWEI DATASET
       │
       ▼
NOTEBOOK 04
Governance Archetype Clustering
       │
       ▼
master_clustered    
       │
       ▼
TIER ASSIGNMENTS
       │
       ▼
NOTEBOOK 05
XGBoost + SHAP Explainability
       │
       ▼
  master_final     
       │
       ▼
FINAL ANALYTICS DATASET
       │
       ▼
STREAMLIT DASHBOARD
```

---

# Project Directory Structure

```text
dwei_project/

├── data/
│
│   ├── raw/
│   ├── interim/
│   ├── master/
│   ├── validation/
│   └── model_outputs/
│
├── notebooks/
│
│   ├── 01_data_cleaning.ipynb
│   ├── 02_lgd_merging.ipynb
│   ├── 03_dwei_score.ipynb
│   ├── 04_clustering.ipynb
│   └── 05_xgboost_shap.ipynb
│
├── models/
│
├── shap_values/
│
├── docs/
│
├── geojson/
│
└── app.py
```

---

# Analytical Framework

The project is built around three conceptual layers.

```text
STRUCTURAL NEED LAYER
       │
       ▼
ADMINISTRATIVE PERFORMANCE LAYER
       │
       ▼
WELFARE OUTCOME LAYER
       │
       ▼
DWEI
```

---

## Structural Need Layer

Represents conditions inherited by district administrations.

Examples:

- Female Literacy
- SC/ST Population Share
- Agricultural Dependence
- Poverty
- Economic Activity

These variables describe the environment within which governance operates.

---

## Administrative Performance Layer

Represents implementation quality.

Examples:

- Wage Timeliness
- Women Participation
- Employment Generation
- Programme Intensity

These variables capture administrative functioning.

---

## Welfare Outcome Layer

Measures observed welfare changes.

Examples:

- Stunting
- Wasting
- Underweight
- Anaemia
- Immunization
- Institutional Delivery
- Sanitation
- Clean Fuel

These represent welfare outcomes experienced by citizens.

---

# NOTEBOOK 01
# Data Cleaning & Feature Engineering

---

## Purpose

Convert raw datasets into district-level analytical features.

This stage standardizes formats, removes inconsistencies, and creates modeling variables.

---

## Input Sources

### NFHS

```text
data/raw/NFHS-4.csv
data/raw/NFHS-5.csv
```

Used for welfare outcomes.

---

### MGNREGS

```text
data/raw/2019-20.csv
data/raw/2020-21.csv
data/raw/2021-22.csv
```

Used for administrative performance indicators.

---

### SHRUG

```text
data/raw/pc11_pca_clean_pc11dist.csv
```

Used for socioeconomic indicators.

---

### SECC

```text
data/raw/secc_cons_rural_pc11dist.csv
```

Used for poverty estimation.

---

### Nightlights

```text
data/raw/viirs_annual_pc11dist.csv
```

Used as economic activity proxy.

---

## Major Operations

### NFHS Cleaning

- Remove metadata rows
- Standardize district names
- Convert indicators to numeric
- Retain district-level observations

---

### MGNREGS Processing

Create:

#### wage_timeliness_pct

Administrative responsiveness.

---

#### avg_days_per_hh

Average employment days generated.

---

#### women_pct

Female participation rate.

---

#### persondays_per_hh

Programme intensity.

---

### Poverty Processing

Generate:

```text
poverty_rate
poverty_log
```

---

### Nightlights Processing

Generate:

```text
night_lights_log
```

---

### SHRUG Processing

Generate:

```text
female_literacy_pct
scst_pct
agri_worker_pct
```

---

## Outputs

```text
data/interim/

├── nfhs4_clean.csv
├── nfhs5_clean.csv
├── mgnregs_features.csv
├── poverty_features.csv
├── nightlight_features.csv
└── shrug_features.csv
```

---

# NOTEBOOK 02
# Geographic Harmonization & Master Dataset Construction

---

## Purpose

All source datasets use different district naming systems.

This notebook creates a unified district geography.

---

## Main Challenge

Different datasets contain:

```text
Mahbubnagar
Mahabub Nagar

Anantapur
Ananthapuramu

Bellary
Ballari
```

and many other variations.

---

## Solution

Use:

```text
LGD District Directory
```

as the canonical district reference.

---

## Inputs

```text
LGD_Master_District Code.xlsx

nfhs4_clean.csv
nfhs5_clean.csv

mgnregs_features.csv
poverty_features.csv
nightlight_features.csv
shrug_features.csv
```

---

## Major Operations

### District Name Standardization

Normalize:

- spelling
- punctuation
- casing

---

### Fuzzy Matching

Resolve district name mismatches.

---

### Manual Validation

Create validation reports.

---

### Master Dataset Creation

Merge all analytical features into a single district-level dataset.

---

## Outputs

```text
data/master/

├── lgd_bridge.csv
├── master_base.csv
└── master_base.parquet
```

---

## Validation Outputs

```text
data/validation/

missingness_report.csv

nfhs_unmatched.csv
mgnregs_unmatched.csv

nfhs_manual_mapping.csv
mgnregs_manual_mapping.csv
```

---

# NOTEBOOK 03
# District Welfare Efficiency Index (DWEI)

---

## Purpose

Construct a welfare efficiency measure that evaluates districts relative to their structural conditions.

---

# Conceptual Logic

Traditional Evaluation:

```text
Outcome
```

DWEI Evaluation:

```text
Observed Outcome
          -
Expected Outcome
```

---

# Step 1
# Welfare Improvement Calculation

Create:

```text
delta_STUNTING
delta_WASTING
delta_UNDERWEIGHT
delta_ANEMIA

delta_IMMUNIZATION
delta_INST_DEL
delta_SANITATION
delta_CLEAN_FUEL
```

representing change between NFHS-4 and NFHS-5.

---

# Step 2
# Expected Outcome Modelling

Use Ridge Regression.

Need variables:

```text
female_literacy_pct
scst_pct
agri_worker_pct
poverty_log
night_lights_log
```

predict expected welfare improvement.

---

# Step 3
# Residual Extraction

```text
Residual
=
Observed
-
Expected
```

---

# Step 4
# Residual Standardization

Convert residuals into:

```text
z_residual_*
```

for comparability.

---

# Step 5
# DWEI Construction

Combine standardized residuals into:

```text
DWEI_score
```

---

## Interpretation

Positive:

```text
Outperformed expectations
```

Negative:

```text
Underperformed expectations
```

---

## Outputs

```text
master_dwei.csv
master_dwei.parquet
```

---

# NOTEBOOK 04
# Governance Archetype Clustering

---

## Purpose

Convert continuous DWEI scores into governance archetypes.

---

# Why Clustering?

DWEI answers:

```text
How efficient?
```

Clustering answers:

```text
What type of district?
```

---

## Models Tested

### Model A

```text
Need Variables
+
Implementation Variables
+
DWEI
```

---

### Model B

```text
Implementation Variables
+
DWEI
```

---

### Model C

Alternative specification.
```
I can continue with **Notebook 04, Notebook 05, model architecture diagrams, file lineage diagrams, tier framework diagrams, and production deployment architecture** in the next part because the full document will be very long (likely 400–500+ lines). This should be pasted first, then I'll give Part 2.



---

## Model Selection

Three clustering configurations were evaluated.

| Model | Features Used | Best k | Best Silhouette |
|---------|---------|---------|---------|
| Model A | Need + Implementation + DWEI | 3 | 0.1868 |
| Model B | Implementation + DWEI | 2 | 0.2592 |
| Model C | Alternative Combination | 3 | 0.2287 |

---

## Why Model B Was Selected

Model B achieved the strongest cluster separation.

Most importantly, Model B demonstrated that:

```text
Implementation variables explain governance archetypes
more clearly than structural variables.
```

This finding became one of the most important discoveries of the project.

---

# Final Clustering Variables

The final clustering model used:

```text
DWEI_score

wage_timeliness_pct
avg_days_per_hh
women_pct
persondays_per_hh
```

---

# Cluster Validation

Hierarchical Clustering was used as an external validation method.

Comparison:

```text
K-Means
vs
Hierarchical Clustering
```

produced:

```text
Adjusted Rand Index (ARI)
≈ 0.41
```

---

## Interpretation

An ARI of approximately 0.41 indicates:

```text
Moderate agreement
```

between two fundamentally different clustering approaches.

This suggests that the clusters capture meaningful structure in the data while acknowledging the complexity of real-world governance systems.

---

# Final Cluster Sizes

| Cluster | District Count |
|----------|----------|
| Cluster 0 | 159 |
| Cluster 1 | 92 |
| Cluster 2 | 198 |
| Cluster 3 | 17 |
| Cluster 4 | 157 |

---

# Cluster Profiles

| Cluster | DWEI | Wage Timeliness | Avg Days | Women % | Persondays |
|-----------|-----------|-----------|-----------|-----------|-----------|
| 0 | -0.417 | 98.72 | 34.24 | 46.42 | 34.74 |
| 1 | -0.117 | 99.36 | 77.32 | 29.33 | 29.82 |
| 2 | 0.198 | 97.86 | 40.58 | 27.31 | 27.80 |
| 3 | -0.340 | 35.11 | 30.21 | 20.24 | 20.62 |
| 4 | 0.279 | 99.74 | 46.79 | 43.08 | 43.58 |

---

# Tier Construction

Clusters were converted into policy-friendly governance archetypes.

Raw cluster IDs were intentionally replaced because:

```text
Cluster 0
Cluster 1
Cluster 2
```

have no policy meaning.

---

## Final Tier Mapping

### Tier I — High Impact Districts

Characteristics:

- Highest DWEI
- Highest programme intensity
- Strong implementation
- Strong welfare efficiency

Cluster:

```text
Cluster 4
```

Districts:

```text
157
```

Average DWEI:

```text
0.279
```

---

### Tier II — Strong Performing Districts

Characteristics:

- Positive welfare efficiency
- Good implementation
- Strong outcomes

Cluster:

```text
Cluster 2
```

Districts:

```text
198
```

Average DWEI:

```text
0.198
```

---

### Tier III — Inclusive Development Districts

Characteristics:

- Extremely high women participation
- Moderate efficiency
- Strong inclusion orientation

Cluster:

```text
Cluster 1
```

Districts:

```text
92
```

Average DWEI:

```text
-0.117
```

Women Participation:

```text
77.32%
```

Highest among all tiers.

---

### Tier IV — Improvement Potential Districts

Characteristics:

- Reasonable implementation indicators
- Negative welfare efficiency
- Untapped administrative potential

Cluster:

```text
Cluster 0
```

Districts:

```text
159
```

Average DWEI:

```text
-0.417
```

---

### Tier V — Special Challenge Districts

Characteristics:

- Severe implementation challenges
- Very low wage timeliness
- Low programme intensity
- Small but distinct group

Cluster:

```text
Cluster 3
```

Districts:

```text
17
```

Average DWEI:

```text
-0.340
```

---

# Tier Framework

```text
Tier I
High Impact Districts
        ▲
        │
Tier II
Strong Performing Districts
        ▲
        │
Tier III
Inclusive Development Districts
        ▲
        │
Tier IV
Improvement Potential Districts
        ▲
        │
Tier V
Special Challenge Districts
```

---

# Outputs

```text
data/master/

master_clustered.csv
master_clustered.parquet

models/

kmeans_tiers.pkl
```

---

# NOTEBOOK 05
# XGBoost Classification & SHAP Explainability

---

## Purpose

Clustering identifies:

```text
WHAT exists
```

XGBoost + SHAP explains:

```text
WHY it exists
```

---

# Conceptual Flow

```text
District Features
        │
        ▼
XGBoost Model
        │
        ▼
Predicted Tier
        │
        ▼
SHAP
        │
        ▼
Feature Contributions
```

---

# Model Inputs

Nine explanatory features were used.

```text
female_literacy_pct
scst_pct
agri_worker_pct
poverty_log
night_lights_log

wage_timeliness_pct
avg_days_per_hh
women_pct
persondays_per_hh
```

---

# Model Target

```text
tier
```

Five-class classification problem.

```text
Tier I
Tier II
Tier III
Tier IV
Tier V
```

---

# Train-Test Pipeline

```text
Master Clustered Dataset
           │
           ▼
Train-Test Split
           │
           ▼
Feature Scaling
           │
           ▼
XGBoost Training
           │
           ▼
Evaluation
           │
           ▼
SHAP Analysis
```

---

# Model Performance

## Accuracy

```text
76%
```

---

## Classification Report

| Tier | Precision | Recall | F1 |
|--------|--------|--------|--------|
| 0 | 0.87 | 0.81 | 0.84 |
| 1 | 0.72 | 0.82 | 0.77 |
| 2 | 0.95 | 1.00 | 0.97 |
| 3 | 0.56 | 0.47 | 0.51 |
| 4 | 1.00 | 1.00 | 1.00 |

---

## Interpretation

Most prediction errors occurred between neighboring governance tiers rather than between extreme tiers.

Example:

```text
Tier III
↔
Tier IV
```

rather than

```text
Tier I
↔
Tier V
```

This indicates that the model successfully learned the overall governance structure.

---

# SHAP Explainability

## Purpose

SHAP decomposes every prediction into feature contributions.

Example:

```text
District
        │
        ▼
Predicted Tier I
        │
        ▼
Which features pushed it there?
```

---

## Global SHAP Importance

| Feature | Mean Absolute SHAP |
|----------|----------|
| women_pct | ~0.83 |
| avg_days_per_hh | ~0.74 |
| persondays_per_hh | ~0.57 |
| wage_timeliness_pct | ~0.54 |
| poverty_log | ~0.17 |
| agri_worker_pct | ~0.14 |
| female_literacy_pct | ~0.13 |
| scst_pct | ~0.12 |
| night_lights_log | ~0.08 |

---

## Most Important Finding

The four strongest predictors were:

```text
women_pct

avg_days_per_hh

persondays_per_hh

wage_timeliness_pct
```

All four originate from:

```text
MGNREGS Implementation Layer
```

This suggests that governance archetypes are differentiated more strongly by implementation characteristics than by structural conditions alone.

---

# Tier-Level SHAP Analysis

SHAP values were aggregated separately for each tier.

This identifies the defining characteristics of each governance archetype.

---

## Tier I

Dominant Drivers:

```text
persondays_per_hh
avg_days_per_hh
women_pct
```

Interpretation:

Strong implementation intensity drives Tier I membership.

---

## Tier II

Dominant Drivers:

```text
avg_days_per_hh
persondays_per_hh
women_pct
```

Interpretation:

Strong but slightly less intensive implementation pattern.

---

## Tier III

Dominant Driver:

```text
women_pct
```

Interpretation:

Inclusion-focused governance pattern.

---

## Tier IV

Characteristics:

```text
Moderate implementation
Negative DWEI
```

Interpretation:

Untapped administrative potential.

---

## Tier V

Characteristics:

```text
Very low wage timeliness
Low programme intensity
```

Interpretation:

Administrative and implementation challenges.

---

# District-Level Explainability

For every district, SHAP explanations were generated.

Outputs include:

```text
Top Positive Drivers

Top Negative Drivers
```

Example:

```text
District:
Alirajpur

Tier:
Tier I

Positive Drivers:
avg_days_per_hh
persondays_per_hh
women_pct

Negative Drivers:
female_literacy_pct
wage_timeliness_pct
scst_pct
```

These explanations support dashboard-level district diagnostics.



---

# Final Production Assets

The project produces a set of finalized analytical assets that can be directly consumed by applications, dashboards, reports, or future analytical pipelines.

These assets represent the end-state outputs of the entire DWEI workflow.

---

# Production Dataset

## master_final.parquet

Location:

```text
data/master/master_final.parquet
```

Purpose:

```text
Single source of truth
for dashboard and deployment.
```

Contains:

- District identifiers
- Structural variables
- Administrative variables
- NFHS indicators
- DWEI score
- Cluster assignments
- Tier assignments

---

## Why This Dataset Exists

Instead of loading:

```text
master_base
master_dwei
master_clustered
```

individually, the dashboard loads one final dataset.

This reduces:

- Complexity
- Memory usage
- Data management overhead

---

# Model Persistence Architecture

All trained machine learning objects are stored separately.

Location:

```text
models/
```

---

## Purpose

Avoid retraining models during dashboard execution.

Without persistence:

```text
Dashboard Start
      │
      ▼
Retrain Model
      │
      ▼
Long Startup Time
```

With persistence:

```text
Dashboard Start
      │
      ▼
Load Saved Model
      │
      ▼
Instant Availability
```

---

# Saved Models

## kmeans_tiers.pkl

Purpose:

Stores final K-Means clustering model.

Used for:

```text
Tier assignment
for future districts.
```

---

## scaler.pkl

Purpose:

Stores feature scaling parameters.

Used for:

```text
Transforming new observations
before XGBoost prediction.
```

---

## tier_label_encoder.pkl

Purpose:

Stores label mapping.

Example:

```text
0 → Tier I
1 → Tier II
2 → Tier III
...
```

---

## xgboost_tier_classifier.pkl

Purpose:

Final trained classifier.

Used for:

```text
Tier prediction
```

and

```text
SHAP explanation generation.
```

---

## xgboost_features.json

Purpose:

Stores feature ordering.

Critical because:

```text
Model expects exact feature order.
```

Example:

```text
women_pct
avg_days_per_hh
...
```

must remain consistent.

---

## model_metadata.json

Purpose:

Stores configuration information.

Examples:

```text
Model Version

Training Date

Feature Count

Hyperparameters
```

---

## model_performance.csv

Purpose:

Stores evaluation metrics.

Examples:

```text
Accuracy

Precision

Recall

F1 Score
```

---

# SHAP Storage Architecture

Location:

```text
shap_values/
```

---

# Why SHAP Is Precomputed

Computing SHAP values for all districts is computationally expensive.

Real-time calculation would:

- Slow dashboard loading
- Increase memory consumption
- Reduce responsiveness

Therefore:

```text
Compute Once
      │
      ▼
Store
      │
      ▼
Reuse
```

---

# shap_values.parquet

Purpose:

Stores SHAP values for all districts.

Contains:

```text
District
Feature
SHAP Contribution
```

for every district-feature combination.

---

## Benefits

Enables:

```text
Instant district explanations
```

without recomputing SHAP.

---

# district_explanations.parquet

Purpose:

Stores human-readable explanation summaries.

Contains:

```text
Top Positive Drivers

Top Negative Drivers
```

for every district.

---

# district_explanations.csv

Purpose:

CSV version for:

- Reporting
- Validation
- Manual inspection

---

# Example Explanation Structure

```text
District:
Alirajpur

Tier:
Tier I

Positive Drivers:

avg_days_per_hh
persondays_per_hh
women_pct

Negative Drivers:

female_literacy_pct
wage_timeliness_pct
scst_pct
```

---

# Complete File Lineage

The entire project can be represented as:

```text
RAW DATA
│
├── NFHS
├── MGNREGS
├── SHRUG
├── SECC
└── Nightlights
│
▼
Notebook 01
│
▼
INTERIM DATASETS
│
├── nfhs4_clean
├── nfhs5_clean
├── mgnregs_features
├── poverty_features
├── nightlight_features
└── shrug_features
│
▼
Notebook 02
│
▼
MASTER BASE
│
▼
Notebook 03
│
▼
MASTER DWEI
│
▼
Notebook 04
│
▼
MASTER CLUSTERED
│
▼
Notebook 05
│
▼
MASTER FINAL
│
├── Models
├── SHAP Values
└── Explanations
│
▼
Dashboard
```

---

# Data Dependency Flow

```text
master_base.parquet
        │
        ▼
master_dwei.parquet
        │
        ▼
master_clustered.parquet
        │
        ▼
master_final.parquet
```

Each stage depends directly on the previous stage.

---

# Analytical Dependency Flow

```text
Need Variables
        │
        ▼
Expected Welfare Improvement
        │
        ▼
Residuals
        │
        ▼
DWEI
        │
        ▼
Clusters
        │
        ▼
Tiers
        │
        ▼
XGBoost
        │
        ▼
SHAP
```

---

# Dashboard Data Architecture

The dashboard should never directly access:

```text
raw/
```

or

```text
interim/
```

datasets.

Instead:

```text
Dashboard
      │
      ▼
master_final.parquet
      │
      ▼
shap_values.parquet
      │
      ▼
district_explanations.parquet
```

This ensures:

- Faster loading
- Cleaner architecture
- Reproducibility

---

# Recommended Dashboard Data Sources

## Core Dataset

```text
data/master/master_final.parquet
```

Used for:

- Search
- Filtering
- Ranking
- Tier display

---

## SHAP Dataset

```text
shap_values/shap_values.parquet
```

Used for:

- Waterfall plots
- SHAP breakdowns

---

## Explanation Dataset

```text
shap_values/district_explanations.parquet
```

Used for:

- District summary cards
- Natural language explanations

---

# Future GeoJSON Layer

Directory:

```text
geojson/
```

Purpose:

Store simplified district boundaries.

Expected file:

```text
india_districts_simplified.geojson
```

---

## Why Simplification Is Necessary

Original district GeoJSONs are often:

```text
20–100 MB
```

and slow to render.

Simplification reduces:

- File size
- Browser load time
- Streamlit rendering time

---

# Future Streamlit Architecture

Proposed structure:

```text
app.py

pages/

├── Overview.py
├── District_Explorer.py
├── Tier_Analysis.py
├── SHAP_Insights.py
├── Map_Explorer.py
└── Methodology.py
```

---

# User Interaction Flow

```text
User Selects District
          │
          ▼
Load District Record
          │
          ▼
Display DWEI
          │
          ▼
Display Tier
          │
          ▼
Display SHAP Explanation
          │
          ▼
Display Comparison
```

---

# Reproducibility Framework

A new researcher should be able to reproduce the project using:

```text
environment.yml

01_data_cleaning.ipynb

02_lgd_merging.ipynb

03_dwei_score.ipynb

04_clustering.ipynb

05_xgboost_shap.ipynb
```

without modifying source code.

This was a core design objective of the project.

---

# Project Completion Status

## Data Engineering

```text
COMPLETE
```

- Data collection
- Cleaning
- Validation
- Harmonization

---

## DWEI Construction

```text
COMPLETE
```

- Outcome modeling
- Residual extraction
- Standardization
- Index creation

---

## Governance Archetypes

```text
COMPLETE
```

- K-Means
- Silhouette analysis
- Hierarchical validation
- Tier creation

---

## Explainable AI

```text
COMPLETE
```

- XGBoost
- Evaluation
- SHAP
- District explanations

---

## Production Assets

```text
COMPLETE
```

- Models saved
- SHAP saved
- Explanations saved
- Final dataset saved

---

## Dashboard Layer

```text
NOT YET STARTED
```

Planned next phase.

---

# Final Architectural Summary

The DWEI project is a multi-stage governance analytics framework that transforms raw administrative and welfare datasets into an explainable district-level efficiency measurement system.

The architecture consists of:

```text
Raw Data
     ↓
Feature Engineering
     ↓
Geographic Harmonization
     ↓
DWEI Construction
     ↓
Governance Archetypes
     ↓
XGBoost Classification
     ↓
SHAP Explainability
     ↓
Production Dataset
     ↓
Interactive Dashboard
```

Each stage produces reusable outputs and preserves full reproducibility, allowing the framework to function as both a research tool and a deployable governance intelligence platform.