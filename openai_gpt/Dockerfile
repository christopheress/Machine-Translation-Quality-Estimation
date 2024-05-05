# Verwende das offizielle Python-Image als Basis
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installieren Sie Abhängigkeiten
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Definieren Sie den Befehl zum Starten der TransQuest-Anwendung
CMD ["uvicorn", "openai_gpt_service:app", "--host=0.0.0.0", "--port=8002", "--reload"]
