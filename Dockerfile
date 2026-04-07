# Stage 1: Build the Vite React Frontend
FROM node:18-bullseye AS frontend-builder
WORKDIR /app/frontend

# Copy all source files cleanly
COPY frontend/ ./

# Force a completely clean layout, bypassing any locked host-environment issues
RUN rm -rf node_modules package-lock.json && \
    npm install && \
    npm run build


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
