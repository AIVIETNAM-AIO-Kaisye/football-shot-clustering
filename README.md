# Football Shot Clustering

Clustering football shot opportunities (*shot quality*) from **StatsBomb open-data** using **K-Means**, and verifying cluster stability using **KNN + k-fold cross-validation**.

> **Research Question:** How does feature scaling and the choice of K affect the clustering of shots by chance quality, and do the discovered clusters truly reflect the real scoring probability?

## Experimental Design

| Component | Role |
|---|---|
| **Experimental Variables** | Feature scaling (`X_unscaled` vs `X_scaled`) · Number of clusters K (2–10) |
| **Control Variables** | Fixed distance metric L2/Euclidean · `random_state=42` |
| **Difference Measurement** | Adjusted Rand Index (ARI) between 2 clustering versions |
| **Internal validation** | Silhouette · Elbow · Gap Statistic |
| **External validation** | Actual goal rate + average xG by cluster (from hidden fields) |
| **Stability Test** | KNN 5-fold CV predicting `cluster_id` → accuracy ± std |

## Data

| Source | `saurabhshahane/statsbomb-football-data` (Kaggle Dataset) |
|---|---|
| Tournaments | FIFA World Cup 2018 (`comp=43, season=3`) + FIFA World Cup 2022 (`comp=43, season=106`) |
| Matches | 128 |

## Quickstart

### Notebooks Suite

The workflow is divided among the team's designated notebooks to prevent git conflicts. These notebooks are designed to be run directly on **Google Colab** or **Kaggle**:
- [notebooks/01_data_and_eda.ipynb](notebooks/01_data_and_eda.ipynb): Data ingestion, shot extraction, and EDA.
- [notebooks/02_modeling.ipynb](notebooks/02_modeling.ipynb): Preprocessing, feature scaling, and K-Means modeling.
- [notebooks/03_evaluation.ipynb](notebooks/03_evaluation.ipynb): Model validation, CV stability, and external evaluation.
- [notebooks/04_master_pipeline.ipynb](notebooks/04_master_pipeline.ipynb): The combined end-to-end master notebook (assembled at the end of the project).

## Team

| Role | Branch | Assignee |
|---|---|---|
| **Phong** — Repo Setup & Infra *(Team Lead)* | `data-eng` | Setup repo, master pipeline, review |
| **Lộc** — Data Engineer | `loc-data` | Raw data extraction, EDA |
| **Thông** — ML & Eval Engineer | `ml-eng` | Feature engineering, preprocessing, K-Means, Validation, Report |
