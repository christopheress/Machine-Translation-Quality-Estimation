# Verwende das offizielle Python-Image als Basis
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installieren Sie Abhängigkeiten
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Modell in das Image kopieren
COPY wmt23-cometkiwi-da-xl /app/wmt23-cometkiwi-da-xl

# Anwendungscode kopieren
COPY cometkiwi_service.py /app/

# Definieren Sie den Befehl zum Starten der TransQuest-Anwendung
CMD ["uvicorn", "cometkiwi_service:app", "--host=0.0.0.0", "--port=8003", "--reload"]
