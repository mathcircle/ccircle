REM set GLFW library env variable
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
  setx GLFW_LIBRARY "%~dp0%external\glfw3_windows_64\lib-mingw-w64\glfw3.dll"
) else (
  echo 'Installer not built for 32-bit installs. Ask Brendan for help.'
  pause
)