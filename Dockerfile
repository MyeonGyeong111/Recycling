# Stage 1: Frontend Build (Vite/React)
FROM node:18-bullseye AS frontend-builder

# package.json이 있는 실제 위치로 이동
WORKDIR /app/frontend/src

# 1. 의존성 파일만 먼저 복사 (캐시 활용)
# 현재 구조상 frontend/src 폴더 안에 package.json이 있으므로 해당 경로 지정
COPY frontend/src/package*.json ./

# 2. 라이브러리 설치
RUN npm install

# 3. 프론트엔드 전체 소스 복사
COPY frontend/src/ ./

# 4. 빌드 실행 (결과물은 보통 ./dist 폴더에 생성됨)
RUN npm run build


# Stage 2: Backend Build (FastAPI)
FROM python:3.10-slim AS backend

WORKDIR /app

# 시스템 의존성 설치 (curl 등)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 5. 파이썬 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 백엔드 소스 코드 복사
COPY app/ ./app/

# 7. Stage 1에서 빌드된 결과물을 백엔드 정적 파일 경로로 복사
# frontend/src/dist 폴더가 생성되었는지 확인 후 복사합니다.
COPY --from=frontend-builder /app/frontend/src/dist/ ./frontend/dist/

# 포트 개방
EXPOSE 8000

# 8. 서버 실행 (app.main:app 경로가 맞는지 확인하세요!)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]