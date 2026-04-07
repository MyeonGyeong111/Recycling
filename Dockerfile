# Stage 1: Build the Vite React Frontend
FROM node:18-slim AS frontend-builder

WORKDIR /app/frontend

# Install dependencies strictly (utilizing cache)
COPY frontend/package.json ./
RUN npm install

# Build the static Vite bundle
COPY frontend/ ./
RUN npm run build


# Stage 2: Build the FastAPI Backend & Serve Frontend
FROM python:3.10-slim AS backend

WORKDIR /app

# Ensure curl is installed for potential healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code
COPY app/ ./app/

# Copy the statically generated frontend build from Stage 1
COPY --from=frontend-builder /app/frontend/dist/ ./frontend/dist/

# Expose API/Web Port
EXPOSE 8000

# Start Uvicorn Server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
