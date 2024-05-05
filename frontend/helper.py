import nltk
from nltk.tokenize import sent_tokenize
from docx import Document
import io

nltk.download('punkt')

def load_text(file):
    if file.name.endswith('.txt'):
        # Behandle als Textdatei
        text = file.getvalue().decode('utf-8')
        return text.split("\n\n")  # Teile Text an doppelten Zeilenumbrüchen (Absätze)
    elif file.name.endswith('.docx'):
        # Behandle als Word-Dokument
        doc = Document(io.BytesIO(file.read()))
        return [paragraph.text for paragraph in doc.paragraphs if paragraph.text]
    else:
        raise ValueError("Unsupported file format")

def split_into_sentences(text, language='german'):
    """Nutzt NLTK, um Text in Sätze aufzuteilen."""
    return sent_tokenize(text, language=language)

def prepare_sentence_pairs(source_paragraphs, target_paragraphs, source_language='german', target_language='english'):
    all_sentence_pairs = []
    for source_text, target_text in zip(source_paragraphs, target_paragraphs):
        source_sentences = split_into_sentences(source_text, language=source_language)
        target_sentences = split_into_sentences(target_text, language=target_language)
        if len(source_sentences) == len(target_sentences):
            all_sentence_pairs.extend(zip(source_sentences, target_sentences))
        else:
            # Optional: Fehlerbehandlung oder Logik zur besseren Anpassung hinzufügen
            pass
    return all_sentence_pairs