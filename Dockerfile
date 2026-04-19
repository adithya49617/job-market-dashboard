# Stage 1: Build React frontend
FROM node:18 AS frontend-build
WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ .
RUN NODE_OPTIONS="--max-old-space-size=2048" npm run build

# Stage 2: Flask backend
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY data/ ./data/

COPY --from=frontend-build /frontend/dist ./static

EXPOSE 7860
CMD ["python", "app.py"]
