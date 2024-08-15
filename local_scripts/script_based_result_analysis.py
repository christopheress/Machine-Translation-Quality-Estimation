import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Pfade der Dateien, die analysiert werden sollen
file_paths = [
    os.getenv('FILE_PATH_1'),
    os.getenv('FILE_PATH_2')
    # Weitere Dateien können hier hinzugefügt werden
]

export_path = os.getenv('EXPORT_PATH')

# Daten einlesen und Wortanzahl berechnen
data_frames = []
for file in file_paths:
    df = pd.read_excel(file, engine='openpyxl')
    df['Word Count'] = df['Source Text'].apply(lambda x: len(x.split()))
    df['Document'] = file.split('/')[-1]  # Dateiname als Dokumentname hinzufügen
    data_frames.append(df)

# Daten zusammenführen
combined_df = data_frames[0]
for df in data_frames[1:]:
    combined_df = pd.merge(combined_df, df, on='Source Text', how='outer', suffixes=('', '_' + df['Document'][0]))

# Wortanzahl auffüllen, falls sie nur in einer Datei vorhanden ist
combined_df['Word Count'] = combined_df.filter(like='Word Count').bfill(axis=1).iloc[:, 0]

# "Length Cluster" Variable berechnen
num_clusters = 5
unique_bins = np.unique(np.percentile(combined_df['Word Count'], np.linspace(0, 100, num_clusters + 1)))
if len(unique_bins) - 1 < num_clusters:
    num_clusters = len(unique_bins) - 1

combined_df['Length Cluster'] = pd.cut(combined_df['Word Count'], bins=unique_bins,
                                       labels=[f'Cluster {i + 1}' for i in range(num_clusters)], include_lowest=True)

# Sicherstellen, dass alle Scores numerisch sind
score_columns = combined_df.filter(like='Score').columns
combined_df[score_columns] = combined_df[score_columns].apply(pd.to_numeric, errors='coerce')

# Durchschnittsscore je Excel / je File berechnen
average_scores = combined_df[score_columns].mean()

# Vergleich der Scores zwischen den Dateien
comparison_results = {}
for i, col1 in enumerate(score_columns):
    for col2 in score_columns[i + 1:]:
        better_col1 = (combined_df[col1] > combined_df[col2]).sum()
        better_col2 = (combined_df[col2] > combined_df[col1]).sum()
        identical = (combined_df[col1] == combined_df[col2]).sum()
        only_col1 = combined_df[col1].notna().sum() - combined_df[col2].notna().sum()
        only_col2 = combined_df[col2].notna().sum() - combined_df[col1].notna().sum()
        comparison_results[f'{col1} vs {col2}'] = {
            'better_col1': better_col1,
            'better_col2': better_col2,
            'identical': identical,
            'only_col1': only_col1,
            'only_col2': only_col2
        }

# Durchschnittsscore je Cluster berechnen
numeric_cols = combined_df.select_dtypes(include=[np.number]).columns
avg_score_per_cluster = combined_df.groupby('Length Cluster')[numeric_cols].mean().filter(like='Score')


# Vergleich der Scores je Cluster
def compare_scores_per_cluster(df):
    cluster_comparison = {}
    for i, col1 in enumerate(score_columns):
        for col2 in score_columns[i + 1:]:
            better_col1_cluster = (df[col1] > df[col2]).sum()
            better_col2_cluster = (df[col2] > df[col1]).sum()
            identical_cluster = (df[col1] == df[col2]).sum()
            cluster_comparison[f'{col1} vs {col2}'] = {
                'better_col1': better_col1_cluster,
                'better_col2': better_col2_cluster,
                'identical': identical_cluster
            }
    return pd.DataFrame(cluster_comparison)


comparison_per_cluster = combined_df.groupby('Length Cluster').apply(compare_scores_per_cluster)

# Ergebnisse in einer Excel-Datei speichern
with pd.ExcelWriter(export_path, engine='openpyxl') as writer:
    combined_df.to_excel(writer, sheet_name='Combined Data', index=False)
    average_scores.to_frame(name='Average Score').to_excel(writer, sheet_name='Average Scores')

    # Vergleich der Scores zwischen den Dateien
    comparison_results_df = pd.DataFrame(comparison_results).T
    comparison_results_df.to_excel(writer, sheet_name='Comparison Results')

    # Durchschnittsscore je Cluster
    avg_score_per_cluster.to_excel(writer, sheet_name='Avg Score Per Cluster')

    # Vergleich der Scores je Cluster
    for cluster, comparison in comparison_per_cluster.groupby(level=0):
        sheet_name = f'Comparison {cluster}'
        comparison.droplevel(0).to_excel(writer, sheet_name=sheet_name)

print("Ergebnisse erfolgreich in die Datei exportiert.")
