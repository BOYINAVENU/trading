# 📦 TRANSFER TO HOME PC - COMPLETE CHECKLIST

## 🎯 What You Need to Do

Transfer the entire `polymarket-sniper` folder from your corporate PC to your home PC, then run the setup.

---

## 📋 **Pre-Transfer Checklist (Corporate PC)**

### ✅ Files to Include
- [x] All `.py` files (bot.py, config.py, etc.)
- [x] `.env` file **WITH YOUR PRIVATE KEY**
- [x] `requirements.txt`
- [x] `setup.bat` / `setup.sh`
- [x] All `.md` documentation files
- [x] `.gitignore` file

### ⚠️ Files You DON'T Need
- [ ] `venv/` folder (will recreate on home PC)
- [ ] `data/` folder (will be created automatically)
- [ ] `logs/` folder (will be created automatically)
- [ ] `__pycache__/` folders (will be recreated)

---

## 🔄 **Transfer Methods**

### Option 1: USB Drive (Recommended)
```
1. Copy entire polymarket-sniper folder to USB
2. Take USB home
3. Copy folder to home PC (e.g., C:\Users\YourName\Projects\)
4. Ready to setup!
```

### Option 2: Cloud Storage (OneDrive, Dropbox, Google Drive)
```
1. Zip the folder: polymarket-sniper.zip
2. Upload to cloud storage
3. Download on home PC
4. Extract and ready to setup!
```

### Option 3: Git (If Using GitHub/GitLab)
```
⚠️ WARNING: Never commit .env file with private key!

1. Add .env to .gitignore (already done)
2. git add .
3. git commit -m "Initial bot setup"
4. git push
5. On home PC: git clone <repo-url>
6. Manually add .env file with private key
```

### Option 4: Email to Yourself
```
1. Zip the folder
2. Email to yourself (if <25MB)
3. Download on home PC
4. Extract
```

---

## 🏠 **Setup on Home PC**

### Step 1: Prerequisites
```bash
# Install Python 3.9+ if not already installed
# Download from: https://www.python.org/downloads/
# ✅ Check "Add Python to PATH" during installation

# Verify installation
python --version
# Should show: Python 3.9.x or higher
```

### Step 2: Navigate to Project
```bash
# Windows
cd C:\Users\YourName\Projects\polymarket-sniper

# Or wherever you copied it
```

### Step 3: Update .env for Home Network
```bash
# Open .env in notepad
notepad .env

# Change this line:
DISABLE_SSL_VERIFICATION=False

# (Change True to False - no corporate proxy at home!)
```

### Step 4: Run Setup
```bash
# This will create venv and install all packages
setup.bat
```

### Step 5: Test Setup
```bash
python test_setup.py
```

Expected output:
```
All tests passed! (5/5)
✓ Bot is ready to run!
```

### Step 6: Run Bot
```bash
python run.py
```

---

## 📝 **Important Configuration Changes**

### ✏️ Edit .env File on Home PC

**FROM (Corporate PC):**
```env
DISABLE_SSL_VERIFICATION=True
```

**TO (Home PC):**
```env
DISABLE_SSL_VERIFICATION=False
```

**Everything else stays the same:**
- Private key ✓
- Alchemy RPC URL ✓
- Trading settings ✓

---

## ✅ **Verification on Home PC**

Run these tests to confirm everything works:

### Test 1: Python Version
```bash
python --version
# Expected: Python 3.9.12 or higher
```

### Test 2: Virtual Environment
```bash
# After running setup.bat
dir venv
# Should see: Scripts/, Lib/, etc.
```

### Test 3: Dependencies
```bash
venv\Scripts\activate
pip list
# Should see: py-clob-client, web3, websockets, etc.
```

### Test 4: Full Setup Test
```bash
python test_setup.py
# Expected: 5/5 tests passing
```

### Test 5: Network Connection (No SSL Issues!)
```bash
python test_network.py
# Expected: Multiple working RPC endpoints
```

---

## 🎯 **Expected Differences: Corporate vs Home**

| Aspect | Corporate PC | Home PC |
|--------|--------------|---------|
| SSL Verification | Disabled (True) | Enabled (False) |
| pip install | Needs --trusted-host | Normal install |
| RPC Connection | May be blocked | Should work perfectly |
| Setup Speed | Slower (proxy) | Faster (direct) |
| Network Issues | Common | Rare |

---

## 🚀 **After Successful Setup**

### Fund Your Wallet
```
1. Get wallet address:
   python test_setup.py
   (will show your address)

2. Send USDC to Polygon network:
   - Minimum: $10-20 (testing)
   - Recommended: $50-100 (trading)

3. Send MATIC to Polygon network:
   - Amount: ~$1-2 (gas fees)
```

### Start Trading
```bash
# Run bot
python run.py

# Monitor in another terminal
Get-Content -Path logs\trading.log -Wait -Tail 50
```

---

## 🆘 **If Something Goes Wrong on Home PC**

### Problem: Python not found
```bash
# Reinstall Python 3.9+
# Make sure to check "Add to PATH"
```

### Problem: pip install fails
```bash
# Update pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

### Problem: test_setup.py fails
```bash
# Check specific error
# Most common: dependencies not installed

# Solution:
venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: RPC connection fails
```bash
# Verify Alchemy API key in .env
# Try alternative RPC from RPC_ENDPOINTS.md
```

---

## 📁 **Minimal File List (If Transferring Selectively)**

**Must Have:**
1. `bot.py`
2. `config.py`
3. `market_scanner.py`
4. `trading_engine.py`
5. `risk_manager.py`
6. `websocket_handler.py`
7. `logger.py`
8. `ssl_helper.py`
9. `run.py`
10. `requirements.txt`
11. `.env` (with your private key!)
12. `setup.bat` (Windows) or `setup.sh` (Mac/Linux)
13. `test_setup.py`
14. `.gitignore`

**Nice to Have:**
- All `.md` documentation files
- `esports_tracker.py` (optional)
- `test_network.py` (diagnostic)
- `polymarket-bot.service` (for VPS later)

---

## ✅ **Final Checklist Before Running**

On home PC, verify:

- [ ] Python 3.9+ installed
- [ ] Project folder copied completely
- [ ] `.env` file has `DISABLE_SSL_VERIFICATION=False`
- [ ] `.env` file has your private key
- [ ] `.env` file has Alchemy RPC URL
- [ ] Ran `setup.bat` successfully
- [ ] `python test_setup.py` shows 5/5 passing
- [ ] Wallet funded with USDC + MATIC on Polygon
- [ ] Ready to run: `python run.py`

---

## 🎉 **You're All Set!**

Once everything is working on your home PC:
1. Bot will run smoothly (no corporate restrictions!)
2. Fast RPC connections
3. No SSL issues
4. Monitor and adjust as needed

**For questions or errors on home PC, come back with the specific error message!**

Good luck! 🚀
