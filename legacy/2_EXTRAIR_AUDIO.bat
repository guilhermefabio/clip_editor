@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo =========================================================
echo   EXTRAINDO O AUDIO DOS CLIPES
echo   (rapido - so o som, pra eu achar os tiroteios)
echo =========================================================
echo.

set "FF=%~dp0_tools\ffmpeg.exe"
if not exist "%FF%" set "FF=ffmpeg"

if exist "%~dp0_proxy" goto :temdir
mkdir "%~dp0_proxy"
:temdir

for %%F in ("%~dp0*.mp4") do (
  echo   [extraindo] %%~nxF
  "%FF%" -y -hide_banner -loglevel error -i "%%F" -vn -ac 1 -ar 22050 -b:a 48k "%~dp0_proxy\%%~nF.mp3"
)

echo.
echo =========================================================
echo   PRONTO! Volta pro chat e me avisa.
echo =========================================================
pause
