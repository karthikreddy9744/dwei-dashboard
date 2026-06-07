**ANURAG UNIVERSITY**

School of Engineering --- Department of AI & ML

**DISTRICT WELFARE EFFICIENCY INDEX**

**(DWEI)**

A Multi-Indicator Machine Learning Framework for

Governance-Adjusted Welfare Performance Analysis Across Indian Districts

  ---------------------- ------------------------------------------------
  **Branch**             B.Tech Artificial Intelligence & Machine
                         Learning

  **Program**            Mini Project --- 2 Credits

  **Year / Semester**    IV Year --- I Semester (4-1)

  **Evaluation**         Seminar & Viva-Voce --- First Week of July 2026

  **University**         Anurag University, Venkatapur, Ghatkesar,
                         Telangana
  ---------------------- ------------------------------------------------

Version 3.0 --- Fully Updated to Actual Downloaded Datasets

**SECTION 1 --- PROJECT IDENTITY**

**1.1 Full Project Title**

  -----------------------------------------------------------------------
  **District Welfare Efficiency Index (DWEI): A Multi-Indicator Machine
  Learning Framework for Governance-Adjusted Welfare Performance Analysis
  Across Indian Districts**

  -----------------------------------------------------------------------

**1.2 Core Problem Statement**

Most government ranking systems measure raw welfare outcomes without
accounting for structural conditions each district starts with. A
wealthy, well-connected, high-literacy district will always rank higher
than a poor tribal district regardless of how well the latter is
actually governed.

  -----------------------------------------------------------------------
  KEY INSIGHT: DWEI asks not \'which districts have the best outcomes?\'
  but \'which districts perform better than their structural conditions
  would predict?\' This separates genuine governance performance from
  inherited structural advantage.

  -----------------------------------------------------------------------

**1.3 Central Mathematical Idea**

+-----------------------------------------------------------------------+
| **DWEI Score = Actual Welfare Improvement − Expected Improvement      |
| (given baseline structural conditions)**                              |
|                                                                       |
| Positive → Outperformed structural expectation → High Governance      |
| Efficiency                                                            |
|                                                                       |
| Negative → Underperformed structural expectation → Low Governance     |
| Efficiency                                                            |
+-----------------------------------------------------------------------+

**1.4 Full Pipeline --- Your Actual Files (Visual Overview)**

Everything below flows from the 19 files you have downloaded. Yellow
files = NOT used. Green files = core pipeline.

+-----------------------------------------------------------------------+
| ┌─────────                                                            |
| ────────────────────────────────────────────────────────────────────┐ |
|                                                                       |
| │ YOUR 19 DOWNLOADED FILES --- DATA ARCHITECTURE │                    |
|                                                                       |
| ├─────────                                                            |
| ──────────┬─────────────────────────┬───────────────────────────────┤ |
|                                                                       |
| │ SHRUG (6 files) │ NFHS (2 files) │ MGNREGS (USE ONLY 3 files) │     |
|                                                                       |
| │ │ │ │                                                               |
|                                                                       |
| │ pc11_pca\_\...csv │ NFHS-4.csv │ ✅ 2019-20.csv │                   |
|                                                                       |
| │ secc_rural .csv │ → Filter Residence │ ✅ 2020-21.csv │             |
|                                                                       |
| │ secc_urban .csv │ Type == Total only │ ✅ 2021-22.csv │             |
|                                                                       |
| │ viirs_ann .csv │ NFHS-5.csv │ │                                     |
|                                                                       |
| │ shrid_key .csv │ → No filter needed │ ❌ 2018-19 (51% valid only) │ |
|                                                                       |
| │ shrid_loc .csv │ │ ❌ 2022-23+ (post NFHS-5) │                      |
|                                                                       |
| │ │ 7 matching indicators │ ❌ 2024-25/25-26 (GP-level) │             |
|                                                                       |
| │ LGD_Master .xlsx │ (exact col names used) │ ❌ 2026-27 (1 month     |
| only) │                                                               |
|                                                                       |
| │ india_dist .geo │ │ │                                               |
|                                                                       |
| └────────┬                                                            |
| ──────────┴───────────┬─────────────┴──────────────┬────────────────┘ |
|                                                                       |
| │ │ │                                                                 |
|                                                                       |
| ▼ ▼ ▼                                                                 |
|                                                                       |
| ┌─────────────────┐ ┌──────────────────────┐                          |
| ┌────────────────────────────┐                                        |
|                                                                       |
| │ NEED LAYER │ │ OUTCOME DELTAS │ │ IMPLEMENTATION LAYER │            |
|                                                                       |
| │ 5 features │ │ 7 indicators │ │ 4 indicators │                      |
|                                                                       |
| │ │ │ NFHS-5 minus NFHS-4 │ │ Avg across 3 years │                    |
|                                                                       |
| │ female_lit_pct │ │ (sign-flipped for │ │ │                          |
|                                                                       |
| │ scst_pct │ │ decrease=improve) │ │ wage_timeliness_pct │            |
|                                                                       |
| │ agri_worker_pct │ │ │ │ (capped at 100) │                           |
|                                                                       |
| │ poverty_log │ │ STUNTING WASTING │ │ persondays_per_hh │            |
|                                                                       |
| │ night_lights_log│ │ UNDERWEIGHT ANEMIA │ │ women_persondays_pct │   |
|                                                                       |
| └───────┬─────────┘ │ INST_DEL SANITATION │ │ avg_days_per_hh │       |
|                                                                       |
| │ │ CLEAN_FUEL IMMUNIZ │ └─────────────┬──────────────┘               |
|                                                                       |
| └────────────┴──────────────────────┴────────────────┘                |
|                                                                       |
| │                                                                     |
|                                                                       |
| ▼                                                                     |
|                                                                       |
| ┌─────────                                                            |
| ────────────────────────────────────────────────────────────────────┐ |
|                                                                       |
| │ LGD BRIDGE: Census 2011 Code = pc11_district_id (SHRUG ↔ LGD ↔      |
| MGNREGS) │                                                            |
|                                                                       |
| │ Three-way merge → master.parquet (22 cols, \~580-620 matched        |
| districts) │                                                          |
|                                                                       |
| └─────────                                                            |
| ──────────────────────┬─────────────────────────────────────────────┘ |
|                                                                       |
| ▼                                                                     |
|                                                                       |
| ┌─────────                                                            |
| ────────────────────────────────────────────────────────────────────┐ |
|                                                                       |
| │ STAGE 1 --- RIDGE REGRESSION (8 separate models, one per outcome    |
| delta) │                                                              |
|                                                                       |
| │ Input: 5 Need features → Predict expected improvement → DWEI        |
| residual │                                                            |
|                                                                       |
| │ DWEI Score = mean of 8 standardised residuals per district │        |
|                                                                       |
| └─────────                                                            |
| ──────────────────────┬─────────────────────────────────────────────┘ |
|                                                                       |
| ▼                                                                     |
|                                                                       |
| ┌─────────                                                            |
| ────────────────────────────────────────────────────────────────────┐ |
|                                                                       |
| │ STAGE 2 --- KMeans CLUSTERING (k=4 to 6, Silhouette + Hierarchical  |
| valid) │                                                              |
|                                                                       |
| │ 5 Performance Tiers assigned to all \~600 matched districts │       |
|                                                                       |
| └─────────                                                            |
| ──────────────────────┬─────────────────────────────────────────────┘ |
|                                                                       |
| ▼                                                                     |
|                                                                       |
| ┌─────────                                                            |
| ────────────────────────────────────────────────────────────────────┐ |
|                                                                       |
| │ STAGE 3 --- XGBoost + SHAP: WHY districts belong to each tier │     |
|                                                                       |
| │ Global policy finding + per-district explanation cards │            |
|                                                                       |
| └─────────                                                            |
| ──────────────────────┬─────────────────────────────────────────────┘ |
|                                                                       |
| ▼                                                                     |
|                                                                       |
| ┌─────────                                                            |
| ────────────────────────────────────────────────────────────────────┐ |
|                                                                       |
| │ STREAMLIT DASHBOARD --- 5 pages, animated, fast-loading             |
| (Parquet+Cache) │                                                     |
|                                                                       |
| │ Map ▪ Explorer ▪ Rankings ▪ Cluster Analysis ▪ Insights │           |
|                                                                       |
| └─────────                                                            |
| ────────────────────────────────────────────────────────────────────┘ |
+-----------------------------------------------------------------------+

**1.5 Who Will Use DWEI**

  ---------------- ------------------------------------------------------
  **User**         **Use Case**

  **District       Search own district → identify which factor drags
  Collector**      performance → compare with similar-condition districts
                   that perform better

  **State          Compare all districts within state → identify Tier 1
  Government**     best practices → direct extra support to Tier 5
                   districts

  **Policy         Study governance patterns nationally → identify which
  Researchers**    administrative variables most predict welfare delivery
                   success

  **NITI Aayog /   Efficiency-adjusted complement to existing SDG
  MoRD**           District Index --- next-generation ranking methodology

  **Students &     Applied governance analytics and development economics
  Academics**      with real Government of India data

  **Citizens**     Understand how their district performs relative to its
                   structural potential --- not just raw numbers
  ---------------- ------------------------------------------------------

**1.6 Variable Selection Philosophy --- Three-Category Structure**

Every variable belongs to one of three categories. This maps directly to
the three ML stages.

  ------------------ ----------------------- -------------------------------
  **Category**       **Variables**           **Criterion + ML Stage**

  **Structural       female_literacy_pct,    Pre-existing conditions that
  Conditions**       scst_pct,               make welfare delivery easier or
                     agri_worker_pct,        harder --- independent of
                     poverty_log,            government action. → Ridge
                     night_lights_log        input (Stage 1)

  **Administrative   wage_timeliness_pct,    Direct measures of government
  Capacity**         persondays_per_hh,      execution quality --- not
                     women_persondays_pct,   budget or policy design. →
                     avg_days_per_hh         XGBoost + SHAP explanatory
                                             features (Stage 3)

  **Welfare          8 NFHS delta            NFHS-4 to NFHS-5 improvements
  Outcomes**         indicators: STUNTING,   measured over 5 years of scheme
                     WASTING, UNDERWEIGHT,   implementation. → DWEI residual
                     ANEMIA, IMMUNIZATION,   computation (Stage 1 target)
                     INST_DEL, SANITATION,   
                     CLEAN_FUEL              
  ------------------ ----------------------- -------------------------------

**SECTION 2 --- COMPLETE TECHNOLOGY STACK**

All free, open-source, no GPU required. Runs on a standard laptop.

**2.1 Core Language & Environment**

  --------------- ------------- --------------------- -------------------------
  **Tool**        **Version**   **Purpose**           **Why This Exact Choice**

  **Python**      3.11.x        Core language         Most stable. All
                                                      libraries fully support
                                                      3.11. Avoid 3.12 --- SHAP
                                                      0.45 has issues.

  **Anaconda**    Latest        Environment           conda env prevents
                                management            dependency conflicts
                                                      between SHAP, XGBoost,
                                                      geopandas.

  **Jupyter       7.x           EDA + model dev, one  5 notebooks --- one per
  Notebook**                    per stage             stage --- clean
                                                      separation of work

  **VS Code**     Latest        app.py development    Streamlit live-reload
                                                      extension + Python
                                                      debugger

  **Git +         Latest        Version control       Required for Streamlit
  GitHub**                                            Cloud free 1-click
                                                      deployment
  --------------- ------------- --------------------- -------------------------

**2.2 Data Processing Layer**

  ------------------------ ------------- ------------------------------- ----------------------
  **Library**              **Version**   **Purpose**                     **Critical Note**

  **pandas**               2.2.x         Load, merge, clean all CSVs and Use 2.x --- Arrow
                                         Excel                           backend is 3× faster.
                                                                         Required for .parquet.

  **numpy**                1.26.x        Log transforms, numerical ops   1.26 most stable with
                                                                         scikit-learn 1.4 and
                                                                         SHAP 0.45

  **openpyxl**             3.1.x         Read                            Required by pandas for
                                         LGD_Master_District_Code.xlsx   .xlsx. Load with
                                                                         header=1 for LGD file.

  **pyarrow**              15.x          Save master.parquet (snappy     50MB CSV → 5MB
                                         compression)                    Parquet. Loads in
                                                                         \<100ms. Most
                                                                         impactful speed fix.

  **fuzzywuzzy**           0.18.x        District name fuzzy matching    Also install
                                         across files                    python-Levenshtein for
                                                                         4--10× speedup.
                                                                         Threshold: 85.

  **python-Levenshtein**   0.21.x        Speeds up fuzzywuzzy            Without this, fuzzy
                                                                         matching 640 districts
                                                                         takes minutes not
                                                                         seconds.
  ------------------------ ------------- ------------------------------- ----------------------

**2.3 Machine Learning Layer**

  ------------------ ------------- ---------------------- ----------------------
  **Library**        **Version**   **Purpose**            **Role in DWEI**

  **scikit-learn**   1.4.x         Ridge, KMeans,         Stages 1 and 2
                                   StandardScaler,        entirely
                                   metrics                

  **xgboost**        2.0.x         Multi-class tier       Stage 3 --- learns
                                   classification         what distinguishes
                                                          tiers

  **shap**           0.45.x        Global + local         Most critical output
                                   explainability         --- global finding +
                                                          per-district cards

  **scipy**          1.12.x        Hierarchical           Ward linkage
                                   clustering validation  dendrogram ---
                                                          validates KMeans
                                                          clusters

  **statsmodels**    0.14.x        Residual diagnostics   Validates Ridge
                                                          residuals before using
                                                          as DWEI proxies

  **joblib**         1.3.x         Save/load model pkl    joblib.dump /
                                   files                  joblib.load for all 4
                                                          model files
  ------------------ ------------- ---------------------- ----------------------

**2.4 Visualization & Dashboard Layer**

  --------------------------- ------------- -------------------------------------------
  **Tool**                    **Version**   **Purpose + Key Note**

  **plotly + plotly-express** 5.20.x        All interactive charts --- choropleth,
                                            radar, bar, scatter, histogram.
                                            px.choropleth_mapbox, px.scatter with
                                            trendline=\'ols\'.

  **matplotlib**              3.8.x         SHAP waterfall and summary plots (SHAP
                                            library renders via matplotlib backend
                                            only)

  **seaborn**                 0.13.x        Correlation heatmaps and EDA plots in
                                            Jupyter notebooks only --- NOT in dashboard

  **streamlit**               1.32.x        Main dashboard --- zero HTML/JS, native
                                            Plotly, free Streamlit Cloud deployment

  **streamlit-extras**        0.4.x         Metric cards, colored badges for Overview
                                            page (total districts, avg DWEI, tier
                                            counts)

  **streamlit-option-menu**   0.3.x         Animated sidebar navigation icons for all 5
                                            pages

  **streamlit-aggrid**        0.3.x         Interactive sortable/filterable rankings
                                            table --- handles 620 rows smoothly

  **geopandas**               0.14.x        Merge simplified GeoJSON with DWEI district
                                            scores for choropleth
  --------------------------- ------------- -------------------------------------------

  -----------------------------------------------------------------------
  GEOJSON MANDATORY ACTION: Your india_district.geojson is 33MB. This
  causes 35+ second map render. You MUST simplify it using mapshaper.org
  BEFORE any dashboard testing. Upload → Visvalingam method → 25%
  simplification → Export as GeoJSON → Save as
  india_districts_simplified.geojson (\~3MB). Map then loads in under 2
  seconds.

  -----------------------------------------------------------------------

**2.5 Complete requirements.txt --- All Pinned Versions**

+-----------------------------------------------------------------------+
| pandas==2.2.2 numpy==1.26.4 openpyxl==3.1.2                           |
|                                                                       |
| pyarrow==15.0.2 fuzzywuzzy==0.18.0 python-Levenshtein==0.21.0         |
|                                                                       |
| scikit-learn==1.4.2 xgboost==2.0.3 shap==0.45.0                       |
|                                                                       |
| scipy==1.12.0 statsmodels==0.14.1 joblib==1.3.2                       |
|                                                                       |
| plotly==5.20.0 matplotlib==3.8.4 seaborn==0.13.2                      |
|                                                                       |
| streamlit==1.32.2 streamlit-extras==0.4.3                             |
| streamlit-option-menu==0.3.6                                          |
|                                                                       |
| streamlit-aggrid==0.3.4 geopandas==0.14.3 shapely==2.0.3              |
+-----------------------------------------------------------------------+

**SECTION 3 --- ALL 19 DOWNLOADED FILES --- DETAILED SPECIFICATION**

  -----------------------------------------------------------------------
  This section documents every one of your 19 downloaded files: its exact
  structure, which columns to use, how to compute derived features, and
  where it fits in the pipeline. Files marked ❌ are NOT used in DWEI but
  are documented for clarity.

  -----------------------------------------------------------------------

**3.1 MGNREGS Files --- 9 Files, 3 Used, 6 Excluded**

You downloaded 9 yearly MGNREGS files: 2018-19 through 2026-27. Here is
the exact decision for each file with data-driven justification.

**MGNREGS Year Selection Decision Table**

  ------------- ---------- --------------- -------------- -------------- --------------------------
  **File**      **Rows**   **Districts**   **Valid Tl%**  **Decision**   **Reason**

  2018-19.csv   8,016      668             **51%**        **❌ EXCLUDE** Only 51% of timeliness
                                                                         values are valid (50--110
                                                                         range). Too noisy to use
                                                                         as governance proxy. Also
                                                                         pre-dates NFHS-5 survey
                                                                         period by 1 year.

  2019-20.csv   8,052      671             **77%**        **✅ USE**     77% valid timeliness.
                                                                         First year of NFHS-5
                                                                         survey period (2019-21).
                                                                         District-level monthly
                                                                         data (8,052 rows = 671
                                                                         districts × 12 months).

  2020-21.csv   8,544      712             **86%**        **✅ USE**     86% valid timeliness. Core
                                                                         NFHS-5 survey year.
                                                                         Highest MGNREGS activity
                                                                         due to COVID reverse
                                                                         migration. Best quality of
                                                                         the three.

  2021-22.csv   8,592      716             **89%**        **✅ USE**     89% valid timeliness ---
                                                                         best quality of all
                                                                         compatible files. Final
                                                                         year of NFHS-5 data
                                                                         collection. Represents
                                                                         governance quality that
                                                                         produced NFHS-5 outcomes.

  2022-23.csv   8,808      734             **78%**        **❌ EXCLUDE** Post NFHS-5 period. NFHS-5
                                                                         outcomes were already
                                                                         measured by 2021. Using
                                                                         2022-23 data to explain
                                                                         2019-21 outcomes creates
                                                                         temporal mismatch.

  2023-24.csv   8,880      740             **87%**        **❌ EXCLUDE** Post NFHS-5. Same temporal
                                                                         mismatch issue. Good
                                                                         quality but wrong time
                                                                         period.

  2024-25.csv   186,996    741             **GP-level**   **❌ EXCLUDE** CRITICAL: 186,996 rows vs
                                                                         8,000 for other years =
                                                                         \~21-25 entries per
                                                                         district per month. This
                                                                         file is GP/Panchayat-level
                                                                         data, NOT district-level.
                                                                         Incompatible granularity.

  2025-26.csv   167,094    754             **GP-level**   **❌ EXCLUDE** Same as 2024-25 ---
                                                                         GP/Panchayat-level
                                                                         granularity (167k rows).
                                                                         Not district-level. Cannot
                                                                         aggregate reliably to
                                                                         district without
                                                                         block-level keys.

  2026-27.csv   10,851     743             **1 month**    **❌ EXCLUDE** Only April data (1 month).
                                                                         Incomplete year. Cannot
                                                                         compute annual aggregates.
  ------------- ---------- --------------- -------------- -------------- --------------------------

  -----------------------------------------------------------------------
  **FINAL MGNREGS DECISION: Use ONLY 2019-20.csv, 2020-21.csv, and
  2021-22.csv. These 3 years: (1) align temporally with the NFHS-5 survey
  period, (2) are all district-level monthly data (\~8,000-8,600 rows
  each), (3) have the best data quality (77-89% valid timeliness values),
  and (4) represent the governance quality that actually produced the
  welfare outcomes measured in NFHS-5.**

  -----------------------------------------------------------------------

**MGNREGS --- All 36 Columns (Same Structure Across All Compatible
Files)**

  -------- --------------------------------------------------- ----------------- ------------------------
  **\#**   **Exact Column Name**                               **Use in DWEI**   **Aggregation Method**

  1        fin_year                                            Filter key        e.g. \'2019-2020\' ---
                                                                                 use to confirm correct
                                                                                 file

  2        month                                               Group by          12 months per district

  3        state_code                                          Join key          LGD state code --- use
                                                                                 for LGD bridge merge

  4        state_name                                          Join key          UPPERCASE in MGNREGS ---
                                                                                 standardize for matching

  5        district_code                                       **PRIMARY JOIN    = LGD District Code. Use
                                                               KEY**             for direct merge with
                                                                                 LGD bridge.

  6        district_name                                       Join key (backup) Fuzzy match fallback if
                                                                                 district_code join fails

  7        Average_days_of_employment_provided_per_Household   ✅ EXTRACT ---    MEAN across 12 months
                                                               avg_days_per_hh   per district per year,
                                                                                 then MEAN across 3 years

  8        Persondays_of_Central_Liability_so_far              ✅ EXTRACT ---    MAX across 12 months
                                                               for persondays    (cumulative) = annual
                                                               calc              total

  9        Women_Persondays                                    ✅ EXTRACT ---    MAX across 12 months
                                                               for women pct     (cumulative) = annual
                                                               calc              total

  10       percentage_payments_gererated_within_15_days        ✅ EXTRACT ---    MEDIAN across 12 months
                                                               wage_timeliness   per district. Then cap
                                                                                 at 100. Then MEAN across
                                                                                 3 years. NOTE TYPO:
                                                                                 \'gererated\' not
                                                                                 \'generated\'.

  11       Total_Households_Worked                             Reference only    Can be used as sanity
                                                                                 check for persondays/HH

  12--36   SC_persondays, ST_persondays,                       Not used in DWEI  Available for future
           Number_of_Completed_Works, etc.                                       extension
  -------- --------------------------------------------------- ----------------- ------------------------

  -----------------------------------------------------------------------
  TIMELINESS COLUMN TYPO --- CRITICAL: The column is named
  \'percentage_payments_gererated_within_15_days\' (misspelling:
  \'gererated\' not \'generated\'). This exact misspelling exists in ALL
  9 MGNREGS files. Copy this name exactly in all your pandas code. Values
  range from 0 to 650,562 --- after taking median across months,
  legitimate values are 85--115. Cap at 100.

  -----------------------------------------------------------------------

**Derived MGNREGS Features --- Computation Steps**

  -------- -------------------------- --------------------------------------------------------- --------------------------
  **\#**   **Feature Name**           **Computation Formula**                                   **Expected Range**

  1        **wage_timeliness_pct**    Step1:                                                    0--100. Districts above 90
                                      median(percentage_payments_gererated_within_15_days) per  have strong administrative
                                      district per year. Step2: min(result, 100). Step3: mean   machinery. Below 50
                                      across 3 years.                                           signals broken payment
                                                                                                infrastructure.

  2        **persondays_per_hh**      Step1: max(Persondays_of_Central_Liability_so_far) per    5--80 days per household.
                                      district per year. Step2: divide by rural_households      Below 20 = low scheme
                                      (pc11_pca_no_hh × agri_worker_pct/100). Step3: mean       penetration. Above 50 =
                                      across 3 years.                                           high reach.

  3        **women_persondays_pct**   Step1: max(Women_Persondays) /                            30--70%. Below 30 suggests
                                      max(Persondays_of_Central_Liability_so_far) × 100 per     women excluded from
                                      district per year. Step2: mean across 3 years.            scheme. MGNREGS mandates
                                                                                                33% minimum.

  4        **avg_days_per_hh**        mean(Average_days_of_employment_provided_per_Household)   10--50 days. Direct
                                      across 12 months per district per year. Then mean across  measure of employment
                                      3 years.                                                  intensity. Already
                                                                                                computed in source --- no
                                                                                                additional calculation.
  -------- -------------------------- --------------------------------------------------------- --------------------------

**3.2 NFHS Files --- NFHS-4.csv and NFHS-5.csv**

  --------------------- -------------------------------------------------
  **NFHS-4.csv**        1.2 MB \| 1,911 rows × 98 columns \| 637
                        districts AFTER filtering Residence Type ==
                        \'Total\'

  **NFHS-5.csv**        361 KB \| 701 rows × 108 columns \| No filter
                        needed --- already district-level totals

  **NFHS-4 filter**     CRITICAL: NFHS-4 has 3 rows per district (Rural,
                        Urban, Total). You MUST filter: df4 =
                        df4\[df4\[\'Residence Type\'\]==\'Total\'\]
                        before any use.

  **NFHS-5 structure**  No \'Residence Type\' column --- all rows are
                        totals. Has \'Year\' column with survey year
                        string.

  **Join key**          Both have: State + District columns. Merge on
                        these after name standardization.
  --------------------- -------------------------------------------------

  -----------------------------------------------------------------------
  NFHS-4 FILTER IS MANDATORY: Without filtering to \'Total\' rows only,
  you will compute deltas using Rural or Urban values instead of district
  totals, producing completely wrong DWEI scores. Always verify:
  len(nfhs4\[nfhs4\[\'Residence Type\'\]==\'Total\'\]) should be 637.

  -----------------------------------------------------------------------

**Outcome Indicators --- Exact Column Names in Both Files**

These 8 indicators have CONFIRMED matching column names across NFHS-4
and NFHS-5 (verified from your actual files). Use these exact names
verbatim in code.

  -------- ------------------ --------------------------------- ------------------- ------------
  **\#**   **Short Name**     **Exact Column Name (Identical in **Sign Convention** **Layer**
                              Both NFHS-4 and NFHS-5)**                             

  1        **STUNTING**       Children Under 5 Years Who Are    **FLIP SIGN**       Outcome
                              Stunted (Height-For-Age) (%)                          
                              (UOM:%(Percentage)), Scaling                          
                              Factor:1                                              

  2        **WASTING**        Children Under 5 Years Who Are    **FLIP SIGN**       Outcome
                              Wasted (Weight-For-Height) (%)                        
                              (UOM:%(Percentage)), Scaling                          
                              Factor:1                                              

  3        **UNDERWEIGHT**    Children Under 5 Years Who Are    **FLIP SIGN**       Outcome
                              Underweight (Weight-For-Age) (%)                      
                              (UOM:%(Percentage)), Scaling                          
                              Factor:1                                              

  4        **ANEMIA**         Children Age Group 6 To 59 Months **FLIP SIGN**       Outcome
                              Who Are Anaemic (%)                                   
                              (UOM:%(Percentage)), Scaling                          
                              Factor:1                                              

  5        **INST_DEL**       Institutional Births (%)          **increase=good**   Outcome
                              (UOM:%(Percentage)), Scaling                          
                              Factor:1                                              

  6        **SANITATION**     Population Living In Households   **increase=good**   Outcome
                              That Use An Improved Sanitation                       
                              Facility (%) (UOM:%(Percentage)),                     
                              Scaling Factor:1                                      

  7        **CLEAN_FUEL**     Households Using Clean Fuel For   **increase=good**   Outcome
                              Cooking (%) (UOM:%(Percentage)),                      
                              Scaling Factor:1                                      

  8        **IMMUNIZATION**   NFHS-4: \'Children In The Age     **increase=good**   Outcome
                              Group Of 12 To 23 Months Who Are                      
                              Fully Immunized (Bacille                              
                              Calmette-Guerin (Bcg)\...)\' \|                       
                              NFHS-5: \'Children Age Group 12                       
                              To 23 Months Fully Vaccinated                         
                              Based On Information From Either                      
                              Vaccination Card Or Mothers                           
                              Recall (%)\...\' --- DIFFERENT                        
                              names, SAME concept. Rename BOTH                      
                              to \'IMMUNIZATION\' before                            
                              computing delta.                                      
  -------- ------------------ --------------------------------- ------------------- ------------

  -----------------------------------------------------------------------
  ANEMIA COLUMN SELECTION: Both NFHS-4 and NFHS-5 have \'Children Age
  Group 6 To 59 Months Who Are Anaemic\' with the EXACT SAME column name.
  Use THIS column for delta computation. Do NOT use \'Women Age Group 15
  To 49 Years\...\' --- that exists only in NFHS-5, not NFHS-4. Always
  use the column that exists IDENTICALLY in both files.

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  WASTING COLUMN: Both files have \'Children Under 5 Years Who Are Wasted
  (Weight-For-Height) (%)\...\' (standard wasting). Both also have
  \'Children Under 5 Years Who Are SEVERELY Wasted\...\' (severe only).
  Use the standard wasting column (without \'Severely\') for delta --- it
  exists in both files with identical name.

  -----------------------------------------------------------------------

**3.3 SHRUG Component Files --- 6 Files (4 Data + 2 Lookup)**

**File 3a --- pc11_pca_clean_pc11dist.csv (Census 2011 Population
Data)**

  --------------------- -------------------------------------------------
  **Size**              323 KB \| 640 rows × 87 columns

  **Primary key**       pc11_state_id + pc11_district_id (composite ---
                        both needed)

  **Coverage**          Exactly 640 Census 2011 districts

  **Purpose**           Source for SC/ST %, female literacy, population,
                        worker categories
  --------------------- -------------------------------------------------

  -------- ---------------------- ------------------------- ---------------------------
  **\#**   **Raw Column(s)**      **Derived Feature**       **Formula**

  1        pc11_pca_f_lit ÷       **female_literacy_pct**   (pc11_pca_f_lit /
           pc11_pca_tot_f                                   pc11_pca_tot_f) × 100

  2        pc11_pca_p_sc +        **scst_pct**              ((pc11_pca_p_sc +
           pc11_pca_p_st ÷                                  pc11_pca_p_st) /
           pc11_pca_tot_p                                   pc11_pca_tot_p) × 100

  3        pc11_pca_main_al_p +   **agri_worker_pct**       ((main_al + marg_al) /
           pc11_pca_marg_al_p ÷                             tot_work_p) × 100. Proxy
           pc11_pca_tot_work_p                              for rural agrarian
                                                            dependence.

  4        pc11_pca_tot_p         **total_population**      Used for per-capita
                                                            normalization

  5        pc11_pca_no_hh         **total_households**      Used to compute MGNREGS
                                                            persondays per rural HH
  -------- ---------------------- ------------------------- ---------------------------

**File 3b --- secc_cons_rural_pc11dist.csv (Rural Poverty)**

  --------------------- -------------------------------------------------
  **Size**              77 KB \| 615 rows

  **Key**               pc11_state_id + pc11_district_id

  **Column to use**     secc_pov_rate_rural --- rural poverty headcount
                        rate (0--1 scale)

  **Transform**         Apply log(1 + secc_pov_rate_rural) before using
                        as need layer feature

  **Missing coverage**  615 of 640 districts --- 25 will have null
                        poverty. Impute with state median.
  --------------------- -------------------------------------------------

**File 3c --- secc_cons_urban_pc11dist.csv (Urban Poverty)**

  --------------------- -------------------------------------------------
  **Size**              72 KB \| 594 rows

  **Key**               pc11_state_id + pc11_district_id

  **Column to use**     secc_pov_rate_urban --- urban poverty headcount
                        rate (0--1 scale)

  **Combine with        poverty_combined = (secc_pov_rate_rural × 0.70) +
  rural**               (secc_pov_rate_urban × 0.30). Adjust weights
                        using rural_pct from PCA if available.

  **Then transform**    poverty_log = log(1 + poverty_combined)
  --------------------- -------------------------------------------------

**File 3d --- viirs_annual_pc11dist.csv (Night Lights --- Economic
Activity)**

  --------------------- -------------------------------------------------
  **Size**              1.6 MB \| 15,360 rows (multiple years ×
                        categories)

  **Key**               pc11_state_id + pc11_district_id + year +
                        category

  **Filter to use**     year == 2019 AND category == \'median-masked\'
                        (aligns with NFHS-5 baseline year)

  **Column to use**     viirs_annual_mean --- mean night light radiance
                        for district

  **Transform**         night_lights_log = log(1 + viirs_annual_mean) ---
                        distribution is right-skewed

  **Alternative**       viirs_annual_sum also available --- use mean
                        unless geographic size varies widely
  --------------------- -------------------------------------------------

**Files 3e & 3f --- shrid_pc11dist_key.csv and shrid_loc_names.csv
(Lookup Files)**

  ---------------------------- -------------------------------------------------
  **shrid_pc11dist_key.csv**   Maps SHRUG internal IDs (shrid2) to
                               pc11_state_id + pc11_district_id. NOT needed in
                               your pipeline since all SHRUG data files are
                               already at pc11dist level.

  **shrid_loc_names.csv**      Maps shrid2 to state_name + district_name. Useful
                               for VERIFYING district name spelling when
                               aligning with NFHS/MGNREGS. Names are in
                               lowercase --- convert to title case before fuzzy
                               matching.

  **How to use**               Optional: load shrid_loc_names, join with key
                               file, use as a reference to check if your
                               fuzzy-matched district names are correct. Not a
                               required pipeline step.
  ---------------------------- -------------------------------------------------

**3.4 LGD_Master_District_Code.xlsx --- The Geographic Bridge**

  --------------------- --------------------------------------------------
  **Size**              35 KB \| 784 rows

  **Load command**      pd.read_excel(\'LGD_Master_District_Code.xlsx\',
                        header=1) --- NOT header=0. Row 0 is a merged
                        title cell.

  **Total rows**        784 --- includes post-2011 districts created by
                        state bifurcations

  **Usable rows**       \~654 rows where Census 2011 Code is non-zero
                        (these can link to SHRUG)
  --------------------- --------------------------------------------------

  -------- --------------------- ------------------- ---------------------------
  **\#**   **Column Name (after  **Value Type**      **Role in DWEI**
           header=1)**                               

  1        **State Code**        LGD numeric state   Match to MGNREGS state_code
                                 codes               for direct join

  2        **State Name (In      Title case state    Fuzzy match to MGNREGS
           English)**            names               state_name (UPPERCASE)

  3        **District Code**     LGD district codes  PRIMARY MERGE KEY → matches
                                                     MGNREGS district_code
                                                     column directly

  4        **District Name(In    Official district   Fuzzy match to NFHS
           English)**            names               District column when
                                                     name-based join needed

  5        **Census 2011 Code**  pc11_district_id    CRITICAL BRIDGE: =
                                 values              pc11_district_id in SHRUG
                                                     files. This joins LGD ↔
                                                     SHRUG. Rows with value 0
                                                     are post-2011 districts ---
                                                     they drop from analysis.
  -------- --------------------- ------------------- ---------------------------

  -----------------------------------------------------------------------
  **THE SINGLE MOST IMPORTANT JOIN: LGD \'Census 2011 Code\' = SHRUG
  \'pc11_district_id\'. This is the linchpin of the entire data pipeline.
  It connects: SHRUG (pc11_district_id) ↔ LGD (Census 2011 Code) ↔
  MGNREGS (district_code = LGD District Code). \~130 districts in LGD
  have Census 2011 Code = 0 (post-2011 bifurcations) and will drop from
  the final merge. Document this count.**

  -----------------------------------------------------------------------

**3.5 india_district.geojson --- Map Boundaries**

  --------------------- -------------------------------------------------
  **Size**              33 MB --- TOO LARGE for direct use

  **Features**          594 district polygons

  **Property keys in    ID_0, ISO, NAME_0 (India), ID_1, NAME_1 (state),
  each feature**        ID_2 (GADM id), NAME_2 (district name)

  **District name key** NAME_2 --- fuzzy match to lgd_district_name from
                        master.parquet

  **State key**         NAME_1 --- for state-level filtering in dashboard

  **Mandatory action**  Simplify to 25% via mapshaper.org → save as
                        india_districts_simplified.geojson (\~3MB)

  **Coverage**          594 features --- some districts in your master
                        (\~620) will not render on map. Acceptable.
  --------------------- -------------------------------------------------

  -----------------------------------------------------------------------
  MANDATORY BEFORE DASHBOARD: Your 33MB GeoJSON causes 35+ second map
  render. Open mapshaper.org in browser → Import → Upload
  india_district.geojson → Simplify → Method: Visvalingam/Weighted → Set
  to 25% → Apply → Export as GeoJSON → Save as
  india_districts_simplified.geojson. This is a one-time operation. Takes
  2 minutes. Reduces map load to under 2 seconds.

  -----------------------------------------------------------------------

**SECTION 4 --- DATA PIPELINE (Five Notebooks, Stage by Stage)**

**Folder Structure**

+-----------------------------------------------------------------------+
| dwei_project/                                                         |
|                                                                       |
| ├── data/                                                             |
|                                                                       |
| │ ├── raw/ ← Copy all 19 files here. NEVER modify originals.          |
|                                                                       |
| │ │ ├── NFHS-4.csv NFHS-5.csv                                         |
|                                                                       |
| │ │ ├── 2019-20.csv 2020-21.csv 2021-22.csv ← ONLY these 3 MGNREGS    |
|                                                                       |
| │ │ ├── pc11_pca_clean_pc11dist.csv                                   |
|                                                                       |
| │ │ ├── secc_cons_rural_pc11dist.csv                                  |
|                                                                       |
| │ │ ├── secc_cons_urban_pc11dist.csv                                  |
|                                                                       |
| │ │ ├── viirs_annual_pc11dist.csv                                     |
|                                                                       |
| │ │ ├── shrid_pc11dist_key.csv shrid_loc_names.csv                    |
|                                                                       |
| │ │ ├── LGD_Master_District_Code.xlsx                                 |
|                                                                       |
| │ │ └── india_district.geojson                                        |
|                                                                       |
| │ ├── processed/ ← Cleaned intermediate files                         |
|                                                                       |
| │ └── master.parquet ← Final merged file --- all ML reads from here   |
|                                                                       |
| ├── notebooks/                                                        |
|                                                                       |
| │ ├── 01_data_cleaning.ipynb                                          |
|                                                                       |
| │ ├── 02_lgd_merging.ipynb                                            |
|                                                                       |
| │ ├── 03_dwei_score.ipynb                                             |
|                                                                       |
| │ ├── 04_clustering.ipynb                                             |
|                                                                       |
| │ └── 05_xgboost_shap.ipynb                                           |
|                                                                       |
| ├── models/ ← ridge_models.pkl scaler.pkl kmeans.pkl xgboost.pkl      |
|                                                                       |
| ├── geojson/ ← india_districts_simplified.geojson (after mapshaper)   |
|                                                                       |
| ├── shap_values/ ← shap_values.parquet (pre-computed)                 |
|                                                                       |
| ├── app.py ← Streamlit entry point                                    |
|                                                                       |
| ├── data_notes.md ← Document EVERY manual decision here               |
|                                                                       |
| └── requirements.txt                                                  |
+-----------------------------------------------------------------------+

**Notebook 01 --- Data Cleaning**

**NFHS-4 Cleaning**

1.  Load NFHS-4.csv

2.  Filter: df4 = df4\[df4\[\'Residence Type\'\] == \'Total\'\] → verify
    637 rows remain

3.  Rename 8 outcome columns to short names using rename dictionary

4.  For STUNTING, WASTING, UNDERWEIGHT, ANEMIA: these will be
    sign-flipped at delta stage

5.  Keep only: State, District + 8 renamed outcome columns

6.  Strip whitespace, convert State and District to title case

7.  Save as processed/nfhs4_clean.csv

**NFHS-5 Cleaning**

8.  Load NFHS-5.csv --- no Residence Type filter needed

9.  Use SAME rename dictionary as NFHS-4 for 7 of the 8 columns

10. For IMMUNIZATION specifically: NFHS-5 column name is different.
    Rename \'Children Age Group 12 To 23 Months Fully Vaccinated Based
    On Information From Either Vaccination Card Or Mothers Recall
    (%)\...\' → \'IMMUNIZATION\'

11. Keep only: State, District + 8 renamed outcome columns

12. Strip whitespace, title case

13. Save as processed/nfhs5_clean.csv

**SHRUG Feature Engineering**

14. Load pc11_pca_clean_pc11dist.csv → compute female_literacy_pct,
    scst_pct, agri_worker_pct, keep total_population and
    total_households

15. Load secc_cons_rural_pc11dist.csv → extract pc11_state_id,
    pc11_district_id, secc_pov_rate_rural

16. Load secc_cons_urban_pc11dist.csv → extract pc11_state_id,
    pc11_district_id, secc_pov_rate_urban

17. Merge rural and urban SECC on pc11_state_id + pc11_district_id

18. Compute: poverty_combined = (secc_pov_rate_rural × 0.70) +
    (secc_pov_rate_urban × 0.30)

19. Apply log: poverty_log = log(1 + poverty_combined)

20. Load viirs_annual_pc11dist.csv → filter year==2019,
    category==\'median-masked\' → get viirs_annual_mean

21. Apply log: night_lights_log = log(1 + viirs_annual_mean)

22. Merge all SHRUG components on pc11_state_id + pc11_district_id

23. Save as processed/shrug_features.csv

**MGNREGS Aggregation --- 3 Files Only**

24. Load 2019-20.csv, 2020-21.csv, 2021-22.csv

25. For each file, group by state_name + district_name + district_code
    and aggregate:

-   timeliness_raw =
    median(percentage_payments_gererated_within_15_days)

-   timeliness_capped = min(timeliness_raw, 100)

-   persondays_annual = max(Persondays_of_Central_Liability_so_far)

-   women_annual = max(Women_Persondays)

-   avg_days = mean(Average_days_of_employment_provided_per_Household)

26. Compute: women_persondays_pct = (women_annual / persondays_annual) ×
    100

27. Average all features across the 3 years per district

28. Save as processed/mgnregs_aggregated.csv

**Notebook 02 --- LGD Bridge and Three-Way Merge**

**Build LGD Bridge**

29. Load LGD_Master_District_Code.xlsx with header=1

30. Rename columns: \'District Code\' → lgd_district_code, \'Census 2011
    Code\' → pc11_district_id, \'State Code\' → lgd_state_code, \'State
    Name (In English)\' → lgd_state_name, \'District Name(In English)\'
    → lgd_district_name

31. Drop rows where pc11_district_id == 0 (post-2011 districts ---
    cannot link to SHRUG)

32. Convert pc11_district_id and pc11_state_id to int for join
    compatibility

**Merge 1 --- LGD ↔ SHRUG**

33. Merge LGD bridge with processed/shrug_features.csv on
    pc11_district_id (and also match pc11_state_id to verify)

34. Result: lgd_district_code + lgd_district_name + lgd_state_name + all
    7 SHRUG features

**Merge 2 --- LGD+SHRUG ↔ MGNREGS**

35. MGNREGS district_code = LGD District Code. Join directly: merge on
    lgd_district_code == district_code

36. If direct join misses \>50 districts: use fuzzy match on
    (state_name + district_name) with threshold 88 as fallback

37. Review all fuzzy matches below 92 manually --- add correct pairs to
    data_notes.md

**Merge 3 --- LGD+SHRUG+MGNREGS ↔ NFHS**

38. Fuzzy match lgd_district_name to NFHS District column, also matching
    state as disambiguation

39. Threshold 85 --- manually review all matches below 92

40. After successful merge: compute 8 delta columns

-   delta_STUNTING = nfhs5_STUNTING − nfhs4_STUNTING (then multiply
    residual by −1 later)

-   delta_WASTING = nfhs5_WASTING − nfhs4_WASTING (flip later)

-   delta_UNDERWEIGHT = nfhs5_UNDERWEIGHT − nfhs4_UNDERWEIGHT (flip
    later)

-   delta_ANEMIA = nfhs5_ANEMIA − nfhs4_ANEMIA (flip later)

-   delta_IMMUNIZATION = nfhs5_IMMUNIZATION − nfhs4_IMMUNIZATION
    (positive = improvement)

-   delta_INST_DEL = nfhs5_INST_DEL − nfhs4_INST_DEL

-   delta_SANITATION = nfhs5_SANITATION − nfhs4_SANITATION

-   delta_CLEAN_FUEL = nfhs5_CLEAN_FUEL − nfhs4_CLEAN_FUEL

41. Final district count target: 580--620 districts

42. Save as data/master.parquet with compression=\'snappy\'

**master.parquet --- All 22 Columns**

  -------- -------------------------- ---------------- ---------------------------
  **\#**   **Column Name**            **Source**       **Type / Layer**

  1        **lgd_district_code**      LGD              Identifier --- primary key
                                                       for all joins

  2        **lgd_district_name**      LGD              Identifier --- display name
                                                       in dashboard

  3        **lgd_state_name**         LGD              Identifier --- state-level
                                                       grouping

  4        **pc11_state_id**          SHRUG            Identifier --- SHRUG link

  5        **pc11_district_id**       SHRUG            Identifier --- SHRUG link

  6        **female_literacy_pct**    PC11 PCA         Need Layer

  7        **scst_pct**               PC11 PCA         Need Layer

  8        **agri_worker_pct**        PC11 PCA         Need Layer

  9        **poverty_log**            SECC R+U         Need Layer ---
                                                       log-transformed

  10       **night_lights_log**       VIIRS 2019       Need Layer ---
                                                       log-transformed

  11       **wage_timeliness_pct**    MGNREGS 3yr      Implementation Layer ---
                                                       KEY (capped at 100)

  12       **persondays_per_hh**      MGNREGS 3yr      Implementation Layer

  13       **women_persondays_pct**   MGNREGS 3yr      Implementation Layer

  14       **avg_days_per_hh**        MGNREGS 3yr      Implementation Layer

  15       **delta_STUNTING**         NFHS 4→5         Outcome --- flip residual
                                                       sign

  16       **delta_WASTING**          NFHS 4→5         Outcome --- flip residual
                                                       sign

  17       **delta_UNDERWEIGHT**      NFHS 4→5         Outcome --- flip residual
                                                       sign

  18       **delta_ANEMIA**           NFHS 4→5         Outcome --- flip residual
                                                       sign (children 6-59mo)

  19       **delta_IMMUNIZATION**     NFHS 4→5         Outcome --- positive =
                                                       improvement

  20       **delta_INST_DEL**         NFHS 4→5         Outcome --- positive =
                                                       improvement

  21       **delta_SANITATION**       NFHS 4→5         Outcome --- positive =
                                                       improvement

  22       **delta_CLEAN_FUEL**       NFHS 4→5         Outcome --- positive =
                                                       improvement
  -------- -------------------------- ---------------- ---------------------------

**SECTION 5 --- MACHINE LEARNING PIPELINE**

**Stage 1 --- DWEI Score (Ridge Regression, Notebook 03)**

  --------------------- -------------------------------------------------
  **Input X**           5 Need features: female_literacy_pct, scst_pct,
                        agri_worker_pct, poverty_log, night_lights_log

  **Target y**          8 delta outcome columns --- 8 separate Ridge
                        models

  **Output**            8 residuals per district → standardized →
                        aggregated to 1 DWEI score
  --------------------- -------------------------------------------------

**Step-by-Step**

43. Load master.parquet

44. Normalize 5 need features using StandardScaler. Fit on all
    districts. Save as models/scaler.pkl

45. For each of 8 delta outcomes: train Ridge Regression (X=scaled need
    features, y=delta)

46. Compute residual: actual_delta − predicted_delta per district per
    outcome

47. For STUNTING, WASTING, UNDERWEIGHT, ANEMIA: multiply residual by −1
    (decrease=improvement)

48. Standardize all 8 residuals to Z-scores independently

49. DWEI_score = simple mean of 8 standardized residuals

50. Sanity check: top 10 should NOT be dominated by wealthy urban
    districts

51. Save DWEI_score to master.parquet

**Evaluation Metrics**

  ---------------------- ------------------- ----------------------------
  **Metric**             **Target**          **Meaning**

  R² per outcome model   \>0.35 acceptable   Low R² = baseline explains
  (8 models)                                 little = residuals contain
                                             more governance signal

  Residual distribution  \~Normal, mean≈0    Confirms residuals are valid
                                             proxies

  DWEI score range       Roughly −2 to +2    Values beyond ±3 are
                                             outliers --- investigate
  ---------------------- ------------------- ----------------------------

**Stage 2 --- Clustering (KMeans, Notebook 04)**

**Step-by-Step**

52. Features: DWEI_score + all 9 input features (5 need + 4
    implementation)

53. Normalize all with StandardScaler

54. Run KMeans k=2 to 7, compute Silhouette Score each time

55. Select k with highest Silhouette Score above 0.45 (expect k=4 or
    k=5)

56. Validate with Hierarchical Clustering (Ward linkage) --- target
    \>80% district agreement

57. Label tiers by average feature profiles

58. Add \'tier\' column to master.parquet

**Expected Tier Profiles**

  ---------- --------------------- ---------------------------- -----------------------
  **Tier**   **Label**             **Expected Profile**         **Likely Districts**

  **1**      **High Efficiency**   High poverty/SC-ST,          Tribal districts
                                   above-expected NFHS          Odisha, Jharkhand, MP
                                   improvements, high           punching above weight
                                   wage_timeliness_pct          

  2          **Structural          Low poverty, high literacy   Urban-adjacent
             Advantage**           --- outcomes high but        districts --- Pune,
                                   predicted by conditions      Bengaluru belt

  3          **Average Delivery**  Middle values --- neither    Majority of districts
                                   outstanding nor failing      across most states

  **4**      **Underperformers**   Moderate need,               Districts with
                                   below-expected outcomes, low potential but poor
                                   wage_timeliness_pct          execution

  **5**      **Critical Failure**  High need AND below-expected Poorest UP/Bihar
                                   outcomes --- lowest          districts
                                   timeliness, lowest women %   
  ---------- --------------------- ---------------------------- -----------------------

**Stage 3 --- XGBoost + SHAP (Notebook 05)**

  -----------------------------------------------------------------------
  WHY XGBOOST AFTER CLUSTERING: Clustering identifies groups but cannot
  explain why. XGBoost learns cluster membership from administrative and
  structural features. SHAP extracts which features most drive tier
  membership --- globally (national policy finding) and per-district
  (explanation card). Clustering = WHAT. XGBoost+SHAP = WHY.

  -----------------------------------------------------------------------

  --------------------- -------------------------------------------------
  **Input X**           9 features: 5 need + 4 MGNREGS implementation

  **Target y**          tier (5-class: 1--5)

  **Model**             XGBoostClassifier ---
                        objective=\'multi:softprob\'
  --------------------- -------------------------------------------------

**Training Steps**

59. Stratified 80/20 split --- preserves tier proportions

60. StandardScaler fit on train set only

61. XGBoost: n_estimators=300, max_depth=4, learning_rate=0.08,
    subsample=0.8, colsample_bytree=0.8

62. 5-fold stratified cross-validation --- report mean ± std accuracy

63. Test set: accuracy, weighted F1, confusion matrix

64. SHAP TreeExplainer → compute for ALL districts → save
    shap_values/shap_values.parquet

65. Extract top-3 positive and negative SHAP contributors per district
    as text strings

  -----------------------------------------------------------------------
  SHAP HUMAN EXPLANATION: Like a student\'s exam breakdown --- Maths +12,
  English +8, Chemistry −6. SHAP breaks a district\'s tier prediction
  into feature contributions. A collector sees: \'Your Tier 5 is 43%
  explained by poor wage timeliness, 31% by low female literacy ---
  poverty explains only 8%.\' Actionable, specific, per-district. BUT:
  SHAP explains model behavior, not real-world causality. Always say
  \'associated with\', never \'causes\'.

  -----------------------------------------------------------------------

**Example Walkthrough --- Vizianagaram, Andhra Pradesh**

+-----------------------------------------------------------------------+
| **EXAMPLE: Vizianagaram, Andhra Pradesh**                             |
|                                                                       |
| Need Layer (SHRUG): female_literacy=58% scst=24% agri_worker=62%      |
| poverty_log=0.84 night_lights_log=1.2                                 |
|                                                                       |
| → Structurally disadvantaged. Ridge predicts modest NFHS              |
| improvements.                                                         |
|                                                                       |
| MGNREGS (avg 2019-20 to 2021-22): timeliness=91% persondays/hh=38     |
| women%=62% avg_days=42                                                |
|                                                                       |
| NFHS Deltas: STUNTING −8.2pp \| IMMUNIZATION +14.3pp \| ANEMIA −6.1pp |
| \| INST_DEL +11.7pp \| SANITATION +18.2pp                             |
|                                                                       |
| **Ridge Residuals: all positive after sign-flip → DWEI_score = +0.62  |
| → Tier 1 \| Rank \~18 of 600**                                        |
|                                                                       |
| SHAP: +wage_timeliness (+0.41σ) +women_pct (+0.28σ) −poverty (−0.19σ) |
|                                                                       |
| Dashboard card: \'Despite structural disadvantage, Vizianagaram\'s    |
| high wage timeliness (91%) drives Tier 1 classification.\'            |
+-----------------------------------------------------------------------+

**SECTION 6 --- VISUALIZATIONS**

All 7 visualizations use Plotly for interactivity. All charts use
\@st.cache_data to prevent recomputation.

**Viz 1 --- India Choropleth Map**

  --------------------- -------------------------------------------------
  **Library**           px.choropleth_mapbox \| GeoJSON:
                        india_districts_simplified.geojson (33MB → 3MB
                        simplified)

  **Join key**          Fuzzy match lgd_district_name ↔ GeoJSON NAME_2
                        property

  **Colors**            Tier 1: #1E7145 \| Tier 2: #82C48A \| Tier 3:
                        #F0A500 \| Tier 4: #E86A1A \| Tier 5: #C0392B

  **Hover**             District, State, DWEI Score, Tier, Rank, Top
                        Driver, Main Drag

  **Click**             Loads District Explorer panel

  **Speed**             Simplified GeoJSON + \@st.cache_data → under 2
                        second render
  --------------------- -------------------------------------------------

**Viz 2 --- DWEI Distribution Histogram**

  --------------------- -------------------------------------------------
  **Library**           px.histogram with marginal=\'rug\'

  **Shows**             Score distribution with tier color zones

  **Animation**         Bars animate from bottom on load
  --------------------- -------------------------------------------------

**Viz 3 --- Cluster Radar Chart**

  --------------------- -------------------------------------------------
  **Library**           Plotly Scatterpolar --- 5 overlaid polygons

  **Shows**             Average of all 9 features per tier

  **Animation**         Each tier polygon fades in with 300ms stagger
  --------------------- -------------------------------------------------

**Viz 4 --- SHAP Global Feature Importance**

  --------------------- -------------------------------------------------
  **Library**           px.bar horizontal, orientation=\'h\'

  **Colors**            Need features in blue (#2E6DA4), Implementation
                        features in gold (#C9952A)

  **Animation**         Bars animate left-to-right, 150ms stagger ---
                        most impactful animation

  **Key Finding**       If wage_timeliness bar \> poverty_log bar: admin
                        efficiency predicts tier more than poverty
  --------------------- -------------------------------------------------

**Viz 5 --- Per-District SHAP Waterfall**

  --------------------- -------------------------------------------------
  **Library**           SHAP waterfall via matplotlib → st.pyplot

  **Performance**       Load from pre-computed shap_values.parquet ---
                        \<500ms render

  **Below chart**       Auto-generated plain-English interpretation
                        sentence
  --------------------- -------------------------------------------------

**Viz 6 --- State Performance Bar Chart**

  --------------------- -------------------------------------------------
  **Library**           px.bar barmode=\'group\'

  **Shows**             Districts per tier per state --- sorted by % Tier
                        1

  **Interaction**       State dropdown with 400ms animated transition
  --------------------- -------------------------------------------------

**Viz 7 --- Feature vs DWEI Scatter**

  --------------------- -------------------------------------------------
  **Library**           px.scatter with trendline=\'ols\'

  **Interaction**       Dropdown selects X-axis feature --- instant
                        animated update

  **Key use**           wage_timeliness_pct vs DWEI shows strongest
                        positive trendline --- best viva argument
  --------------------- -------------------------------------------------

**SECTION 7 --- DASHBOARD ARCHITECTURE**

**7.1 Five-Page Structure With Purpose Statements**

  ---------- -------------- ------------------------ ---------------------------
  **Page**   **Name**       **Purpose**              **Primary Visualization**

  1          **Overview**   National snapshot ---    Choropleth map full width +
                            user immediately grasps  4 metric cards
                            scale and geography of   
                            welfare efficiency       
                            variation                

  2          **District     Deep dive into any       SHAP waterfall + score
             Explorer**     district --- for         card + explanation text
                            administrators to        
                            understand their         
                            district\'s specific     
                            strengths and gaps       

  3          **Rankings**   Enable comparison ---    AgGrid table + Compare Two
                            benchmark any district   Districts + histogram
                            against peers or         
                            state/national average   

  4          **Cluster      Identify patterns among  Radar chart + state bar
             Analysis**     similar districts ---    chart + tier profile table
                            what do Tier 1 districts 
                            do that Tier 5 do not?   

  5          **Insights**   Convert model outputs to SHAP global bar + scatter
                            policy findings --- the  explorer + written findings
                            national SHAP story and  
                            governance conclusions   
  ---------- -------------- ------------------------ ---------------------------

**7.2 District Search Justification**

  -----------------------------------------------------------------------
  Administrators and citizens are almost always interested in one
  specific district. The search feature allows instant retrieval of DWEI
  score, tier, rank, and SHAP explanation for any district --- making
  DWEI a practical administrative tool, not just an academic ranking.

  -----------------------------------------------------------------------

**7.3 Compare Two Districts Feature**

+-----------------------------------------------------------------------+
| \[ Search District A \] vs \[ Search District B \]                    |
|                                                                       |
| ┌───────────────────────┐ ┌───────────────────────┐                   |
|                                                                       |
| │ Vizianagaram, AP │ │ Shravasti, UP │                                |
|                                                                       |
| │ DWEI: +0.62 │ │ DWEI: -0.71 │                                       |
|                                                                       |
| │ Tier: 1 (High Eff.) │ │ Tier: 5 (Critical) │                        |
|                                                                       |
| │ Rank: 18 / 600 │ │ Rank: 585 / 600 │                                |
|                                                                       |
| │ wage_timeliness: 91% │ │ wage_timeliness: 22% │                     |
|                                                                       |
| └───────────────────────┘ └───────────────────────┘                   |
|                                                                       |
| Below: Side-by-side radar chart of all 9 feature values               |
+-----------------------------------------------------------------------+

**7.4 Five Performance Optimizations**

  ------------------ ------------------------------------------------------
  **Optimization**   **What and Why**

  **1. Parquet**     master.parquet + shap_values.parquet with
                     compression=\'snappy\'. 50MB CSV → 5MB. Loads in
                     \<100ms.

  **2. Cache**       \@st.cache_data on ALL data load functions.
                     \@st.cache_resource on model load. First load once,
                     all subsequent interactions from memory.

  **3. GeoJSON**     Simplify india_district.geojson (33MB) to 25% via
                     mapshaper.org → \~3MB. Map load: 35s → \<2s.
                     MANDATORY.

  **4. Pre-SHAP**    NEVER compute SHAP at runtime. Pre-compute all
                     districts in Notebook 05, save as shap_values.parquet.
                     Per-district render: \<500ms.

  5\. Plotly Config  config={\'displayModeBar\':False} +
                     use_container_width=True on all charts. Explicit
                     height on every chart prevents layout jitter.
  ------------------ ------------------------------------------------------

  -----------------------------------------------------------------------
  DWEI is a decision-support tool, not a decision-making tool. It
  highlights patterns requiring further administrative investigation. No
  district should be penalised based solely on DWEI scores without
  field-level verification.

  -----------------------------------------------------------------------

**SECTION 8 --- PROJECT PLAN**

**8.1 Five-Week Execution Plan**

  ---------- ------------- ----------------------------------- ------------------
  **Week**   **Phase**     **Tasks**                           **Deliverable**

  **1**      Data Cleaning Setup conda env + install           5 clean CSVs in
             NB01          requirements.txt. Clean NFHS-4      processed/
                           (filter Total, rename 8 cols).      
                           Clean NFHS-5 (rename 8 cols).       
                           Engineer SHRUG features from 4      
                           component files. Log-transform      
                           poverty and night lights. Aggregate 
                           MGNREGS --- 3 files only (2019-20,  
                           2020-21, 2021-22). Cap timeliness   
                           at 100. Save 5 processed CSVs.      

  **2**      LGD Merge     Load LGD with header=1. Drop Census master.parquet +
             NB02          2011 Code==0 rows. Build LGD-SHRUG  data_notes.md
                           bridge via pc11_district_id. Merge  
                           LGD+SHRUG. Merge with MGNREGS via   
                           district_code. Fuzzy-match NFHS     
                           districts to LGD names. Compute 8   
                           delta columns with sign conventions 
                           documented. Write data_notes.md.    
                           Save master.parquet.                

  **3**      ML NB03-05    NB03: Ridge (8 models), residuals,  DWEI + tiers +
                           DWEI scores, validation. NB04:      SHAP. 4 pkl files.
                           KMeans k=2-7, Silhouette,           
                           Hierarchical validation, tier       
                           labels. NB05: XGBoost               
                           training+evaluation, SHAP for all   
                           districts, shap_values.parquet.     
                           Save all 4 pkl files. Identify      
                           national SHAP finding.              

  **4**      Dashboard     Simplify GeoJSON (mapshaper). Build Working local
                           all 5 pages. Implement all 7 Plotly dashboard
                           charts with animations.             
                           Compare-two-districts panel. Apply  
                           all 5 optimizations. UI design.     
                           Test all interactions.              

  **5**      Report+Viva   Streamlit Cloud deployment. Project Live URL +
                           report PDF. 12-slide seminar deck.  report + slides
                           Rehearse all 8 viva answers. Test   
                           demo: search → SHAP card → compare. 
  ---------- ------------- ----------------------------------- ------------------

**8.2 Team Allocation**

  ------- ---------------------- ---------------------------------------------------
  **M**   **Role**               **Responsibilities**

  M1      **Data Engineer**      Owns NB01 + NB02 entirely. All cleaning, SHRUG
                                 feature engineering, MGNREGS aggregation (3 files
                                 only), LGD bridge, three-way merge, data_notes.md.

  M2      **ML Scoring**         Owns NB03. Ridge for 8 outcome models. Residuals
                                 with sign conventions. DWEI score aggregation. EDA
                                 notebook with Seaborn correlation heatmap.

  M3      **ML Clustering+SHAP** Owns NB04 + NB05. KMeans + Silhouette +
                                 Hierarchical validation. XGBoost training +
                                 evaluation. SHAP for all districts →
                                 shap_values.parquet. Key finding identification.

  M4      **Dashboard+Deploy**   GeoJSON simplification. All 5 Streamlit pages. All
                                 7 Plotly charts. Compare panel. All 5
                                 optimizations. Streamlit Cloud deployment. Report +
                                 seminar slides.
  ------- ---------------------- ---------------------------------------------------

**SECTION 9 --- VIVA PREPARATION**

**9.1 Eight Likely Questions With Complete Answers**

**Q1: Why not use raw NFHS-5 numbers to rank districts?**

  -----------------------------------------------------------------------
  Raw numbers conflate geography with governance. A wealthy urban
  district will always score higher regardless of governance quality. Our
  residual approach predicts expected improvement from structural
  conditions, then measures how far above or below that prediction the
  actual improvement falls --- isolating the governance contribution.

  -----------------------------------------------------------------------

**Q2: Why Ridge Regression not a more complex model?**

  -----------------------------------------------------------------------
  \(1\) Only 580--620 data points --- complex models overfit. (2) Need
  features are correlated (poverty and literacy correlate) --- Ridge
  handles this via L2 regularization. (3) We need interpretable
  coefficients to validate the model before using its residuals as DWEI
  scores.

  -----------------------------------------------------------------------

**Q3: Why only 3 MGNREGS years? You had 9 files.**

  -----------------------------------------------------------------------
  2019-20, 2020-21, and 2021-22 align with the NFHS-5 survey period
  (2019-21) --- these are the governance inputs that produced the welfare
  outcomes measured in NFHS-5. 2018-19 excluded: only 51% valid
  timeliness values. 2022-23 onwards: post-NFHS-5, temporal mismatch.
  2024-25 and 2025-26: GP/Panchayat-level data (186k rows vs 8k for other
  years) --- incompatible granularity. 2026-27: only 1 month of data.

  -----------------------------------------------------------------------

**Q4: Why cap MGNREGS timeliness at 100?**

  -----------------------------------------------------------------------
  The column contains cumulative monthly counts in some records,
  producing values up to 650,562. After taking median across 12 months,
  legitimate values cluster at 85--115. Values above 100 after
  aggregation reflect minor double-counting artifacts in the source MIS.
  Capping at 100 maintains interpretability as a percentage while
  preserving the administrative efficiency signal.

  -----------------------------------------------------------------------

**Q5: Why XGBoost after clustering?**

  -----------------------------------------------------------------------
  Clustering identifies groups but cannot explain why districts belong to
  them. XGBoost learns cluster membership patterns from administrative
  features. SHAP extracts which features most drive that membership.
  Clustering = WHAT exists. XGBoost + SHAP = WHY it exists.

  -----------------------------------------------------------------------

**Q6: Can a rich district have a low DWEI score?**

  -----------------------------------------------------------------------
  Yes --- this is a key conceptual point. If Ridge predicts 95%
  immunization for a wealthy district given its structural conditions,
  and the actual NFHS-5 value is 88%, the residual is negative. The
  district underperformed its own structural potential despite high
  absolute numbers. DWEI rewards governance, not wealth.

  -----------------------------------------------------------------------

**Q7: What does SHAP actually measure?**

  -----------------------------------------------------------------------
  SHAP decomposes each prediction into feature contributions --- like
  breaking a student\'s exam score into subject contributions.
  Technically: Shapley values from game theory, showing each feature\'s
  average marginal contribution across all feature orderings. Critical:
  SHAP explains model behavior, not real-world causality.

  -----------------------------------------------------------------------

**Q8: Should government trust DWEI for decisions?**

  -----------------------------------------------------------------------
  DWEI is a decision-support tool, not a decision-making tool. A Tier 5
  flag should prompt field investigation --- not automatic penalties.
  DWEI complements but does not replace ground-level assessment.

  -----------------------------------------------------------------------

**9.2 Formal Limitations --- For Report**

66. MGNREGS timeliness column has source-level typo (\'gererated\') and
    anomalous values requiring capping --- introduces measurement
    uncertainty in the key implementation variable.

67. 2024-25 and 2025-26 MGNREGS files are GP/Panchayat-level granularity
    and cannot be used at district level without block-level geographic
    keys.

68. Residuals capture all unexplained variance --- governance, civil
    society, local shocks, migration, and noise --- not governance
    alone.

69. SHAP explains model behavior, not real-world causality. Associations
    ≠ causal effects.

70. \~130 post-2011 districts have LGD Census 2011 Code = 0 and drop
    from analysis.

71. SHRUG baseline uses 2011 Census --- structural changes 2011--2019
    are not captured.

72. GeoJSON has 594 features; some matched districts (\~620) will not
    render on map.

**SECTION 10 --- DEPLOYMENT & FINAL OUTPUTS**

**10.1 Streamlit Cloud Deployment**

73. Push dwei_project/ to GitHub (public repo)

74. Include requirements.txt, app.py,
    geojson/india_districts_simplified.geojson

75. Include data/master.parquet and shap_values/shap_values.parquet

76. DO NOT push raw data files (too large for GitHub 100MB limit)

77. share.streamlit.io → Sign in GitHub → Select repo → Main file:
    app.py → Deploy

78. Live URL: yourapp.streamlit.app --- share before viva

**10.2 Deliverables Checklist**

  ------- ---------------------------------------- ---------------------------------------
  **✓**   **Deliverable**                          **Format**

  □       **Live Dashboard URL**                   Streamlit Cloud --- shareable link

  □       **master.parquet**                       22 columns, 580--620 districts, DWEI +
                                                   tier

  □       **shap_values.parquet**                  Pre-computed SHAP for all districts

  □       **india_districts_simplified.geojson**   Simplified from 33MB → 3MB

  □       **5 Jupyter Notebooks**                  01_cleaning through 05_xgboost_shap

  □       **4 Model pkl files**                    ridge, scaler, kmeans, xgboost

  □       **data_notes.md**                        All manual decisions documented

  □       **Project Report PDF**                   8--10 pages with limitations section

  □       **12-Slide Seminar Deck**                Including live demo slide

  □       **GitHub Repository**                    All code + requirements.txt + README
  ------- ---------------------------------------- ---------------------------------------

**10.3 12-Slide Seminar Structure**

  ----------- ------------------ -------------------------------------------------
  **Slide**   **Title**          **Content**

  1           **Title**          Project name, team, branch, university, date

  2           **The Problem**    Raw rankings mislead --- wealthy district always
                                 wins. Need efficiency-adjusted approach.

  3           **DWEI Approach**  Core equation. Conceptual flow diagram from your
                                 actual 19 files.

  4           **Data Sources**   3 MGNREGS years chosen (why not all 9). NFHS-4
                                 filter. SHRUG components.

  5           **ML Pipeline**    Full flow diagram: files → Ridge → DWEI → KMeans
                                 → XGBoost+SHAP → Dashboard

  6           **Stage 1          DWEI score distribution. Top 5 and bottom 5
              Results**          districts named.

  7           **Stage 2          Silhouette plot + radar chart. Tier distribution
              Results**          across India.

  8           **India Map**      Full choropleth. Most impactful slide. Full
                                 width.

  9           **Key SHAP         Global bar chart. National finding:
              Finding**          wage_timeliness predicts tier more than poverty.

  10          **Governance       Top 10 Tier 1 districts. Vizianagaram
              Heroes**           walkthrough. What they share.

  11          **Live Demo**      Open dashboard → search district → SHAP card →
                                 compare two districts.

  12          **Conclusion**     3 key findings + limitations + future work
                                 (UDISE, PMGSY)
  ----------- ------------------ -------------------------------------------------

**SECTION 11 --- CIVIL SERVICES VALUE**

**11.1 GS + Sociology Relevance**

  --------------- -------------------------------------------------------
  **Area**        **What DWEI Gives You**

  **GS-2:         Hands-on analysis of MGNREGS wage payment
  Governance**    infrastructure, DBT effectiveness, district
                  administration capacity. Writing about governance
                  reforms --- you draw from real analysis, not memorized
                  text.

  **GS-2: Social  NFHS-5 stunting, anemia, SC/ST outcomes across 600+
  Justice**       districts --- understood as distributions with known
                  drivers, not as page numbers.

  **GS-3:         MGNREGS mechanics, 3-year data aggregation, wage
  Economy**       infrastructure, rural employment --- learned through
                  real MIS data, not textbook.

  **Essay Paper** \'Data-driven governance\', \'evidence-based policy\',
                  \'separating intent from outcome\' --- anchored with
                  real findings.

  **Sociology     SC/ST % as structural disadvantage (Ambedkar) + female
  Optional**      literacy + agri_worker_pct (Srinivas) --- quantified at
                  district scale across India.
  --------------- -------------------------------------------------------

**11.2 The IAS Interview Answer**

  -----------------------------------------------------------------------
  When asked: \'You studied AI/ML --- why civil services?\' You say:
  \'Sir, for my mini project I built a district-level welfare efficiency
  index using NFHS-4, NFHS-5, three years of MGNREGS MIS data, and SHRUG
  --- covering 600 Indian districts. The key finding was that MGNREGS
  wage payment timeliness --- how quickly district administrations pay
  wages --- predicted which welfare efficiency tier a district belonged
  to more strongly than poverty level, female literacy, or SC/ST
  population. That means administrative execution quality matters more
  than structural conditions. I want to be on the administrative side of
  that equation --- directly improving that execution quality.\'
  Specific. Evidence-based. Uses real dataset names. Connects technical
  skill to IAS aspiration. No other candidate will have this answer.

  -----------------------------------------------------------------------
