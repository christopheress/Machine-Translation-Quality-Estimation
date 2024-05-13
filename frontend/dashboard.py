import streamlit as st
import requests
import json
import os
from io import BytesIO
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from model_interface import TransQuestModel, OpenAIModel, CometKiwiModel
from helper import load_text, prepare_sentence_pairs

debug = False

# Angenommen, das Volume ist unter /data im Container gemountet
SAVE_DIR = Path("/data/results")
SAVE_DIR.mkdir(parents=True, exist_ok=True)  # Stellt sicher, dass das Verzeichnis existiert


# Modell-URLs und -Instanzen initialisieren
model_urls = {
    "transquest": os.getenv("TRANSQUEST_URL") + "/evaluate/",
    "openai_gpt": os.getenv("OPENAI_GPT_URL") + "/evaluate/",
    "openai_gpt_error_detection": os.getenv("OPENAI_GPT_URL") + "/error_detection/",
    "cometkiwi": os.getenv("COMETKIWI_URL") + "/evaluate/"
}

models = {
    "transquest": TransQuestModel(model_urls["transquest"]),
    "openai_gpt": OpenAIModel(model_urls["openai_gpt"]),
    "openai_gpt_error_detection": OpenAIModel(model_urls["openai_gpt_error_detection"]),
    "cometkiwi": CometKiwiModel(model_urls["cometkiwi"]),
}

def evaluate_translation_quality(model, source_text, target_text,
                                 gpt_model_version=None, source_language=None,
                                 target_language=None):
    try:
        response = model.query(source_text, target_text, gpt_model_version=gpt_model_version,
                               source_language=source_language, target_language=target_language)
        if response.status_code == 200:
            score = response.json()["score"]
            return {'success': True, 'score': score}
        else:
            message = 'Fehler bei der Antwort vom Backend.'
            if response.status_code == 503:
                message += ' Der Dienst ist noch nicht gestartet. Bitte versuche es später erneut.'
            else:
                message += f' Fehlercode: {response.status_code}, Antwort: {response.text}'
            return {'success': False, 'message': message}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'message': f'Ein Fehler ist aufgetreten beim Versuch, das Backend zu erreichen: {e}'}


# Streamlit Application
st.title('Machine Translation Quality Estimation')

tab1, tab2, tab3 = st.tabs(["Datenvorverarbeitung", "MTQE Modell Verarbeitung", "MTQE Analyse"])

with tab1:
    st.header("Datenvorverarbeitung")
    uploaded_file_source = st.file_uploader("Lade die Quelldatei hoch", type=['txt', 'docx'], key='source_upload')
    uploaded_file_target = st.file_uploader("Lade die Zieldatei hoch", type=['txt', 'docx'], key='target_upload')

    # Spracheinstellungen hinzufügen
    source_language = st.selectbox("Wähle die Quellsprache", ('german', 'english', 'spanish', 'french'), key='source_language_preprocess')
    target_language = st.selectbox("Wähle die Zielsprache", ('english', 'german', 'spanish', 'french'), key='target_language_preprocess')
    min_words = st.slider("Minimale Wortanzahl im Quelltext pro Satz", min_value=1, max_value=20, value=2, step=1, key='min_words_slider')
    process_button = st.button("Texte verarbeiten")

    if uploaded_file_source and uploaded_file_target and process_button:
        source_paragraphs = load_text(uploaded_file_source)
        target_paragraphs = load_text(uploaded_file_target)

        if len(source_paragraphs) == len(target_paragraphs):
            sentence_pairs = prepare_sentence_pairs(source_paragraphs, target_paragraphs, source_language, target_language, min_words)
            df_sentence_pairs = pd.DataFrame(sentence_pairs, columns=['Source Text', 'Target Text'])
            st.session_state['sentence_pairs_df'] = df_sentence_pairs
            st.write('Satzpaare gefunden:', len(df_sentence_pairs))
        else:
            st.error("Die Anzahl der Absätze in den Quell- und Zieltexten stimmt nicht überein.")

        json_data = df_sentence_pairs.to_json(orient='records', lines=True, force_ascii=False)
        download_filename = f"satzpaare_{uploaded_file_target.name.split('.')[0]}.json"
        st.download_button(label="Download Satzpaare als JSON", data=json_data, file_name=download_filename, mime='application/json')


with tab2:
    st.header("MTQE Modell Verarbeitung")

    def load_json(file):
        # Einlesen der Datei zeilenweise und Parsen jedes JSON-Objekts einzeln
        return [json.loads(line) for line in file]

    input_method = st.radio("Wähle die Eingabemethode", ('JSON-Datei hochladen', 'Text direkt eingeben'), key='input_method')

    if input_method == 'JSON-Datei hochladen':
        uploaded_json = st.file_uploader("Lade die JSON mit Satzpaaren hoch", type=['json'], key='json_upload')

        # Prüfe, ob eine neue Datei hochgeladen wurde
        if uploaded_json is not None:
            if 'uploaded_json_name' not in st.session_state or st.session_state['uploaded_json_name'] != uploaded_json.name:
                st.session_state['uploaded_json_name'] = uploaded_json.name
                # Lösche results_df, wenn eine neue Datei hochgeladen wird
                if 'results_df' in st.session_state:
                    del st.session_state['results_df']

            sentence_pairs = load_json(uploaded_json)
            st.session_state['sentence_pairs'] = sentence_pairs

    elif input_method == 'Text direkt eingeben':
        with st.form(key='direct_input_form'):
            source_text_input = st.text_area("Quelltext", key='source_text_input')
            target_text_input = st.text_area("Zieltext", key='target_text_input')
            submit_text = st.form_submit_button("Text speichern")

            if submit_text:
                # Speichere die direkt eingegebenen Texte als Satzpaare im Session State
                if 'sentence_pairs' not in st.session_state or not isinstance(st.session_state['sentence_pairs'], list):
                    st.session_state['sentence_pairs'] = []

                st.session_state['sentence_pairs'].append({'Source Text': source_text_input, 'Target Text': target_text_input})
                st.success("Text erfolgreich gespeichert!")

    # Check if uploaded json exists and assign file_name
    if 'uploaded_json_name' in st.session_state:
        file_name = st.session_state['uploaded_json_name']
    else:
        file_name = 'direct_input'

    # Checkbox zur Auswahl, ob Satzpaare angezeigt werden sollen
    show_pairs = st.checkbox("Satzpaare anzeigen", value=False)

    if show_pairs:
        # Setze max_value basierend auf der Anzahl der Satzpaare, sichere mindestens 1 als Wert
        max_pairs = len(st.session_state.get('sentence_pairs', []))
        max_value = max(1, max_pairs)  # Verhindert StreamlitAPIException bei leerer Liste

        # Standardwert auf min(max_value, 5) setzen, um sicherzustellen, dass er nicht größer als max_value ist
        default_value = min(max_value, 5)

        num_pairs_to_show = st.number_input("Anzahl der anzuzeigenden Satzpaare",
                                            min_value=1,
                                            max_value=max_value,
                                            value=default_value)

        if 'sentence_pairs' in st.session_state and st.session_state['sentence_pairs']:
            st.write("Verarbeitete oder geladene Satzpaare:")
            for i, pair in enumerate(st.session_state['sentence_pairs'][:num_pairs_to_show]):
                st.text_area(f"Quellsatz {i + 1}", value=pair['Source Text'], height=100, key=f'source_{i}')
                st.text_area(f"Zielsatz {i + 1}", value=pair['Target Text'], height=100, key=f'target_{i}')
        else:
            st.write("Keine Satzpaare gefunden. Bitte lade Daten in Tab 1 oder lade eine JSON-Datei hoch.")
    else:
        st.write("Satzpaare werden nicht angezeigt. Aktiviere die Option oben, um sie anzuzeigen.")

    model_choice = st.selectbox("Wähle ein Modell aus", options=list(models.keys()), key='model_choice')

    if model_choice in ['openai_gpt', 'openai_gpt_error_detection']:
        gpt_model_version = st.selectbox(
            'Wähle die Version des OpenAI GPT-Modells aus',
            ('gpt-3.5-turbo', 'gpt-4-turbo-preview'),  # Liste der verfügbaren Modellversionen
            key='gpt_model_version'
        )
        source_language = st.selectbox(
            'Wähle die Quellsprache aus',
            ('german', 'english', 'french', 'spanish'),  # Liste der verfügbaren Sprachen
            key='source_language'
        )
        target_language = st.selectbox(
            'Wähle die Zielsprache aus',
            ('german', 'english', 'french', 'spanish'),  # Liste der verfügbaren Sprachen
            key='target_language'
        )
    else:
        gpt_model_version = None
        source_language = None
        target_language = None

    # Vor dem Button zur Qualitätsbewertung
    show_results = st.checkbox("Ergebnisse anzeigen", value=True)

    # Hinzufügen einer Checkbox, um automatischen Download zu bestätigen
    auto_download = st.checkbox("Automatischen Download der Excel-Datei aktivieren?", value=False)

    if st.button('Qualität einschätzen', key='estimate_quality'):
        if 'sentence_pairs' in st.session_state and st.session_state['sentence_pairs']:
            total_pairs = len(st.session_state['sentence_pairs'])
            progress_bar = st.progress(0)
            progress_text = st.empty()  # Für die Prozentanzeige

            # Initialisiere einen leeren DataFrame
            results_df = pd.DataFrame(columns=['File', 'Model', 'Source Text', 'Target Text', 'Score',
                                               'Error_Detection', 'Error'])

            for i, pair in enumerate(st.session_state['sentence_pairs']):
                source_text = pair['Source Text']
                target_text = pair['Target Text']

                if debug:
                    st.write(f'Verarbeite Satzpaar {i + 1}')
                    st.write(f'Quellsatz: {source_text}')
                    st.write(f'Zielsatz: {target_text}')

                result = evaluate_translation_quality(models[model_choice], source_text, target_text,
                                                      gpt_model_version=gpt_model_version,
                                                      source_language=source_language,
                                                      target_language=target_language)


                # Füge die Ergebnisse dem DataFrame hinzu
                new_row = {
                    'File': file_name,
                    'Model': model_choice,
                    'Source Text': source_text,
                    'Target Text': target_text,
                    'Score': result.get('score') if result['success'] else None,
                    'Error_Detection': result.get('error') if result['success'] else None,
                    'Error': result.get('message') if not result['success'] else None
                }
                new_row_df = pd.DataFrame([new_row])
                results_df = pd.concat([results_df, new_row_df], ignore_index=True)

                # Aktualisiere Fortschrittsanzeige und Prozentanzeige
                progress = (i + 1) / total_pairs
                progress_bar.progress(progress)
                progress_text.text(f'Verarbeitungsfortschritt: {int(progress * 100)}%')

            # Speichern der Ergebnisse im Session State für den Download
            st.session_state['results_df'] = results_df
            progress_text.empty()  # Entferne die Prozentanzeige nach Abschluss

            if 'results_df' in st.session_state and auto_download:
                file_path = SAVE_DIR / f"ergebnisse_{file_name.split('.')[0]}_{model_choice}.xlsx"
                st.session_state['results_df'].to_excel(file_path, index=False)
                st.success(f"Ergebnisse wurden automatisch gespeichert: {file_path}")
                # docker cp 2534f2367b6614c8785a2aac34dbe435eb479655eccb83cd74b4f5b0ee76a7b8:/data/results/ergebnisse_direct_input_transquest.xlsx /Users/christopheressmann/Downloads/ergebnisse_direct_input_transquest.xlsx

    # Ergebnisse anzeigen, wenn gewünscht und vorhanden
    if show_results and 'results_df' in st.session_state:
        st.dataframe(st.session_state['results_df'][['Model', 'Source Text', 'Target Text', 'Score', 'Error']])

        # Download-Button für die Ergebnisse
        output = BytesIO()
        st.session_state['results_df'].to_excel(output, index=False)
        output.seek(0)

        download_filename = f"ergebnisse_{file_name.split('.')[0]}_{model_choice}.xlsx"
        st.download_button(label="Download Ergebnisse als Excel", data=output, file_name=download_filename,
                           mime="application/vnd.ms-excel")

with tab3:
    st.header("Ergebnisanalyse")

    # Gruppierung der Einstellungen in einem Expander
    with st.expander("Einstellungen für die Analyse"):
        uploaded_files = st.file_uploader("Lade Excel-Dateien mit Ergebnissen hoch", type=['xlsx'], key='excel_upload', accept_multiple_files=True)
        min_word_count = st.number_input("Mindestanzahl der Wörter pro Satz", min_value=1, value=1, step=1, key='min_word_count')
        exclude_extremes = st.checkbox("Extremwerte ausschließen", value=False, key='exclude_extremes')
        if exclude_extremes:
            extreme_percentile = st.slider("Prozentsatz der niedrigsten Scores, die ausgeschlossen werden sollen", min_value=0, max_value=10, value=5, step=1, key='extreme_percentile')
        number_of_length_clusters = st.slider("Anzahl der Satzlängen-Cluster", min_value=2, max_value=10, value=4, step=1, key='length_clusters')

    if uploaded_files:
        all_results = []
        avg_scores_list = []
        sentence_scores = []
        sentence_length_clusters = []
        sentence_sets = []
        cluster_info = []

        for uploaded_file in uploaded_files:
            temp_df = pd.read_excel(uploaded_file, engine='openpyxl')
            temp_df['Document'] = uploaded_file.name
            temp_df['Word Count'] = temp_df['Source Text'].apply(lambda x: len(x.split()))
            temp_df['Score'] = pd.to_numeric(temp_df['Score'], errors='coerce')  # Konvertiere die Score-Spalte in float
            temp_df = temp_df[temp_df['Word Count'] >= min_word_count]

            if exclude_extremes:
                temp_df = temp_df.dropna(subset=['Score'])
                cutoff_score = np.percentile(temp_df['Score'], extreme_percentile)
                temp_df = temp_df[temp_df['Score'] > cutoff_score]

            sentence_sets.append(set(temp_df['Source Text']))

        # Finden der Schnittmenge aller Sätze, die in allen Dateien vorhanden sind
        common_sentences = set.intersection(*sentence_sets)

        for uploaded_file in uploaded_files:
            temp_df = pd.read_excel(uploaded_file, engine='openpyxl')
            temp_df = temp_df[temp_df['Source Text'].isin(common_sentences)]
            temp_df['Document'] = uploaded_file.name
            temp_df['Word Count'] = temp_df['Source Text'].apply(lambda x: len(x.split()))
            temp_df['Score'] = pd.to_numeric(temp_df['Score'], errors='coerce')

            sentence_scores.append(temp_df[['Source Text', 'Score', 'Document']])
            avg_score_current_file = temp_df['Score'].mean()
            avg_scores_list.append({'Document': uploaded_file.name, 'Average Score': avg_score_current_file})

            # Anwendung der Quantile-Einteilung und Speicherung der Cluster-Grenzen
            quantiles, bins = pd.qcut(temp_df['Word Count'], q=number_of_length_clusters, retbins=True,
                                      labels=[f'Cluster {i + 1}' for i in range(number_of_length_clusters)])
            temp_df['Length Cluster'] = quantiles
            sentence_length_clusters.append(temp_df[['Source Text', 'Score', 'Length Cluster', 'Document']])
            all_results.append(temp_df)

            # Speichern der Cluster-Informationen
            cluster_labels = [f'Cluster {i + 1}' for i in range(number_of_length_clusters)]
            for i in range(len(bins) - 1):
                cluster_info.append({'Cluster': cluster_labels[i], 'Min Words': bins[i], 'Max Words': bins[i + 1] - 1})

        combined_df = pd.concat(all_results, ignore_index=True)
        avg_score_df = pd.DataFrame(avg_scores_list)
        length_cluster_df = pd.concat(sentence_length_clusters, ignore_index=True)
        cluster_info_df = pd.DataFrame(cluster_info)

        length_cluster_scores = length_cluster_df.pivot_table(index=['Source Text', 'Length Cluster'],
                                                              columns='Document', values='Score',
                                                              aggfunc='mean').reset_index()

        # Bestimmung der besten Durchschnitte je Cluster und Dokument
        best_count_per_cluster = length_cluster_scores.groupby('Length Cluster').apply(
            lambda df: df.iloc[:, 1:].idxmax(axis=1).value_counts())
        mean_scores_per_cluster = length_cluster_df.groupby(['Length Cluster', 'Document']).agg({'Score': 'mean'})

        # Long to wide mean_scores_per_cluster
        mean_scores_per_cluster = mean_scores_per_cluster.unstack(level=1)
        mean_scores_per_cluster.columns = mean_scores_per_cluster.columns.droplevel(0)
        mean_scores_per_cluster = mean_scores_per_cluster.reset_index()

        # Erstellen von Tabs für die verschiedenen Ergebnisanzeigen
        tab1, tab2, tab3, tab4 = st.tabs(["Kombinierte und Durchschnittliche Ergebnisse", "Detaillierte Analysen", "Visualisierungen", "Satzlängen-Analyse"])

        with tab1:
            st.subheader("Kombinierte Ergebnisse")
            st.dataframe(combined_df)
            st.subheader("Durchschnittlicher Qualitätsscore je Datei")
            st.dataframe(avg_score_df)

        sentence_score_df = pd.concat(sentence_scores, ignore_index=True)
        sentence_score_pivot = sentence_score_df.pivot_table(index='Source Text', columns='Document', values='Score', aggfunc='first').reset_index()

        best_source_count = {doc: {'Best Count': 0, 'Only Score': 0, 'Identical Scores': 0} for doc in sentence_score_pivot.columns[1:]}
        for index, row in sentence_score_pivot.iterrows():
            scores = row[1:].dropna()
            if scores.empty:
                continue
            best_score = scores.max()
            best_docs = scores[scores == best_score].index.tolist()
            if len(best_docs) == 1:
                best_source_count[best_docs[0]]['Best Count'] += 1
            elif len(best_docs) > 1:
                for doc in best_docs:
                    best_source_count[doc]['Identical Scores'] += 1
            if len(scores) == 1:
                doc_with_only_score = scores.index[0]
                best_source_count[doc_with_only_score]['Only Score'] += 1

        analysis_results = [{'Document': doc, **counts} for doc, counts in best_source_count.items()]
        analysis_df = pd.DataFrame(analysis_results)

        with tab2:
            st.subheader("Detaillierte Analyse der Bewertungen je Quelle")
            st.table(analysis_df)
            st.subheader("Score je Satz von verschiedenen Inputdateien")
            st.dataframe(sentence_score_pivot)

        with tab3:
            show_graph = st.checkbox("Ergebnisse visualisieren", value=True)
            if show_graph:
                st.subheader("Durchschnittliche Qualitätsscores je Datei")
                st.bar_chart(avg_score_df.set_index('Document'))
                st.subheader("Beste Bewertungen je Quelle")
                st.bar_chart(analysis_df.set_index('Document'))

        with tab4:
            # Checkbox, um zusätzliche Cluster-Informationen ein- oder auszublenden
            show_info = st.checkbox("Cluster-Informationen anzeigen", value=False)
            if show_info:
                st.subheader("Satzlängen-Cluster-Informationen")
                st.dataframe(cluster_info_df)

            # Untertitel und Darstellung der Durchschnittswerte nach Satzlänge
            st.subheader("Analyse nach Satzlänge")
            st.dataframe(mean_scores_per_cluster)

            # Erstellung eines Balkendiagramms zur Visualisierung der Durchschnittswerte mit Plotly
            fig = px.bar(mean_scores_per_cluster, x='Length Cluster',
                         y=[col for col in mean_scores_per_cluster.columns if col != 'Length Cluster'],
                         barmode='group', title="Average Scores by Document and Cluster")
            st.plotly_chart(fig, use_container_width=True)

            # Untertitel für die Analyse der besten Scores je Cluster
            st.subheader("Häufigkeit des besten Inputs je Cluster")
            st.table(best_count_per_cluster)

            # Untertitel für die Darstellung der besten Bewertungen je Cluster
            st.subheader("Beste Bewertungen je Cluster")
            best_count_per_cluster = best_count_per_cluster.reset_index()
            fig = px.bar(best_count_per_cluster, x='Length Cluster',
                         y=[col for col in best_count_per_cluster.columns if col != 'Length Cluster'],
                         barmode='group', title="Best Count per Cluster")
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Keine Dateien zum Analysieren gefunden. Bitte lade mindestens eine Datei hoch.")