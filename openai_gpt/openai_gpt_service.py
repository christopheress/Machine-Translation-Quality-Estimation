from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import re
import os

app = FastAPI()


class TranslationInput(BaseModel):
    source_text: str
    target_text: str
    source_language: str = "german"
    target_language: str = "english"
    gpt_model_version: str = "gpt-3.5-turbo"


class OpenAIGPTModelStrategy:
    def __init__(self, api_key):
        self.api_key = api_key

    def evaluate(self, source_text, target_text, gpt_model_version,
                 source_language="german", target_language="english"):
        openai.api_key = self.api_key
        # Ansatz: (Yang et al., 2023)
        messages = [
            {"role": "system", "content": "You are a highly intelligent translation evaluation model."},
            {"role": "system", "content": "You understand multiple languages fluently."},
            {"role": "system",
             "content": "You can evaluate the accuracy, fluency, and the preservation of the original meaning in translations between specified languages."},
            {"role": "system",
             "content": "You categorize the quality of the translation as one of [highly fluent; fluent; neutral; disfluent; highly disfluent]."},
            {"role": "system",
             "content": "Highly fluent means the translation is nearly perfect, fluent indicates good quality with minor errors, neutral means the translation is acceptable but with notable errors, disfluent indicates the translation has significant errors affecting comprehension, and highly disfluent means the translation is largely incomprehensible or incorrect."},
            {"role": "system",
             "content": "You will only output one of these five categories to describe the translation."},
            {"role": "user",
             "content": f"Original sentence in {source_language}: {source_text}\nTranslated sentence in {target_language}: {target_text}"}
        ]

        model = gpt_model_version

        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                seed=10
            )

            # Extrahiere die Antwort vom Modell
            answer = response.choices[0].message['content']

            # Definieren Sie eine Liste der gültigen Kategorien
            valid_categories = ['highly fluent', 'fluent', 'neutral', 'disfluent', 'highly disfluent']

            # Überprüfen, ob die Antwort eine der gültigen Kategorien ist
            if answer.lower() in valid_categories:
                return answer  # Gibt die Kategorie direkt zurück
            else:
                return "Invalid response " + answer  # Gibt einen Hinweis zurück, falls die Antwort ungültig ist

        except Exception as e:
            print(f"Error in translation quality evaluation: {e}")
            return 0  # Im Fehlerfall, gibt 0 zurück


# Setzen Sie Ihren OpenAI API-Schlüssel hier
api_key = os.getenv("OPENAI_API_KEY")
openai_gpt_strategy = OpenAIGPTModelStrategy(api_key)


@app.post("/evaluate/")
def evaluate(translation: TranslationInput):
    score = openai_gpt_strategy.evaluate(translation.source_text, translation.target_text,
                                         translation.gpt_model_version, translation.source_language,
                                         translation.target_language)
    return {"score": score}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
