# BizOPS Portal

> Toomics Global BizOps 팀 산출물 관리 포탈 (GitHub Pages)

## 배포 URL

**https://tg-bizops.github.io/BizOPS/**

## 현황

- **문서**: 61건 (9개 카테고리)
- **디자인 시스템**: Data-Dense Dashboard 스타일 (Fira Code + Fira Sans)
- **업데이트**: 2026-03-08

## 구조

```
BizOPS/
├── index.html                 # 포탈 메인 (히어로 KPI + 아코디언 카테고리)
├── design-system/             # 디자인 시스템
│   └── bizops-portal/
│       ├── MASTER.md          # 글로벌 디자인 규칙 (컬러/타이포/컴포넌트)
│       └── pages/             # 페이지별 오버라이드 (예정)
├── weekly-reports/            # 주간 CS+차지백 분석 리포트
│   ├── index.html             # 주간 리포트 아카이브
│   └── cs_weekly_analysis_*   # W1~W4 상세 + 요약본
├── cs/                        # CS 운영 매뉴얼 (EN/KO), 플로우, 인포그래픽, 대시보드 매뉴얼
├── chargeback/                # 차지백 운영 매뉴얼, 플로우, 증빙 템플릿
├── chatbot/                   # CS 챗봇 프로젝트 문서
├── faq/                       # FAQ 매뉴얼 (10개 언어)
├── legal/                     # 이용약관 (10개 언어)
├── ticket/                    # 티켓 대시보드
├── ip/                        # IP 보호 운영 매뉴얼
├── scripts/                   # 인덱스 생성 유틸리티
└── CLAUDE.md                  # Claude Code 설정
```

## 카테고리

| 카테고리 | 건수 | 주요 문서 |
|---------|------|----------|
| CS 운영 | 10 | CS 매뉴얼 EN/KO v2.8, Fraud 분석, 자동화 로드맵 |
| FAQ | 10 | 10개 언어 FAQ (EN/FR/DE/ES/PT/JP/CN/TW/IT/TH) |
| AI 챗봇 | 13 | 시스템 개요, 비용 분석, 운영 매뉴얼, 데모 스크립트 |
| 차지백 | 4 | 운영 매뉴얼 v1.4, 플로우, 증빙 템플릿 |
| IP 보호 | 1 | IP 보호 운영 매뉴얼 |
| CS Dashboard | 3 | 대시보드 매뉴얼, 퀵스타트, 통합 로드맵 |
| 대시보드 | 2 | 티켓 대시보드 |
| 정책/약관 | 10 | 이용약관 10개 언어 |
| 기타 | 4 | 포탈 매뉴얼, 템플릿 |

## 디자인 시스템

`design-system/bizops-portal/MASTER.md`에 정의된 글로벌 디자인 규칙:

- **컬러**: Blue primary (#1E40AF) + Amber CTA (#F59E0B)
- **타이포**: Fira Code (heading) + Fira Sans (body)
- **레이아웃**: Sticky navbar → Hero (gradient + stat strip) → Search/Filter → Accordion sections
- **스타일**: Data-Dense Dashboard — 카테고리별 컬러 코딩, 링크 카드 그리드, 반응형 (375/768/1024px)
- **라이트모드만** (다크모드 금지)

CS AI Dashboard (`toomics-ai-agent/dashboard/`)와 동일한 디자인 토큰 공유.

## 배포 방식

### 자동 배포 (GitHub Actions)

`toomics-ai-agent` 레포에서 `reports/` 내 HTML/XLSX 파일이 main에 push되면 자동 배포됩니다.

### 수동 배포

```bash
bash /Claude/toomics-ai-agent/scripts/sync_to_portal.sh
```

## 관리자

유종선 (BizOps PM)
