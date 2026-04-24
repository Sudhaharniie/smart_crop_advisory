@echo off
echo ========================================
echo  RESTARTING APPLICATION WITH NEW FIXES
echo ========================================
echo.

echo [STEP 1] Stopping any running Flask instances...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" 2>nul
timeout /t 2 >nul

echo [STEP 2] Verifying models are correct...
python check_model.py
if %errorlevel% neq 0 (
    echo ERROR: Model verification failed!
    echo Run: python train_models_improved.py
    pause
    exit /b 1
)
echo.

echo [STEP 3] Starting Flask application...
echo.
echo ========================================
echo  APPLICATION STARTING
echo ========================================
echo.
echo Open your browser to: http://localhost:5000
echo.
echo Expected Results:
echo - Confidence: 98.4%%
echo - Profit: Rs 92,500 (positive)
echo - Dark mode: All visible
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py
