@echo off
cd /d "C:\Users\crist\Desktop\Workflow(Projects)\AI_calling agent\AI_VAPI_AGENT"
start "ngrok" cmd /k "ngrok.exe http 5000"
timeout /t 10 /nobreak >nul
start "server" cmd /k "venv\Scripts\python.exe server.py"
timeout /t 5 /nobreak >nul
start "make_calls" cmd /k "venv\Scripts\python.exe make_calls.py"
exit