# Player Style Clustering

Clustering football playing styles (*tactical player profiles*) from **StatsBomb open-data** using **K-Means**, and verifying cluster stability using **KNN + 5-fold cross-validation**.

> **Research Question:** How do feature scaling transformations (Unscaled, StandardScaler, RobustScaler) and the choice of hyperparameter $k$ affect the clustering of player styles from multi-event aggregate data, and how stably do the discovered clusters reflect distinct tactical roles?

## Experimental Design

| Component | Role |
|---|---|
| **Experimental Variables** | Feature scaling (`Unscaled`, `StandardScaler`, `RobustScaler`) · Number of clusters $k$ (2–10) |
| **Control Variables** | Fixed distance metric L2/Euclidean · `random_state=42` · $\ge 900$ minutes threshold |
| **Difference Measurement** | Adjusted Rand Index (ARI) between clustering variants |
| **Internal Validation** | Silhouette score · Elbow method (Inertia) · Gap Statistic |
| **External Validation** | Position group purity + Normalized Mutual Information (NMI) vs. `primary_position` |
| **Stability Test** | KNN 5-fold cross-validation predicting `cluster_id` $\rightarrow$ accuracy $\pm$ std |

## Data

| Source | `saurabhshahane/statsbomb-football-data` (Kaggle Dataset) / StatsBomb Open Data |
|---|---|
| Competitions | Premier League (`comp=2, season=27`), La Liga (`comp=11, season=27`), Serie A (`comp=12, season=27`) |
| Season | 2015/2016 (full 380-match schedule for all 3 leagues = 1,140 matches total) |
| Sample Size | 1,016 qualified players ($\ge 900$ minutes played) $\times$ 29 numeric features |

## Quickstart

### Notebooks Suite

The workflow is organized into modular notebooks designed to be run directly on **Google Colab** or **Kaggle**:
- [notebooks/01_data_and_eda.ipynb](notebooks/01_data_and_eda.ipynb): Data ingestion, multi-event feature extraction, and exploratory data analysis.
- [notebooks/02_modeling.ipynb](notebooks/02_modeling.ipynb): Preprocessing (median imputation, scaling) and K-Means modeling ($k$-selection, ARI comparison).
- [notebooks/03_evaluation.ipynb](notebooks/03_evaluation.ipynb): Cluster validation (position purity, NMI), KNN stability testing, and tactical interpretation.
- [notebooks/04_master_pipeline.ipynb](notebooks/04_master_pipeline.ipynb): Combined end-to-end master pipeline (extract/load $\rightarrow$ preprocess $\rightarrow$ cluster $\rightarrow$ validate).
- [notebooks/05_striker_subclustering.ipynb](notebooks/05_striker_subclustering.ipynb): Case study — fine-grained K-Means sub-clustering of the 152 striker players from Cluster 1, revealing three tactical archetypes (Poacher, Target Man, Deep-Lying Forward).

## Team & Contributions

| Member | Role | Responsibilities |
|---|---|---|
| **Nguyễn Thanh Phong** | Team Lead / Infra | Repository setup, master pipeline orchestration, code review |
| **Võ Công Tuấn Lộc** | Data Engineer | Data ingestion, minute extraction, exploratory data analysis |
| **Trương Hoàng Thông** | ML & Evaluation Engineer | Feature engineering, K-Means modeling, validation, technical report |
