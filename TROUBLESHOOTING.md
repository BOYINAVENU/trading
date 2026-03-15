# 🔧 Troubleshooting Guide

## Common Installation Issues

### 1. Permission Denied Creating Virtual Environment

**Error**: `[Errno 13] Permission denied: '...venv\Scripts\python.exe'`

#### Cause
- Existing venv folder with locked files
- Antivirus blocking execution
- Insufficient permissions
- Python process still running

#### Solutions

**Option A: Remove existing venv and retry (Recommended)**
```bash
# Run the fix script
fix_permissions.bat

# Then run setup
setup_corporate.bat
```

**Option B: Manual cleanup**
```bash
# 1. Close all Python processes and terminals
# 2. Delete venv folder manually
#    Navigate to: C:\Users\AL55582\CascadeProjects\polymarket-sniper
#    Delete the "venv" folder
# 3. Run setup again
setup_corporate.bat
```

**Option C: Run as Administrator**
```bash
# Right-click Command Prompt → Run as administrator
cd C:\Users\AL55582\CascadeProjects\polymarket-sniper
setup_corporate.bat
```

**Option D: Install without virtual environment**
```bash
# Install to system Python (not recommended but works)
setup_no_venv.bat
```

**Option E: Use conda instead of venv**
```bash
# If you have Anaconda/Miniconda
conda create -n polymarket python=3.9
conda activate polymarket
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

### 2. SSL Certificate Errors

**Error**: `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain`

#### Solution
See **CORPORATE_NETWORK_FIX.md** for complete guide.

**Quick Fix**:
```bash
setup_corporate.bat
```

---

### 3. Antivirus Blocking Installation

**Symptoms**:
- Setup hangs or freezes
- Permission errors
- "Access denied" messages

#### Solution
```bash
# Temporarily disable antivirus
# Then run setup
setup_corporate.bat

# Re-enable antivirus after installation
```

**Whitelist these paths**:
- `C:\Users\AL55582\CascadeProjects\polymarket-sniper\venv`
- Python installation folder
- pip cache folder

---

### 4. Python Not Found

**Error**: `'python' is not recognized as an internal or external command`

#### Solution
**Option A: Add Python to PATH**
1. Find Python installation (usually `C:\Users\AL55582\AppData\Local\Programs\Python\Python3XX`)
2. Add to PATH:
   - Win+R → `sysdm.cpl` → Advanced → Environment Variables
   - Edit PATH, add Python folder and Scripts subfolder
3. Restart terminal

**Option B: Use full path**
```bash
# Replace "python" with full path
C:\Users\AL55582\AppData\Local\Programs\Python\Python39\python.exe -m venv venv
```

**Option C: Reinstall Python**
1. Download from https://python.org/downloads/
2. **Check "Add Python to PATH" during installation**
3. Install

---

### 5. pip Install Fails - Package Not Found

**Error**: `Could not find a version that satisfies the requirement...`

#### Solution
```bash
# Update pip first
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

# Install packages one by one to identify problem
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org py-clob-client
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org web3
# ... etc
```

---

### 6. ImportError When Running Bot

**Error**: `ModuleNotFoundError: No module named 'py_clob_client'`

#### Cause
- Dependencies not installed in active environment
- Wrong Python environment activated

#### Solution
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Verify you see (venv) in prompt
# Then reinstall dependencies
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# Verify installation
python test_setup.py
```

---

### 7. Web3 Connection Errors

**Error**: `Could not connect to Polygon RPC`

#### Solution
```bash
# Try different RPC URLs in .env
POLYGON_RPC_URL=https://polygon-rpc.com
# OR
POLYGON_RPC_URL=https://rpc-mainnet.maticvigil.com
# OR
POLYGON_RPC_URL=https://polygon-mainnet.infura.io/v3/YOUR_INFURA_KEY
```

---

### 8. Insufficient Balance Errors

**Error**: `Insufficient balance for trade`

#### Cause
- Not enough USDC on Polygon
- USDC on wrong network (Ethereum instead of Polygon)
- Balance below minimum threshold

#### Solution
```bash
# 1. Verify you have USDC on Polygon (not Ethereum mainnet)
python test_setup.py  # Shows balances

# 2. Bridge USDC to Polygon
#    Use: https://wallet.polygon.technology/bridge

# 3. Check minimum balance setting in .env
MIN_BALANCE_USDC=10.0  # Lower this if needed
```

---

### 9. No Opportunities Found

**Not an error** - this is normal!

Markets with ≥98% probability and <5 min to close are rare.

#### Solutions to find more opportunities
```env
# In .env file:

# Lower probability threshold (more opportunities, slightly more risk)
MIN_PROBABILITY_THRESHOLD=95.0

# Increase time window (more opportunities, slightly more risk)
TIME_TO_CLOSE_THRESHOLD_MINUTES=10

# Run during peak times:
# - Major esports tournaments (LoL Worlds, Dota TI)
# - US sports prime time (evenings EST)
# - High volatility crypto periods
```

---

### 10. Bot Crashes on Startup

**Error**: Various errors when running `python bot.py`

#### Diagnostic Steps
```bash
# 1. Run setup test to identify issue
python test_setup.py

# 2. Check logs
type logs\trading.log

# 3. Verify .env configuration
# Make sure PRIVATE_KEY is set correctly

# 4. Test Python version
python --version  # Should be 3.9+
```

---

## Quick Diagnostic Commands

```bash
# Check Python version
python --version

# Check if virtual environment is activated
where python  # Should show venv\Scripts\python.exe

# List installed packages
pip list

# Verify specific package
pip show py-clob-client

# Test imports
python -c "import py_clob_client; import web3; print('OK')"

# Check wallet connection
python -c "from config import Config; from web3 import Web3; w3 = Web3(Web3.HTTPProvider(Config.POLYGON_RPC_URL)); print('Connected:', w3.is_connected())"
```

---

## Installation Method Decision Tree

```
Can you create venv?
│
├─ YES → Use setup_corporate.bat (recommended)
│
├─ NO → Permission error?
│   │
│   ├─ YES → Try fix_permissions.bat
│   │   │
│   │   ├─ Works → Continue with setup_corporate.bat
│   │   │
│   │   └─ Still fails → Try setup_no_venv.bat OR run as admin
│   │
│   └─ Other error → See specific error section above
│
└─ SSL errors? → See CORPORATE_NETWORK_FIX.md
```

---

## Emergency: Quick Manual Install

If all automated scripts fail:

```bash
# 1. Open Command Prompt as Administrator

# 2. Navigate to project
cd C:\Users\AL55582\CascadeProjects\polymarket-sniper

# 3. Create venv (if possible)
python -m venv venv
venv\Scripts\activate

# 4. Install pip packages with trusted hosts
python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip

pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org py-clob-client web3 python-dotenv requests websockets matplotlib pandas aiohttp colorama tabulate python-dateutil

# 5. Setup config
copy .env.example .env
mkdir data
mkdir logs

# 6. Edit .env and add PRIVATE_KEY

# 7. Test
python test_setup.py
```

---

## Still Having Issues?

### Checklist
- [ ] Python 3.9+ installed (`python --version`)
- [ ] Command Prompt run as Administrator
- [ ] Antivirus disabled temporarily
- [ ] venv folder deleted (if exists)
- [ ] Corporate network SSL workaround applied
- [ ] .env file created with valid PRIVATE_KEY
- [ ] Internet connection working

### Get Help
1. Run `python test_setup.py` and share output
2. Check `logs/trading.log` for errors
3. Share exact error message
4. Include Python version and OS version

---

## Common Questions

**Q: Do I need a virtual environment?**
A: No, but it's recommended. You can use `setup_no_venv.bat` to install to system Python.

**Q: Can I use Anaconda instead?**
A: Yes! Create conda environment and install requirements.txt.

**Q: Why do I need --trusted-host flags?**
A: Corporate networks intercept SSL with self-signed certificates. This bypasses that.

**Q: Is it safe to disable SSL verification for PyPI?**
A: Yes, PyPI is the official Python package repository. Your network is causing the issue, not PyPI.

**Q: Can I run this on Mac/Linux?**
A: Yes, use `setup.sh` instead of `.bat` files. Most issues here are Windows-specific.

---

**Most common fix**: Run `fix_permissions.bat` then `setup_corporate.bat`
