# Public Work — 하오디자인 공공기관 홈페이지

공공기관·대학·협회 대상 인쇄물(연차보고서, 정책 리플렛, 기관 브로슈어, 행사 포스터, 다국어 안내물) 전용 하오디자인 홈페이지입니다.

## 미리보기

`run.bat`을 더블클릭하면 http://localhost:5021 이 열립니다. (Python 필요)

## 구조

- `index.html` — 페이지 전체 (HTML + CSS + JS 한 파일)
- `assets/works/` — 공공기관 포트폴리오 PDF에서 뽑은 표지(`*-cover.jpg`) · 내지(`*-inner.jpg`)
- `assets/hero.mp4`, `assets/hero-poster.jpg` — 메인 배경 영상 (위 포트폴리오 페이지로 제작)
- `tools/render_pdfs.py` — PDF → 표지·내지 JPG 변환 (PyMuPDF, Pillow)
- `tools/make_hero_video.py` — 포트폴리오 이미지 → 배경 영상 생성 (Pillow, ffmpeg)
- `run.bat` — 로컬 미리보기 서버

### 포트폴리오 추가하는 법

1. PDF를 `tools/render_pdfs.py`의 `SRC` 폴더에 넣고, `SLUG`에 `"파일명 일부": "영문-슬러그"`를 추가
2. `python tools/render_pdfs.py` 실행 → `assets/works/슬러그-cover.jpg`, `슬러그-inner.jpg` 생성
3. `index.html`의 `WORKS` 배열에 `{..., s:'슬러그'}` 한 줄 추가
4. (선택) 배경 영상에도 넣으려면 `tools/make_hero_video.py`의 `SCENES` 수정 후 실행

## 색상 (하오디자인 브랜드 톤)

`index.html` 맨 위 `:root`에서 한 번에 바꿀 수 있습니다.

| 토큰 | 값 | 쓰임 |
|---|---|---|
| `--ink` / `--ink-2` | `#1a1918` / `#2e2c2a` | 웜 차콜 — 히어로 영상 배경, 헤더 메뉴 박스, 탭, 푸터. 그 외 큰 면은 밝게 |
| `--red` / `--red-d` | `#e83817` / `#b82a0f` | 하오 로고 버밀리언 — CTA 밴드 · 팝업 · 회사소개서 배너 · 버튼 · 강조어 |
| `--gold` | `#a8865d` | 샴페인 브론즈 — PUBLIC 배지 · 리플렛 칩 등 아주 작게 |
| `--bg-soft` / `--line` | `#f6f3ef` / `#e9e4de` | 아이보리 배경 · 구분선 |

## 내용 수정 방법

문구·포트폴리오는 `index.html` 맨 아래 `<script>` 안의 데이터 배열만 고치면 화면에 반영됩니다.

| 배열 | 화면 위치 |
|---|---|
| `MENU` | 상단 메뉴 · 전체메뉴 |
| `SEARCH_WORDS` | 메인 검색창에 타이핑되는 추천 검색어 |
| `WORKS` | PUBLIC WORKS 포트폴리오 — 앞 절반은 1줄(왼쪽으로 흐름), 나머지는 2줄(오른쪽으로 흐름). 마우스를 올리면 멈추고, 클릭하면 표지·내지 크게 보기 |
| `WORKS_BG` | PUBLIC WORKS 뒤의 큰 배경 문구 (단어별 블러 인) |
| `WHY` | WHY HAO DESIGN 탭 |
| `SERVICES` | WHAT WE MAKE 카드 |
| `PROCESS` | PROCESS 단계 |
| `FAQ` | FAQ (FAQPage 스키마 자동 생성) |

로고 · 캐릭터 이미지만 haodesign.co.kr 서버를 직접 참조하고, 나머지 이미지 · 영상은 `assets/` 안에 있습니다.

## 게시 전 확인할 것

- 서비스 약속 문구(견적 1일 이내, 회사 서류 제공 등)가 실제 운영과 맞는지
- 회사소개서 · 카카오톡 상담 · 온라인 견적 · 패밀리 사이트 링크 (현재 임시 링크)

## 함께 수정하는 방법

1. `git pull` — 최신 내용 받기
2. 파일 수정 후 `run.bat`으로 확인
3. `git add .` → `git commit -m "수정 내용"` → `git push`
