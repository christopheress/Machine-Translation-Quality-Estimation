from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transquest.algo.sentence_level.monotransquest.run_model import MonoTransQuestModel

app = FastAPI()

# Eingabemodell für die Übersetzungsdaten
class TranslationInput(BaseModel):
    source_text: str
    target_text: str

# TransQuest Modellstrategie
class TransQuestModelStrategy:
    def __init__(self, model_type, model_name, use_cuda=False):
        self.model = MonoTransQuestModel(model_type, model_name, use_cuda=use_cuda)

    def evaluate(self, source_text, target_text):
        score, _ = self.model.predict([[source_text, target_text]])
        return float(score)

transquest_strategy = TransQuestModelStrategy("xlmroberta", "TransQuest/monotransquest-da-multilingual", use_cuda=False)

# Route zur Bewertung der Übersetzungsqualität
@app.post("/evaluate/")
def evaluate(translation: TranslationInput):
    # Verwenden Sie die TransQuestModelStrategy-Instanz, um den Qualitätsscore zu berechnen
    score = transquest_strategy.evaluate(translation.source_text, translation.target_text)
    return {"score": score}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}