import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from oscar_utils import mark_oscar_awards
from golden_globe_utils import mark_golden_globes

# Load data
netflix = pd.read_csv('data/netflix_titles.csv')
disney = pd.read_csv('data/disney_plus_titles.csv')
oscars = pd.read_csv('data/oscar_award.csv', on_bad_lines='skip', sep='\t')  
golden_globe = pd.read_csv('data/golden_globe_award.csv', on_bad_lines='skip')

# ============================================================================
# HELPERS
# ============================================================================

# Constants for charts
CATEGORIES = ['Winners', 'Nominees']
PLATFORMS = ['Netflix', 'Disney+']
COLORS = ['#E50914', '#1E4B8C']

OSCAR_COLOR = "#D4AF37"
BOTH_COLOR = "#046307"
GG_COLOR = "#FFD700"

netflix, disney = mark_oscar_awards(netflix, disney, oscars)
netflix, disney = mark_golden_globes(netflix, disney, golden_globe)

# Create flags for any award
netflix['has_oscar'] = netflix['bp_winner'] | netflix['anim_winner']
netflix['has_gg'] = netflix['gg_best_winner'] | netflix['gg_anim_winner'] 
netflix['has_any_award'] = netflix['has_oscar'] | netflix['has_gg']

disney['has_oscar'] = disney['bp_winner'] | disney['anim_winner'] 
disney['has_gg'] = disney['gg_best_winner'] | disney['gg_anim_winner'] 
disney['has_any_award'] = disney['has_oscar'] | disney['has_gg']

# Count winners
netflix_oscar_total = netflix[['bp_winner', 'anim_winner']].sum().sum()
disney_oscar_total = disney[['bp_winner', 'anim_winner']].sum().sum()

netflix_golden_globe_total = netflix[['gg_best_winner', 'gg_anim_winner']].sum().sum()
disney_golden_globe_total = disney[['gg_best_winner', 'gg_anim_winner']].sum().sum()

# Count nominees
netflix_oscar_nom_total = netflix[['bp_nominee', 'anim_nominee']].sum().sum()
disney_oscar_nom_total = disney[['bp_nominee', 'anim_nominee']].sum().sum()

netflix_golden_globe_nom_total = netflix[['gg_best_nominee', 'gg_anim_nominee']].sum().sum()
disney_golden_globe_nom_total = disney[['gg_best_nominee', 'gg_anim_nominee']].sum().sum()

# Count overlap and exclusive wards
netflix_both = netflix[netflix['has_oscar'] & netflix['has_gg']].shape[0]
netflix_oscar_only = netflix[netflix['has_oscar'] & ~netflix['has_gg']].shape[0]
netflix_gg_only = netflix[netflix['has_gg'] & ~netflix['has_oscar']].shape[0]

disney_both = disney[disney['has_oscar'] & disney['has_gg']].shape[0]
disney_oscar_only = disney[disney['has_oscar'] & ~disney['has_gg']].shape[0]
disney_gg_only = disney[disney['has_gg'] & ~disney['has_oscar']].shape[0]

netflix_total_awards = netflix['has_any_award'].sum()
disney_total_awards = disney['has_any_award'].sum()

totals = [netflix_total_awards, disney_total_awards]

# Data Points for Visualisation
# Oscar
netflix_oscar_vals = [netflix_oscar_total, netflix_oscar_nom_total]
disney_oscar_vals = [disney_oscar_total, disney_oscar_nom_total]

# Golden Globe
netflix_gg_vals = [netflix_golden_globe_total, netflix_golden_globe_nom_total]
disney_gg_vals = [disney_golden_globe_total, disney_golden_globe_nom_total]

# Density
nf_density = (netflix_total_awards / len(netflix)) * 1000
ds_density = (disney_total_awards / len(disney)) * 1000
densities = [nf_density, ds_density]

volumes = [len(netflix), len(disney)]


# ============================================================================
# VISUALIZATION
# ============================================================================

# Chart 1: Side-by-Side Comparison (Oscar vs GG)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

x = np.arange(2)
width = 0.35

ax1.bar(x - width/2, netflix_oscar_vals, width, label='Netflix', color=COLORS[0])
ax1.bar(x + width/2, disney_oscar_vals, width, label='Disney+', color=COLORS[1])
ax1.set_title('Oscar Awards', fontweight='bold', fontsize=14)
ax1.set_ylabel('Number of Films', fontsize=12)
ax1.set_xticks(x)
ax1.set_xticklabels(CATEGORIES)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

for container in ax1.containers:
    ax1.bar_label(container, fontweight='bold', fontsize=10)

ax2.bar(x - width/2, netflix_gg_vals, width, label='Netflix', color=COLORS[0])
ax2.bar(x + width/2, disney_gg_vals, width, label='Disney+', color=COLORS[1])
ax2.set_title('Golden Globe Awards', fontweight='bold', fontsize=14)
ax2.set_ylabel('Number of Films', fontsize=12)
ax2.set_xticks(x)
ax2.set_xticklabels(CATEGORIES)
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

for container in ax2.containers:
    ax2.bar_label(container, fontweight='bold', fontsize=10)

plt.suptitle('Netflix vs Disney+: Oscar & Golden Globe Comparison', 
             fontweight='bold', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('combined_charts/combined_oscar_gg.png', dpi=300, bbox_inches='tight')


# Chart 2: Total Unique Award Content
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(PLATFORMS, totals, color=COLORS, edgecolor='black', linewidth=2)
ax.set_ylabel('Total Unique Award Films', fontsize=13)
ax.set_title('Total Award-Winning Content (Oscar + Golden Globe)', fontweight='bold', fontsize=16)
ax.set_ylim(0, max(totals) * 1.15)
ax.grid(axis='y', alpha=0.3)

for i, v in enumerate(totals):
    ax.text(i, v + 3, str(v), ha='center', fontweight='bold', fontsize=14)

plt.tight_layout()
plt.savefig('combined_charts/total_awards.png', dpi=300, bbox_inches='tight')


# Chart 3: Stacked Bar (Oscar + GG breakdown)
fig, ax = plt.subplots(figsize=(10, 6))

# Stack the bars
x_pos = np.arange(len(PLATFORMS))
width = 0.6

p1 = ax.bar(x_pos, [netflix_oscar_only, disney_oscar_only], width, 
            label='Oscar Only', color=OSCAR_COLOR, edgecolor='black')
p2 = ax.bar(x_pos, [netflix_both, disney_both], width, 
            bottom=[netflix_oscar_only, disney_oscar_only], 
            label='Both Awards', color=BOTH_COLOR, edgecolor='black')
p3 = ax.bar(x_pos, [netflix_gg_only, disney_gg_only], width, 
            bottom=[netflix_oscar_only + netflix_both, disney_oscar_only + disney_both],
            label='Golden Globe Only', color=GG_COLOR, edgecolor='black')

ax.set_ylabel('Number of Films', fontsize=13)
ax.set_ylim(0, max(totals) * 1.15)
ax.set_title('Oscar, Golden Globe and Both', 
             fontweight='bold', fontsize=16)
ax.set_xticks(x_pos)
ax.set_xticklabels(PLATFORMS)
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)

# Add total labels
for i, total in enumerate(totals):
    ax.text(i, total + 2, str(total), ha='center', fontweight='bold', fontsize=14)

plt.tight_layout()
plt.savefig('combined_charts/stacked_awards_unique.png', dpi=300, bbox_inches='tight')


# Chart 4: Prestige Density
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(PLATFORMS, densities, color=COLORS, edgecolor='black', linewidth=2)
ax.set_ylabel('Award Films per 1,000 Titles', fontsize=13)
ax.set_title('Oscar and Golden Globe Winners Density', fontweight='bold', fontsize=16)
ax.set_ylim(0, max(densities) * 1.15)
ax.grid(axis='y', alpha=0.3)

for i, v in enumerate(densities):
    ax.text(i, v + 1, f'{v:.1f}', ha='center', fontweight='bold', fontsize=14)

plt.tight_layout()
plt.savefig('combined_charts/award_density.png', dpi=300, bbox_inches='tight')


# Chart 5: Strategic Positioning Matrix
fig, ax = plt.subplots(figsize=(10, 8))

# Scatter plot
for i, platform in enumerate(PLATFORMS):
    ax.scatter(volumes[i], densities[i], s=2000, c=COLORS[i], 
               alpha=1, zorder=3)
    ax.text(volumes[i], densities[i], platform, 
            ha='center', va='center', fontweight='bold', 
            fontsize=10, color='white', zorder=4)

# Quadrant lines
ax.axhline(y=np.mean(densities), color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.axvline(x=np.mean(volumes), color='gray', linestyle='--', alpha=0.5, linewidth=1)

ax.set_xlabel('Catalog Size (Number of Titles)', fontsize=13, fontweight='bold')
ax.set_ylabel('Prestige Density (Awards per 1,000 Titles)', fontsize=13, fontweight='bold')
ax.set_title('Strategic Positioning: Volume vs Quality', fontsize=16, fontweight='bold', pad=20)

# Annotations
ax.annotate('Volume Strategy', 
            xy=(volumes[0], densities[0]), 
            xytext=(volumes[0] - 1000, densities[0] + 2),
            fontsize=11, style='italic',
            arrowprops=dict(arrowstyle='->', color=COLORS[0], lw=1.5))

ax.annotate('Quality Strategy', 
            xy=(volumes[1], densities[1]), 
            xytext=(volumes[1] + 1500, densities[1] - 2),
            fontsize=11, style='italic',
            arrowprops=dict(arrowstyle='->', color=COLORS[1], lw=1.5))

ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig('combined_charts/strategic_positioning.png', dpi=300, bbox_inches='tight')

# ============================================================================ 
# FINAL SUMMARY
# ============================================================================

summary = pd.DataFrame({
    'Platform': PLATFORMS,
    'Total Awards': totals,
    'Oscar Wins': [netflix_oscar_total, disney_oscar_total],
    'Golden Globe Wins': [netflix_golden_globe_total, disney_golden_globe_total],
    'Both Awards': [netflix_both, disney_both],
    'Density (per 1,000 titles)': [f"{d:.2f}" for d in densities]
})

print("\n=== Summary Table ===")
print(summary)
print("\nThank you for reading!")
