# --- Stage 1: Frontend Build (Vite/React) ---
# Vite 8은 Node.js 20.19.0 또는 22.12.0 이상의 버전을 필수로 요구합니다.
FROM node:20-alpine AS frontend-builder

# package.json이 있는 실제 위치로 이동합니다.
WORKDIR /app/frontend/src

# 1. 의존성 설치 (캐시 활용을 위해 설정 파일만 먼저 복사)
COPY frontend/src/package*.json ./
RUN npm install

# 2. 프론트엔드 전체 소스 복사
COPY frontend/src/ ./

# 3. 정적 파일 빌드 (dist 폴더 생성)
# CI=false 설정은 사소한 Warning으로 인해 빌드가 멈추는 것을 방지합니다.
RUN CI=false npm run build


# --- Stage 2: Backend & Final Image (FastAPI) ---
FROM python:3.10-slim AS backend

WORKDIR /app

# 시스템 패키지 업데이트 및 curl 설치 (헬스체크용)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 4. 파이썬 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 백엔드 어플리케이션 코드 복사
COPY app/ ./app/

# 6. Stage 1에서 빌드된 결과물(dist)을 백엔드 폴더로 가져오기
# Vite 빌드 결과물 위치(/app/frontend/src/dist)를 정확히 지정합니다.
COPY --from=frontend-builder /app/frontend/src/dist/ ./frontend/dist/

# 컨테이너 포트 개방
EXPOSE 8000

# 7. 서버 실행 명령어
# app.main:app 경로가 실제 파일 구조와 맞는지 확인해 주세요!
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]