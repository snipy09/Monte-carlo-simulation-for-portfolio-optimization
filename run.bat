@echo off
REM Quick Start Script for Monte Carlo Portfolio Optimization (Windows)

echo ================================================
echo Monte Carlo Portfolio Optimizer - Quick Start
echo ================================================
echo.

REM 1. Check Python installation
echo [Step 1] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python not found. Please install Python 3.8 or higher.
    exit /b 1
)
echo OK Python found
echo.

REM 2. Create virtual environment
echo [Step 2] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo OK Virtual environment created
) else (
    echo OK Virtual environment already exists
)
echo.

REM 3. Activate virtual environment
echo [Step 3] Activating virtual environment...
call venv\Scripts\activate.bat
echo OK Virtual environment activated
echo.

REM 4. Install dependencies
echo [Step 4] Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
echo OK Dependencies installed
echo.

REM 5. Run optimization
echo [Step 5] Running Portfolio Optimization...
echo ================================================
echo.
python main.py
echo.
echo ================================================
echo OK Optimization complete!
echo.
echo Output files generated in .\output\
echo   - portfolio_optimization_report.txt
echo   - efficient_frontier.png
echo   - return_distribution.png
echo   - optimal_allocation.png
echo.
echo To run interactive Streamlit UI:
echo   streamlit run app.py
echo.
echo ================================================
pause
