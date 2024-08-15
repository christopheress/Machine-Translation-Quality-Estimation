import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the Excel file
file_path = os.getenv('EXCEL_FILE_PATH')
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

# Save and show the plot
output_plot_path = os.getenv('PLOT_OUTPUT_PATH_1')
plt.savefig(output_plot_path)
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

# Save and show the plot
output_plot_path_2 = os.getenv('PLOT_OUTPUT_PATH_2')
plt.savefig(output_plot_path_2)
plt.show()
