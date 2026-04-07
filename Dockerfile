# Stage 1: Frontend Build
FROM node:18-bullseye AS frontend-builder

# 핵심: 워킹 디렉토리를 아예 package.json이 있는 곳으로 잡습니다.
WORKDIR /app/frontend/src

# 1. 의존성 설치 (캐시 활용)
COPY frontend/src/package*.json ./
RUN npm install

# 2. 모든 소스 복사 (index.html, vite.config.js 등 포함)
# 현재 위치가 /app/frontend/src 이므로, 로컬의 frontend/src 내용을 여기에 붓습니다.
COPY frontend/src/ ./

# 3. 빌드 실행
# 여기서 에러가 난다면 로컬에서 'npm run build'가 성공하는지 확인이 필요합니다.
RUN npm run build


# Stage 2: Backend & Final Image
FROM python:3.10-slim AS backend
WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 파이썬 설정
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 백엔드 코드 복사
COPY app/ ./app/

# 4. 프론트엔드 빌드 결과물 복사
# 중요: Vite 빌드 결과물이 /app/frontend/src/dist 에 생기는지 확인하세요.
COPY --from=frontend-builder /app/frontend/src/dist/ ./frontend/dist/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]