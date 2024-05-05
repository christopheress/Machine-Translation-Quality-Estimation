import pandas as pd
import seaborn as sns

# Path to the uploaded CSV file
csv_file_path = '/Users/christopheressmann/Downloads/Finale_Literatur.csv'

# Reading the CSV file
literature_df = pd.read_csv(csv_file_path)

# Displaying the first few rows to understand the structure and available columns
literature_df.head()
#
# Extracting publication year data
pub_year_data = literature_df['Publication Year'].dropna()  # Removing NaN values

# Counting the occurrence of each publication year
pub_year_distribution = pub_year_data.value_counts().sort_index()

# Plotting
import matplotlib.pyplot as plt

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

plt.savefig('/Users/christopheressmann/Library/CloudStorage/OneDrive-andsafeAG/Studium/4. Masterarbeit/Literatur/Grafiken/Jahre.png')
plt.show()
# %%

publication_type_distribution = literature_df['Item Type'].value_counts(normalize=True) * 100
publication_type_distribution = publication_type_distribution.rename(index={'thesis': 'Akademische Abschlussarbeiten',
                                                                            'book': 'Buch',
                                                                            'journalArticle': 'Journal Artikel',
                                                                            'conferencePaper': 'Konferenzbeitrag',
                                                                            'preprint': 'Preprint'})

# Creating a pie chart to visualize the distribution of publication types
plt.figure(figsize=(10, 6))
plt.pie(publication_type_distribution, labels=publication_type_distribution.index, autopct='%1.1f%%', startangle=140)
plt.title('Verteilung der Publikationstypen')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Das Plot als Bilddatei speichern
plt.savefig('/Users/christopheressmann/Library/CloudStorage/OneDrive-andsafeAG/Studium/4. Masterarbeit/Literatur/Grafiken/Publikationstypen.png')

# Showing the plot
plt.show()

# interpreting the results
"""
Die Verteilung der Publikationstypen in deiner systematischen Literaturrecherche liefert wertvolle Einblicke in die bevorzugten Kommunikationskanäle und Formate in der Forschungsgemeinschaft, die sich mit der Qualitätseinschätzung maschineller Übersetzungen befasst. 
Journalartikel dominieren mit 55.1% deutlich, was auf die Bedeutung peer-reviewter Zeitschriften in diesem Forschungsfeld hinweist. In wissenschaftlichen Journalen veröffentlichte Arbeiten gelten allgemein als qualitativ hochwertig, da sie einen strengen Begutachtungsprozess durchlaufen. Dieses Format ermöglicht es Forschenden, ihre Ergebnisse detailliert darzustellen und trägt zur Wissensgrundlage des Feldes bei.
Konferenzbeiträge machen 22.4% aus und sind ein weiteres wichtiges Medium für die Dissemination neuer Forschungsergebnisse. Konferenzen bieten eine Plattform für den direkten Austausch innerhalb der Community, die Präsentation von laufenden Arbeiten und die Diskussion neuester Trends und Methoden. Die relativ hohe Anzahl an Konferenzbeiträgen unterstreicht die Dynamik des Forschungsfelds und den kontinuierlichen Informationsfluss zwischen den Forschenden.
Die Kategorie "Thesen/Dissertationen" umfasst 10.2% der Publikationen und bezieht sich auf umfangreiche akademische Arbeiten, die oft tiefe Einblicke in spezifische Aspekte des Forschungsbereichs bieten. Diese Arbeiten tragen zur wissenschaftlichen Diskussion bei, indem sie detaillierte Untersuchungen und Analysen zu bestimmten Fragestellungen liefern.
Preprints und Bücher stellen jeweils 6.1% der Publikationen dar. Preprints, die Vorabveröffentlichungen von Forschungsarbeiten sind, ermöglichen eine schnelle Verbreitung neuer Erkenntnisse und fördern die offene wissenschaftliche Kommunikation. Bücher und Buchkapitel hingegen bieten die Möglichkeit, Themen umfassend und aus verschiedenen Perspektiven zu behandeln, was insbesondere für die Darstellung von Überblicksarbeiten und methodischen Grundlagen nützlich ist.
Insgesamt reflektiert die Verteilung der Publikationstypen die Vielfalt der Kommunikationswege in der Forschungsgemeinschaft zur Qualitätseinschätzung maschineller Übersetzungen. Die Dominanz von Journalartikeln und Konferenzbeiträgen spiegelt die Wichtigkeit formeller und peer-reviewter Kanäle wider, während Thesen/Dissertationen, Preprints und Bücher ergänzende Einblicke und tiefere Analysen bieten. Diese Vielfalt unterstützt einen reichhaltigen wissenschaftlichen Dialog und fördert Innovationen und Fortschritte im Forschungsfeld.
"""

"""
Die Analyse der Themenentwicklung über die Zeit basierend auf den Titeln der Publikationen von 2016 bis 2023 zeigt, dass sich die Forschungsthemen innerhalb des Bereichs "Machine Translation Quality Estimation" sowohl inhaltlich als auch methodisch weiterentwickelt haben. Hier sind einige Beobachtungen:
- **2016**: Der Fokus lag auf grundlegenden Aspekten der Qualitätseinschätzung auf Dokumenten- und Satzebene.
- **2018**: Ähnliche Schwerpunkte wie 2016, mit einer Konzentration auf die Kernthemen der maschinellen Übersetzung und Qualitätseinschätzung.
- **2019**: Es erscheinen spezifischere Themen, darunter die Bewertung von Fehlern, Post-Editing und die Verwendung von Embeddings. Der Begriff "OpenKiwi" deutet auf spezifische Werkzeuge oder Frameworks hin.
- **2020**: Der Schwerpunkt verschiebt sich hin zu anspruchsvolleren Methoden wie "Cross-Lingual" Ansätzen und "Unsupervised Learning". "TransQuest" wird als spezifisches Tool oder Modell genannt.
- **2021**: Es zeigt sich eine Diversifizierung der Themen, einschließlich spezifischer Projekte oder Experimente wie "MLQE" und "DirectQE". Die Begriffe "IntelliCat" und "Dataset" deuten auf die Entwicklung spezifischer Ressourcen und Tools hin.
- **2022**: Neben der Fortsetzung von Themen wie der menschlichen Bewertung und dem Einfluss auf die Übersetzungsqualität, tauchen neue Begriffe wie "Kvality" und "Mutual" auf, was auf eine Erweiterung der Forschungsinteressen hindeutet.
- **2023**: Die Themen richten sich stärker auf aktuelle Entwicklungen, einschließlich "Large Language Models", "Metrics" und spezifischen Herausforderungen wie "Shared Task". Der Begriff "XComet" deutet auf die Einführung neuer Tools oder Frameworks hin.
Diese Entwicklung spiegelt die kontinuierliche Evolution und Spezialisierung innerhalb des Forschungsfeldes wider, von allgemeineren Konzepten zu detaillierteren Untersuchungen spezifischer Aspekte, Methoden und Tools der Qualitätseinschätzung maschineller Übersetzungen. Die Einführung und der Fokus auf spezifische Tools sowie die Berücksichtigung von "Large Language Models" in den jüngsten Jahren zeigen, dass die Forschung zunehmend technologische Fortschritte und deren Anwendungsmöglichkeiten exploriert.
"""