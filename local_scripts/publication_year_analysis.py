import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Path to the uploaded CSV file
csv_file_path = os.getenv('CSV_FILE_PATH')

# Reading the CSV file
literature_df = pd.read_csv(csv_file_path)

# Displaying the first few rows to understand the structure and available columns
literature_df.head()

# Extracting publication year data
pub_year_data = literature_df['Publication Year'].dropna()  # Removing NaN values

# Counting the occurrence of each publication year
pub_year_distribution = pub_year_data.value_counts().sort_index()

plt.figure(figsize=(10, 4))
bars = plt.bar(pub_year_distribution.index, pub_year_distribution.values, color='skyblue', zorder=3)

# Adding the number of publications on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, yval, int(yval), va='bottom', ha='center', zorder=4)

plt.xlabel('Jahr der Veröffentlichung')
plt.ylabel('Anzahl der Veröffentlichungen')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='-', zorder=0)

# Save and show the plot
output_plot_path_1 = os.getenv('PLOT_OUTPUT_PATH_1')
plt.savefig(output_plot_path_1)
plt.show()

publication_type_distribution = literature_df['Item Type'].value_counts(normalize=True) * 100
publication_type_distribution = publication_type_distribution.rename(index={
    'thesis': 'Akademische Abschlussarbeiten',
    'book': 'Buch',
    'journalArticle': 'Journal Artikel',
    'conferencePaper': 'Konferenzbeitrag',
    'preprint': 'Preprint'
})

# Creating a pie chart to visualize the distribution of publication types
plt.figure(figsize=(10, 6))
plt.pie(publication_type_distribution, labels=publication_type_distribution.index, autopct='%1.1f%%', startangle=140)
plt.title('Verteilung der Publikationstypen')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Save and show the plot
output_plot_path_2 = os.getenv('PLOT_OUTPUT_PATH_2')
plt.savefig(output_plot_path_2)
plt.show()
