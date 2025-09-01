# FitPet Scraper

## 🚀 프로젝트 설정

```shell
poetry install

cp .env.template .env
```

## 🛠️ 주요 기술 스택

- **언어**: Python 3.12
- **패키지 관리**: Poetry
- **컨테이너화**: Docker, Docker Compose

## 📝 프로젝트 구조

```
├── app/                  # 애플리케이션 소스 코드
    ├── api/              # API 엔드포인트 및 관련 로직 
    ├── config/           # 데이터베이스, 로그 등 설정 
    ├── dto/              # 데이터 전송 객체 
    ├── entity/           # 데이터베이스 테이블과 매핑되는 엔티티 
    ├── enum/             # 애플리케이션에서 사용되는 열거형 
    ├── exception/        # 커스텀 예외 및 예외 핸들러 
    ├── repository/       # 데이터베이스 접근 로직 
    ├── scraper/          # 웹 스크레이핑 로직 
    ├── service/          # 비즈니스 로직 
    ├── task/             # Celery 비동기 작업 
    └── util/             # 유틸리티 함수
├── data/                 # 데이터 파일
├── .env                  # 환경 변수 파일
├── .env.template         # 환경 변수 템플릿
├── main.py               # 애플리케이션 진입점
├── pyproject.toml        # Poetry 의존성 및 프로젝트 설정
├── Dockerfile            # Docker 이미지 빌드 설정
├── docker-compose.yaml   # Docker 다중 컨테이너 실행 설정 (배포는 k8s)
└── README.md             # 프로젝트 문서
```

## 🐳 Docker

```shell
docker login

docker buildx build --platform=linux/arm64 --target web    -t girr311/fitpet-scraper:web    .
docker buildx build --platform=linux/arm64 --target worker -t girr311/fitpet-scraper:worker .
docker buildx build --platform=linux/arm64 --target beat   -t girr311/fitpet-scraper:beat   .

docker push girr311/fitpet-scraper:web
docker push girr311/fitpet-scraper:worker
docker push girr311/fitpet-scraper:beat
```