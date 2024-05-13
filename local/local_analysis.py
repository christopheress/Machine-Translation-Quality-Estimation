import pandas as pd
import requests
from frontend.model_interface import TransQuestModel, OpenAIModel, CometKiwiModel


# Definition der Modell-URLs aus Umgebungsvariablen
model_urls = {
    "transquest": "http://0.0.0.0:8001/evaluate/",
    "openai_gpt": "http://0.0.0.0:8002/evaluate/",
    "cometkiwi": "http://0.0.0.0:8003/evaluate/"
}

# Modelle instanziieren
models = {
    "transquest": TransQuestModel(model_urls["transquest"]),
    #"openai_gpt": OpenAIModel(model_urls["openai_gpt"]),
    #"cometkiwi": CometKiwiModel(model_urls["cometkiwi"])
}

# Excel-Datei einlesen
data = pd.read_excel('/Users/christopheressmann/Library/CloudStorage/OneDrive-andsafeAG/Studium/4. Masterarbeit/Testdaten_MTQE.xlsx')

# Funktion zum Bewerten der Übersetzungsqualität
def evaluate_translation_quality(model, source_text, target_text, gpt_model_version=None, source_language=None, target_language=None):
    try:
        response = model.query(source_text, target_text, gpt_model_version=gpt_model_version, source_language=source_language, target_language=target_language)
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


# Funktion zum Senden der Anfragen und Speichern der Antworten
def process_translation_evaluations(data, models):
    total_rows = len(data)
    for index, row in data.iterrows():
        # Drucken des Fortschritts
        print(f'Verarbeite Zeile {index + 1} von {total_rows}...')

        source_text = row['Input']
        good_translation = row['Good']
        bad_translation = row['Bad']

        # Durchgehen aller Modelle und Ausführung der Anfragen
        for model_name, model in models.items():
            # Bewertung der guten Übersetzung
            good_result = evaluate_translation_quality(model, source_text, good_translation)
            if good_result['success']:
                data.at[index, f'{model_name}_good_score'] = good_result['score']
            else:
                print(f'Fehler bei guter Übersetzung mit {model_name}: {good_result["message"]}')

            # Bewertung der schlechten Übersetzung
            bad_result = evaluate_translation_quality(model, source_text, bad_translation)
            if bad_result['success']:
                data.at[index, f'{model_name}_bad_score'] = bad_result['score']
            else:
                print(f'Fehler bei schlechter Übersetzung mit {model_name}: {bad_result["message"]}')

    return data

# Verarbeitung durchführen
updated_data = process_translation_evaluations(data, models)

# Ergebnisse in eine neue Excel-Datei speichern
output_filename = '/Users/christopheressmann/Library/CloudStorage/OneDrive-andsafeAG/Studium/4. Masterarbeit/Testdaten_MTQE_result_tr.xlsx'
updated_data.to_excel(output_filename, index=False)

print(f'Die aktualisierte Excel-Datei wurde gespeichert: {output_filename}')
