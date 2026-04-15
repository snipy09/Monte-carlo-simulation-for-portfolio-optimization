#!/bin/bash
# Quick Start Script for Monte Carlo Portfolio Optimization

echo "================================================"
echo "Monte Carlo Portfolio Optimizer - Quick Start"
echo "================================================"
echo ""

# 1. Check Python installation
echo "[Step 1] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python found: $(python3 --version)"
echo ""

# 2. Create virtual environment
echo "[Step 2] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# 3. Activate virtual environment
echo "[Step 3] Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# 4. Install dependencies
echo "[Step 4] Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Dependencies installed"
echo ""

# 5. Run optimization
echo "[Step 5] Running Portfolio Optimization..."
echo "================================================"
echo ""
python main.py
echo ""
echo "================================================"
echo "✅ Optimization complete!"
echo ""
echo "📊 Output files generated in ./output/"
echo "   - portfolio_optimization_report.txt"
echo "   - efficient_frontier.png"
echo "   - return_distribution.png"
echo "   - optimal_allocation.png"
echo ""
echo "🌐 To run interactive Streamlit UI:"
echo "   streamlit run app.py"
echo ""
echo "================================================"
