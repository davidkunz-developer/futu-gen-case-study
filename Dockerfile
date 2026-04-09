# --- Stage 1: Build Frontend ---
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# --- Stage 2: Final Image ---
FROM python:3.10-slim

# Instalace systémových závislostí
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    build-essential \
    python3-dev \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Kopírování requirements a instalace
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování backendového kódu
COPY . .

# Kopírování buildu frontendu z 1. fáze
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose FastAPI port
EXPOSE 8000

# Spuštění Uvicorn serveru
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
