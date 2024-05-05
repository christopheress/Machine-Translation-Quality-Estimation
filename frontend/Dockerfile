# Verwende das offizielle Python-Image als Basis
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere notwendige Pakete für den NLTK Download
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Kopiere die Anforderungsdatei in das Arbeitsverzeichnis
COPY requirements.txt .

# Installiere alle benötigten Pakete
RUN pip install --no-cache-dir -r requirements.txt

# Installiere spaCy Sprachmodelle
RUN python -m nltk.downloader punkt

# Kopiere den restlichen Quellcode in das Arbeitsverzeichnis
COPY . .

# Exponiere den Port, auf dem Streamlit läuft
EXPOSE 8501

# Starte Streamlit, wenn der Container startet
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
