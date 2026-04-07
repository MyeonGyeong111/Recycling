# Recycling API 프로젝트 가이드

이 저장소는 자취생들을 위한 분리수거 지원 API (FastAPI 기반) 프로젝트 구조와 실행 방법을 담고 있습니다.

## 1. 프로젝트 패키지 요구사항 (`requirements.txt`)
MLOps 환경 및 FastAPI 구동에 필요한 최소한의 필수 라이브러리들로 구성되어 있습니다.

```text
fastapi>=0.100.0
uvicorn[standard]>=0.22.0
pydantic>=2.0.0
python-multipart>=0.0.6
```

- **fastapi**: 비동기 API 서버 프레임워크
- **uvicorn**: FastAPI 실행을 위한 ASGI 서버
- **pydantic**: 데이터 검증용 라이브러리 (요청/응답 스키마 관리)
- **python-multipart**: 이미지 파일 업로드와 같은 `form-data` 처리를 위한 필수 패키지

---

## 2. 프로젝트 폴더 구조 (Directory Structure)
코드 유지보수 및 Docker 환경 확장을 고려한 MLOps 친화적인 폴더 구조입니다.

```text
recycling_api/
├── docker-compose.yml       # MLOps 컨테이너 실행을 돕는 로컬 컴포즈 환경세팅
├── Dockerfile               # API 서비스를 컨테이너화하기 위한 독립된 환경정의
├── requirements.txt         # 파이썬 의존성 패키지 목록
└── app/                     # 메인 애플리케이션 코드가 들어가는 디렉토리
    ├── main.py              # FastAPI 앱 실행의 Entrypoint (CORS 및 루트 설정)
    │
    ├── core/                # 환경 변수 및 공통 설정 모음
    │   └── config.py
    │
    ├── schemas/             # Pydantic 모델을 활용한 Request / Response 모델 정의
    │   └── recycle.py
    │
    ├── services/            # 비즈니스 로직과 ML 모델 예측 코드가 들어가는 곳
    │   └── recycle_service.py
    │
    └── api/                 # 외부에서 접근하는 엔드포인트 라우팅 모음
        ├── routers.py       # API 엔드포인트들을 그룹화하여 묶어주는 역할
        └── endpoints/       
            └── recycle.py   # 예측, 정보제공, 가이드라인 등 실제 분리수거 API 로직
```

---

## 3. 실행 방법 (How to Run)

가장 권장되는 실행 방법은 Docker를 활용하는 것입니다. 터미널에서 현재 디렉토리로 이동한 뒤 아래 명령어를 호출하세요.

```bash
docker compose up -d --build
```
실행이 성공적으로 완료되면 브라우저에서 `http://127.0.0.1:8000/docs` 로 접속하여 API 명세서를 확인하고 테스트할 수 있습니다.
