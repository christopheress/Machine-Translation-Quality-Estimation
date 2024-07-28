import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file to analyze the data
model = "co" # co | tr
file_path = '/Users/christopheressmann/Library/CloudStorage/OneDrive-andsafeAG/Studium/4. Masterarbeit/Testdaten_MTQE_result_'+model+'.xlsx'
data = pd.read_excel(file_path)

if model == "co":
    model_long = "cometkiwi"
elif model == "tr":
    model_long = "transquest"


# Display the first few rows of the dataframe to understand its structure
data.head()

# Calculate the difference between good and bad scores
data['score_difference'] = data[model_long + '_good_score'] - data[model_long + '_bad_score']

# Set up the figure for plotting
plt.rcParams.update({'font.size': 14})  # Setzt die Standard-Schriftgröße auf 14
plt.figure(figsize=(14, 7))

# Create a barplot to visualize the score differences by groups
sns.barplot(x='score_difference', y='Gruppe', data=data, errorbar=None, palette='viridis')
plt.title('Differenz der ' + model_long + ' Scores zwischen guten und schlechten Übersetzungen pro Gruppe',
          x=0.2)
plt.xlabel('Score Differenz')
plt.ylabel('Gruppe')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Show the plot
plt.savefig('/Users/christopheressmann/Library/CloudStorage/OneDrive-andsafeAG/Studium/4. Masterarbeit/Test_Dokument/grafiken/Scores_'+ model + '_Groups.png')
plt.show()

# Berechnungen für korrekt und fehlerhaft vorhergesagte Fälle
data['good_better_than_bad'] = data[model_long + '_good_score'] > data[model_long + '_bad_score']
data['good_worse_than_bad'] = data[model_long + '_good_score'] <= data[model_long + '_bad_score']
good_better_count_by_group = data.groupby('Gruppe')['good_better_than_bad'].sum()
good_worse_count_by_group = data.groupby('Gruppe')['good_worse_than_bad'].sum()
total_counts_by_group = data.groupby('Gruppe').size()
good_better_percentage_by_group = good_better_count_by_group / total_counts_by_group * 100
good_worse_percentage_by_group = good_worse_count_by_group / total_counts_by_group * 100

# Daten für die Visualisierung vorbereiten
plot_data = pd.DataFrame({
    'Good Better Percentage': good_better_percentage_by_group,
    'Good Worse Percentage': good_worse_percentage_by_group,
    'Good Better Count': good_better_count_by_group,
    'Good Worse Count': good_worse_count_by_group
}).reset_index()

plt.figure(figsize=(14, 9))
bars_good = plt.bar(plot_data['Gruppe'], plot_data['Good Better Percentage'], color='green', label='Korrekt vorhergesagt')
bars_bad = plt.bar(plot_data['Gruppe'], plot_data['Good Worse Percentage'], bottom=plot_data['Good Better Percentage'], color='red', label='Fehlerhaft vorhergesagt')

# Textbeschriftungen für gute Vorhersagen
for idx, bar in enumerate(bars_good):
    yval = bar.get_height()
    count = plot_data.loc[idx, 'Good Better Count']
    percentage = plot_data.loc[idx, 'Good Better Percentage']
    plt.text(bar.get_x() + bar.get_width()/2, yval - 5, f'{int(count)} \n ({percentage:.1f}%)', ha='center', va='top', color='white', fontweight='bold')

plt.title(model_long + ': Prozentsatz und absolute Anzahl der korrekt und fehlerhaft vorhergesagten Fälle pro Gruppe')
plt.xlabel('Gruppe')
plt.ylabel('Prozentsatz (%)')
plt.xticks(rotation=45, ha='right')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper left')
plt.tight_layout()

# Das Plot als Bilddatei speichern
plt.savefig('/Users/christopheressmann/Library/CloudStorage/OneDrive-andsafeAG/Studium/4. Masterarbeit/Test_Dokument/grafiken/Prozent_korrekt_Groups_'+model+'.png')
plt.show()
