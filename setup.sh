#!/bin/bash

echo "===================================================================="
echo "POLYMARKET SNIPER BOT - LINUX/MAC QUICK SETUP"
echo "===================================================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.9+ first"
    exit 1
fi

echo "[1/5] Python detected"
python3 --version

# Create virtual environment
echo ""
echo "[2/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment and install dependencies
echo ""
echo "[3/5] Installing dependencies..."
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

# Copy .env.example to .env if it doesn't exist
echo ""
echo "[4/5] Setting up configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template"
    echo "[IMPORTANT] Edit .env file and add your PRIVATE_KEY before running!"
else
    echo ".env file already exists"
fi

# Create data and logs directories
mkdir -p data logs

# Run setup test
echo ""
echo "[5/5] Running setup verification..."
python test_setup.py

echo ""
echo "===================================================================="
echo "SETUP COMPLETE!"
echo "===================================================================="
echo ""
echo "NEXT STEPS:"
echo "1. Edit .env file and add your Ethereum private key"
echo "   nano .env"
echo "2. Fund your wallet with USDC on Polygon network"
echo "3. Run: python test_setup.py (to verify everything works)"
echo "4. Run: python run.py (to start the bot)"
echo ""
echo "===================================================================="
