# --- Stage 1: Frontend Build (Vite/React) ---
# 로그에서 Vite가 요구한 대로 Node.js 20 버전을 사용합니다.
FROM node:20-alpine AS frontend-builder

# 로그상 작업 디렉토리 구조를 맞춥니다.
WORKDIR /app/frontend

# 1. 패키지 파일 복사 및 설치
# 로그에서 'frontend/package.json'을 찾았으므로 경로를 맞춤 조정합니다.
COPY frontend/package*.json ./
RUN npm install

# 2. 소스 복사 및 빌드
COPY frontend/ ./
RUN npm run build


# --- Stage 2: Backend & Final Image (FastAPI) ---
FROM python:3.10-slim AS backend

WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 3. 파이썬 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 백엔드 코드 복사
COPY app/ ./app/

# 5. 프론트엔드 빌드 결과물 가져오기
# Vite 빌드 결과물인 dist 폴더를 백엔드 쪽으로 복사합니다.
COPY --from=frontend-builder /app/frontend/dist/ ./frontend/dist/

# 포트 설정
EXPOSE 8000

# 6. 실행 명령어
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]