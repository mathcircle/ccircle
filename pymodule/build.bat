@echo off
set ARCH=64
set INSTALL=1
set PYPATH="C:\Python36\"
set VCPATH="C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\"

pushd %VCPATH%
if "%ARCH%"=="32" (
  set BUILDPATH=build\lib.win-x86-3.6\
  call vcvarsall.bat x86
) else if "%ARCH%"=="64" (
  set BUILDPATH=build\lib.win-amd64-3.6\
  call vcvarsall.bat amd64
)
popd

python build.py bdist_wininst --title="Coding Circle Python Extensions"

if "%INSTALL%"=="1" (
  copy %BUILDPATH%*.pyd %PYPATH%Lib\
  copy %BUILDPATH%*.pyd dist\
)
pause
