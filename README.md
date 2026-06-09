# Exploratory Data Analysis (EDA) on a Recruitment Dataset

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-f37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![seaborn](https://img.shields.io/badge/seaborn-0.13-4c72b0)](https://seaborn.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A comprehensive, end-to-end Exploratory Data Analysis project on a recruitment dataset containing **1,500 candidate records** with assessment scores, demographic information, and hiring outcomes.

---

## Project Overview

This project uncovers patterns in candidate applications and hiring decisions through rigorous statistical analysis and rich visualisations. It is structured for both HR practitioners looking for actionable insights and data professionals studying EDA methodology.

### What's Inside

| Deliverable | Location | Description |
|-------------|----------|-------------|
| **Jupyter Notebook** | `Notebook/EDA_Recruitment_Dataset.ipynb` | Full EDA with code, charts, and explanations |
| **Insights Summary** | `Insights/Insights_Summary.md` | Key findings, trends, and 3 HR recommendations |
| **Charts (17 total)** | `Outputs/` | Publication-quality visualisations |
| **Dataset** | `Dataset/recruitment_data.csv` | Raw recruitment data (1,500 rows × 11 columns) |
| **Requirements** | `requirements.txt` | Python dependencies |

---

## Dataset Description

**File:** `Dataset/recruitment_data.csv`  
**Shape:** 1,500 rows × 11 columns  
**Missing Values:** None

| Column | Type | Description |
|--------|------|-------------|
| `Age` | int | Candidate age (20–50) |
| `Gender` | int | 0 = Female, 1 = Male |
| `EducationLevel` | int | 1 = High School, 2 = Bachelor's, 3 = Master's, 4 = PhD |
| `ExperienceYears` | int | Years of work experience (0–15) |
| `PreviousCompanies` | int | Number of previous employers (1–5) |
| `DistanceFromCompany` | float | Distance from workplace in km |
| `InterviewScore` | int | Interview performance score (0–100) |
| `SkillScore` | int | Technical skill assessment score (0–100) |
| `PersonalityScore` | int | Personality/behavioural assessment score (0–100) |
| `RecruitmentStrategy` | int | 1 = Aggressive, 2 = Moderate, 3 = Conservative |
| `HiringDecision` | int | **Target variable** — 0 = Not Hired, 1 = Hired |

---

## Key Results at a Glance

- **Overall Hiring Rate: 31%** (465 out of 1,500 candidates hired)
- **Interview Score** is the strongest predictor of hiring (Pearson r ≈ 0.47)
- **PhD holders** have significantly higher hiring rates than Bachelor's degree holders
- **Moderate recruitment strategy** provides the best volume-to-quality pipeline balance
- **Distance from company** has no statistically significant impact on hiring (p ≥ 0.05)

---

## Analysis Sections

1. **Environment Setup & Imports** — Library configuration and global plot aesthetics
2. **Data Loading & Initial Inspection** — Schema overview, descriptive statistics
3. **Data Cleaning & Preprocessing** — Label decoding, feature engineering, outlier detection
4. **Univariate Analysis** — Individual distributions of all features
5. **Bivariate & Multivariate Analysis** — Cross-feature relationships
6. **Hiring Decision Deep-Dive** — Factor-by-factor hiring rate breakdowns
7. **Score Analysis** — Interview, Skill, and Personality score comparisons
8. **Correlation Analysis** — Pearson heatmap and feature importance ranking
9. **Recruitment Strategy Analysis** — Volume, hiring rate, and score by strategy
10. **Key Insights & Recommendations** — Executive dashboard + HR recommendations

---

## Charts Generated

| Chart | Description |
|-------|-------------|
| `00_executive_dashboard.png` | 6-panel executive summary dashboard |
| `01_hiring_decision_distribution.png` | Bar + pie chart of overall hiring outcomes |
| `02_continuous_distributions.png` | Histograms + KDE for 7 numeric features |
| `03_categorical_distributions.png` | Horizontal bar charts for 4 categorical features |
| `04_hiring_rate_by_education.png` | Hiring rate by education level |
| `05_hiring_rate_by_experience.png` | Hiring rate trend across experience years |
| `06_age_dist_hired_vs_rejected.png` | KDE of age for hired vs rejected |
| `07_pairplot_scores.png` | Pairplot of assessment scores coloured by outcome |
| `08_hiring_rate_gender_education.png` | Grouped bar by gender × education |
| `09_distance_vs_hiring.png` | Box + violin plots of distance by outcome |
| `10_hiring_by_age_group.png` | Hiring rate and volume by age group |
| `11_score_distributions.png` | KDE comparison of all scores (hired vs rejected) |
| `12_scores_by_education.png` | Mean scores by education level |
| `13_correlation_heatmap.png` | Lower-triangle Pearson correlation heatmap |
| `14_feature_correlation_bar.png` | Feature correlation ranking with HiringDecision |
| `15_recruitment_strategy_comparison.png` | Volume, rate, and score by recruitment strategy |
| `16_previous_companies_vs_hiring.png` | Hiring rate by number of previous employers |

---

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/sandudul/Exploratory-Data-Analysis-EDA-on-a-Recruitment-Dataset.git
cd Exploratory-Data-Analysis-EDA-on-a-Recruitment-Dataset
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Jupyter Notebook
```bash
jupyter notebook Notebook/EDA_Recruitment_Dataset.ipynb
```

### 4. (Optional) Generate charts via standalone script
```bash
python Notebook/run_eda.py
```
Charts will be saved to the `Outputs/` folder.

---

## Data-Driven Recommendations

### 1. Calibrate and Standardise the Interview Process
Interview Score is the most predictive signal. Implement structured interview frameworks (e.g., STAR method), interviewer calibration sessions, and consistent scoring rubrics to reduce bias and improve reliability.

### 2. Audit and Replace the Personality Assessment
Personality Score is the weakest predictor among the three assessment dimensions. Commission a validity study and consider replacing the instrument with a role-specific Situational Judgement Test (SJT) or a validated work-relevant personality inventory.

### 3. Adopt a Tiered Recruitment Strategy
- **Default → Moderate strategy** for most roles (best pipeline balance)
- **Aggressive strategy** only for hard-to-fill or urgent roles
- **Conservative strategy** for senior / specialist positions requiring highly qualified, focused pipelines

---

## Project Structure

```
Exploratory-Data-Analysis-EDA-on-a-Recruitment-Dataset/
├── Dataset/
│   └── recruitment_data.csv          # Raw dataset
├── Notebook/
│   ├── EDA_Recruitment_Dataset.ipynb # Main Jupyter Notebook
│   └── run_eda.py                    # Standalone chart generator
├── Outputs/
│   ├── 00_executive_dashboard.png
│   ├── 01_hiring_decision_distribution.png
│   └── ... (17 charts total)
├── Insights/
│   └── Insights_Summary.md           # Key findings & recommendations
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

---

## Requirements

See [`requirements.txt`](requirements.txt) for the full list. Core dependencies:

- `pandas >= 2.0`
- `numpy >= 1.24`
- `matplotlib >= 3.7`
- `seaborn >= 0.12`
- `scikit-learn >= 1.3`
- `scipy >= 1.11`
- `jupyter >= 1.0`

---

## License

This project is licensed under the MIT License.