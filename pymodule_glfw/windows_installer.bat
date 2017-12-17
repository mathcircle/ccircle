REM set GLFW library env variable
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
  setx GLFW_LIBRARY "%~dp0%external\glfw3\lib\glfw3.dll"
) else (
  echo 'Installer not built for 32-bit installs. Ask Brendan for help.'
  pause
)

python -m pip install glfw-cffi numpy Pillow