"""
generate_charts.py – runs at Docker build time to pre-render all Matplotlib figures.
"""
import os, json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
CHARTS_DIR = os.path.join(BASE_DIR, 'static', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(BASE_DIR, 'titanic.csv'))

# ── Palette ──────────────────────────────────────────────────
DARK_BG  = '#0a0a0f'
CARD_BG  = '#12121a'
ACCENT1  = '#e63946'
ACCENT2  = '#4cc9f0'
ACCENT3  = '#f8c537'
TEXT     = '#e8e8f0'
GRID     = '#1e1e2e'

def setup_fig(figsize=(10, 5)):
    fig, ax = plt.subplots(figsize=figsize, facecolor=DARK_BG)
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=TEXT, labelsize=10)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.grid(color=GRID, linewidth=0.5, alpha=0.7)
    return fig, ax

def save(fig, name):
    path = os.path.join(CHARTS_DIR, name)
    fig.savefig(path, dpi=120, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print(f'  ✓  {name}')

# 1. Survival by class
fig, ax = setup_fig((9, 5))
surv = df.groupby(['Pclass', 'Survived']).size().unstack(fill_value=0)
x, w = np.arange(len(surv)), 0.35
b1 = ax.bar(x - w/2, surv[0], w, color=ACCENT1, alpha=0.85, label='Did Not Survive')
b2 = ax.bar(x + w/2, surv[1], w, color=ACCENT2, alpha=0.85, label='Survived')
ax.set_xticks(x); ax.set_xticklabels(['1st Class','2nd Class','3rd Class'], fontsize=12, color=TEXT)
ax.set_ylabel('Passengers', color=TEXT, fontsize=11)
ax.set_title('Survival by Passenger Class', fontsize=15, color=TEXT, pad=15, fontweight='bold')
for bar in list(b1)+list(b2):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+3,
            str(int(bar.get_height())), ha='center', va='bottom', color=TEXT, fontsize=9)
ax.legend(facecolor=CARD_BG, edgecolor=GRID, labelcolor=TEXT, fontsize=10)
plt.tight_layout(); save(fig, 'survival_by_class.png')

# 2. Age distribution
fig, ax = setup_fig((10, 5))
ax.hist(df[df['Survived']==0]['Age'].dropna(), bins=30, color=ACCENT1, alpha=0.7, label='Did Not Survive')
ax.hist(df[df['Survived']==1]['Age'].dropna(), bins=30, color=ACCENT2, alpha=0.7, label='Survived')
ax.set_xlabel('Age', color=TEXT, fontsize=11); ax.set_ylabel('Count', color=TEXT, fontsize=11)
ax.set_title('Age Distribution by Survival Outcome', fontsize=15, color=TEXT, pad=15, fontweight='bold')
ax.legend(facecolor=CARD_BG, edgecolor=GRID, labelcolor=TEXT, fontsize=10)
plt.tight_layout(); save(fig, 'age_distribution.png')

# 3. Survival by sex
fig, ax = setup_fig((7, 5))
ss = df.groupby('Sex')['Survived'].mean() * 100
cols = [ACCENT2 if s == 'female' else ACCENT1 for s in ss.index]
bars = ax.bar(ss.index, ss.values, color=cols, alpha=0.85, width=0.4)
for bar, val in zip(bars, ss.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5,
            f'{val:.1f}%', ha='center', color=TEXT, fontsize=13, fontweight='bold')
ax.set_ylabel('Survival Rate (%)', color=TEXT, fontsize=11)
ax.set_title('Survival Rate by Gender', fontsize=15, color=TEXT, pad=15, fontweight='bold')
ax.set_ylim(0, 100); ax.set_xticklabels(['Female','Male'], fontsize=12)
plt.tight_layout(); save(fig, 'survival_by_sex.png')

# 4. Fare distribution
fig, ax = setup_fig((10, 5))
ax.hist(np.log1p(df[df['Survived']==0]['Fare']), bins=35, color=ACCENT1, alpha=0.7, label='Did Not Survive')
ax.hist(np.log1p(df[df['Survived']==1]['Fare']), bins=35, color=ACCENT3, alpha=0.7, label='Survived')
ax.set_xlabel('Log(Fare + 1)', color=TEXT, fontsize=11); ax.set_ylabel('Count', color=TEXT, fontsize=11)
ax.set_title('Fare Distribution by Survival (Log Scale)', fontsize=15, color=TEXT, pad=15, fontweight='bold')
ax.legend(facecolor=CARD_BG, edgecolor=GRID, labelcolor=TEXT, fontsize=10)
plt.tight_layout(); save(fig, 'fare_distribution.png')

# 5. Embarkation survival
fig, ax = setup_fig((8, 5))
emb = df.groupby('Embarked')['Survived'].agg(['sum','count'])
emb['rate'] = emb['sum'] / emb['count'] * 100
port_labels = {'S':'Southampton','C':'Cherbourg','Q':'Queenstown'}
labels = [port_labels.get(p, p) for p in emb.index]
bars = ax.bar(labels, emb['rate'], color=[ACCENT2, ACCENT3, ACCENT1][:len(labels)], alpha=0.85, width=0.4)
for bar, val in zip(bars, emb['rate']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.2,
            f'{val:.1f}%', ha='center', color=TEXT, fontsize=12, fontweight='bold')
ax.set_ylabel('Survival Rate (%)', color=TEXT, fontsize=11)
ax.set_title('Survival Rate by Port of Embarkation', fontsize=15, color=TEXT, pad=15, fontweight='bold')
ax.set_ylim(0, 80); plt.tight_layout(); save(fig, 'survival_by_embark.png')

# 6. Correlation heatmap
fig, ax = setup_fig((8, 6))
corr = df[['Survived','Pclass','Age','SibSp','Parch','Fare']].corr()
cmap = sns.diverging_palette(10, 220, as_cmap=True)
sns.heatmap(corr, ax=ax, cmap=cmap, vmin=-1, vmax=1, center=0,
            annot=True, fmt='.2f', annot_kws={'size':10,'color':TEXT},
            linewidths=0.5, linecolor=DARK_BG, cbar_kws={'shrink':0.8})
ax.set_title('Feature Correlation Matrix', fontsize=15, color=TEXT, pad=15, fontweight='bold')
ax.tick_params(colors=TEXT, labelsize=9)
plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
plt.setp(ax.get_yticklabels(), rotation=0)
cb = ax.collections[0].colorbar
plt.setp(cb.ax.yaxis.get_ticklabels(), color=TEXT)
plt.tight_layout(); save(fig, 'correlation_heatmap.png')

# Stats JSON
stats = {
    'total_passengers': int(len(df)),
    'total_survived':   int(df['Survived'].sum()),
    'survival_rate':    round(float(df['Survived'].mean()*100), 1),
    'avg_age':          round(float(df['Age'].mean()), 1),
    'avg_fare':         round(float(df['Fare'].mean()), 2),
    'missing_age':      int(df['Age'].isna().sum()),
    'class_breakdown':  {int(k): int(v) for k, v in df['Pclass'].value_counts().sort_index().items()},
    'sex_breakdown':    {k: int(v) for k, v in df['Sex'].value_counts().items()},
    'class_survival_rates': {int(k): round(float(v*100),1)
                             for k, v in df.groupby('Pclass')['Survived'].mean().items()},
    'sex_survival_rates': {k: round(float(v*100),1)
                           for k, v in df.groupby('Sex')['Survived'].mean().items()},
}
with open(os.path.join(BASE_DIR, 'stats.json'), 'w') as f:
    json.dump(stats, f, indent=2)

print('\nAll charts and stats generated ✓')
