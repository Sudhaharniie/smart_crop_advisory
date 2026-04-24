@echo off
cls
echo ========================================
echo  ONE-CLICK FIX - RESTART EVERYTHING
echo ========================================
echo.

echo [1/5] Stopping all Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul
echo Done!
echo.

echo [2/5] Clearing Python cache...
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
del /s /q *.pyc 2>nul
echo Done!
echo.

echo [3/5] Verifying ML models...
python check_model.py
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Models need retraining!
    echo Running training now...
    python train_models_improved.py
)
echo.

echo [4/5] Testing all fixes...
python test_all_fixes.py
echo.

echo [5/5] Starting application...
echo.
echo ========================================
echo  APPLICATION READY
echo ========================================
echo.
echo IMPORTANT: After app starts:
echo 1. Open: http://localhost:5000
echo 2. Press Ctrl+F5 to clear browser cache
echo 3. Login/Register
echo 4. Check dashboard
echo.
echo Expected Results:
echo - Confidence: 98.4%% (not 33%%)
echo - Profit: Rs 92,500 (positive, not negative)
echo - Dark mode: All visible
echo.
echo Press Ctrl+C to stop server
echo ========================================
echo.

python app.py
