import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# ============================================================================
# LOAD DATA
# ============================================================================

netflix = pd.read_csv('data/netflix_titles.csv')
disney = pd.read_csv('data/disney_plus_titles.csv')
oscars = pd.read_csv('data/oscar_award.csv', on_bad_lines='skip', sep='\t')  # Tab-separated

# Check what we have
print(oscars['Category'].value_counts().head(10))


# ============================================================================
# HELPERS
# ============================================================================

# Constants for charts
CATEGORIES = ['Winners', 'Nominees']
PLATFORMS = ['Netflix', 'Disney+']
COLORS = ['#E50914', '#1E4B8C']

# Clean titles
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


def mark_oscar_awards(netflix: pd.DataFrame, disney: pd.DataFrame, oscars: pd.DataFrame):
    """
    Add Oscar-related flags (winner/nominee) for Best Picture and Animated Feature
    to the given Netflix and Disney DataFrames.

    Returns: updated (netflix, disney)
    """
    # Clean titles in Oscar dataset
    oscars = oscars.copy()
    oscars['clean'] = oscars['Film'].apply(clean_title)

    # Separate categories
    best_picture = oscars[oscars['Category'] == 'BEST PICTURE']
    animated = oscars[oscars['Category'] == 'ANIMATED FEATURE FILM']

    # Get sets of winners and nominees
    bp_winners = set(best_picture[best_picture['Winner'] == True]['clean'])
    bp_nominees = set(best_picture[best_picture['Winner'].isna()]['clean'])
    anim_winners = set(animated[animated['Winner'] == True]['clean'])
    anim_nominees = set(animated[animated['Winner'].isna()]['clean'])

    # Clean streaming service titles
    for df in [netflix, disney]:
        df['clean'] = df['title'].apply(clean_title)
        df['bp_winner'] = df['clean'].isin(bp_winners)
        df['bp_nominee'] = df['clean'].isin(bp_nominees)
        df['anim_winner'] = df['clean'].isin(anim_winners)
        df['anim_nominee'] = df['clean'].isin(anim_nominees)

    return netflix, disney


def summarize_oscar_wins(netflix: pd.DataFrame, disney: pd.DataFrame) -> pd.DataFrame:
    """
    Return a summary DataFrame with Oscar winner counts per platform.
    """
    data = {
        'Platform': ['Netflix', 'Disney+'],
        'Best Picture Wins': [
            netflix['bp_winner'].sum(),
            disney['bp_winner'].sum()
        ],
        'Animated Wins': [
            netflix['anim_winner'].sum(),
            disney['anim_winner'].sum()
        ],
    }
    df = pd.DataFrame(data)
    df['Total Oscar Wins'] = df['Best Picture Wins'] + df['Animated Wins']
    return df

netflix, disney = mark_oscar_awards(netflix, disney, oscars)

# Data Points for Visualisation
netflix_bp_winners = netflix['bp_winner'].sum()
netflix_bp_nominees = netflix['bp_nominee'].sum()
netflix_anim_winners = netflix['anim_winner'].sum()
netflix_anim_nominees = netflix['anim_nominee'].sum()

disney_bp_winners = disney['bp_winner'].sum()
disney_bp_nominees = disney['bp_nominee'].sum()
disney_anim_winners = disney['anim_winner'].sum()
disney_anim_nominees = disney['anim_nominee'].sum()

# Totals
netflix_total = netflix_bp_winners + netflix_anim_winners
disney_total = disney_bp_winners + disney_anim_winners

# Volumes
volumes = [len(netflix), len(disney)]

# Density per 1000 titles
netflix_density = netflix_total / len(netflix) * 1000
disney_density = disney_total / len(disney) * 1000
densities = [netflix_density, disney_density]


# ============================================================================
# VISUALISATION
# ============================================================================

# Chart 1: Category breakdown
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

x = np.arange(len(CATEGORIES))
width = 0.35

# Best Picture
ax1.bar(x - width/2, [netflix_bp_winners, netflix_bp_nominees], width, 
        label='Netflix', color=COLORS[0])
ax1.bar(x + width/2, [disney_bp_winners, disney_bp_nominees], width, 
        label='Disney+', color=COLORS[1])
ax1.set_title('Best Picture', fontweight='bold', fontsize=14)
ax1.set_ylabel('Number of Films')
ax1.set_xticks(x)
ax1.set_xticklabels(CATEGORIES)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

for container in ax1.containers:
    ax1.bar_label(container, fontweight='bold', fontsize=10)

# Animated Feature
ax2.bar(x - width/2, [netflix_anim_winners, netflix_anim_nominees], width, 
        label='Netflix', color=COLORS[0])
ax2.bar(x + width/2, [disney_anim_winners, disney_anim_nominees], width, 
        label='Disney+', color=COLORS[1])
ax2.set_title('Animated Feature', fontweight='bold', fontsize=14)
ax2.set_ylabel('Number of Films')
ax2.set_xticks(x)
ax2.set_xticklabels(CATEGORIES)
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

for container in ax2.containers:
    ax2.bar_label(container, fontweight='bold', fontsize=10)

plt.suptitle('Oscar Winners by Category: Netflix vs Disney+', 
             fontweight='bold', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('oscar_charts/oscar_by_category.png', dpi=300, bbox_inches='tight')


# Chart 2: Density (per 1000 titles)
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(PLATFORMS, densities, color=COLORS, edgecolor='black', linewidth=2)
ax.set_title('Oscar Winners per 1,000 Titles', 
             fontweight='bold', fontsize=16)
ax.set_ylim(0, max(densities) * 1.15)
ax.grid(axis='y', alpha=0.3)

for i, v in enumerate(densities):
    ax.text(i, v + 0.2, f'{v:.1f}', ha='center', fontweight='bold', fontsize=14)

plt.tight_layout()
plt.savefig('oscar_charts/oscar_density.png', dpi=300, bbox_inches='tight')


# Chart 3
fig, ax = plt.subplots(figsize=(10, 8))

# Create scatter plot
for i, platform in enumerate(PLATFORMS):
    ax.scatter(volumes[i], densities[i], s=1000, c=COLORS[i], 
               alpha=1, zorder=3)
    
    # Add platform labels
    ax.text(volumes[i], densities[i], platform, 
            ha='center', va='center', fontweight='bold', 
            fontsize=8, color='white', zorder=4)

# Add quadrant lines
ax.axhline(y=np.mean(densities), color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.axvline(x=np.mean(volumes), color='gray', linestyle='--', alpha=0.5, linewidth=1)

# Labels and styling
ax.set_xlabel('Catalog Size (Number of Titles)', fontsize=13, fontweight='bold')
ax.set_ylabel('Prestige Density (Awards per 1,000 Titles)', fontsize=13, fontweight='bold')
ax.set_title('Strategic Positioning: Volume vs Quality', fontsize=16, fontweight='bold', pad=20)

# Add quadrant labels
ax.text(volumes[0] * 0.95, densities[1] * 0.95, 'High Volume\nHigh Quality', 
        ha='right', va='top', fontsize=10, style='italic', color='gray')
ax.text(volumes[1] * 1.05, densities[1] * 0.95, 'Low Volume\nHigh Quality', 
        ha='left', va='top', fontsize=10, style='italic', color='gray', 
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
ax.text(volumes[0] * 0.95, densities[0] * 1.05, 'High Volume\nLow Quality', 
        ha='right', va='bottom', fontsize=10, style='italic', color='gray',
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.3))
ax.text(volumes[1] * 1.05, densities[0] * 1.05, 'Low Volume\nLow Quality', 
        ha='left', va='bottom', fontsize=10, style='italic', color='gray')

# Grid
ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
ax.set_axisbelow(True)

# Add annotations with arrows
ax.annotate('Volume Strategy', 
            xy=(volumes[0], densities[0]), 
            xytext=(volumes[0] - 1000, densities[0] + 2),
            fontsize=10, style='italic',
            arrowprops=dict(arrowstyle='->', color='#E50914', lw=1.5))

ax.annotate('Quality Strategy', 
            xy=(volumes[1], densities[1]), 
            xytext=(volumes[1] + 1500, densities[1] - 2),
            fontsize=10, style='italic',
            arrowprops=dict(arrowstyle='->', color='#1E4B8C', lw=1.5))

plt.tight_layout()
plt.savefig('oscar_charts/strategic_positioning_matrix.png', dpi=300, bbox_inches='tight')
plt.show()
