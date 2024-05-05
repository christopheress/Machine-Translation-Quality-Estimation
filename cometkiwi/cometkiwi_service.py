from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from comet import download_model, load_from_checkpoint

app = FastAPI()


class TranslationInput(BaseModel):
    source_text: str
    target_text: str


class CometKiwiModelStrategy:
    def __init__(self, model_name):
        model_path = "/app/wmt23-cometkiwi-da-xl/checkpoints/model.ckpt"
        self.model = load_from_checkpoint(model_path)

    def evaluate(self, source_text, target_text):
        results = self.model.predict([{"src": source_text, "mt": target_text}], batch_size=8, gpus=0)
        score = results["scores"][0]
        return score


cometkiwi_strategy = CometKiwiModelStrategy("Unbabel/wmt23-cometkiwi-da-xl")


@app.post("/evaluate/")
def evaluate(translation: TranslationInput):
    score = cometkiwi_strategy.evaluate(translation.source_text, translation.target_text)
    return {"score": score}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
