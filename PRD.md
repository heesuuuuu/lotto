# 기술 요구서: 스피또 당첨 추천 사이트

## 개요
동행복권 사이트에서 스피또 관련 데이터를 크롤링하여, 당첨 가능성이 높은 스피또를 추천하는 웹사이트를 개발한다.

## 주요 기능
1. **데이터 크롤링**
   - Playwright를 사용하여 동행복권 사이트에서 스피또 관련 정보를 자동으로 수집
   - 당첨권 남은 수량, 전체 발행 수량, 당첨금 등 주요 데이터 추출
2. **데이터 분석 및 추천 알고리즘**
   - 수집된 데이터를 바탕으로 당첨 가능성이 높은 스피또를 계산
   - 남은 당첨권/전체 발행권 비율, 1등 남은 개수 등 다양한 지표 활용
3. **웹사이트 구현**
   - Python(Flask/Django) 또는 Node.js(Express) 기반의 웹사이트 개발
   - 사용자에게 추천 결과 및 데이터 시각화 제공
4. **자동 데이터 갱신**
   - 주기적으로 크롤러를 실행하여 최신 데이터 반영
   - 스케줄러(Cron 등) 또는 서버 내장 기능 활용
5. **배포 및 운영**
   - AWS, Vercel, Heroku 등 클라우드 플랫폼에 배포
   - 운영 및 모니터링 환경 구축

## 기술 스택
- **크롤링:** Playwright (Python 또는 Node.js)
- **백엔드:** Python(Flask/Django) 또는 Node.js(Express)
- **프론트엔드:** HTML/CSS/JavaScript, 필요시 React 등
- **데이터베이스:** SQLite, PostgreSQL, 또는 MongoDB (필요시)
- **배포:** AWS, Vercel, Heroku 등

## 개발 절차
1. Playwright 기반 크롤러 개발 및 데이터 추출
2. 추천 알고리즘 설계 및 구현
3. 웹사이트 UI/UX 설계 및 개발
4. 자동화 및 배포 환경 구축

## 기타 고려사항
- 동행복권 사이트의 구조 변경 시 크롤러 유지보수 필요
- 데이터 수집 주기 및 서버 부하 관리
- 사용자 개인정보 및 보안 고려

## 프로젝트 파일 구조 (최신 권장)
```
lotto/
├── docker-compose.yml           # 전체 서비스 컨테이너 관리
├── requirements/                # 파이썬 패키지 분리 관리
│   ├── base.txt                 # 공통 패키지 (예: requests, playwright)
│   ├── airflow.txt              # apache-airflow, pendulum 등
│   ├── backend.txt              # django, djangorestframework 등
│   └── crawler.txt              # playwright, beautifulsoup4 등
├── airflow/                     # Airflow 관련 코드 및 설정
│   ├── dags/
│   ├── logs/                    # 실행 로그 (Docker 볼륨 마운트용)
│   └── plugins/                 # 커스텀 오퍼레이터
├── backend/                     # Django 프로젝트
│   ├── manage.py
│   ├── lotto_backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   └── apps/                    # 기능별 Django 앱
│       ├── lotto/               # 로또/스피또 관련 기능
│       └── accounts/            # 사용자 인증 등
├── frontend/                    # React 프론트엔드
│   ├── src/
│   ├── public/
│   └── package.json
├── crawler/                     # Playwright 크롤러 코드
│   └── crawl.py
├── data/                        # 크롤링/분석 데이터 저장
│   └── lotto_data.json
├── tests/                       # 테스트 코드
│   ├── test_crawler.py
│   ├── test_backend.py
│   └── test_frontend.js
├── PRD.md                       # 프로젝트 요구사항 문서
└── README.md                    # 프로젝트 설명
```

- requirements/ 디렉토리로 파이썬 패키지 충돌 방지 및 Docker 빌드 최적화
- airflow/logs, airflow/plugins 디렉토리로 운영 및 확장성 강화
- docker-compose.yml로 전체 서비스 컨테이너 일괄 관리
- Django backend는 apps/로 기능별 분리하여 확장성 확보

이 구조는 대규모 확장, 운영, 협업에 모두 적합합니다.

---
문의: heesu@heesu-MacBookAir
