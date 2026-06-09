"""
run_eda.py -- Standalone script that mirrors every chart cell in the notebook.
Outputs are saved to ../Outputs/ relative to this script.
"""
import os, sys, warnings, io
warnings.filterwarnings('ignore')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pandas  as pd
import numpy   as np
import matplotlib
matplotlib.use('Agg')                      # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from   matplotlib.gridspec import GridSpec
import seaborn as sns
from   scipy   import stats

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE    = os.path.dirname(os.path.abspath(__file__))
DATA    = os.path.join(BASE, '..', 'Dataset', 'recruitment_data.csv')
OUT_DIR = os.path.join(BASE, '..', 'Outputs')
os.makedirs(OUT_DIR, exist_ok=True)

def save(name):
    path = os.path.join(OUT_DIR, name)
    plt.savefig(path, bbox_inches='tight', dpi=150)
    plt.close('all')
    print(f'  ✅ Saved: {name}')

# ── Global aesthetics ──────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0f1117', 'axes.facecolor': '#1a1d27',
    'axes.edgecolor': '#3a3f5c',   'axes.labelcolor': '#e0e0e0',
    'xtick.color': '#b0b0c0',      'ytick.color': '#b0b0c0',
    'text.color': '#e0e0e0',       'grid.color': '#2e3250',
    'grid.linestyle': '--',        'grid.alpha': 0.5,
    'font.family': 'DejaVu Sans',  'axes.titlesize': 14,
    'axes.labelsize': 12,          'legend.facecolor': '#1a1d27',
    'legend.edgecolor': '#3a3f5c', 'figure.dpi': 120,
})
PALETTE      = ['#6c63ff', '#ff6584', '#43e97b', '#f9a825', '#00d2ff']
HIRED_COLOR  = '#43e97b'
REJECT_COLOR = '#ff6584'
ACCENT       = '#6c63ff'

# ── Load & preprocess ─────────────────────────────────────────────────────────
print('Loading data ...')
df = pd.read_csv(DATA)
df['Gender_Label']              = df['Gender'].map({0:'Female', 1:'Male'})
edu_map  = {1:"High School", 2:"Bachelor's", 3:"Master's", 4:'PhD'}
df['EducationLevel_Label']      = df['EducationLevel'].map(edu_map)
strat_map = {1:'Aggressive', 2:'Moderate', 3:'Conservative'}
df['RecruitmentStrategy_Label'] = df['RecruitmentStrategy'].map(strat_map)
df['HiringDecision_Label']      = df['HiringDecision'].map({0:'Not Hired', 1:'Hired'})
df['CompositeScore']            = (df['InterviewScore']*0.40 +
                                   df['SkillScore']*0.35 +
                                   df['PersonalityScore']*0.25).round(2)
df['AgeGroup'] = pd.cut(df['Age'], bins=[19,25,30,35,40,45,51],
                        labels=['20–25','26–30','31–35','36–40','41–45','46–50'])
edu_order = ["High School", "Bachelor's", "Master's", 'PhD']
print(f'Dataset shape: {df.shape}\n')

# ══════════════════════════════════════════════════════════════════════════════
# 01 — Hiring Decision Distribution
# ══════════════════════════════════════════════════════════════════════════════
print('Generating charts ...')
counts = df['HiringDecision_Label'].value_counts()
colors = [HIRED_COLOR if v == 'Hired' else REJECT_COLOR for v in counts.index]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Overall Hiring Decision Distribution', fontsize=16, fontweight='bold', y=1.02)
bars = axes[0].bar(counts.index, counts.values, color=colors, edgecolor='white', linewidth=0.8, width=0.5)
for bar, val in zip(bars, counts.values):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+15,
                 f'{val:,}\n({val/len(df)*100:.1f}%)', ha='center', va='bottom', fontsize=11)
axes[0].set_title('Count of Candidates', fontsize=13)
axes[0].set_ylabel('Number of Candidates')
axes[0].set_ylim(0, counts.max()*1.18)
axes[0].grid(axis='y', alpha=0.4)
wedges,texts,autotexts = axes[1].pie(
    counts.values, labels=counts.index, colors=colors, autopct='%1.1f%%', startangle=140,
    textprops={'color':'white','fontsize':12}, wedgeprops={'edgecolor':'#0f1117','linewidth':2})
for at in autotexts: at.set_fontweight('bold')
axes[1].set_title('Proportion', fontsize=13)
plt.tight_layout()
save('01_hiring_decision_distribution.png')

# ══════════════════════════════════════════════════════════════════════════════
# 02 — Continuous Feature Distributions
# ══════════════════════════════════════════════════════════════════════════════
cont_features = ['Age','ExperienceYears','DistanceFromCompany',
                 'InterviewScore','SkillScore','PersonalityScore','CompositeScore']
fig, axes = plt.subplots(2, 4, figsize=(20, 8))
fig.suptitle('Distribution of Continuous Features', fontsize=16, fontweight='bold', y=1.01)
axes = axes.flatten()
for i, col in enumerate(cont_features):
    ax = axes[i]
    sns.histplot(df[col], ax=ax, color=PALETTE[i%len(PALETTE)], kde=True, edgecolor='none', alpha=0.8)
    ax.axvline(df[col].mean(),   color='white',  linestyle='--', linewidth=1.5, label=f'Mean={df[col].mean():.1f}')
    ax.axvline(df[col].median(), color='yellow', linestyle=':',  linewidth=1.5, label=f'Median={df[col].median():.1f}')
    ax.set_title(col, fontsize=12, fontweight='bold'); ax.set_xlabel('')
    ax.legend(fontsize=8); ax.grid(axis='y', alpha=0.3)
axes[-1].set_visible(False)
plt.tight_layout()
save('02_continuous_distributions.png')

# ══════════════════════════════════════════════════════════════════════════════
# 03 — Categorical Distributions
# ══════════════════════════════════════════════════════════════════════════════
cat_specs = [
    ('Gender_Label',              'Gender Distribution'),
    ('EducationLevel_Label',      'Education Level Distribution'),
    ('RecruitmentStrategy_Label', 'Recruitment Strategy Distribution'),
    ('AgeGroup',                  'Age Group Distribution'),
]
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle('Distribution of Categorical Features', fontsize=16, fontweight='bold', y=1.01)
axes = axes.flatten()
for i, (col, title) in enumerate(cat_specs):
    ax   = axes[i]
    vals = df[col].value_counts()
    clrs = PALETTE[:len(vals)]
    bars = ax.barh(vals.index.astype(str), vals.values, color=clrs, edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, vals.values):
        ax.text(val+5, bar.get_y()+bar.get_height()/2,
                f'{val:,} ({val/len(df)*100:.1f}%)', va='center', fontsize=10)
    ax.set_title(title, fontsize=12, fontweight='bold'); ax.set_xlabel('Count')
    ax.set_xlim(0, vals.max()*1.2); ax.grid(axis='x', alpha=0.3); ax.invert_yaxis()
plt.tight_layout()
save('03_categorical_distributions.png')

# ══════════════════════════════════════════════════════════════════════════════
# 04 — Hiring Rate by Education
# ══════════════════════════════════════════════════════════════════════════════
edu_hire = df.groupby('EducationLevel_Label')['HiringDecision'].mean().reset_index()
edu_hire.columns = ['EducationLevel','HiringRate']
edu_hire['HiringRate'] *= 100
edu_hire['EducationLevel'] = pd.Categorical(edu_hire['EducationLevel'], categories=edu_order, ordered=True)
edu_hire = edu_hire.sort_values('EducationLevel')

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(edu_hire['EducationLevel'], edu_hire['HiringRate'],
              color=PALETTE[:4], edgecolor='white', linewidth=0.8, width=0.55)
for bar, val in zip(bars, edu_hire['HiringRate']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f'{val:.1f}%', ha='center', fontsize=11, fontweight='bold')
ax.axhline(df['HiringDecision'].mean()*100, color='white', linestyle='--', linewidth=1.5,
           label=f'Overall avg ({df["HiringDecision"].mean()*100:.1f}%)')
ax.set_title('Hiring Rate by Education Level', fontsize=14, fontweight='bold')
ax.set_ylabel('Hiring Rate (%)'); ax.set_ylim(0, edu_hire['HiringRate'].max()*1.25)
ax.legend(fontsize=10); ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
save('04_hiring_rate_by_education.png')

# ══════════════════════════════════════════════════════════════════════════════
# 05 — Hiring Rate by Experience
# ══════════════════════════════════════════════════════════════════════════════
exp_hire = df.groupby('ExperienceYears')['HiringDecision'].mean() * 100
fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(exp_hire.index, exp_hire.values, alpha=0.25, color=ACCENT)
ax.plot(exp_hire.index, exp_hire.values, color=ACCENT, linewidth=2.5, marker='o', markersize=6)
ax.axhline(df['HiringDecision'].mean()*100, color='yellow', linestyle='--', linewidth=1.5,
           label=f'Overall avg ({df["HiringDecision"].mean()*100:.1f}%)')
ax.set_title('Hiring Rate by Years of Experience', fontsize=14, fontweight='bold')
ax.set_xlabel('Years of Experience'); ax.set_ylabel('Hiring Rate (%)')
ax.legend(fontsize=10); ax.set_xticks(exp_hire.index); ax.grid(alpha=0.3)
plt.tight_layout()
save('05_hiring_rate_by_experience.png')

# ══════════════════════════════════════════════════════════════════════════════
# 06 — Age Distribution: Hired vs Not Hired
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 5))
sns.kdeplot(data=df[df['HiringDecision']==1]['Age'], ax=ax,
            color=HIRED_COLOR, fill=True, alpha=0.5, label='Hired', linewidth=2)
sns.kdeplot(data=df[df['HiringDecision']==0]['Age'], ax=ax,
            color=REJECT_COLOR, fill=True, alpha=0.5, label='Not Hired', linewidth=2)
ax.set_title('Age Distribution — Hired vs Not Hired', fontsize=14, fontweight='bold')
ax.set_xlabel('Age'); ax.set_ylabel('Density'); ax.legend(fontsize=11); ax.grid(alpha=0.3)
plt.tight_layout()
save('06_age_dist_hired_vs_rejected.png')

# ══════════════════════════════════════════════════════════════════════════════
# 07 — Pairplot (scores)
# ══════════════════════════════════════════════════════════════════════════════
score_cols = ['InterviewScore','SkillScore','PersonalityScore','CompositeScore']
pair_df    = df[score_cols + ['HiringDecision_Label']].copy()
palette_pair = {'Hired': HIRED_COLOR, 'Not Hired': REJECT_COLOR}
g = sns.pairplot(pair_df, hue='HiringDecision_Label', palette=palette_pair,
                 plot_kws={'alpha': 0.45, 's': 18}, diag_kind='kde')
g.figure.suptitle('Pairplot: Assessment Scores by Hiring Decision', y=1.02, fontsize=15, fontweight='bold')
g.figure.patch.set_facecolor('#0f1117')
for ax in g.axes.flatten():
    if ax:
        ax.set_facecolor('#1a1d27')
        ax.grid(alpha=0.2, color='#2e3250')
save('07_pairplot_scores.png')

# ══════════════════════════════════════════════════════════════════════════════
# 08 — Hiring Rate by Gender & Education
# ══════════════════════════════════════════════════════════════════════════════
pivot = df.groupby(['Gender_Label','EducationLevel_Label'])['HiringDecision'].mean().unstack()*100
pivot = pivot[edu_order]
fig, ax = plt.subplots(figsize=(12, 5))
pivot.plot(kind='bar', ax=ax, color=PALETTE[:4], edgecolor='white', linewidth=0.6, width=0.7)
ax.set_title('Hiring Rate by Gender & Education Level', fontsize=14, fontweight='bold')
ax.set_xlabel('Gender'); ax.set_ylabel('Hiring Rate (%)')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(title='Education', bbox_to_anchor=(1.01,1), loc='upper left')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
save('08_hiring_rate_gender_education.png')

# ══════════════════════════════════════════════════════════════════════════════
# 09 — Distance vs Hiring
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.boxplot(data=df, x='HiringDecision_Label', y='DistanceFromCompany', ax=axes[0],
            palette={'Hired': HIRED_COLOR, 'Not Hired': REJECT_COLOR}, linewidth=1.2, width=0.5)
axes[0].set_title('Distance from Company vs Hiring Decision', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Hiring Decision'); axes[0].set_ylabel('Distance (km)'); axes[0].grid(axis='y',alpha=0.3)
sns.violinplot(data=df, x='HiringDecision_Label', y='DistanceFromCompany', ax=axes[1],
               palette={'Hired': HIRED_COLOR, 'Not Hired': REJECT_COLOR}, inner='quartile', linewidth=1.2)
axes[1].set_title('Distance Distribution (Violin)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Hiring Decision'); axes[1].set_ylabel(''); axes[1].grid(axis='y',alpha=0.3)
plt.tight_layout()
save('09_distance_vs_hiring.png')

# ══════════════════════════════════════════════════════════════════════════════
# 10 — Hiring by Age Group
# ══════════════════════════════════════════════════════════════════════════════
age_hire  = df.groupby('AgeGroup', observed=True)['HiringDecision'].agg(['mean','count']).reset_index()
age_hire['mean'] *= 100
fig, ax1 = plt.subplots(figsize=(11, 5))
bars = ax1.bar(age_hire['AgeGroup'].astype(str), age_hire['mean'],
               color=PALETTE, edgecolor='white', linewidth=0.8, width=0.6)
for bar, val in zip(bars, age_hire['mean']):
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
             f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')
ax2 = ax1.twinx()
ax2.plot(age_hire['AgeGroup'].astype(str), age_hire['count'],
         color='white', linewidth=2, marker='D', markersize=7, label='Candidate Count')
ax1.set_title('Hiring Rate & Candidate Count by Age Group', fontsize=14, fontweight='bold')
ax1.set_xlabel('Age Group'); ax1.set_ylabel('Hiring Rate (%)')
ax2.set_ylabel('Number of Candidates'); ax2.legend(loc='upper right', fontsize=10)
ax1.grid(axis='y',alpha=0.3)
plt.tight_layout()
save('10_hiring_by_age_group.png')

# ══════════════════════════════════════════════════════════════════════════════
# 11 — Score Distributions KDE
# ══════════════════════════════════════════════════════════════════════════════
scores = ['InterviewScore','SkillScore','PersonalityScore','CompositeScore']
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Score Distributions: Hired vs Not Hired', fontsize=16, fontweight='bold', y=1.01)
axes = axes.flatten()
for i, score in enumerate(scores):
    ax = axes[i]
    sns.kdeplot(data=df[df['HiringDecision']==1][score], ax=ax,
                fill=True, color=HIRED_COLOR,  alpha=0.55, linewidth=2, label='Hired')
    sns.kdeplot(data=df[df['HiringDecision']==0][score], ax=ax,
                fill=True, color=REJECT_COLOR, alpha=0.55, linewidth=2, label='Not Hired')
    m_hire = df[df['HiringDecision']==1][score].mean()
    m_rej  = df[df['HiringDecision']==0][score].mean()
    ax.axvline(m_hire, color=HIRED_COLOR,  linestyle='--', linewidth=1.5)
    ax.axvline(m_rej,  color=REJECT_COLOR, linestyle='--', linewidth=1.5)
    ax.set_title(score, fontsize=13, fontweight='bold')
    ax.set_xlabel('Score (0–100)'); ax.legend(fontsize=10); ax.grid(alpha=0.3)
    _, p = stats.ttest_ind(df[df['HiringDecision']==1][score],
                           df[df['HiringDecision']==0][score])
    ax.text(0.97, 0.97, f'p={p:.4f}', transform=ax.transAxes,
            ha='right', va='top', fontsize=9, color='white',
            bbox=dict(facecolor='#0f1117', alpha=0.7, edgecolor='none'))
plt.tight_layout()
save('11_score_distributions.png')

# ══════════════════════════════════════════════════════════════════════════════
# 12 — Scores by Education
# ══════════════════════════════════════════════════════════════════════════════
score_edu = df.groupby('EducationLevel_Label')[scores].mean().reindex(edu_order)
fig, ax = plt.subplots(figsize=(12, 5))
score_edu.plot(kind='bar', ax=ax, color=PALETTE[:4], edgecolor='white', linewidth=0.6)
ax.set_title('Average Scores by Education Level', fontsize=14, fontweight='bold')
ax.set_xlabel('Education Level'); ax.set_ylabel('Average Score (0–100)')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(bbox_to_anchor=(1.01,1), loc='upper left')
ax.grid(axis='y',alpha=0.3)
plt.tight_layout()
save('12_scores_by_education.png')

# ══════════════════════════════════════════════════════════════════════════════
# 13 — Correlation Heatmap
# ══════════════════════════════════════════════════════════════════════════════
numeric_cols = ['Age','ExperienceYears','PreviousCompanies','DistanceFromCompany',
                'InterviewScore','SkillScore','PersonalityScore','CompositeScore',
                'EducationLevel','HiringDecision']
corr_matrix = df[numeric_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
fig, ax = plt.subplots(figsize=(13, 9))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', linewidths=0.5,
            cmap=sns.diverging_palette(260, 20, s=90, l=40, as_cmap=True),
            ax=ax, vmin=-1, vmax=1, annot_kws={'size':9},
            linecolor='#0f1117', cbar_kws={'shrink':0.8})
ax.set_title('Feature Correlation Matrix', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
save('13_correlation_heatmap.png')

hire_corr = corr_matrix['HiringDecision'].drop('HiringDecision').sort_values(ascending=False)

# ══════════════════════════════════════════════════════════════════════════════
# 14 — Feature Correlation Bar
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
clr14 = [HIRED_COLOR if v >= 0 else REJECT_COLOR for v in hire_corr.values]
bars  = ax.barh(hire_corr.index[::-1], hire_corr.values[::-1],
                color=clr14[::-1], edgecolor='white', linewidth=0.5)
ax.axvline(0, color='white', linewidth=1)
for bar, val in zip(bars, hire_corr.values[::-1]):
    xpos = val+0.005 if val >= 0 else val-0.005
    ax.text(xpos, bar.get_y()+bar.get_height()/2,
            f'{val:.3f}', va='center', ha='left' if val >= 0 else 'right', fontsize=9)
ax.set_title('Correlation of Features with Hiring Decision', fontsize=14, fontweight='bold')
ax.set_xlabel('Pearson Correlation Coefficient'); ax.grid(axis='x',alpha=0.3)
plt.tight_layout()
save('14_feature_correlation_bar.png')

# ══════════════════════════════════════════════════════════════════════════════
# 15 — Recruitment Strategy Comparison
# ══════════════════════════════════════════════════════════════════════════════
strat_summary = df.groupby('RecruitmentStrategy_Label').agg(
    CandidateCount    = ('HiringDecision','count'),
    HiringRate        = ('HiringDecision','mean'),
    AvgInterviewScore = ('InterviewScore','mean'),
    AvgSkillScore     = ('SkillScore','mean'),
    AvgCompositeScore = ('CompositeScore','mean'),
).reset_index()
strat_summary['HiringRate'] *= 100
strategies = strat_summary['RecruitmentStrategy_Label']
clrs       = [PALETTE[0], PALETTE[1], PALETTE[2]]

fig, axes = plt.subplots(1, 3, figsize=(17, 5))
fig.suptitle('Recruitment Strategy Comparison', fontsize=16, fontweight='bold', y=1.02)
axes[0].bar(strategies, strat_summary['CandidateCount'], color=clrs, edgecolor='white', linewidth=0.8, width=0.5)
for i,v in enumerate(strat_summary['CandidateCount']):
    axes[0].text(i, v+5, str(v), ha='center', fontsize=11, fontweight='bold')
axes[0].set_title('Candidate Volume', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Count'); axes[0].set_ylim(0, strat_summary['CandidateCount'].max()*1.15)
axes[0].grid(axis='y',alpha=0.3)
bars2 = axes[1].bar(strategies, strat_summary['HiringRate'], color=clrs, edgecolor='white', linewidth=0.8, width=0.5)
for bar,val in zip(bars2, strat_summary['HiringRate']):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                 f'{val:.1f}%', ha='center', fontsize=11, fontweight='bold')
axes[1].axhline(df['HiringDecision'].mean()*100, color='white', linestyle='--', linewidth=1.5,
                label=f'Overall avg ({df["HiringDecision"].mean()*100:.1f}%)')
axes[1].set_title('Hiring Rate', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Hiring Rate (%)'); axes[1].set_ylim(0, strat_summary['HiringRate'].max()*1.25)
axes[1].legend(fontsize=9); axes[1].grid(axis='y',alpha=0.3)
bars3 = axes[2].bar(strategies, strat_summary['AvgCompositeScore'], color=clrs, edgecolor='white', linewidth=0.8, width=0.5)
for bar,val in zip(bars3, strat_summary['AvgCompositeScore']):
    axes[2].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                 f'{val:.1f}', ha='center', fontsize=11, fontweight='bold')
axes[2].set_title('Avg Composite Score', fontsize=12, fontweight='bold')
axes[2].set_ylabel('Score (0–100)'); axes[2].set_ylim(0, 80); axes[2].grid(axis='y',alpha=0.3)
plt.tight_layout()
save('15_recruitment_strategy_comparison.png')

# ══════════════════════════════════════════════════════════════════════════════
# 16 — Previous Companies vs Hiring
# ══════════════════════════════════════════════════════════════════════════════
prev_hire  = df.groupby('PreviousCompanies')['HiringDecision'].mean() * 100
prev_count = df.groupby('PreviousCompanies').size()
fig, ax1 = plt.subplots(figsize=(10, 5))
clrs_prev = PALETTE[:len(prev_hire)]
bars = ax1.bar(prev_hire.index.astype(str), prev_hire.values,
               color=clrs_prev, edgecolor='white', linewidth=0.8, width=0.6)
for bar,val in zip(bars, prev_hire.values):
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
             f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')
ax2 = ax1.twinx()
ax2.plot(prev_count.index.astype(str), prev_count.values,
         color='white', linewidth=2, marker='o', markersize=7, label='Count')
ax1.set_title('Hiring Rate by Number of Previous Companies', fontsize=14, fontweight='bold')
ax1.set_xlabel('Number of Previous Companies'); ax1.set_ylabel('Hiring Rate (%)')
ax2.set_ylabel('Candidate Count'); ax2.legend(loc='upper right', fontsize=9)
ax1.grid(axis='y',alpha=0.3)
plt.tight_layout()
save('16_previous_companies_vs_hiring.png')

# ══════════════════════════════════════════════════════════════════════════════
# 00 — Executive Dashboard
# ══════════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(20, 14), facecolor='#0f1117')
gs  = GridSpec(3, 4, figure=fig, hspace=0.5, wspace=0.4)

ax1 = fig.add_subplot(gs[0,0])
sizes = [df['HiringDecision'].sum(), (df['HiringDecision']==0).sum()]
ax1.pie(sizes, colors=[HIRED_COLOR,REJECT_COLOR], autopct='%1.0f%%', startangle=140,
        wedgeprops={'edgecolor':'#0f1117','linewidth':2},
        textprops={'color':'white','fontsize':11,'fontweight':'bold'}, pctdistance=0.75)
centre = plt.Circle((0,0), 0.55, fc='#1a1d27')
ax1.add_patch(centre)
ax1.text(0, 0, '31%\nHired', ha='center', va='center', fontsize=13, fontweight='bold', color='white')
ax1.set_title('Hiring Split', fontsize=12, fontweight='bold', pad=10)

ax2 = fig.add_subplot(gs[0,1:3])
ax2.bar(edu_hire['EducationLevel'], edu_hire['HiringRate'],
        color=PALETTE[:4], edgecolor='white', linewidth=0.6, width=0.55)
ax2.axhline(31, color='white', linestyle='--', linewidth=1.2, alpha=0.7)
ax2.set_title('Hiring Rate by Education', fontsize=12, fontweight='bold')
ax2.set_ylabel('%'); ax2.grid(axis='y',alpha=0.3)

ax3 = fig.add_subplot(gs[0,3])
ax3.barh(strat_summary['RecruitmentStrategy_Label'], strat_summary['HiringRate'],
         color=clrs, edgecolor='white', linewidth=0.6, height=0.5)
ax3.set_title('Hire Rate by Strategy', fontsize=12, fontweight='bold')
ax3.set_xlabel('%'); ax3.grid(axis='x',alpha=0.3); ax3.invert_yaxis()

ax4 = fig.add_subplot(gs[1,:])
score_long = df.melt(id_vars='HiringDecision_Label',
                     value_vars=['InterviewScore','SkillScore','PersonalityScore'],
                     var_name='ScoreType', value_name='Score')
sns.boxplot(data=score_long, x='ScoreType', y='Score', hue='HiringDecision_Label', ax=ax4,
            palette={'Hired':HIRED_COLOR,'Not Hired':REJECT_COLOR}, linewidth=1, width=0.5)
ax4.set_title('Score Comparison: Hired vs Not Hired', fontsize=13, fontweight='bold')
ax4.set_xlabel(''); ax4.set_ylabel('Score (0–100)'); ax4.grid(axis='y',alpha=0.3); ax4.legend(fontsize=10)

ax5 = fig.add_subplot(gs[2,:2])
ax5.fill_between(exp_hire.index, exp_hire.values, alpha=0.25, color=ACCENT)
ax5.plot(exp_hire.index, exp_hire.values, color=ACCENT, linewidth=2.5, marker='o', markersize=5)
ax5.axhline(31, color='yellow', linestyle='--', linewidth=1.2, alpha=0.7)
ax5.set_title('Hiring Rate by Experience (Years)', fontsize=13, fontweight='bold')
ax5.set_xlabel('Experience (Years)'); ax5.set_ylabel('%'); ax5.grid(alpha=0.3)

ax6 = fig.add_subplot(gs[2,2:])
clrs_c = [HIRED_COLOR if v >= 0 else REJECT_COLOR for v in hire_corr.values]
ax6.barh(hire_corr.index, hire_corr.values, color=clrs_c, edgecolor='white', linewidth=0.5)
ax6.axvline(0, color='white', linewidth=1)
ax6.set_title('Feature → Hiring Correlation', fontsize=13, fontweight='bold')
ax6.set_xlabel('Pearson r'); ax6.grid(axis='x',alpha=0.3)

fig.suptitle('Recruitment EDA — Executive Dashboard', fontsize=20,
             fontweight='bold', color='white', y=1.01)
save('00_executive_dashboard.png')

print('\n🎉 All charts saved to Outputs/')
