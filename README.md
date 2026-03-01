# BizOPS Portal

> Toomics Global BizOps 팀 산출물 관리 포탈 (GitHub Pages)

## 배포 URL

**https://tg-bizops.github.io/BizOPS/**

## 구조

```
BizOPS/
├── index.html              # 포탈 메인 페이지 (카테고리별 문서 목록)
├── weekly-reports/          # 주간 CS+차지백 분석 리포트
│   ├── index.html           # 주간 리포트 아카이브
│   └── cs_weekly_analysis_* # W1~W4 상세 + 요약본
├── cs/                      # CS 운영 매뉴얼, 플로우, 인포그래픽
├── chargeback/              # 차지백 운영 매뉴얼, 플로우, 증빙 템플릿
├── chatbot/                 # CS 챗봇 프로젝트 문서
├── ticket/                  # 티켓 대시보드
├── ip/                      # IP 보호 운영 매뉴얼
├── 기타/                    # 기타 산출물
├── scripts/                 # 인덱스 생성 등 유틸리티
└── CLAUDE.md                # Claude Code 설정
```

## 배포 방식

### 자동 배포 (GitHub Actions)

`toomics-ai-agent` 레포에서 `reports/` 내 HTML/XLSX 파일이 main에 push되면 자동 배포됩니다.

### 수동 배포

```bash
bash /Claude/toomics-ai-agent/scripts/sync_to_portal.sh
```

## 관리자

유종선 (BizOps PM)
