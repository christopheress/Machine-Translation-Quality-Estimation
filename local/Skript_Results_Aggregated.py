import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = '/Users/christopheressmann/Library/CloudStorage/OneDrive-andsafeAG/Studium/4. Masterarbeit/Test_Dokument/ergebnisse/Skript_QE_Aggregiert.xlsx'
data = pd.read_excel(file_path, sheet_name='Tabelle1')

# Calculate the score difference for each ID and QE model
data['Score_Diff'] = data.groupby(['ID', 'QE_Modell'])['Score'].transform(lambda x: x.max() - x.min())

# Calculate the range (difference) for each QE model
range_diff = data.groupby('QE_Modell')['Score_Diff'].mean()

# Plot the score difference range for each QE model
plt.figure(figsize=(10, 6))
range_diff.plot(kind='bar', color=['blue', 'orange'])
plt.title('Average Score Range by QE Model')
plt.xlabel('QE Model')
plt.ylabel('Average Score Range')
plt.xticks(rotation=0)
plt.grid(axis='y')

# Show the plot
plt.savefig('/Users/christopheressmann/Library/CloudStorage/OneDrive-andsafeAG/Studium/4. Masterarbeit/Test_Dokument/grafiken/Score_Range_QE_Model.png')
plt.show()

# Filter the data for Cometkiwi
cometkiwi_data = data[data['QE_Modell'] == 'Cometkiwi']

# Calculate the average "Anzahl bessere Bewertungen" for each MT_Engine
average_bessere_bewertungen = cometkiwi_data.groupby('MT_Engine')['Anzahl bessere Bewertungen'].mean()

# Plot the average "Anzahl bessere Bewertungen" for each MT_Engine under Cometkiwi QE model
plt.figure(figsize=(10, 6))
average_bessere_bewertungen.plot(kind='bar', color=['blue', 'orange'])
plt.title('Average Anzahl bessere Bewertungen by MT Engine (Cometkiwi QE Model)')
plt.xlabel('MT Engine')
plt.ylabel('Average Anzahl bessere Bewertungen')
plt.xticks(rotation=0)
plt.grid(axis='y')

# Show the plot
plt.savefig('/Users/christopheressmann/Library/CloudStorage/OneDrive-andsafeAG/Studium/4. Masterarbeit/Test_Dokument/grafiken/Anzahl_bessere_Bewertungen.png')
plt.show()
