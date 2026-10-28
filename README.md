# Public Work — 하오디자인 공공기관 홈페이지

공공기관·대학·협회 대상 인쇄물(연차보고서, 정책 리플렛, 기관 브로슈어, 행사 포스터, 다국어 안내물) 전용 하오디자인 홈페이지입니다.

## 미리보기

`run.bat`을 더블클릭하면 http://localhost:5021 이 열립니다. (Python 필요)

## 구조

- `index.html` — 페이지 전체 (HTML + CSS + JS 한 파일)
- `assets/works/` — 공공기관 포트폴리오 PDF에서 뽑은 표지(`*-cover.jpg`) · 내지(`*-inner.jpg`)
- `assets/hero.mp4`, `assets/hero-poster.jpg` — 메인 배경 영상 (위 포트폴리오 페이지로 제작)
- `assets/about/` — ABOUT · FACILITY 섹션의 제작설비 사진(인쇄 · 후가공 · 재단)
- `tools/render_pdfs.py` — PDF → 표지·내지 JPG 변환 (PyMuPDF, Pillow)
- `tools/make_hero_video.py` — 포트폴리오 이미지 → 배경 영상 생성 (Pillow, ffmpeg)
- `run.bat` — 로컬 미리보기 서버

### 포트폴리오 추가하는 법

1. PDF를 `tools/render_pdfs.py`의 `SRC` 폴더에 넣고, `SLUG`에 `"파일명 일부": "영문-슬러그"`를 추가
2. `python tools/render_pdfs.py` 실행 → `assets/works/슬러그-cover.jpg`, `슬러그-inner.jpg` 생성
3. `index.html`의 `WORKS` 배열에 `{..., s:'슬러그'}` 한 줄 추가
4. (선택) 배경 영상에도 넣으려면 `tools/make_hero_video.py`의 `SCENES` 수정 후 실행

## 레이아웃 · 효과

UNIST 메인(1920px 실측)의 레이아웃과 효과를 그대로 쓰고, 내용만 하오디자인 공공기관 콘텐츠로 채웠습니다.

| 섹션 | 효과 |
|---|---|
| 헤더 | 반투명 흰 헤더 + 네이비 견적문의 박스, 마우스를 올리면 전체메뉴 |
| 히어로 | 포트폴리오로 만든 배경 영상 + 하단 유리 검색창 |
| PUBLIC WORKS | 큰 배경 문구가 카드 앞에서 블러 인 → 카드 2줄이 반대 방향으로 흐름 → 문구는 뒤로 물러남, 하단 range 바 |
| Information for 담당자 | 슬라이더 + 배너 3개 |
| WHY HAO DESIGN | 화면 고정, 배경 문구 → 세로 카드 4장이 차례로 올라옴 |
| WHAT WE MAKE | 카드 슬라이더(점 · 화살표) |
| PROCESS | 화면 고정, 2열 카드가 서로 다른 속도로 올라감 → 마지막에 설비 사진 + 십자 |
| SINCE 2013 | 연혁 카드 슬라이더 |
| 전체 | Lenis 부드러운 스크롤(움직임 줄이기 설정이면 기본 스크롤) |

## 색상 (네이비 미드나잇 + 하오 버밀리언)

`index.html` `<style>` 아래쪽 '하오디자인 콘텐츠 적용' 블록의 `:root`에서 바꿉니다.

| 토큰 | 값 | 쓰임 |
|---|---|---|
| `--navy` | `#0E1B2C` | 헤더 글자 · 견적문의 박스 · 푸터 |
| `--red` / `--red-d` | `#E83817` / `#B82A0F` | 하오 로고 버밀리언 — 제목 점 · 팝업 · 회사소개서 배너 · PROCESS 칩 |
| `--steel` | `#8FA3B8` | 리플렛 칩 · 보조 칩 |
| `--bgtxt-d` / `--bgtxt-l` | `#9FB0C2` / `#E7EBF0` | 큰 배경 문구(앞 · 뒤) |
| `--ivory` | `#F5F2EC` | WHAT WE MAKE 배경 · 배너 |

배경 영상 색을 바꾸려면 `tools/make_hero_video.py`의 `bg()`를 고친 뒤 실행하고, `index.html`의 `hero.mp4?v=` 숫자를 올려 주세요(브라우저 캐시 갱신).

## 내용 수정 방법

문구·포트폴리오는 `index.html` 맨 아래 `<script>` 안의 데이터 배열만 고치면 화면에 반영됩니다.

| 배열 | 화면 위치 |
|---|---|
| `MENU` / `LINK` | 상단 메뉴 · 전체메뉴 / 메뉴별 이동할 섹션 |
| `TODAY_BG` | PUBLIC WORKS 뒤의 큰 배경 문구 |
| `WORKS` | PUBLIC WORKS 포트폴리오 — 앞 절반은 1줄(←), 나머지는 2줄(→). 마우스를 올리면 멈춤 |
| `WHY_BG` / `WHY` | WHY HAO DESIGN 배경 문구 / 카드 4장 |
| `SERVICES` | WHAT WE MAKE 카드 |
| `PROCESS` | PROCESS 6단계 카드 (사진은 haodesign.co.kr 회사소개의 제작과정 사진) |
| `HISTORY` | SINCE 2013 연혁 카드 (연도 순서대로 `{y, t, i}`) |

로고 · 캐릭터 · 제작과정 사진은 haodesign.co.kr 서버를 직접 참조하고, 나머지 이미지 · 영상은 `assets/` 안에 있습니다.

## 게시 전 확인할 것

- 회사소개서 · 온라인 견적 · 패밀리 사이트 · 운영 채널 링크 (현재 임시 링크)
- 이전 버전(회사소개 SINCE 타임라인 · FAQ · CTA 포함)은 git 기록의 `73045c9` 커밋에 있습니다

## 함께 수정하는 방법

1. `git pull` — 최신 내용 받기
2. 파일 수정 후 `run.bat`으로 확인
3. `git add .` → `git commit -m "수정 내용"` → `git push`
