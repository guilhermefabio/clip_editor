@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
echo =========================================================
echo   RENDERIZANDO 5 SHORTS  -  1080x1920 60fps
echo   Cortes centrados nos confrontos com inimigo em quadro.
echo =========================================================
set "FF=%~dp0_tools\ffmpeg.exe"
if not exist "%FF%" set "FF=ffmpeg"

if not exist "%~dp0_seg1" mkdir "%~dp0_seg1"
if exist "%~dp0_lista1.txt" del "%~dp0_lista1.txt"
echo.
echo   ---- SHORT 1 de 5 ----
echo     corte 1/34  1.788.666.071 523s cx113px
"%FF%" -y -hide_banner -loglevel error -ss 522.4 -t 2.017 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 1.6667 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\000.mp4"
echo file '_seg1/000.mp4'>>"%~dp0_lista1.txt"
echo     corte 2/34  1.788.666.071 523s cx113px
"%FF%" -y -hide_banner -loglevel error -ss 524.07 -t 2.017 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.6667 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\001.mp4"
echo file '_seg1/001.mp4'>>"%~dp0_lista1.txt"
echo     corte 3/34  1.788.666.071 523s cx113px
"%FF%" -y -hide_banner -loglevel error -ss 525.73 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\002.mp4"
echo file '_seg1/002.mp4'>>"%~dp0_lista1.txt"
echo     corte 4/34  1.788.666.108 293s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 292.4 -t 1.183 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\003.mp4"
echo file '_seg1/003.mp4'>>"%~dp0_lista1.txt"
echo     corte 5/34  1.788.666.108 293s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 293.23 -t 1.183 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\004.mp4"
echo file '_seg1/004.mp4'>>"%~dp0_lista1.txt"
echo     corte 6/34  1.788.666.108 293s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 294.07 -t 1.183 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\005.mp4"
echo file '_seg1/005.mp4'>>"%~dp0_lista1.txt"
echo     corte 7/34  1.788.666.086 32s cx35px
"%FF%" -y -hide_banner -loglevel error -ss 31.4 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\006.mp4"
echo file '_seg1/006.mp4'>>"%~dp0_lista1.txt"
echo     corte 8/34  1.788.666.086 32s cx35px
"%FF%" -y -hide_banner -loglevel error -ss 32.23 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\007.mp4"
echo file '_seg1/007.mp4'>>"%~dp0_lista1.txt"
echo     corte 9/34  1.788.666.086 32s cx35px
"%FF%" -y -hide_banner -loglevel error -ss 33.07 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\008.mp4"
echo file '_seg1/008.mp4'>>"%~dp0_lista1.txt"
echo     corte 10/34  1.788.666.108 345s cx21px
"%FF%" -y -hide_banner -loglevel error -ss 344.4 -t 1.183 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\009.mp4"
echo file '_seg1/009.mp4'>>"%~dp0_lista1.txt"
echo     corte 11/34  1.788.666.108 345s cx21px
"%FF%" -y -hide_banner -loglevel error -ss 345.23 -t 1.183 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\010.mp4"
echo file '_seg1/010.mp4'>>"%~dp0_lista1.txt"
echo     corte 12/34  1.788.666.108 345s cx21px
"%FF%" -y -hide_banner -loglevel error -ss 346.07 -t 1.183 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\011.mp4"
echo file '_seg1/011.mp4'>>"%~dp0_lista1.txt"
echo     corte 13/34  1.788.666.028 319s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 318.4 -t 1.183 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\012.mp4"
echo file '_seg1/012.mp4'>>"%~dp0_lista1.txt"
echo     corte 14/34  1.788.666.028 319s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 319.23 -t 1.183 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\013.mp4"
echo file '_seg1/013.mp4'>>"%~dp0_lista1.txt"
echo     corte 15/34  1.788.666.028 319s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 320.07 -t 1.183 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\014.mp4"
echo file '_seg1/014.mp4'>>"%~dp0_lista1.txt"
echo     corte 16/34  1.788.666.086 390s cx55px
"%FF%" -y -hide_banner -loglevel error -ss 389.4 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\015.mp4"
echo file '_seg1/015.mp4'>>"%~dp0_lista1.txt"
echo     corte 17/34  1.788.666.086 390s cx55px
"%FF%" -y -hide_banner -loglevel error -ss 390.23 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\016.mp4"
echo file '_seg1/016.mp4'>>"%~dp0_lista1.txt"
echo     corte 18/34  1.788.666.086 390s cx55px
"%FF%" -y -hide_banner -loglevel error -ss 391.07 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\017.mp4"
echo file '_seg1/017.mp4'>>"%~dp0_lista1.txt"
echo     corte 19/34  1.788.666.071 210s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 209.4 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0':'108.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.6667 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\018.mp4"
echo file '_seg1/018.mp4'>>"%~dp0_lista1.txt"
echo     corte 20/34  1.788.666.071 210s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 210.23 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=558:994:'1001.0':'43.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.6667 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\019.mp4"
echo file '_seg1/019.mp4'>>"%~dp0_lista1.txt"
echo     corte 21/34  1.788.666.071 210s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 211.07 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\020.mp4"
echo file '_seg1/020.mp4'>>"%~dp0_lista1.txt"
echo     corte 22/34  1.788.666.071 523s cx113px
"%FF%" -y -hide_banner -loglevel error -ss 522.4 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\021.mp4"
echo file '_seg1/021.mp4'>>"%~dp0_lista1.txt"
echo     corte 23/34  1.788.666.071 523s cx113px
"%FF%" -y -hide_banner -loglevel error -ss 523.23 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\022.mp4"
echo file '_seg1/022.mp4'>>"%~dp0_lista1.txt"
echo     corte 24/34  1.788.666.071 523s cx113px
"%FF%" -y -hide_banner -loglevel error -ss 524.07 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\023.mp4"
echo file '_seg1/023.mp4'>>"%~dp0_lista1.txt"
echo     corte 25/34  1.788.666.108 293s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 292.4 -t 1.183 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\024.mp4"
echo file '_seg1/024.mp4'>>"%~dp0_lista1.txt"
echo     corte 26/34  1.788.666.108 293s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 293.23 -t 1.183 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\025.mp4"
echo file '_seg1/025.mp4'>>"%~dp0_lista1.txt"
echo     corte 27/34  1.788.666.108 293s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 294.07 -t 1.183 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=474:842:'1043.0+3.00*sin(2*PI*t*7)':'119.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\026.mp4"
echo file '_seg1/026.mp4'>>"%~dp0_lista1.txt"
echo     corte 28/34  1.788.666.086 32s cx35px
"%FF%" -y -hide_banner -loglevel error -ss 31.4 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=522:928:'1019.0+3.00*sin(2*PI*t*7)':'76.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\027.mp4"
echo file '_seg1/027.mp4'>>"%~dp0_lista1.txt"
echo     corte 29/34  1.788.666.086 32s cx35px
"%FF%" -y -hide_banner -loglevel error -ss 32.23 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=474:842:'1043.0+3.00*sin(2*PI*t*7)':'119.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\028.mp4"
echo file '_seg1/028.mp4'>>"%~dp0_lista1.txt"
echo     corte 30/34  1.788.666.086 32s cx35px
"%FF%" -y -hide_banner -loglevel error -ss 33.07 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=522:928:'1019.0+3.00*sin(2*PI*t*7)':'76.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\029.mp4"
echo file '_seg1/029.mp4'>>"%~dp0_lista1.txt"
echo     corte 31/34  1.788.666.108 480s cx19px
"%FF%" -y -hide_banner -loglevel error -ss 479.4 -t 0.767 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=474:842:'1043.0+5.00*sin(2*PI*t*7)':'119.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4167 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\030.mp4"
echo file '_seg1/030.mp4'>>"%~dp0_lista1.txt"
echo     corte 32/34  1.788.666.108 345s cx21px
"%FF%" -y -hide_banner -loglevel error -ss 344.4 -t 0.767 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=522:928:'1019.0+5.00*sin(2*PI*t*7)':'76.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4167 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\031.mp4"
echo file '_seg1/031.mp4'>>"%~dp0_lista1.txt"
echo     corte 33/34  1.788.666.108 345s cx21px
"%FF%" -y -hide_banner -loglevel error -ss 344.82 -t 0.767 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=474:842:'1043.0+5.00*sin(2*PI*t*7)':'119.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4167 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\032.mp4"
echo file '_seg1/032.mp4'>>"%~dp0_lista1.txt"
echo     corte 34/34  1.788.666.108 345s cx21px
"%FF%" -y -hide_banner -loglevel error -ss 345.23 -t 0.767 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=522:928:'1019.0+5.00*sin(2*PI*t*7)':'76.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4167 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg1\033.mp4"
echo file '_seg1/033.mp4'>>"%~dp0_lista1.txt"
echo     juntando e colando a trilha...
"%FF%" -y -hide_banner -loglevel error -f concat -safe 0 -i "%~dp0_lista1.txt" -i "%~dp0beat_1.wav" -c:v copy -c:a aac -b:a 192k -shortest "%~dp0SHORT_1.mp4"

if not exist "%~dp0_seg2" mkdir "%~dp0_seg2"
if exist "%~dp0_lista2.txt" del "%~dp0_lista2.txt"
echo.
echo   ---- SHORT 2 de 5 ----
echo     corte 1/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 187.4 -t 1.950 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 1.6000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\000.mp4"
echo file '_seg2/000.mp4'>>"%~dp0_lista2.txt"
echo     corte 2/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 189.0 -t 1.950 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.6000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\001.mp4"
echo file '_seg2/001.mp4'>>"%~dp0_lista2.txt"
echo     corte 3/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 190.6 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\002.mp4"
echo file '_seg2/002.mp4'>>"%~dp0_lista2.txt"
echo     corte 4/34  1.788.666.086 70s cx47px
"%FF%" -y -hide_banner -loglevel error -ss 69.4 -t 1.150 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\003.mp4"
echo file '_seg2/003.mp4'>>"%~dp0_lista2.txt"
echo     corte 5/34  1.788.666.086 70s cx47px
"%FF%" -y -hide_banner -loglevel error -ss 70.2 -t 1.150 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\004.mp4"
echo file '_seg2/004.mp4'>>"%~dp0_lista2.txt"
echo     corte 6/34  1.788.666.086 70s cx47px
"%FF%" -y -hide_banner -loglevel error -ss 71.0 -t 1.150 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\005.mp4"
echo file '_seg2/005.mp4'>>"%~dp0_lista2.txt"
echo     corte 7/34  1.788.666.028 3s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 2.4 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\006.mp4"
echo file '_seg2/006.mp4'>>"%~dp0_lista2.txt"
echo     corte 8/34  1.788.666.028 3s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 3.2 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\007.mp4"
echo file '_seg2/007.mp4'>>"%~dp0_lista2.txt"
echo     corte 9/34  1.788.666.028 3s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 4.0 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\008.mp4"
echo file '_seg2/008.mp4'>>"%~dp0_lista2.txt"
echo     corte 10/34  1.788.666.071 334s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 333.4 -t 1.150 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\009.mp4"
echo file '_seg2/009.mp4'>>"%~dp0_lista2.txt"
echo     corte 11/34  1.788.666.071 334s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 334.2 -t 1.150 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\010.mp4"
echo file '_seg2/010.mp4'>>"%~dp0_lista2.txt"
echo     corte 12/34  1.788.666.071 334s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 335.0 -t 1.150 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\011.mp4"
echo file '_seg2/011.mp4'>>"%~dp0_lista2.txt"
echo     corte 13/34  1.788.666.028 79s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 78.4 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\012.mp4"
echo file '_seg2/012.mp4'>>"%~dp0_lista2.txt"
echo     corte 14/34  1.788.666.028 79s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 79.2 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\013.mp4"
echo file '_seg2/013.mp4'>>"%~dp0_lista2.txt"
echo     corte 15/34  1.788.666.028 79s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 80.0 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\014.mp4"
echo file '_seg2/014.mp4'>>"%~dp0_lista2.txt"
echo     corte 16/34  1.788.666.028 476s cx78px
"%FF%" -y -hide_banner -loglevel error -ss 475.4 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\015.mp4"
echo file '_seg2/015.mp4'>>"%~dp0_lista2.txt"
echo     corte 17/34  1.788.666.028 476s cx78px
"%FF%" -y -hide_banner -loglevel error -ss 476.2 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\016.mp4"
echo file '_seg2/016.mp4'>>"%~dp0_lista2.txt"
echo     corte 18/34  1.788.666.028 476s cx78px
"%FF%" -y -hide_banner -loglevel error -ss 477.0 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\017.mp4"
echo file '_seg2/017.mp4'>>"%~dp0_lista2.txt"
echo     corte 19/34  1.788.666.028 493s cx31px
"%FF%" -y -hide_banner -loglevel error -ss 492.4 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0':'108.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.6000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\018.mp4"
echo file '_seg2/018.mp4'>>"%~dp0_lista2.txt"
echo     corte 20/34  1.788.666.028 493s cx31px
"%FF%" -y -hide_banner -loglevel error -ss 493.2 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=558:994:'1001.0':'43.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.6000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\019.mp4"
echo file '_seg2/019.mp4'>>"%~dp0_lista2.txt"
echo     corte 21/34  1.788.666.028 493s cx31px
"%FF%" -y -hide_banner -loglevel error -ss 494.0 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\020.mp4"
echo file '_seg2/020.mp4'>>"%~dp0_lista2.txt"
echo     corte 22/34  1.788.619.696 66s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 65.4 -t 1.150 -i "%~dp0clipe_1.788.619.696.170.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\021.mp4"
echo file '_seg2/021.mp4'>>"%~dp0_lista2.txt"
echo     corte 23/34  1.788.619.696 66s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 66.2 -t 1.150 -i "%~dp0clipe_1.788.619.696.170.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\022.mp4"
echo file '_seg2/022.mp4'>>"%~dp0_lista2.txt"
echo     corte 24/34  1.788.619.696 66s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 67.0 -t 1.150 -i "%~dp0clipe_1.788.619.696.170.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\023.mp4"
echo file '_seg2/023.mp4'>>"%~dp0_lista2.txt"
echo     corte 25/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 187.4 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\024.mp4"
echo file '_seg2/024.mp4'>>"%~dp0_lista2.txt"
echo     corte 26/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 188.2 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\025.mp4"
echo file '_seg2/025.mp4'>>"%~dp0_lista2.txt"
echo     corte 27/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 189.0 -t 1.150 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=474:842:'1043.0+3.00*sin(2*PI*t*7)':'119.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\026.mp4"
echo file '_seg2/026.mp4'>>"%~dp0_lista2.txt"
echo     corte 28/34  1.788.666.086 70s cx47px
"%FF%" -y -hide_banner -loglevel error -ss 69.4 -t 1.150 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=522:928:'1019.0+3.00*sin(2*PI*t*7)':'76.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\027.mp4"
echo file '_seg2/027.mp4'>>"%~dp0_lista2.txt"
echo     corte 29/34  1.788.666.086 70s cx47px
"%FF%" -y -hide_banner -loglevel error -ss 70.2 -t 1.150 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=474:842:'1043.0+3.00*sin(2*PI*t*7)':'119.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\028.mp4"
echo file '_seg2/028.mp4'>>"%~dp0_lista2.txt"
echo     corte 30/34  1.788.666.086 70s cx47px
"%FF%" -y -hide_banner -loglevel error -ss 71.0 -t 1.150 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=522:928:'1019.0+3.00*sin(2*PI*t*7)':'76.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\029.mp4"
echo file '_seg2/029.mp4'>>"%~dp0_lista2.txt"
echo     corte 31/34  1.788.666.028 3s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 2.4 -t 0.750 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=474:842:'1043.0+5.00*sin(2*PI*t*7)':'119.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\030.mp4"
echo file '_seg2/030.mp4'>>"%~dp0_lista2.txt"
echo     corte 32/34  1.788.666.028 3s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 2.8 -t 0.750 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=522:928:'1019.0+5.00*sin(2*PI*t*7)':'76.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\031.mp4"
echo file '_seg2/031.mp4'>>"%~dp0_lista2.txt"
echo     corte 33/34  1.788.666.028 3s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 3.2 -t 0.750 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=474:842:'1043.0+5.00*sin(2*PI*t*7)':'119.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\032.mp4"
echo file '_seg2/032.mp4'>>"%~dp0_lista2.txt"
echo     corte 34/34  1.788.666.071 334s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 333.4 -t 0.750 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=522:928:'1019.0+5.00*sin(2*PI*t*7)':'76.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4000 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg2\033.mp4"
echo file '_seg2/033.mp4'>>"%~dp0_lista2.txt"
echo     juntando e colando a trilha...
"%FF%" -y -hide_banner -loglevel error -f concat -safe 0 -i "%~dp0_lista2.txt" -i "%~dp0beat_2.wav" -c:v copy -c:a aac -b:a 192k -shortest "%~dp0SHORT_2.mp4"

if not exist "%~dp0_seg3" mkdir "%~dp0_seg3"
if exist "%~dp0_lista3.txt" del "%~dp0_lista3.txt"
echo.
echo   ---- SHORT 3 de 5 ----
echo     corte 1/34  1.788.666.028 319s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 318.4 -t 2.089 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 1.7391 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\000.mp4"
echo file '_seg3/000.mp4'>>"%~dp0_lista3.txt"
echo     corte 2/34  1.788.666.028 319s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 320.14 -t 2.089 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.7391 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\001.mp4"
echo file '_seg3/001.mp4'>>"%~dp0_lista3.txt"
echo     corte 3/34  1.788.666.028 319s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 321.88 -t 1.220 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\002.mp4"
echo file '_seg3/002.mp4'>>"%~dp0_lista3.txt"
echo     corte 4/34  1.788.666.086 390s cx55px
"%FF%" -y -hide_banner -loglevel error -ss 389.4 -t 1.220 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\003.mp4"
echo file '_seg3/003.mp4'>>"%~dp0_lista3.txt"
echo     corte 5/34  1.788.666.086 390s cx55px
"%FF%" -y -hide_banner -loglevel error -ss 390.27 -t 1.220 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\004.mp4"
echo file '_seg3/004.mp4'>>"%~dp0_lista3.txt"
echo     corte 6/34  1.788.666.071 210s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 209.4 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\005.mp4"
echo file '_seg3/005.mp4'>>"%~dp0_lista3.txt"
echo     corte 7/34  1.788.666.071 210s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 210.27 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\006.mp4"
echo file '_seg3/006.mp4'>>"%~dp0_lista3.txt"
echo     corte 8/34  1.788.666.071 210s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 211.14 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\007.mp4"
echo file '_seg3/007.mp4'>>"%~dp0_lista3.txt"
echo     corte 9/34  1.788.666.086 245s cx22px
"%FF%" -y -hide_banner -loglevel error -ss 244.4 -t 1.220 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\008.mp4"
echo file '_seg3/008.mp4'>>"%~dp0_lista3.txt"
echo     corte 10/34  1.788.666.086 245s cx22px
"%FF%" -y -hide_banner -loglevel error -ss 245.27 -t 1.220 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\009.mp4"
echo file '_seg3/009.mp4'>>"%~dp0_lista3.txt"
echo     corte 11/34  1.788.666.071 142s cx18px
"%FF%" -y -hide_banner -loglevel error -ss 141.4 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\010.mp4"
echo file '_seg3/010.mp4'>>"%~dp0_lista3.txt"
echo     corte 12/34  1.788.666.071 142s cx18px
"%FF%" -y -hide_banner -loglevel error -ss 142.27 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\011.mp4"
echo file '_seg3/011.mp4'>>"%~dp0_lista3.txt"
echo     corte 13/34  1.788.666.071 142s cx18px
"%FF%" -y -hide_banner -loglevel error -ss 143.14 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\012.mp4"
echo file '_seg3/012.mp4'>>"%~dp0_lista3.txt"
echo     corte 14/34  1.788.666.071 153s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 152.4 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\013.mp4"
echo file '_seg3/013.mp4'>>"%~dp0_lista3.txt"
echo     corte 15/34  1.788.666.071 153s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 153.27 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\014.mp4"
echo file '_seg3/014.mp4'>>"%~dp0_lista3.txt"
echo     corte 16/34  1.788.666.071 153s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 154.14 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\015.mp4"
echo file '_seg3/015.mp4'>>"%~dp0_lista3.txt"
echo     corte 17/34  1.788.666.108 79s cx68px
"%FF%" -y -hide_banner -loglevel error -ss 78.4 -t 1.220 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\016.mp4"
echo file '_seg3/016.mp4'>>"%~dp0_lista3.txt"
echo     corte 18/34  1.788.666.108 79s cx68px
"%FF%" -y -hide_banner -loglevel error -ss 79.27 -t 1.220 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\017.mp4"
echo file '_seg3/017.mp4'>>"%~dp0_lista3.txt"
echo     corte 19/34  1.788.666.108 79s cx68px
"%FF%" -y -hide_banner -loglevel error -ss 80.14 -t 1.220 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=486:864:'1037.0':'108.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.7391 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\018.mp4"
echo file '_seg3/018.mp4'>>"%~dp0_lista3.txt"
echo     corte 20/34  1.788.666.071 272s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 271.4 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=558:994:'1001.0':'43.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.7391 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\019.mp4"
echo file '_seg3/019.mp4'>>"%~dp0_lista3.txt"
echo     corte 21/34  1.788.666.071 272s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 272.27 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\020.mp4"
echo file '_seg3/020.mp4'>>"%~dp0_lista3.txt"
echo     corte 22/34  1.788.666.028 319s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 318.4 -t 1.220 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\021.mp4"
echo file '_seg3/021.mp4'>>"%~dp0_lista3.txt"
echo     corte 23/34  1.788.666.028 319s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 319.27 -t 1.220 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\022.mp4"
echo file '_seg3/022.mp4'>>"%~dp0_lista3.txt"
echo     corte 24/34  1.788.666.028 319s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 320.14 -t 1.220 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\023.mp4"
echo file '_seg3/023.mp4'>>"%~dp0_lista3.txt"
echo     corte 25/34  1.788.666.086 390s cx55px
"%FF%" -y -hide_banner -loglevel error -ss 389.4 -t 1.220 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\024.mp4"
echo file '_seg3/024.mp4'>>"%~dp0_lista3.txt"
echo     corte 26/34  1.788.666.086 390s cx55px
"%FF%" -y -hide_banner -loglevel error -ss 390.27 -t 1.220 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\025.mp4"
echo file '_seg3/025.mp4'>>"%~dp0_lista3.txt"
echo     corte 27/34  1.788.666.071 210s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 209.4 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=474:842:'1043.0+3.00*sin(2*PI*t*7)':'119.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\026.mp4"
echo file '_seg3/026.mp4'>>"%~dp0_lista3.txt"
echo     corte 28/34  1.788.666.071 210s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 210.27 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=522:928:'1019.0+3.00*sin(2*PI*t*7)':'76.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\027.mp4"
echo file '_seg3/027.mp4'>>"%~dp0_lista3.txt"
echo     corte 29/34  1.788.666.071 210s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 211.14 -t 1.220 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=474:842:'1043.0+3.00*sin(2*PI*t*7)':'119.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\028.mp4"
echo file '_seg3/028.mp4'>>"%~dp0_lista3.txt"
echo     corte 30/34  1.788.666.086 245s cx22px
"%FF%" -y -hide_banner -loglevel error -ss 244.4 -t 1.220 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=522:928:'1019.0+3.00*sin(2*PI*t*7)':'76.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8696 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\029.mp4"
echo file '_seg3/029.mp4'>>"%~dp0_lista3.txt"
echo     corte 31/34  1.788.666.086 245s cx22px
"%FF%" -y -hide_banner -loglevel error -ss 245.27 -t 0.785 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=474:842:'1043.0+5.00*sin(2*PI*t*7)':'119.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4348 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\030.mp4"
echo file '_seg3/030.mp4'>>"%~dp0_lista3.txt"
echo     corte 32/34  1.788.666.086 245s cx22px
"%FF%" -y -hide_banner -loglevel error -ss 245.7 -t 0.785 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=522:928:'1019.0+5.00*sin(2*PI*t*7)':'76.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4348 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\031.mp4"
echo file '_seg3/031.mp4'>>"%~dp0_lista3.txt"
echo     corte 33/34  1.788.666.071 142s cx18px
"%FF%" -y -hide_banner -loglevel error -ss 141.4 -t 0.785 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=474:842:'1043.0+5.00*sin(2*PI*t*7)':'119.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4348 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\032.mp4"
echo file '_seg3/032.mp4'>>"%~dp0_lista3.txt"
echo     corte 34/34  1.788.666.071 142s cx18px
"%FF%" -y -hide_banner -loglevel error -ss 141.83 -t 0.785 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=522:928:'1019.0+5.00*sin(2*PI*t*7)':'76.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4348 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg3\033.mp4"
echo file '_seg3/033.mp4'>>"%~dp0_lista3.txt"
echo     juntando e colando a trilha...
"%FF%" -y -hide_banner -loglevel error -f concat -safe 0 -i "%~dp0_lista3.txt" -i "%~dp0beat_3.wav" -c:v copy -c:a aac -b:a 192k -shortest "%~dp0SHORT_3.mp4"

if not exist "%~dp0_seg4" mkdir "%~dp0_seg4"
if exist "%~dp0_lista4.txt" del "%~dp0_lista4.txt"
echo.
echo   ---- SHORT 4 de 5 ----
echo     corte 1/34  1.788.666.028 476s cx78px
"%FF%" -y -hide_banner -loglevel error -ss 475.4 -t 1.889 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 1.5385 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\000.mp4"
echo file '_seg4/000.mp4'>>"%~dp0_lista4.txt"
echo     corte 2/34  1.788.666.028 476s cx78px
"%FF%" -y -hide_banner -loglevel error -ss 476.94 -t 1.889 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.5385 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\001.mp4"
echo file '_seg4/001.mp4'>>"%~dp0_lista4.txt"
echo     corte 3/34  1.788.666.028 476s cx78px
"%FF%" -y -hide_banner -loglevel error -ss 478.48 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\002.mp4"
echo file '_seg4/002.mp4'>>"%~dp0_lista4.txt"
echo     corte 4/34  1.788.666.028 493s cx31px
"%FF%" -y -hide_banner -loglevel error -ss 492.4 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\003.mp4"
echo file '_seg4/003.mp4'>>"%~dp0_lista4.txt"
echo     corte 5/34  1.788.666.028 493s cx31px
"%FF%" -y -hide_banner -loglevel error -ss 493.17 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\004.mp4"
echo file '_seg4/004.mp4'>>"%~dp0_lista4.txt"
echo     corte 6/34  1.788.666.028 493s cx31px
"%FF%" -y -hide_banner -loglevel error -ss 493.94 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\005.mp4"
echo file '_seg4/005.mp4'>>"%~dp0_lista4.txt"
echo     corte 7/34  1.788.619.696 66s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 65.4 -t 1.119 -i "%~dp0clipe_1.788.619.696.170.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\006.mp4"
echo file '_seg4/006.mp4'>>"%~dp0_lista4.txt"
echo     corte 8/34  1.788.619.696 66s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 66.17 -t 1.119 -i "%~dp0clipe_1.788.619.696.170.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\007.mp4"
echo file '_seg4/007.mp4'>>"%~dp0_lista4.txt"
echo     corte 9/34  1.788.619.696 66s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 66.94 -t 1.119 -i "%~dp0clipe_1.788.619.696.170.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\008.mp4"
echo file '_seg4/008.mp4'>>"%~dp0_lista4.txt"
echo     corte 10/34  1.788.666.028 36s cx18px
"%FF%" -y -hide_banner -loglevel error -ss 35.4 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\009.mp4"
echo file '_seg4/009.mp4'>>"%~dp0_lista4.txt"
echo     corte 11/34  1.788.666.028 36s cx18px
"%FF%" -y -hide_banner -loglevel error -ss 36.17 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\010.mp4"
echo file '_seg4/010.mp4'>>"%~dp0_lista4.txt"
echo     corte 12/34  1.788.666.028 36s cx18px
"%FF%" -y -hide_banner -loglevel error -ss 36.94 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\011.mp4"
echo file '_seg4/011.mp4'>>"%~dp0_lista4.txt"
echo     corte 13/34  1.788.666.071 523s cx113px
"%FF%" -y -hide_banner -loglevel error -ss 522.4 -t 1.119 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\012.mp4"
echo file '_seg4/012.mp4'>>"%~dp0_lista4.txt"
echo     corte 14/34  1.788.666.071 523s cx113px
"%FF%" -y -hide_banner -loglevel error -ss 523.17 -t 1.119 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\013.mp4"
echo file '_seg4/013.mp4'>>"%~dp0_lista4.txt"
echo     corte 15/34  1.788.666.071 523s cx113px
"%FF%" -y -hide_banner -loglevel error -ss 523.94 -t 1.119 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\014.mp4"
echo file '_seg4/014.mp4'>>"%~dp0_lista4.txt"
echo     corte 16/34  1.788.666.108 293s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 292.4 -t 1.119 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\015.mp4"
echo file '_seg4/015.mp4'>>"%~dp0_lista4.txt"
echo     corte 17/34  1.788.666.108 293s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 293.17 -t 1.119 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\016.mp4"
echo file '_seg4/016.mp4'>>"%~dp0_lista4.txt"
echo     corte 18/34  1.788.666.108 293s cx85px
"%FF%" -y -hide_banner -loglevel error -ss 293.94 -t 1.119 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\017.mp4"
echo file '_seg4/017.mp4'>>"%~dp0_lista4.txt"
echo     corte 19/34  1.788.666.086 32s cx35px
"%FF%" -y -hide_banner -loglevel error -ss 31.4 -t 1.119 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=486:864:'1037.0':'108.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.5385 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\018.mp4"
echo file '_seg4/018.mp4'>>"%~dp0_lista4.txt"
echo     corte 20/34  1.788.666.086 32s cx35px
"%FF%" -y -hide_banner -loglevel error -ss 32.17 -t 1.119 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=558:994:'1001.0':'43.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.5385 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\019.mp4"
echo file '_seg4/019.mp4'>>"%~dp0_lista4.txt"
echo     corte 21/34  1.788.666.086 32s cx35px
"%FF%" -y -hide_banner -loglevel error -ss 32.94 -t 1.119 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\020.mp4"
echo file '_seg4/020.mp4'>>"%~dp0_lista4.txt"
echo     corte 22/34  1.788.666.028 476s cx78px
"%FF%" -y -hide_banner -loglevel error -ss 475.4 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\021.mp4"
echo file '_seg4/021.mp4'>>"%~dp0_lista4.txt"
echo     corte 23/34  1.788.666.028 476s cx78px
"%FF%" -y -hide_banner -loglevel error -ss 476.17 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\022.mp4"
echo file '_seg4/022.mp4'>>"%~dp0_lista4.txt"
echo     corte 24/34  1.788.666.028 476s cx78px
"%FF%" -y -hide_banner -loglevel error -ss 476.94 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\023.mp4"
echo file '_seg4/023.mp4'>>"%~dp0_lista4.txt"
echo     corte 25/34  1.788.666.028 493s cx31px
"%FF%" -y -hide_banner -loglevel error -ss 492.4 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\024.mp4"
echo file '_seg4/024.mp4'>>"%~dp0_lista4.txt"
echo     corte 26/34  1.788.666.028 493s cx31px
"%FF%" -y -hide_banner -loglevel error -ss 493.17 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\025.mp4"
echo file '_seg4/025.mp4'>>"%~dp0_lista4.txt"
echo     corte 27/34  1.788.666.028 493s cx31px
"%FF%" -y -hide_banner -loglevel error -ss 493.94 -t 1.119 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=474:842:'1043.0+3.00*sin(2*PI*t*7)':'119.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\026.mp4"
echo file '_seg4/026.mp4'>>"%~dp0_lista4.txt"
echo     corte 28/34  1.788.619.696 66s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 65.4 -t 1.119 -i "%~dp0clipe_1.788.619.696.170.mp4" -vf "crop=522:928:'1019.0+3.00*sin(2*PI*t*7)':'76.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\027.mp4"
echo file '_seg4/027.mp4'>>"%~dp0_lista4.txt"
echo     corte 29/34  1.788.619.696 66s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 66.17 -t 1.119 -i "%~dp0clipe_1.788.619.696.170.mp4" -vf "crop=474:842:'1043.0+3.00*sin(2*PI*t*7)':'119.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\028.mp4"
echo file '_seg4/028.mp4'>>"%~dp0_lista4.txt"
echo     corte 30/34  1.788.619.696 66s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 66.94 -t 1.119 -i "%~dp0clipe_1.788.619.696.170.mp4" -vf "crop=522:928:'1019.0+3.00*sin(2*PI*t*7)':'76.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.7692 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\029.mp4"
echo file '_seg4/029.mp4'>>"%~dp0_lista4.txt"
echo     corte 31/34  1.788.666.028 36s cx18px
"%FF%" -y -hide_banner -loglevel error -ss 35.4 -t 0.735 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=474:842:'1043.0+5.00*sin(2*PI*t*7)':'119.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.3846 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\030.mp4"
echo file '_seg4/030.mp4'>>"%~dp0_lista4.txt"
echo     corte 32/34  1.788.666.028 36s cx18px
"%FF%" -y -hide_banner -loglevel error -ss 35.78 -t 0.735 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=522:928:'1019.0+5.00*sin(2*PI*t*7)':'76.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.3846 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\031.mp4"
echo file '_seg4/031.mp4'>>"%~dp0_lista4.txt"
echo     corte 33/34  1.788.666.028 36s cx18px
"%FF%" -y -hide_banner -loglevel error -ss 36.17 -t 0.735 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=474:842:'1043.0+5.00*sin(2*PI*t*7)':'119.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.3846 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\032.mp4"
echo file '_seg4/032.mp4'>>"%~dp0_lista4.txt"
echo     corte 34/34  1.788.666.071 523s cx113px
"%FF%" -y -hide_banner -loglevel error -ss 522.4 -t 0.735 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=522:928:'1019.0+5.00*sin(2*PI*t*7)':'76.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.3846 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg4\033.mp4"
echo file '_seg4/033.mp4'>>"%~dp0_lista4.txt"
echo     juntando e colando a trilha...
"%FF%" -y -hide_banner -loglevel error -f concat -safe 0 -i "%~dp0_lista4.txt" -i "%~dp0beat_4.wav" -c:v copy -c:a aac -b:a 192k -shortest "%~dp0SHORT_4.mp4"

if not exist "%~dp0_seg5" mkdir "%~dp0_seg5"
if exist "%~dp0_lista5.txt" del "%~dp0_lista5.txt"
echo.
echo   ---- SHORT 5 de 5 ----
echo     corte 1/34  1.788.666.071 153s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 152.4 -t 2.168 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 1.8182 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\000.mp4"
echo file '_seg5/000.mp4'>>"%~dp0_lista5.txt"
echo     corte 2/34  1.788.666.071 153s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 154.22 -t 2.168 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.8182 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\001.mp4"
echo file '_seg5/001.mp4'>>"%~dp0_lista5.txt"
echo     corte 3/34  1.788.666.071 153s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 156.04 -t 1.259 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\002.mp4"
echo file '_seg5/002.mp4'>>"%~dp0_lista5.txt"
echo     corte 4/34  1.788.666.108 79s cx68px
"%FF%" -y -hide_banner -loglevel error -ss 78.4 -t 1.259 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\003.mp4"
echo file '_seg5/003.mp4'>>"%~dp0_lista5.txt"
echo     corte 5/34  1.788.666.108 79s cx68px
"%FF%" -y -hide_banner -loglevel error -ss 79.31 -t 1.259 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\004.mp4"
echo file '_seg5/004.mp4'>>"%~dp0_lista5.txt"
echo     corte 6/34  1.788.666.108 79s cx68px
"%FF%" -y -hide_banner -loglevel error -ss 80.22 -t 1.259 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\005.mp4"
echo file '_seg5/005.mp4'>>"%~dp0_lista5.txt"
echo     corte 7/34  1.788.666.071 272s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 271.4 -t 1.259 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\006.mp4"
echo file '_seg5/006.mp4'>>"%~dp0_lista5.txt"
echo     corte 8/34  1.788.666.071 272s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 272.31 -t 1.259 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\007.mp4"
echo file '_seg5/007.mp4'>>"%~dp0_lista5.txt"
echo     corte 9/34  1.788.666.028 517s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 516.4 -t 1.259 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\008.mp4"
echo file '_seg5/008.mp4'>>"%~dp0_lista5.txt"
echo     corte 10/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 187.4 -t 1.259 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\009.mp4"
echo file '_seg5/009.mp4'>>"%~dp0_lista5.txt"
echo     corte 11/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 188.31 -t 1.259 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\010.mp4"
echo file '_seg5/010.mp4'>>"%~dp0_lista5.txt"
echo     corte 12/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 189.22 -t 1.259 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\011.mp4"
echo file '_seg5/011.mp4'>>"%~dp0_lista5.txt"
echo     corte 13/34  1.788.666.086 70s cx47px
"%FF%" -y -hide_banner -loglevel error -ss 69.4 -t 1.259 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\012.mp4"
echo file '_seg5/012.mp4'>>"%~dp0_lista5.txt"
echo     corte 14/34  1.788.666.086 70s cx47px
"%FF%" -y -hide_banner -loglevel error -ss 70.31 -t 1.259 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\013.mp4"
echo file '_seg5/013.mp4'>>"%~dp0_lista5.txt"
echo     corte 15/34  1.788.666.086 70s cx47px
"%FF%" -y -hide_banner -loglevel error -ss 71.22 -t 1.259 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\014.mp4"
echo file '_seg5/014.mp4'>>"%~dp0_lista5.txt"
echo     corte 16/34  1.788.666.028 3s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 2.4 -t 1.259 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\015.mp4"
echo file '_seg5/015.mp4'>>"%~dp0_lista5.txt"
echo     corte 17/34  1.788.666.028 3s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 3.31 -t 1.259 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\016.mp4"
echo file '_seg5/016.mp4'>>"%~dp0_lista5.txt"
echo     corte 18/34  1.788.666.028 3s cx23px
"%FF%" -y -hide_banner -loglevel error -ss 4.22 -t 1.259 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\017.mp4"
echo file '_seg5/017.mp4'>>"%~dp0_lista5.txt"
echo     corte 19/34  1.788.666.071 334s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 333.4 -t 1.259 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0':'108.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.8182 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\018.mp4"
echo file '_seg5/018.mp4'>>"%~dp0_lista5.txt"
echo     corte 20/34  1.788.666.071 334s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 334.31 -t 1.259 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=558:994:'1001.0':'43.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.8182 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\019.mp4"
echo file '_seg5/019.mp4'>>"%~dp0_lista5.txt"
echo     corte 21/34  1.788.666.071 334s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 335.22 -t 1.259 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\020.mp4"
echo file '_seg5/020.mp4'>>"%~dp0_lista5.txt"
echo     corte 22/34  1.788.666.071 153s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 152.4 -t 1.259 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\021.mp4"
echo file '_seg5/021.mp4'>>"%~dp0_lista5.txt"
echo     corte 23/34  1.788.666.071 153s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 153.31 -t 1.259 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\022.mp4"
echo file '_seg5/022.mp4'>>"%~dp0_lista5.txt"
echo     corte 24/34  1.788.666.071 153s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 154.22 -t 1.259 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=558:994:'1001.0+3.00*sin(2*PI*t*7)':'43.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\023.mp4"
echo file '_seg5/023.mp4'>>"%~dp0_lista5.txt"
echo     corte 25/34  1.788.666.108 79s cx68px
"%FF%" -y -hide_banner -loglevel error -ss 78.4 -t 1.259 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\024.mp4"
echo file '_seg5/024.mp4'>>"%~dp0_lista5.txt"
echo     corte 26/34  1.788.666.108 79s cx68px
"%FF%" -y -hide_banner -loglevel error -ss 79.31 -t 1.259 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\025.mp4"
echo file '_seg5/025.mp4'>>"%~dp0_lista5.txt"
echo     corte 27/34  1.788.666.108 79s cx68px
"%FF%" -y -hide_banner -loglevel error -ss 80.22 -t 1.259 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=474:842:'1043.0+3.00*sin(2*PI*t*7)':'119.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\026.mp4"
echo file '_seg5/026.mp4'>>"%~dp0_lista5.txt"
echo     corte 28/34  1.788.666.071 272s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 271.4 -t 1.259 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=522:928:'1019.0+3.00*sin(2*PI*t*7)':'76.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\027.mp4"
echo file '_seg5/027.mp4'>>"%~dp0_lista5.txt"
echo     corte 29/34  1.788.666.071 272s cx26px
"%FF%" -y -hide_banner -loglevel error -ss 272.31 -t 1.259 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=474:842:'1043.0+3.00*sin(2*PI*t*7)':'119.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\028.mp4"
echo file '_seg5/028.mp4'>>"%~dp0_lista5.txt"
echo     corte 30/34  1.788.666.028 517s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 516.4 -t 1.259 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=522:928:'1019.0+3.00*sin(2*PI*t*7)':'76.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.9091 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\029.mp4"
echo file '_seg5/029.mp4'>>"%~dp0_lista5.txt"
echo     corte 31/34  1.788.666.028 517s cx24px
"%FF%" -y -hide_banner -loglevel error -ss 517.31 -t 0.804 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=474:842:'1043.0+5.00*sin(2*PI*t*7)':'119.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4545 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\030.mp4"
echo file '_seg5/030.mp4'>>"%~dp0_lista5.txt"
echo     corte 32/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 187.4 -t 0.804 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=522:928:'1019.0+5.00*sin(2*PI*t*7)':'76.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4545 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\031.mp4"
echo file '_seg5/031.mp4'>>"%~dp0_lista5.txt"
echo     corte 33/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 187.85 -t 0.804 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=474:842:'1043.0+5.00*sin(2*PI*t*7)':'119.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4545 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\032.mp4"
echo file '_seg5/032.mp4'>>"%~dp0_lista5.txt"
echo     corte 34/34  1.788.666.028 188s cx70px
"%FF%" -y -hide_banner -loglevel error -ss 188.31 -t 0.804 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=522:928:'1019.0+5.00*sin(2*PI*t*7)':'76.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4545 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "%~dp0_seg5\033.mp4"
echo file '_seg5/033.mp4'>>"%~dp0_lista5.txt"
echo     juntando e colando a trilha...
"%FF%" -y -hide_banner -loglevel error -f concat -safe 0 -i "%~dp0_lista5.txt" -i "%~dp0beat_5.wav" -c:v copy -c:a aac -b:a 192k -shortest "%~dp0SHORT_5.mp4"

echo.
echo =========================================================
echo   PRONTO:  SHORT_1.mp4  ate  SHORT_5.mp4
echo =========================================================
pause