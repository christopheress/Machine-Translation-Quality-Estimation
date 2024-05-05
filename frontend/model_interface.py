import requests

class ModelInterface:
    def __init__(self, url):
        self.url = url

    def query(self, source_text, target_text, **kwargs):
        raise NotImplementedError("Diese Methode muss von Unterklassen implementiert werden.")


class TransQuestModel(ModelInterface):
    def query(self, source_text, target_text, **kwargs):
        return(requests.post(self.url, json={"source_text": source_text, "target_text": target_text}))


class OpenAIModel(ModelInterface):
    def query(self, source_text, target_text, source_language, target_language, **kwargs):
        gpt_model_version = kwargs.get('gpt_model_version', 'latest')
        return requests.post(self.url, json={
            "source_text": source_text,
            "target_text": target_text,
            "source_language": source_language,
            "target_language": target_language,
            "gpt_model_version": gpt_model_version
        })



class CometKiwiModel(ModelInterface):
    def query(self, source_text, target_text, **kwargs):
        return(requests.post(self.url, json={"source_text": source_text, "target_text": target_text}))
