@echo off
rem 하오디자인 공공기관 홈페이지 로컬 미리보기
cd /d "%~dp0"
start "" http://localhost:5021/
python -m http.server 5021
