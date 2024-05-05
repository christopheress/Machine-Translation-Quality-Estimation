# Verwende das offizielle Python-Image als Basis
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere systemabhängige Pakete einschließlich gcc und python3-dev
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 1. Modell: TransQuest
RUN git clone https://github.com/TharinduDR/TransQuest.git /app/TransQuest
RUN pip install /app/TransQuest

# Installieren Sie Abhängigkeiten
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den TransQuest-Code in den Container
COPY . .

# Definieren Sie den Befehl zum Starten der TransQuest-Anwendung
CMD ["uvicorn", "transquest_service:app", "--host=0.0.0.0", "--port=8001", "--reload"]
