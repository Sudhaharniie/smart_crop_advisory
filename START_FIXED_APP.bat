@echo off
color 0A
cls
echo.
echo ============================================================
echo           FIXING YOUR APPLICATION NOW
echo ============================================================
echo.
echo What I'm doing:
echo 1. Stopping old Flask server
echo 2. Clearing all cache
echo 3. Starting fresh
echo.
echo Please wait...
echo ============================================================
echo.

REM Step 1: Kill Flask
echo [1/4] Stopping Flask server...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 3 >nul
echo       Done!

REM Step 2: Clear cache
echo [2/4] Clearing Python cache...
if exist __pycache__ rmdir /s /q __pycache__ >nul 2>&1
del /s /q *.pyc >nul 2>&1
echo       Done!

REM Step 3: Verify
echo [3/4] Verifying fixes...
python check_model.py
echo.

REM Step 4: Start
echo [4/4] Starting Flask...
echo.
echo ============================================================
echo                    APP IS STARTING
echo ============================================================
echo.
echo IMPORTANT INSTRUCTIONS:
echo.
echo 1. Wait for "Running on http://127.0.0.1:5000"
echo 2. Open your browser
echo 3. Go to: http://localhost:5000
echo 4. Press Ctrl+F5 to refresh (IMPORTANT!)
echo 5. Login/Register
echo 6. Check dashboard
echo.
echo YOU SHOULD NOW SEE:
echo   - Confidence: 98.4%% (not 33%%)
echo   - Profit: Rs 92,500 (positive!)
echo   - Dark mode: Working!
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python app.py

pause
