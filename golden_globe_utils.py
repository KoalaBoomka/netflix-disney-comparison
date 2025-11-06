import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# ============================================================================
# LOAD DATA
# ============================================================================
netflix = pd.read_csv('data/netflix_titles.csv')
disney = pd.read_csv('data/disney_plus_titles.csv')
golden_globe = pd.read_csv('data/golden_globe_award.csv', on_bad_lines='skip')

# ============================================================================
# HELPERS
# ============================================================================

# Constants for charts
CATEGORIES = ['Winners', 'Nominees']
PLATFORMS = ['Netflix', 'Disney+']
COLORS = ['#E50914', '#1E4B8C']

BEST_CONTENT_CATEGORIES = [
    'Best Television Limited Series, Anthology Series, or Motion Picture Made for Television',
    'Best Television Series - Drama',
    'Best Television Series - Musical or Comedy',
    'Best Motion Picture - Drama',
    'Best Motion Picture - Musical or Comedy',
    'Best Motion Picture – Non-English Language'
]

# Clean function
def clean_title(title: str) -> str:
    """
    Clean up movie titles by lowercasing, removing year markers like '(2020)',
    punctuation, and extra spaces.
    """
    if pd.isna(title): return ""
    title = str(title).lower()
    title = re.sub(r'\s*\(\d{4}\)', '', title)
    title = re.sub(r'[^a-z0-9\s]', '', title)
    return ' '.join(title.split())


def mark_golden_globes(netflix: pd.DataFrame, disney: pd.DataFrame, gg: pd.DataFrame):
    """
    Add Golden Globe-related flags (winner/nominee) for Best Picture/TV Series
    and Animated Feature to the given Netflix and Disney DataFrames.

    Returns: updated (netflix, disney)
    """
    gg = gg.copy()
    gg['clean'] = gg['title'].apply(clean_title)

    gg_best = gg[gg['award'].isin(BEST_CONTENT_CATEGORIES)]
    gg_anim = gg[gg['award'] == 'Best Motion Picture - Animated']

    # Sets of winners/nominees
    best_winners = set(gg_best[gg_best['winner'] == True]['clean'])
    best_nominees = set(gg_best[gg_best['winner'] == False]['clean'])
    gg_anim_winners = set(gg_anim[gg_anim['winner'] == True]['clean'])
    gg_anim_nominees = set(gg_anim[gg_anim['winner'] == False]['clean'])

    for df in [netflix, disney]:
        df['clean'] = df['title'].apply(clean_title)
        df['gg_best_winner'] = df['clean'].isin(best_winners)
        df['gg_best_nominee'] = df['clean'].isin(best_nominees)
        df['gg_anim_winner'] = df['clean'].isin(gg_anim_winners)
        df['gg_anim_nominee'] = df['clean'].isin(gg_anim_nominees)

    return netflix, disney


def summarize_golden_globe_wins(netflix: pd.DataFrame, disney: pd.DataFrame) -> pd.DataFrame:
    """
    Return a summary DataFrame with Golden Globe winner counts per platform.
    """
    data = {
        'Platform': ['Netflix', 'Disney+'],
        'Best Picture Wins': [
            netflix['gg_best_winner'].sum(),
            disney['gg_best_winner'].sum()
        ],
        'Animated Wins': [
            netflix['gg_anim_winner'].sum(),
            disney['gg_anim_winner'].sum()
        ],
    }
    df = pd.DataFrame(data)
    df['Total Golden Globe Wins'] = df['Best Picture Wins'] + df['Animated Wins']
    return df

netflix, disney = mark_golden_globes(netflix, disney, golden_globe)


# Data Points for Visualisation
netflix_gg_best_winners = netflix['gg_best_winner'].sum()
netflix_gg_best_nominees = netflix['gg_best_nominee'].sum()
netflix_gg_anim_winners = netflix['gg_anim_winner'].sum()
netflix_gg_anim_nominees = netflix['gg_anim_nominee'].sum()

disney_gg_best_winners = disney['gg_best_winner'].sum()
disney_gg_best_nominees = disney['gg_best_nominee'].sum()
disney_gg_anim_winners = disney['gg_anim_winner'].sum()
disney_gg_anim_nominees = disney['gg_anim_nominee'].sum()

# Totals
netflix_total = netflix_gg_best_winners + netflix_gg_anim_winners
disney_total = disney_gg_best_winners + disney_gg_anim_winners
totals = [netflix_total, disney_total]

# Density per platform
netflix_density = (netflix_total / len(netflix)) * 1000
disney_density = (disney_total / len(disney)) * 1000
densities = [netflix_density, disney_density]


# ============================================================================
# VISUALIZATION
# ============================================================================

# Chart 1
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

x = np.arange(len(CATEGORIES))
width = 0.35

# Best Picture/TV
ax1.bar(x - width/2, [netflix_gg_best_winners, netflix_gg_best_nominees], width, 
        label='Netflix', color=COLORS[0])
ax1.bar(x + width/2, [disney_gg_best_winners, disney_gg_best_nominees], width, 
        label='Disney+', color=COLORS[1])
ax1.set_title('Best Picture/TV Series', fontweight='bold', fontsize=14)
ax1.set_ylabel('Number of Titles')
ax1.set_xticks(x)
ax1.set_xticklabels(CATEGORIES)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

for container in ax1.containers:
    ax1.bar_label(container, fontweight='bold', fontsize=10)

# Animated
ax2.bar(x - width/2, [netflix_gg_anim_winners, netflix_gg_anim_nominees], width, 
        label='Netflix', color=COLORS[0])
ax2.bar(x + width/2, [disney_gg_anim_winners, disney_gg_anim_nominees], width, 
        label='Disney+', color=COLORS[1])
ax2.set_title('Best Animated Feature', fontweight='bold', fontsize=14)
ax2.set_ylabel('Number of Titles')
ax2.set_xticks(x)
ax2.set_xticklabels(CATEGORIES)
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

for container in ax2.containers:
    ax2.bar_label(container, fontweight='bold', fontsize=10)

plt.suptitle('Golden Globe Awards by Category: Netflix vs Disney+', 
             fontweight='bold', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('golden_globe_charts/gg_by_category.png', dpi=300, bbox_inches='tight')


# Chart 2: Density (per 1000 titles)
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(PLATFORMS, densities, color=COLORS, edgecolor='black', linewidth=2)
ax.set_title('Golden Globe Winners per 1,000 Titles', 
             fontweight='bold', fontsize=16)
ax.set_ylim(0, max(densities) * 1.15)
ax.grid(axis='y', alpha=0.3)

for i, v in enumerate(densities):
    ax.text(i, v + 0.2, f'{v:.1f}', ha='center', fontweight='bold', fontsize=14)

plt.tight_layout()
plt.savefig('golden_globe_charts/gg_density.png', dpi=300, bbox_inches='tight')
plt.show()