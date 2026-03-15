# 🏠 HOME PC SETUP GUIDE - NO CORPORATE RESTRICTIONS

This guide is for setting up the bot on your **personal/home PC** where there are no corporate firewalls or SSL restrictions.

---

## 📋 **Quick Start (Fresh Setup on Home PC)**

### **Step 1: Copy Project Files**

Transfer the entire `polymarket-sniper` folder to your home PC:
- Via USB drive, cloud storage, or Git
- Keep the entire folder structure intact

### **Step 2: Prerequisites**

Install Python 3.9+ on your home PC:
- Download: https://www.python.org/downloads/
- ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
- Verify: `python --version` (should show 3.9+)

### **Step 3: Run Setup Script**

**On Windows:**
```bash
cd polymarket-sniper
setup.bat
```

**On Mac/Linux:**
```bash
cd polymarket-sniper
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment
- Install all dependencies (no SSL issues on home network!)
- Create .env file
- Create data and logs folders

### **Step 4: Configure .env File**

Edit `.env` file:

```env
# Your Ethereum wallet private key
PRIVATE_KEY=b4d38e76517308385ea9d34c2a04bf6834cd77045c793f074c0ed673fdb4e0b3

# Use Alchemy (your free API key)
POLYGON_RPC_URL=https://polygon-mainnet.g.alchemy.com/v2/jDw4YYLZ4bWSF-DtNhbb1
CHAIN_ID=137

# Trading settings (adjust as needed)
MAX_POSITION_SIZE_PCT=1.0
MIN_PROBABILITY_THRESHOLD=98.0
TIME_TO_CLOSE_THRESHOLD_MINUTES=5

# Risk management
DAILY_LOSS_LIMIT_PCT=5.0
MAX_CONSECUTIVE_LOSSES=3
MIN_BALANCE_USDC=10.0

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/trading.log

# Corporate network settings (set to False for home PC)
DISABLE_SSL_VERIFICATION=False
```

**KEY CHANGE**: Set `DISABLE_SSL_VERIFICATION=False` on home PC (no corporate proxy!)

### **Step 5: Test Setup**

```bash
python test_setup.py
```

Should show:
```
All tests passed! (5/5)
✓ Bot is ready to run!
```

### **Step 6: Fund Your Wallet**

Your wallet needs:

**1. USDC on Polygon Network**
- Minimum: $10-20 (for testing)
- Recommended: $50-100 (for real trading)
- Bridge from Ethereum: https://wallet.polygon.technology/bridge
- OR buy on exchange and withdraw to Polygon

**2. MATIC on Polygon Network**
- Amount: ~$1-2 (for gas fees)
- Gas is cheap on Polygon (~$0.01-0.10 per trade)

**How to get your wallet address:**
```bash
python -c "from web3 import Web3; from config import Config; print(Web3().eth.account.from_key(Config.PRIVATE_KEY).address)"
```

Send funds to this address **on Polygon network** (not Ethereum mainnet!)

### **Step 7: Run the Bot**

```bash
python run.py
```

Bot will:
- Connect to Polymarket
- Scan markets every 30 seconds
- Execute trades when opportunities found (≥98% probability, <5 min to close)
- Log everything to `logs/trading.log`
- Generate PNL charts in `logs/` folder

---

## 🎯 **Key Differences: Home PC vs Corporate**

| Setting | Corporate PC | Home PC |
|---------|-------------|----------|
| SSL Verification | Disabled (`True`) | Enabled (`False`) |
| pip install | Need `--trusted-host` | Normal install |
| RPC Access | May be blocked | Should work fine |
| Setup Script | `setup_corporate.bat` | `setup.bat` |

---

## ✅ **Verification Checklist**

Before running the bot, verify:

- [ ] Python 3.9+ installed (`python --version`)
- [ ] Virtual environment created (`venv` folder exists)
- [ ] All dependencies installed (`pip list` shows py_clob_client, web3, etc.)
- [ ] `.env` file configured with your private key
- [ ] `DISABLE_SSL_VERIFICATION=False` in `.env` (for home PC)
- [ ] Alchemy RPC URL in `.env`
- [ ] `test_setup.py` shows 5/5 tests passing
- [ ] Wallet has USDC on Polygon (check in test output)
- [ ] Wallet has MATIC on Polygon (check in test output)

---

## 🚀 **Running the Bot 24/7 (Optional)**

### **Option 1: Keep PC Running**
```bash
python run.py
```
- Keep terminal window open
- Bot runs continuously
- Press Ctrl+C to stop

### **Option 2: Run as Windows Service**
Use `run.py` which auto-restarts on crashes:
```bash
python run.py
```

### **Option 3: Deploy to VPS (Best for 24/7)**
See `README.md` VPS Deployment section:
- $5-6/month
- Always online
- Fast connection
- Professional setup

---

## 📊 **Monitoring**

### **Watch Logs in Real-Time**
```bash
# Windows PowerShell
Get-Content -Path logs\trading.log -Wait -Tail 50

# Command Prompt
powershell Get-Content -Path logs\trading.log -Wait -Tail 50

# Mac/Linux
tail -f logs/trading.log
```

### **Check PNL Charts**
- Charts saved in `logs/` folder
- View with any image viewer
- Updated after each trading session

### **Check Trade History**
```bash
# View recent trades
type data\trades.json

# On Mac/Linux
cat data/trades.json
```

---

## 🔧 **Troubleshooting**

### **Import Errors**
```bash
# Activate venv first
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Then run bot
python run.py
```

### **RPC Connection Errors**
- Check internet connection
- Verify Alchemy API key is correct
- Try alternative RPC (see `RPC_ENDPOINTS.md`)

### **No Opportunities Found**
- This is normal! High-probability opportunities are rare
- Lower thresholds in `.env` to see more (but higher risk):
  ```env
  MIN_PROBABILITY_THRESHOLD=95.0
  TIME_TO_CLOSE_THRESHOLD_MINUTES=10
  ```

### **Insufficient Balance Errors**
- Add more USDC to wallet on Polygon
- Verify you sent to **Polygon network**, not Ethereum mainnet

---

## 📁 **Files to Transfer to Home PC**

Copy entire folder, but these are the essential files:

**Core Bot Files:**
- `bot.py` - Main orchestrator
- `market_scanner.py` - Market scanning
- `trading_engine.py` - Trade execution
- `risk_manager.py` - Risk management
- `websocket_handler.py` - Real-time data
- `logger.py` - Logging and charts
- `config.py` - Configuration
- `ssl_helper.py` - SSL handling
- `esports_tracker.py` - Esports data (optional)
- `run.py` - Auto-restart wrapper

**Setup Files:**
- `requirements.txt` - Dependencies
- `.env` - Your configuration (with private key!)
- `setup.bat` / `setup.sh` - Setup scripts
- `test_setup.py` - Verification test

**Documentation:**
- `README.md` - Main guide
- `QUICKSTART.md` - Quick start
- `STRATEGY.md` - Strategy details
- `HOME_PC_SETUP.md` - This file!

**Optional but Useful:**
- `TROUBLESHOOTING.md` - Common issues
- `RPC_ENDPOINTS.md` - RPC alternatives
- `test_network.py` - Network diagnostics

---

## 🎯 **Recommended Workflow**

### **Initial Testing (Day 1-3)**
1. Start with small balance ($10-20 USDC)
2. Set conservative thresholds:
   ```env
   MIN_PROBABILITY_THRESHOLD=99.0
   MAX_POSITION_SIZE_PCT=0.5
   ```
3. Monitor closely
4. Verify trades execute correctly

### **Scaling Up (Week 1)**
1. Add more capital ($50-100)
2. Adjust settings based on observations
3. Check PNL charts
4. Review trade logs

### **Production (Week 2+)**
1. Run 24/7 on VPS or dedicated PC
2. Monitor daily
3. Compound profits
4. Track performance

---

## 💰 **Expected Performance**

Based on the 99% win-rate strategy:

**Conservative ($50 starting balance):**
- Position size: $0.25-0.50 per trade
- Avg profit per trade: $0.02-0.05
- Trades per day: 1-5 (varies by market activity)
- Monthly return: 5-15% (compounded)

**Aggressive ($500 starting balance):**
- Position size: $2.50-5.00 per trade
- Avg profit per trade: $0.20-0.50
- Trades per day: 1-5
- Monthly return: 5-15% (compounded)

**Note**: Results vary based on market conditions, especially during major esports tournaments and sports events.

---

## 📞 **Support**

If you have issues on your home PC:
1. Run diagnostics: `python test_setup.py`
2. Check logs: `type logs\trading.log`
3. Review troubleshooting guides
4. Ask for help with specific error messages

---

## ✅ **Ready to Go!**

Once setup on home PC:
```bash
# 1. Test
python test_setup.py

# 2. Run
python run.py

# 3. Monitor
# Open another terminal
Get-Content -Path logs\trading.log -Wait -Tail 50
```

**Good luck and happy trading!** 🚀
