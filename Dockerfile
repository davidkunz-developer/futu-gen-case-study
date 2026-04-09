FROM python:3.10-slim

# Instalace systémových závislostí pro audio a pyannote/whisper
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    build-essential \
    python3-dev \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Kopírování requirements a intalace
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování zbytku kódu
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Spuštění Uvicorn serveru
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
