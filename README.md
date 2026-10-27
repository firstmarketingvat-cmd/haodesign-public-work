# Public Work — 하오디자인 공공기관 홈페이지

공공기관·대학·협회 대상 인쇄물(연차보고서, 정책 리플렛, 기관 브로슈어, 행사 포스터, 다국어 안내물) 전용 하오디자인 홈페이지입니다.

## 미리보기

`run.bat`을 더블클릭하면 http://localhost:5021 이 열립니다. (Python 필요)

## 구조

- `index.html` — 페이지 전체 (HTML + CSS + JS 한 파일)
- `run.bat` — 로컬 미리보기 서버

## 내용 수정 방법

문구·포트폴리오는 `index.html` 맨 아래 `<script>` 안의 데이터 배열만 고치면 화면에 반영됩니다.

| 배열 | 화면 위치 |
|---|---|
| `MENU` | 상단 메뉴 · 전체메뉴 |
| `HERO_IMG`, `HERO_CHIPS` | 메인 비주얼 이미지 · 바로가기 버튼 |
| `WORKS` | PUBLIC WORKS 포트폴리오 |
| `WHY` | WHY HAO DESIGN 탭 |
| `SERVICES` | WHAT WE MAKE 카드 |
| `PROCESS` | PROCESS 단계 |
| `FAQ` | FAQ (FAQPage 스키마 자동 생성) |

이미지는 현재 haodesign.co.kr 서버의 이미지를 직접 참조합니다.

## 게시 전 확인할 것

- 서비스 약속 문구(견적 1일 이내, 회사 서류 제공 등)가 실제 운영과 맞는지
- 회사소개서 · 카카오톡 상담 · 온라인 견적 · 패밀리 사이트 링크 (현재 임시 링크)
- 메인 비주얼 · WHY 배경을 공공 분야 작업 이미지로 교체

## 함께 수정하는 방법

1. `git pull` — 최신 내용 받기
2. 파일 수정 후 `run.bat`으로 확인
3. `git add .` → `git commit -m "수정 내용"` → `git push`
