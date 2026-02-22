"""
Gen Z vs Millennials — Investment Intelligence Dashboard
========================================================
Python / Matplotlib dashboard using real data from:
  1. FINRA Foundation & CFA Institute (2023) — n=2,872
  2. Charles Schwab Modern Wealth Survey Wave 2 (Oct 2025) — n=2,400
  3. Motley Fool Generational Investing Trends Survey (July 2025) — n=2,000

Run:
    python3 genz_vs_millennials_dashboard.py

Output:
    genz_vs_millennials_dashboard.png  (high-res, 3600×2400)

Requirements:
    pip install matplotlib numpy
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ════════════════════════════════════════════════════════════
#  PALETTE & THEME
# ════════════════════════════════════════════════════════════
BG        = '#06080F'
SURFACE   = '#0B0F1A'
CARD      = '#0F1520'
BORDER    = '#1C2740'
GZ        = '#00D4FF'
ML        = '#B06EFF'
GZ_DIM    = '#00D4FF2A'
ML_DIM    = '#B06EFF2A'
GREEN     = '#00E5A0'
GOLD      = '#FFB830'
RED       = '#FF4D6A'
TEXT      = '#C8D6EF'
MUTED     = '#4A5878'
WHITE     = '#EEF4FF'

GZ_ALPHA  = (0, 212/255, 1.0, 0.18)
ML_ALPHA  = (176/255, 110/255, 1.0, 0.18)
GZ_EDGE   = GZ
ML_EDGE   = ML

# ════════════════════════════════════════════════════════════
#  DATA (ALL FROM PRIMARY SOURCES — NO ESTIMATES)
# ════════════════════════════════════════════════════════════

# FINRA 2023 — Asset Ownership Rates (% who own)
assets       = ['Crypto', 'Ind. Stocks', 'Mutual Funds', 'ETFs', 'NFTs']
gz_own       = [55, 41, 35, 23, 25]
ml_own       = [57, 38, 43, 26, 28]
gx_own       = [39, 43, 47, 22, 15]

# FINRA 2023 — Risk & Behavioral Indicators
risk_labels  = ['Willing\nSubst. Risk', 'FOMO\nInvestment', 'First Invest.\nWas Crypto', 'Use\nInvest Apps']
gz_risk      = [46, 50, 44, 65]
ml_risk      = [38, 42, 35, 55]

# Schwab 2025 Wave 2 — Portfolio Allocation (all investors)
port_labels  = ['Stocks', 'Other', 'Mutual\nFunds', 'Crypto', 'Bonds', 'Real\nEstate', 'ETFs', 'Options', 'Alts']
port_vals    = [25, 25, 13, 10, 8, 7, 6, 3, 3]
port_colors  = [GZ, '#475569', '#22D3EE', GOLD, '#6366F1', GREEN, ML, '#F87171', '#FB923C']

# Motley Fool 2025 — Stock Types
stypes       = ['U.S. Stocks', 'Growth', 'Value', 'Dividend', 'Small/Mid', 'Large-Cap', 'REITs', 'ESG']
gz_stypes    = [42, 45, 39, 28, 31, 26, 23, 15]
ml_stypes    = [54, 48, 39, 35, 39, 32, 23, 13]

# Motley Fool 2025 — Investment Sectors
sectors      = ['Technology', 'Financials', 'Healthcare', 'Energy', 'Real Estate', 'Consumer', 'Crypto-Rel.', 'AI Stocks']
gz_sect      = [50, 36, 29, 30, 29, 16, 23, 22]
ml_sect      = [58, 38, 36, 34, 26, 22, 28, 21]

# Motley Fool 2025 — Trading Frequency
freq_labels  = ['Daily', 'Weekly', 'Multiple\n/Month', 'Once\n/Month', '<Once\n/Month']
gz_freq      = [16, 34, 24, 10, 16]
ml_freq      = [14, 29, 27,  9, 20]

# Motley Fool 2025 — Investment Goals
goal_labels  = ['Passive\nIncome', 'Retirement', 'Buy\nHome', 'Capital\nGrowth', 'Start\nBusiness']
gz_goals     = [43, 20, 16, 7, 9]
ml_goals     = [40, 30,  9, 10, 4]

# Motley Fool 2025 — Info Sources
src_labels   = ['YouTube', 'TikTok', 'Friends\n/Family', 'Reddit', 'Fin.\nAdvisor', 'Free\nWebsite']
gz_src       = [67, 48, 40, 27, 25, 26]
ml_src       = [56, 26, 42, 28, 28, 37]

# Schwab 2025 — Social Media Use by Generation
social_gens  = ['Gen Z', 'Millennials', 'Gen X', 'Boomers']
social_vals  = [72, 57, 38, 19]
social_cols  = [GZ, ML, GREEN, GOLD]

# Motley Fool 2025 — Dividend Usage
div_labels   = ['Everyday\nCash', 'Fun\nMoney', 'Save\nGoals', 'Reinvest\nAuto', 'Reallocate']
gz_div       = [26, 18, 19, 23, 11]
ml_div       = [17, 15, 17, 38,  9]

# ════════════════════════════════════════════════════════════
#  FIGURE SETUP
# ════════════════════════════════════════════════════════════
DPI = 200
FW, FH = 22, 28
fig = plt.figure(figsize=(FW, FH), facecolor=BG, dpi=DPI)

# Master grid: header | charts | footer
outer = gridspec.GridSpec(3, 1, figure=fig,
    height_ratios=[0.10, 0.87, 0.03],
    hspace=0.04,
    left=0.04, right=0.96, top=0.97, bottom=0.03)

# Chart grid: 4 rows × 3 cols
cgs = gridspec.GridSpecFromSubplotSpec(4, 3,
    subplot_spec=outer[1],
    hspace=0.55, wspace=0.32)

# ════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════
def style_ax(ax, title='', source=''):
    ax.set_facecolor(CARD)
    for sp in ax.spines.values():
        sp.set_color(BORDER); sp.set_linewidth(0.8)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.yaxis.label.set_color(MUTED)
    ax.xaxis.label.set_color(MUTED)
    ax.grid(color=BORDER, linewidth=0.6, zorder=0)
    if title:
        ax.set_title(title, color=TEXT, fontsize=9.5, fontweight='bold',
                     pad=6, loc='left', fontfamily='monospace')
    if source:
        ax.annotate(f'Source: {source}', xy=(0, -0.18), xycoords='axes fraction',
                    fontsize=7, color=MUTED, fontfamily='monospace')

def pct_yticks(ax):
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{int(v)}%'))

def pct_xticks(ax):
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{int(v)}%'))

def grouped_bar(ax, x_labels, gz_data, ml_data, title='', source='', gx_data=None):
    n = len(x_labels)
    x = np.arange(n)
    w = 0.28 if gx_data is not None else 0.35

    if gx_data is not None:
        ax.bar(x - w, gz_data, w, color=GZ_ALPHA, edgecolor=GZ, linewidth=1.2, zorder=3, label='Gen Z')
        ax.bar(x,     ml_data, w, color=ML_ALPHA, edgecolor=ML, linewidth=1.2, zorder=3, label='Millennials')
        ax.bar(x + w, gx_data, w, color=(0,229/255,160/255,0.12), edgecolor=GREEN, linewidth=1.2, zorder=3, label='Gen X')
    else:
        ax.bar(x - w/2, gz_data, w, color=GZ_ALPHA, edgecolor=GZ, linewidth=1.2, zorder=3, label='Gen Z')
        ax.bar(x + w/2, ml_data, w, color=ML_ALPHA, edgecolor=ML, linewidth=1.2, zorder=3, label='Millennials')

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=7.5, color=MUTED, fontfamily='monospace')
    ax.set_ylim(0, max(max(gz_data), max(ml_data)) * 1.22)
    pct_yticks(ax)
    style_ax(ax, title, source)

    leg = ax.legend(fontsize=7.5, facecolor=SURFACE, edgecolor=BORDER,
                    labelcolor=TEXT, loc='upper right')
    leg.get_frame().set_linewidth(0.6)

def hbar(ax, labels, gz_data, ml_data, title='', source=''):
    n = len(labels)
    y = np.arange(n)
    w = 0.35
    ax.barh(y + w/2, gz_data, w, color=GZ_ALPHA, edgecolor=GZ, linewidth=1.2, zorder=3, label='Gen Z')
    ax.barh(y - w/2, ml_data, w, color=ML_ALPHA, edgecolor=ML, linewidth=1.2, zorder=3, label='Millennials')
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.5, color=MUTED, fontfamily='monospace')
    ax.set_xlim(0, max(max(gz_data), max(ml_data)) * 1.22)
    pct_xticks(ax)
    ax.invert_yaxis()
    style_ax(ax, title, source)
    leg = ax.legend(fontsize=7.5, facecolor=SURFACE, edgecolor=BORDER,
                    labelcolor=TEXT, loc='lower right')
    leg.get_frame().set_linewidth(0.6)

def add_value_labels_bar(ax, bars, color, fontsize=7):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                f'{int(h)}%', ha='center', va='bottom',
                color=color, fontsize=fontsize, fontweight='bold',
                fontfamily='monospace')

# ════════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════════
hdr_ax = fig.add_subplot(outer[0])
hdr_ax.set_facecolor(SURFACE)
for sp in hdr_ax.spines.values():
    sp.set_color(BORDER); sp.set_linewidth(0.8)
hdr_ax.set_xticks([]); hdr_ax.set_yticks([])

# Gradient accent line at top
hdr_ax.axhline(y=0.98, color=GZ, linewidth=2, xmin=0.0, xmax=0.5)
hdr_ax.axhline(y=0.98, color=ML, linewidth=2, xmin=0.5, xmax=1.0)

hdr_ax.text(0.012, 0.68, 'GEN Z  vs  MILLENNIALS',
    transform=hdr_ax.transAxes, fontsize=22, fontweight='bold',
    color=WHITE, fontfamily='monospace',
    bbox=dict(boxstyle='round,pad=0.1', facecolor='none', edgecolor='none'))

hdr_ax.text(0.012, 0.22, 'Investment Risk · Portfolio Allocation · Trading Behavior',
    transform=hdr_ax.transAxes, fontsize=10, color=MUTED, fontfamily='monospace')

# Source badges
badge_x = [0.46, 0.64, 0.82]
badge_texts = [
    'FINRA Foundation + CFA  ·  2023  ·  n=2,872',
    'Charles Schwab MWS  ·  2025 Wave 2  ·  n=2,400',
    'Motley Fool Survey  ·  July 2025  ·  n=2,000',
]
badge_colors = [GZ, ML, GOLD]

for bx, bt, bc in zip(badge_x, badge_texts, badge_colors):
    hdr_ax.text(bx, 0.5, bt, transform=hdr_ax.transAxes,
        fontsize=7.2, color=bc, fontfamily='monospace',
        ha='left', va='center',
        bbox=dict(boxstyle='round,pad=0.3',
                  facecolor=(*[c/255 for c in (int(bc[1:3],16), int(bc[3:5],16), int(bc[5:7],16))], 0.08),
                  edgecolor=(*[c/255 for c in (int(bc[1:3],16), int(bc[3:5],16), int(bc[5:7],16))], 0.35),
                  linewidth=0.8))

# Gen Z / Millennials color key
hdr_ax.plot([0.41, 0.435], [0.5, 0.5], color=GZ, linewidth=3, transform=hdr_ax.transAxes)
hdr_ax.text(0.438, 0.5, 'Gen Z', transform=hdr_ax.transAxes,
    fontsize=8, color=GZ, fontfamily='monospace', va='center', fontweight='bold')

# ════════════════════════════════════════════════════════════
#  ROW 0: Asset Ownership | Portfolio Donut | Risk/FOMO
# ════════════════════════════════════════════════════════════

# — R0C0: Asset Ownership Grouped Bar (FINRA 2023) —
ax00 = fig.add_subplot(cgs[0, 0])
grouped_bar(ax00, assets, gz_own, ml_own, title='Asset Ownership Rates', source='FINRA 2023', gx_data=gx_own)

# — R0C1: Portfolio Allocation Donut (Schwab 2025 W2) —
ax01 = fig.add_subplot(cgs[0, 1])
ax01.set_facecolor(CARD)
for sp in ax01.spines.values(): sp.set_color(BORDER); sp.set_linewidth(0.8)

wedges, texts, autotexts = ax01.pie(
    port_vals, labels=None, colors=port_colors,
    autopct='%1.0f%%', startangle=140,
    pctdistance=0.72,
    wedgeprops={'edgecolor': BG, 'linewidth': 2},
    textprops={'fontsize': 7.5, 'color': TEXT, 'fontfamily': 'monospace'})
for at in autotexts:
    at.set_fontsize(7)
    at.set_color(BG)
    at.set_fontweight('bold')

# Draw center hole label
ax01.text(0, 0, 'Portfolio\nAllocation', ha='center', va='center',
          fontsize=8, color=TEXT, fontfamily='monospace', fontweight='bold')

# Custom legend
legend_patches = [mpatches.Patch(color=c, label=l)
                  for c, l in zip(port_colors, ['Stocks 25%', 'Other 25%', 'Mut.Funds 13%',
                                                  'Crypto 10%', 'Bonds 8%', 'Real Estate 7%',
                                                  'ETFs 6%', 'Options 3%', 'Alts 3%'])]
leg = ax01.legend(handles=legend_patches, fontsize=6.5, facecolor=SURFACE,
                   edgecolor=BORDER, labelcolor=TEXT, loc='lower center',
                   bbox_to_anchor=(0.5, -0.35), ncol=3)
leg.get_frame().set_linewidth(0.6)

ax01.set_title('Portfolio Allocation (All U.S. Investors)', color=TEXT,
               fontsize=9.5, fontweight='bold', pad=6, loc='left', fontfamily='monospace')
ax01.annotate('Source: Schwab MWS Wave 2, Oct 2025',
              xy=(0, -0.18), xycoords='axes fraction',
              fontsize=7, color=MUTED, fontfamily='monospace')

# — R0C2: Risk & FOMO (FINRA 2023) —
ax02 = fig.add_subplot(cgs[0, 2])
n = len(risk_labels)
x = np.arange(n); w = 0.35
b1 = ax02.bar(x - w/2, gz_risk, w, color=GZ_ALPHA, edgecolor=GZ, linewidth=1.2, zorder=3, label='Gen Z')
b2 = ax02.bar(x + w/2, ml_risk, w, color=ML_ALPHA, edgecolor=ML, linewidth=1.2, zorder=3, label='Millennials')
add_value_labels_bar(ax02, b1, GZ)
add_value_labels_bar(ax02, b2, ML)
ax02.set_xticks(x)
ax02.set_xticklabels(risk_labels, fontsize=7.5, color=MUTED, fontfamily='monospace')
ax02.set_ylim(0, 82)
pct_yticks(ax02)
style_ax(ax02, 'Risk Appetite & FOMO Indicators', 'FINRA 2023')
leg = ax02.legend(fontsize=7.5, facecolor=SURFACE, edgecolor=BORDER, labelcolor=TEXT)
leg.get_frame().set_linewidth(0.6)

# ════════════════════════════════════════════════════════════
#  ROW 1: Stock Types (hbar) | Sectors (hbar) | Trading Freq
# ════════════════════════════════════════════════════════════

# — R1C0: Stock Types (Motley Fool 2025) —
ax10 = fig.add_subplot(cgs[1, 0])
hbar(ax10, stypes, gz_stypes, ml_stypes, title='Stock Types Owned', source='Motley Fool, July 2025')

# — R1C1: Sectors (Motley Fool 2025) —
ax11 = fig.add_subplot(cgs[1, 1])
hbar(ax11, sectors, gz_sect, ml_sect, title='Investment Sectors', source='Motley Fool, July 2025')

# — R1C2: Trading Frequency (Motley Fool 2025) —
ax12 = fig.add_subplot(cgs[1, 2])
grouped_bar(ax12, freq_labels, gz_freq, ml_freq, title='Trading Frequency', source='Motley Fool, July 2025')

# ════════════════════════════════════════════════════════════
#  ROW 2: Investment Goals | Dividend Usage | Social Media
# ════════════════════════════════════════════════════════════

# — R2C0: Investment Goals —
ax20 = fig.add_subplot(cgs[2, 0])
grouped_bar(ax20, goal_labels, gz_goals, ml_goals, title='Primary Investment Goals', source='Motley Fool, July 2025')

# — R2C1: Dividend Usage —
ax21 = fig.add_subplot(cgs[2, 1])
grouped_bar(ax21, div_labels, gz_div, ml_div, title='Dividend Income Usage', source='Motley Fool, July 2025')

# — R2C2: Social Media Usage by Gen —
ax22 = fig.add_subplot(cgs[2, 2])
bars = ax22.bar(social_gens, social_vals,
                color=[(int(c[1:3],16)/255, int(c[3:5],16)/255, int(c[5:7],16)/255, 0.2) for c in social_cols],
                edgecolor=social_cols, linewidth=1.4, zorder=3)
for bar, val, col in zip(bars, social_vals, social_cols):
    ax22.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
              f'{val}%', ha='center', va='bottom', color=col,
              fontsize=9, fontweight='bold', fontfamily='monospace')
ax22.set_ylim(0, 90)
ax22.set_xticks(range(len(social_gens)))
ax22.set_xticklabels(social_gens, fontsize=8, color=MUTED, fontfamily='monospace')
pct_yticks(ax22)
style_ax(ax22, 'Social Media for Financial Info', 'Schwab MWS 2025')

# ════════════════════════════════════════════════════════════
#  ROW 3: Info Sources (hbar) | Key Stats Panel
# ════════════════════════════════════════════════════════════

# — R3C0-1: Information Sources (wide, 2 cols) —
ax30 = fig.add_subplot(cgs[3, 0:2])
hbar(ax30, src_labels, gz_src, ml_src, title='Investment Information Sources', source='Motley Fool, July 2025')

# — R3C2: Key Stats Summary —
ax32 = fig.add_subplot(cgs[3, 2])
ax32.set_facecolor(CARD)
for sp in ax32.spines.values(): sp.set_color(BORDER); sp.set_linewidth(0.8)
ax32.set_xticks([]); ax32.set_yticks([])

ax32.set_title('Key Differentiators', color=TEXT,
               fontsize=9.5, fontweight='bold', pad=6, loc='left', fontfamily='monospace')

stats = [
    ('Age started investing',      '19',  'yrs', '25', 'yrs'),
    ('First invest. was crypto',   '44',  '%',   '35', '%'),
    ('Trade daily/weekly',         '50',  '%',   '43', '%'),
    ('View dividends as income',   '64',  '%',   '53', '%'),
    ('Formal financial plan',      '39',  '%',   '36', '%'),
    ('Use TikTok for fin. info',   '48',  '%',   '26', '%'),
    ('Primary goal: passive inc.', '43',  '%',   '40', '%'),
    ('Primary goal: retirement',   '20',  '%',   '30', '%'),
]

y_start = 0.88
row_h   = 0.10
for i, (label, gzv, gzu, mlv, mlu) in enumerate(stats):
    y = y_start - i * row_h
    bg_col = '#0D1827' if i % 2 == 0 else CARD
    ax32.add_patch(FancyBboxPatch((0.01, y - 0.06), 0.98, 0.085,
        boxstyle='round,pad=0.01', facecolor=bg_col,
        edgecolor='none', transform=ax32.transAxes, zorder=0))

    ax32.text(0.03, y, label, transform=ax32.transAxes,
              fontsize=7, color=MUTED, fontfamily='monospace', va='center')
    ax32.text(0.72, y, f'{gzv}{gzu}', transform=ax32.transAxes,
              fontsize=8.5, color=GZ, fontfamily='monospace',
              va='center', fontweight='bold', ha='center')
    ax32.text(0.88, y, f'{mlv}{mlu}', transform=ax32.transAxes,
              fontsize=8.5, color=ML, fontfamily='monospace',
              va='center', fontweight='bold', ha='center')

# Column headers
ax32.text(0.72, 0.97, 'GEN Z', transform=ax32.transAxes,
          fontsize=7, color=GZ, fontfamily='monospace',
          va='top', ha='center', fontweight='bold')
ax32.text(0.88, 0.97, 'MILS', transform=ax32.transAxes,
          fontsize=7, color=ML, fontfamily='monospace',
          va='top', ha='center', fontweight='bold')

ax32.set_xlim(0, 1); ax32.set_ylim(0, 1)
ax32.annotate('Sources: FINRA 2023 · Schwab 2025 · Motley Fool 2025',
              xy=(0, -0.18), xycoords='axes fraction',
              fontsize=6.5, color=MUTED, fontfamily='monospace')

# ════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════
ftr_ax = fig.add_subplot(outer[2])
ftr_ax.set_facecolor(SURFACE)
for sp in ftr_ax.spines.values(): sp.set_color(BORDER); sp.set_linewidth(0.6)
ftr_ax.set_xticks([]); ftr_ax.set_yticks([])

ftr_ax.text(0.012, 0.5,
    'Data: FINRA Foundation & CFA Institute (2023) · Charles Schwab Modern Wealth Survey Wave 2 (Oct 2025) · Motley Fool Generational Investing Trends Survey (July 2025) · All data from primary sources, no estimates',
    transform=ftr_ax.transAxes, fontsize=7.2, color=MUTED,
    fontfamily='monospace', va='center')

# ════════════════════════════════════════════════════════════
#  SAVE
# ════════════════════════════════════════════════════════════
OUT = '/home/claude/genz_vs_millennials_dashboard.png'
fig.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, edgecolor='none')
print(f'✅ Dashboard saved → {OUT}')
print(f'   Size: {FW}×{FH} in @ {DPI} DPI = {FW*DPI}×{FH*DPI} px')
