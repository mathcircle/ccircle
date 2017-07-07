@echo off
set OUTFILE=ccupdate
set SUBSYS=Windows
set CONSOLE=0

pushd "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\"
call vcvarsall.bat amd64
popd

set INCLUDE=./include/;%INCLUDE%

set CC=cl /nologo
set CC=%CC% /D_CRT_SECURE_NO_DEPRECATE
set CC=%CC% /DWIN32_LEAN_AND_MEAN

set CC=%CC% /O2
set CC=%CC% /MT
set CC=%CC% /MP
set CC=%CC% /W3
set LN=/link /SUBSYSTEM:Windows /OUT:%OUTFILE%.exe

%CC% ./src/*.c %LN%
if errorlevel 1 goto FAIL
echo Build PASSING
del /F /Q *.obj %OUTFILE%.lib %OUTFILE%.exp
pause
goto EOF

:FAIL
echo Build FAILING
del /F /Q *.obj %OUTFILE%.lib %OUTFILE%.exp
pause
