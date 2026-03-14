@echo off
color 0E
cls
echo.
echo ================================================================
echo           COMPREHENSIVE FIX - RESTART AND DEBUG
echo ================================================================
echo.

REM Kill all Python
echo [1/6] Stopping all Python processes...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 >nul
echo       Done!

REM Clear cache
echo [2/6] Clearing all cache...
if exist __pycache__ rmdir /s /q __pycache__ >nul 2>&1
if exist instance\__pycache__ rmdir /s /q instance\__pycache__ >nul 2>&1
del /s /q *.pyc >nul 2>&1
echo       Done!

REM Verify model
echo [3/6] Verifying ML model...
python check_model.py
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Model verification failed!
    echo Retraining model now...
    python train_models_improved.py
)
echo.

REM Test fixes
echo [4/6] Testing all fixes...
python test_all_fixes.py
echo.

REM Check files
echo [5/6] Checking critical files...
if exist "static\css\dark-mode-fixes.css" (
    echo       [OK] dark-mode-fixes.css exists
) else (
    echo       [ERROR] dark-mode-fixes.css MISSING!
)

if exist "model.pkl" (
    echo       [OK] model.pkl exists
) else (
    echo       [ERROR] model.pkl MISSING!
)

if exist "static\js\charts.js" (
    echo       [OK] charts.js exists
) else (
    echo       [ERROR] charts.js MISSING!
)
echo.

REM Start app
echo [6/6] Starting Flask application...
echo.
echo ================================================================
echo                    APPLICATION STARTING
echo ================================================================
echo.
echo IMPORTANT: After app starts, follow these steps:
echo.
echo 1. Wait for "Running on http://127.0.0.1:5000"
echo.
echo 2. Open your browser and go to:
echo    http://localhost:5000/debug
echo.
echo 3. Check the debug page:
echo    - Model confidence should be 98.4%%
echo    - Profit should be positive
echo    - All files should show OK
echo.
echo 4. If debug page shows all OK, then go to:
echo    http://localhost:5000
echo.
echo 5. Press Ctrl+F5 to clear browser cache
echo.
echo 6. Login and check dashboard
echo.
echo 7. You should NOW see:
echo    - Confidence: 98.4%%
echo    - Profit: Rs 92,500
echo    - All charts visible
echo.
echo Press Ctrl+C to stop the server
echo ================================================================
echo.

start http://localhost:5000/debug

python app.py

pause
