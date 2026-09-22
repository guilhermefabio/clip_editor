@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
echo =========================================================
echo   RENDER FINAL DO EDIT PHONK  -  1080x1920 60fps
echo   Sai do arquivo original, qualidade cheia.
echo =========================================================
set "FF=%~dp0_tools\ffmpeg.exe"
if not exist "%FF%" set "FF=ffmpeg"
if not exist "%~dp0_seg" mkdir "%~dp0_seg"
if exist "%~dp0_lista.txt" del "%~dp0_lista.txt"

echo   corte 1 de 34  -  galpao industrial
"%FF%" -y -hide_banner -loglevel error -ss 543.75 -t 2.017 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 1.6667 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\000.mp4"
echo file '_seg/000.mp4'>>"%~dp0_lista.txt"
echo   corte 2 de 34  -  corredor de madeira
"%FF%" -y -hide_banner -loglevel error -ss 32.75 -t 2.017 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=546:972:'1007.0+3.00*sin(2*PI*t*7)':'54.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.6667 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\001.mp4"
echo file '_seg/001.mp4'>>"%~dp0_lista.txt"
echo   corte 3 de 34  -  corrida externa
"%FF%" -y -hide_banner -loglevel error -ss 579.75 -t 1.183 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=498:886:'1031.0+3.00*sin(2*PI*t*7)':'97.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\002.mp4"
echo file '_seg/002.mp4'>>"%~dp0_lista.txt"
echo   corte 4 de 34  -  arma em primeiro plano
"%FF%" -y -hide_banner -loglevel error -ss 416.75 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=576:1026:'992.0+3.00*sin(2*PI*t*7)':'27.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\003.mp4"
echo file '_seg/003.mp4'>>"%~dp0_lista.txt"
echo   corte 5 de 34  -  interior, rajada
"%FF%" -y -hide_banner -loglevel error -ss 22.75 -t 1.183 -i "%~dp0clipe_1.788.666.099.033.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\004.mp4"
echo file '_seg/004.mp4'>>"%~dp0_lista.txt"
echo   corte 6 de 34  -  galpao industrial
"%FF%" -y -hide_banner -loglevel error -ss 541.25 -t 1.183 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=546:972:'1007.0+3.00*sin(2*PI*t*7)':'54.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\005.mp4"
echo file '_seg/005.mp4'>>"%~dp0_lista.txt"
echo   corte 7 de 34  -  corredor de madeira
"%FF%" -y -hide_banner -loglevel error -ss 36.75 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=498:886:'1031.0+3.00*sin(2*PI*t*7)':'97.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\006.mp4"
echo file '_seg/006.mp4'>>"%~dp0_lista.txt"
echo   corte 8 de 34  -  corrida externa
"%FF%" -y -hide_banner -loglevel error -ss 577.25 -t 1.183 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=576:1026:'992.0+3.00*sin(2*PI*t*7)':'27.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\007.mp4"
echo file '_seg/007.mp4'>>"%~dp0_lista.txt"
echo   corte 9 de 34  -  arma em primeiro plano
"%FF%" -y -hide_banner -loglevel error -ss 414.25 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\008.mp4"
echo file '_seg/008.mp4'>>"%~dp0_lista.txt"
echo   corte 10 de 34  -  interior, rajada
"%FF%" -y -hide_banner -loglevel error -ss 20.25 -t 1.183 -i "%~dp0clipe_1.788.666.099.033.mp4" -vf "crop=546:972:'1007.0+3.00*sin(2*PI*t*7)':'54.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\009.mp4"
echo file '_seg/009.mp4'>>"%~dp0_lista.txt"
echo   corte 11 de 34  -  varanda externa
"%FF%" -y -hide_banner -loglevel error -ss 296.75 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=498:886:'1031.0+3.00*sin(2*PI*t*7)':'97.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\010.mp4"
echo file '_seg/010.mp4'>>"%~dp0_lista.txt"
echo   corte 12 de 34  -  comodo interno
"%FF%" -y -hide_banner -loglevel error -ss 474.75 -t 1.183 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=576:1026:'992.0+3.00*sin(2*PI*t*7)':'27.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\011.mp4"
echo file '_seg/011.mp4'>>"%~dp0_lista.txt"
echo   corte 13 de 34  -  interior, troca de tiros
"%FF%" -y -hide_banner -loglevel error -ss 51.75 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\012.mp4"
echo file '_seg/012.mp4'>>"%~dp0_lista.txt"
echo   corte 14 de 34  -  varanda externa
"%FF%" -y -hide_banner -loglevel error -ss 291.75 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=546:972:'1007.0+3.00*sin(2*PI*t*7)':'54.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\013.mp4"
echo file '_seg/013.mp4'>>"%~dp0_lista.txt"
echo   corte 15 de 34  -  comodo interno
"%FF%" -y -hide_banner -loglevel error -ss 477.75 -t 1.183 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=498:886:'1031.0+3.00*sin(2*PI*t*7)':'97.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\014.mp4"
echo file '_seg/014.mp4'>>"%~dp0_lista.txt"
echo   corte 16 de 34  -  interior, troca de tiros
"%FF%" -y -hide_banner -loglevel error -ss 49.25 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=576:1026:'992.0+3.00*sin(2*PI*t*7)':'27.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\015.mp4"
echo file '_seg/015.mp4'>>"%~dp0_lista.txt"
echo   corte 17 de 34  -  varanda com inimigos
"%FF%" -y -hide_banner -loglevel error -ss 20.75 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\016.mp4"
echo file '_seg/016.mp4'>>"%~dp0_lista.txt"
echo   corte 18 de 34  -  interior escuro
"%FF%" -y -hide_banner -loglevel error -ss 452.75 -t 1.183 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=546:972:'1007.0+3.00*sin(2*PI*t*7)':'54.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\017.mp4"
echo file '_seg/017.mp4'>>"%~dp0_lista.txt"
echo   corte 19 de 34  -  interior, avanco
"%FF%" -y -hide_banner -loglevel error -ss 119.5 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=498:886:'1031.0':'97.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.6667 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\018.mp4"
echo file '_seg/018.mp4'>>"%~dp0_lista.txt"
echo   corte 20 de 34  -  varanda com inimigos
"%FF%" -y -hide_banner -loglevel error -ss 24.75 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=576:1026:'992.0':'27.0',setpts=2.0*PTS,scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 1.6667 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\019.mp4"
echo file '_seg/019.mp4'>>"%~dp0_lista.txt"
echo   corte 21 de 34  -  interior escuro
"%FF%" -y -hide_banner -loglevel error -ss 450.25 -t 1.183 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\020.mp4"
echo file '_seg/020.mp4'>>"%~dp0_lista.txt"
echo   corte 22 de 34  -  interior, avanco
"%FF%" -y -hide_banner -loglevel error -ss 117.0 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=546:972:'1007.0+3.00*sin(2*PI*t*7)':'54.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\021.mp4"
echo file '_seg/021.mp4'>>"%~dp0_lista.txt"
echo   corte 23 de 34  -  corredor iluminado
"%FF%" -y -hide_banner -loglevel error -ss 169.75 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=498:886:'1031.0+3.00*sin(2*PI*t*7)':'97.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\022.mp4"
echo file '_seg/022.mp4'>>"%~dp0_lista.txt"
echo   corte 24 de 34  -  interior, arma apontada
"%FF%" -y -hide_banner -loglevel error -ss 433.75 -t 1.183 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=576:1026:'992.0+3.00*sin(2*PI*t*7)':'27.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\023.mp4"
echo file '_seg/023.mp4'>>"%~dp0_lista.txt"
echo   corte 25 de 34  -  sala com janelas
"%FF%" -y -hide_banner -loglevel error -ss 243.75 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=588:1048:'986.0+3.00*sin(2*PI*t*7)':'16.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\024.mp4"
echo file '_seg/024.mp4'>>"%~dp0_lista.txt"
echo   corte 26 de 34  -  corredor iluminado
"%FF%" -y -hide_banner -loglevel error -ss 176.75 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=546:972:'1007.0+3.00*sin(2*PI*t*7)':'54.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\025.mp4"
echo file '_seg/025.mp4'>>"%~dp0_lista.txt"
echo   corte 27 de 34  -  interior, arma apontada
"%FF%" -y -hide_banner -loglevel error -ss 438.75 -t 1.183 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\026.mp4"
echo file '_seg/026.mp4'>>"%~dp0_lista.txt"
echo   corte 28 de 34  -  sala com janelas
"%FF%" -y -hide_banner -loglevel error -ss 249.75 -t 1.183 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\027.mp4"
echo file '_seg/027.mp4'>>"%~dp0_lista.txt"
echo   corte 29 de 34  -  externa, estrutura metalica
"%FF%" -y -hide_banner -loglevel error -ss 359.75 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=486:864:'1037.0+3.00*sin(2*PI*t*7)':'108.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\028.mp4"
echo file '_seg/028.mp4'>>"%~dp0_lista.txt"
echo   corte 30 de 34  -  externa, estrutura metalica
"%FF%" -y -hide_banner -loglevel error -ss 354.75 -t 1.183 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=534:950:'1013.0+3.00*sin(2*PI*t*7)':'65.0+2.40*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fps=60,format=yuv420p" -t 0.8333 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\029.mp4"
echo file '_seg/029.mp4'>>"%~dp0_lista.txt"
echo   corte 31 de 34  -  galpao industrial
"%FF%" -y -hide_banner -loglevel error -ss 543.75 -t 0.767 -i "%~dp0clipe_1.788.666.108.219.mp4" -vf "crop=486:864:'1037.0+5.00*sin(2*PI*t*7)':'108.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4167 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\030.mp4"
echo file '_seg/030.mp4'>>"%~dp0_lista.txt"
echo   corte 32 de 34  -  corredor de madeira
"%FF%" -y -hide_banner -loglevel error -ss 32.75 -t 0.767 -i "%~dp0clipe_1.788.666.086.994.mp4" -vf "crop=534:950:'1013.0+5.00*sin(2*PI*t*7)':'65.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4167 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\031.mp4"
echo file '_seg/031.mp4'>>"%~dp0_lista.txt"
echo   corte 33 de 34  -  corrida externa
"%FF%" -y -hide_banner -loglevel error -ss 579.75 -t 0.767 -i "%~dp0clipe_1.788.666.028.140.mp4" -vf "crop=486:864:'1037.0+5.00*sin(2*PI*t*7)':'108.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4167 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\032.mp4"
echo file '_seg/032.mp4'>>"%~dp0_lista.txt"
echo   corte 34 de 34  -  arma em primeiro plano
"%FF%" -y -hide_banner -loglevel error -ss 416.75 -t 0.767 -i "%~dp0clipe_1.788.666.071.210.mp4" -vf "crop=534:950:'1013.0+5.00*sin(2*PI*t*7)':'65.0+4.00*cos(2*PI*t*9)',scale=1080:1920:flags=lanczos,curves=all='0/0.015 0.25/0.255 0.55/0.66 1/0.99',eq=contrast=1.24:saturation=0.56:brightness=0.005:gamma=1.05,unsharp=5:5:0.9:5:5:0.0,vignette=PI/5,fade=t=in:st=0:d=0.07:color=white,fps=60,format=yuv420p" -t 0.4167 -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "%~dp0_seg\033.mp4"
echo file '_seg/033.mp4'>>"%~dp0_lista.txt"

echo.
echo   Juntando os cortes e colando a trilha...
"%FF%" -y -hide_banner -loglevel error -f concat -safe 0 -i "%~dp0_lista.txt" -i "%~dp0audio\beat_phonk.wav" -c:v copy -c:a aac -b:a 192k -shortest "%~dp0EDIT_PHONK.mp4"

echo.
echo =========================================================
echo   PRONTO:  EDIT_PHONK.mp4
echo =========================================================
pause