import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

# 1. Data Loading and Cleaning
# Note: Use 'netflix_titles.csv' if the file is in the same folder as this script
df = pd.read_csv('C:\\Users\\Ian Medina\\Desktop\\Proyectos de programación\\Netflix Project\\netflix_titles.csv') 

# Fill missing values
cols_to_fill = ['director', 'cast', 'country', 'date_added', 'rating', 'duration', 'listed_in', 'description']
for col in cols_to_fill:
    df[col] = df[col].fillna('Unknown')

# Standardize dates and extract the year
df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), format='%B %d, %Y', errors='coerce')
df['year_added'] = df['date_added'].dt.year

# 2. Data Preparation for Visualizations
movies_count = len(df[df['type'] == 'Movie'])
tv_shows_count = len(df[df['type'] == 'TV Show'])
top_countries = df['country'].value_counts().head(10)

# Filter content added since 2015 for the trend chart
content_since_2015 = df[df['year_added'] >= 2015]
trend_data = content_since_2015['year_added'].value_counts().sort_index().reset_index()
trend_data.columns = ['year_added', 'count']

# 3. Dashboard Styling (Netflix Theme)
plt.style.use('seaborn-v0_8-white')
netflix_red = '#E50914'
dark_grey = '#221F1F'

fig = plt.figure(figsize=(16, 12), facecolor='white')
fig.suptitle('Netflix Catalog Strategic Analysis', fontsize=28, fontweight='bold', color=dark_grey, y=0.98)

# Create a grid: 2 rows and 2 columns
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# --- CHART 1: Content Type Distribution (Donut Chart) ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.pie([movies_count, tv_shows_count], labels=['Movies', 'TV Shows'], autopct='%1.1f%%', 
        startangle=140, colors=[netflix_red, '#564d4d'], pctdistance=0.82, explode=(0.05, 0),
        textprops={'fontsize': 12, 'fontweight': 'bold'})
# Draw a white circle in the center for the "donut" effect
ax1.add_artist(plt.Circle((0,0), 0.70, fc='white'))
ax1.set_title('Distribution of Content Type', fontsize=16, fontweight='bold', pad=15)

# --- CHART 2: Top 10 Countries (Horizontal Bar Chart) ---
ax2 = fig.add_subplot(gs[0, 1])
sns.barplot(x=top_countries.values, y=top_countries.index, palette='Reds_r', ax=ax2)
ax2.set_title('Top 10 Content-Producing Countries', fontsize=16, fontweight='bold', pad=15)
ax2.set_xlabel('Number of Titles', fontsize=12)
ax2.set_ylabel('')
sns.despine(left=True, bottom=True)
ax2.grid(axis='x', linestyle='--', alpha=0.6)

# --- CHART 3: Content Trend (Area Chart) ---
ax3 = fig.add_subplot(gs[1, :]) # Spans the entire bottom row
ax3.plot(trend_data['year_added'], trend_data['count'], marker='o', color=netflix_red, linewidth=4, markersize=10)
ax3.fill_between(trend_data['year_added'], trend_data['count'], color=netflix_red, alpha=0.1)
ax3.set_title('Evolution of Content Added (2015 - Present)', fontsize=16, fontweight='bold', pad=15)
ax3.set_xlabel('Year Added', fontsize=12)
ax3.set_ylabel('Amount of Content', fontsize=12)
ax3.set_xticks(trend_data['year_added'].astype(int))
ax3.grid(axis='y', linestyle='--', alpha=0.5)
sns.despine()

# Footer / Signature
plt.figtext(0.5, 0.02, 'Data Analysis: Ian Medina | Source: Netflix Dataset', 
            ha='center', fontsize=10, color='gray', style='italic')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()