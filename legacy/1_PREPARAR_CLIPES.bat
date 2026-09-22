@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo =========================================================
echo   PREPARANDO OS CLIPES PARA O EDIT PHONK
echo   (pode deixar rodando, nao feche esta janela)
echo =========================================================
echo.

set "FF=%~dp0_tools\ffmpeg.exe"
set "FP=%~dp0_tools\ffprobe.exe"

if exist "%FF%" goto :temff

where ffmpeg >nul 2>nul
if not errorlevel 1 (
  set "FF=ffmpeg"
  set "FP=ffprobe"
  goto :temff
)

echo [1/3] ffmpeg nao encontrado no sistema. Baixando build oficial...
echo       ^(~100 MB, so acontece uma vez^)
if not exist "%~dp0_tools" mkdir "%~dp0_tools"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; $u='https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'; $z=Join-Path $env:TEMP 'ffmpeg_dl.zip'; Invoke-WebRequest -Uri $u -OutFile $z -UseBasicParsing; $d=Join-Path $env:TEMP 'ffmpeg_ex'; if(Test-Path $d){Remove-Item $d -Recurse -Force}; Expand-Archive -Path $z -DestinationPath $d -Force; $e=Get-ChildItem $d -Recurse -Filter ffmpeg.exe | Select-Object -First 1; $p=Get-ChildItem $d -Recurse -Filter ffprobe.exe | Select-Object -First 1; Copy-Item $e.FullName (Join-Path '%~dp0_tools' 'ffmpeg.exe') -Force; Copy-Item $p.FullName (Join-Path '%~dp0_tools' 'ffprobe.exe') -Force; Remove-Item $z -Force"
if errorlevel 1 goto :erro

:temff
echo.
echo [2/3] Lendo informacoes dos clipes...
if exist "%~dp0_proxy" goto :temdir
mkdir "%~dp0_proxy"
:temdir

if exist "%~dp0_proxy\INFO.txt" del "%~dp0_proxy\INFO.txt"
for %%F in ("%~dp0*.mp4") do (
  echo   - %%~nxF
  echo ### %%~nxF>>"%~dp0_proxy\INFO.txt"
  "%FP%" -v error -show_entries format=duration -show_entries stream=width,height,r_frame_rate,codec_type -of default=noprint_wrappers=1 "%%F">>"%~dp0_proxy\INFO.txt"
  echo.>>"%~dp0_proxy\INFO.txt"
)

echo.
echo [3/3] Gerando versoes leves ^(480p, sem audio^) para analise...
echo       Isso e a parte demorada. Cada clipe leva alguns minutos.
echo.
for %%F in ("%~dp0*.mp4") do (
  if exist "%~dp0_proxy\%%~nF.mp4" (
    echo   [ja existe] %%~nxF
  ) else (
    echo   [convertendo] %%~nxF
    "%FF%" -y -hide_banner -loglevel error -stats -i "%%F" -vf "scale=-2:480" -c:v libx264 -crf 32 -preset veryfast -an "%~dp0_proxy\%%~nF.mp4"
  )
)

echo.
echo =========================================================
echo   PRONTO! Pode voltar pro chat do Claude e avisar.
echo =========================================================
echo.
pause
exit /b 0

:erro
echo.
echo ---------------------------------------------------------
echo   ERRO ao baixar o ffmpeg. Verifique a internet e tente
echo   de novo, ou avise no chat.
echo ---------------------------------------------------------
pause
exit /b 1
