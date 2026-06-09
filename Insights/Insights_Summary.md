# Insights Summary — Recruitment EDA

**Dataset:** `Dataset/recruitment_data.csv`  
**Records:** 1,500 candidates · 11 features  
**Analysis Period:** Recruitment cycle captured in the dataset  

---

## Key Findings

| # | Finding | Detail |
|---|---------|--------|
| 1 | **Selective hiring** | Only **31%** of candidates (465 / 1,500) received a hiring offer. |
| 2 | **Interview Score dominates** | Hired candidates averaged ~20 points higher on Interview Score than rejected ones — the single strongest differentiator (Pearson r ≈ 0.47 with HiringDecision). |
| 3 | **Higher education → higher hire rate** | PhD holders are hired at a notably higher rate than High School graduates; the gap widens further when combined with relevant experience. |
| 4 | **Distance is irrelevant** | A T-test confirms no statistically significant difference in `DistanceFromCompany` between hired and rejected candidates (p ≥ 0.05). |
| 5 | **Gender is balanced** | The dataset is nearly gender-equal (50.8% Female / 49.2% Male) with comparable hiring rates across genders. |
| 6 | **Personality Score least predictive** | Personality Score shows the smallest distributional gap between hired and rejected groups, suggesting it carries limited weight in current decisions. |
| 7 | **Moderate strategy dominates** | 51.3% of all candidates come through the Moderate recruitment strategy, which also delivers a hiring rate near the overall average. |

---

## Observed Trends

### 📈 Score Dynamics
- **Composite Score threshold**: Candidates above ~60 Composite Score (weighted: 40% Interview + 35% Skill + 25% Personality) are hired at a dramatically higher rate.
- **Score clustering**: Hired candidates cluster strongly above 60 across all three assessment dimensions; rejected candidates cluster below 45.
- **Skill Score** is the second-most predictive metric after Interview Score.

### 🎓 Education × Experience Synergy
- Candidates with **Master's or PhD + 8–12 years of experience** show the highest hire rates.
- Very junior candidates (0–2 years) are hired at near-average rates when Interview and Skill Scores are high, suggesting potential is recognised.

### 🏢 Previous Companies Effect
- Candidates with **3–4 previous employers** show a slightly elevated hiring rate — interpreted as valuable diverse experience.
- Candidates with only 1 previous company or 5+ are hired at a slightly lower rate.

### 📅 Age Group Patterns
- The **31–35 and 36–40** age bands have the largest candidate pools.
- Hiring rate is broadly uniform across age groups (~28–34%), indicating age is not a meaningful discriminator in this dataset.

### 🗺 Recruitment Strategy
| Strategy | Candidates | Hiring Rate |
|----------|-----------|-------------|
| Aggressive | 445 | ~28% |
| Moderate | 770 | ~31% |
| Conservative | 285 | ~35% |

Conservative strategy attracts fewer but higher-quality candidates; Aggressive fills the funnel but dilutes quality.

---

## Data-Driven Recommendations for HR / Recruitment Teams

### Recommendation 1 — Calibrate and Standardise the Interview Process 🎯
> **Impact: HIGH**  
> Interview Score is the most predictive hiring signal. Invest in:
> - Structured behavioural interview frameworks (e.g., STAR method)
> - Inter-rater reliability training and calibration sessions between interviewers
> - Score rubrics that make grades comparable across roles and departments
>
> *Even a moderate improvement in interview scoring reliability will directly increase predictive validity.*

### Recommendation 2 — Audit and Replace the Personality Assessment 🧠
> **Impact: MEDIUM–HIGH**  
> Personality Score shows the weakest correlation with hiring outcomes among all three assessment pillars. HR teams should:
> - Commission a validity study on the current personality instrument
> - Consider replacing it with a role-specific situational judgement test (SJT) or a validated structured personality inventory (e.g., Big Five work-relevant facets)
> - Re-weight the Composite Score once the new instrument is validated
>
> *Reducing signal noise from a weak predictor improves overall decision quality without adding cost.*

### Recommendation 3 — Adopt Moderate Strategy as Default; Use Aggressive Selectively 📊
> **Impact: MEDIUM**  
> The Moderate recruitment strategy provides the optimal pipeline volume-to-quality balance. HR teams should:
> - Set Moderate strategy as the **default** for most roles
> - Trigger Aggressive strategy only for **hard-to-fill or time-critical roles** where volume is essential
> - Deploy Conservative strategy for **senior / specialist roles** where a smaller, highly qualified pipeline is preferred
>
> *This tiered approach avoids the high screening overhead of Aggressive while meeting urgent hiring needs.*

---

## Statistical Appendix

| Metric | Value |
|--------|-------|
| Total candidates | 1,500 |
| Hired | 465 (31.0%) |
| Not Hired | 1,035 (69.0%) |
| Mean Age | 35.1 years |
| Mean Experience | 7.7 years |
| Mean Interview Score | 50.6 / 100 |
| Mean Skill Score | 51.1 / 100 |
| Mean Personality Score | 49.4 / 100 |
| Mean Composite Score | 50.5 / 100 |
| Hired — Avg Interview Score | ~65 |
| Not Hired — Avg Interview Score | ~44 |
| Hired — Avg Composite Score | ~63 |
| Not Hired — Avg Composite Score | ~45 |
| Interview Score × HiringDecision (Pearson r) | ~0.47 |
| Skill Score × HiringDecision (Pearson r) | ~0.39 |
| Personality Score × HiringDecision (Pearson r) | ~0.32 |
| Distance × HiringDecision (p-value) | ≥ 0.05 (not significant) |
