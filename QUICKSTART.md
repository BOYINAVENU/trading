# 🚀 Quick Start Guide - 5 Minutes to First Trade

## Prerequisites Checklist
- [ ] Ethereum wallet with private key
- [ ] Polygon USDC balance (min $50)
- [ ] Python 3.9+ installed
- [ ] 5 minutes of your time

---

## Step 1: Install (1 minute)

### Windows
```bash
# Run automated setup
setup.bat
```

### Linux/Mac
```bash
# Make setup script executable and run
chmod +x setup.sh
./setup.sh
```

### Manual Installation
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy config template
cp .env.example .env
```

---

## Step 2: Configure (2 minutes)

Edit `.env` file:

```env
# REQUIRED: Add your private key
PRIVATE_KEY=0x1234567890abcdef...

# OPTIONAL: Adjust these if needed (defaults are good)
MAX_POSITION_SIZE_PCT=1.0
MIN_PROBABILITY_THRESHOLD=98.0
TIME_TO_CLOSE_THRESHOLD_MINUTES=5
```

**Where to get your private key:**
- MetaMask: Account Details → Export Private Key
- **⚠️ Never share this key or commit it to git!**

---

## Step 3: Fund Wallet (1 minute)

Get USDC on Polygon network:

**Option A - Bridge from Ethereum:**
1. Go to https://wallet.polygon.technology/bridge
2. Bridge USDC from Ethereum to Polygon

**Option B - Buy directly:**
1. Buy USDC on exchange (Coinbase, Binance)
2. Withdraw to Polygon network (cheaper fees)

**Recommended amounts:**
- Testing: $50-100
- Serious trading: $500-1000+

---

## Step 4: Test Setup (30 seconds)

```bash
python test_setup.py
```

This verifies:
- ✓ Python version correct
- ✓ All dependencies installed
- ✓ Private key configured
- ✓ Wallet connected
- ✓ Balance sufficient

---

## Step 5: Run Bot (30 seconds)

```bash
# Start with auto-restart
python run.py

# OR direct run
python bot.py
```

**You should see:**
```
====================================================================
POLYMARKET SNIPER BOT STARTED
====================================================================
Strategy: High-probability sniper (≥98%)
Time threshold: ≤5 minutes
Position size: 1% per trade
Daily loss limit: 5%
====================================================================

--- Scan #1 at 14:30:15 ---
Scan complete: 0 markets, 0 opportunities
```

---

## What to Expect

### First Hour
- Bot scans markets every 30 seconds
- May not find opportunities immediately (98%+ markets are rare)
- Check logs: `tail -f logs/trading.log` (Linux/Mac) or open `logs/trading.log` in editor

### First Trade
When opportunity found:
```
OPPORTUNITY: Will Team A win? | Outcome: Yes | Prob: 98.50% | Closes in: 180s
EXECUTING TRADE
Market: Will Team A win?
Outcome: Yes
Probability: 98.50%
Price: $0.985
Position Size: $10.00
Shares: 10.15
```

### After 24 Hours
- View PNL chart: `data/pnl_chart.png`
- Check trade history: `data/trades.json`
- Review daily stats in logs

---

## Common Issues & Fixes

### "No opportunities found"
✅ **Normal** - 98%+ markets are rare
- Wait during major esports tournaments
- Try lowering threshold to 95%: `MIN_PROBABILITY_THRESHOLD=95.0`
- Increase time window: `TIME_TO_CLOSE_THRESHOLD_MINUTES=10`

### "Insufficient balance"
- Check you have USDC on **Polygon** (not Ethereum mainnet)
- Verify balance: `python test_setup.py`
- Fund wallet with more USDC

### "Failed to initialize bot"
- Check private key in `.env` (no quotes, starts with 0x)
- Verify Python 3.9+: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`

### Bot crashes
- Check logs: `logs/trading.log`
- Run test: `python test_setup.py`
- Auto-restart enabled with `python run.py`

---

## Monitoring Your Bot

### Real-time Logs
```bash
# Linux/Mac
tail -f logs/trading.log

# Windows PowerShell
Get-Content logs/trading.log -Wait -Tail 50
```

### Check Performance
- **PNL Chart**: `data/pnl_chart.png` (updated hourly)
- **Trade History**: `data/trades.json`
- **Performance Data**: `data/performance.json`

### Daily Stats
Bot logs stats every 10 scans:
```
DAILY SUMMARY: PNL: $23.50 | Trades: 15 | Win Rate: 93.3% | Consecutive Losses: 0
```

---

## Optimizing for Your Needs

### More Aggressive (more trades, higher risk)
```env
MIN_PROBABILITY_THRESHOLD=95.0
TIME_TO_CLOSE_THRESHOLD_MINUTES=10
MAX_POSITION_SIZE_PCT=2.0
```

### More Conservative (fewer trades, lower risk)
```env
MIN_PROBABILITY_THRESHOLD=99.0
TIME_TO_CLOSE_THRESHOLD_MINUTES=3
MAX_POSITION_SIZE_PCT=0.5
```

### Esports Focus
1. Get Riot API key: https://developer.riotgames.com/
2. Get Steam API key: https://steamcommunity.com/dev/apikey
3. Add to `.env`:
   ```env
   RIOT_API_KEY=your_key
   DOTA_STEAM_API_KEY=your_key
   ```

---

## Running 24/7 on VPS

### Quick VPS Setup (DigitalOcean/Vultr)

```bash
# 1. SSH into VPS
ssh user@your-vps-ip

# 2. Clone repo
git clone <repo-url>
cd polymarket-sniper

# 3. Run setup
chmod +x setup.sh
./setup.sh

# 4. Edit config
nano .env
# Add private key

# 5. Setup systemd service
sudo cp polymarket-bot.service /etc/systemd/system/
sudo nano /etc/systemd/system/polymarket-bot.service
# Edit username in file

sudo systemctl daemon-reload
sudo systemctl enable polymarket-bot
sudo systemctl start polymarket-bot

# 6. Check status
sudo systemctl status polymarket-bot
```

---

## Safety Reminders

1. ✅ Start with small amounts ($50-100)
2. ✅ Test for 24 hours before increasing capital
3. ✅ Never commit `.env` file to git
4. ✅ Use dedicated wallet (not your main wallet)
5. ✅ Monitor daily - check logs once per day
6. ✅ Withdraw profits regularly

---

## Getting Help

- **Setup Issues**: Run `python test_setup.py`
- **Trading Questions**: Read `STRATEGY.md`
- **Technical Details**: Check `README.md`
- **Logs**: Always check `logs/trading.log` first

---

## Success Metrics

After **1 week**, you should see:
- 30-100+ trades executed
- 95-98% win rate
- 10-20% return on capital
- PNL chart trending upward

If not meeting these:
1. Check logs for errors
2. Verify wallet has sufficient USDC
3. Try less strict parameters (lower threshold)
4. Ensure bot running during peak hours (esports tournaments)

---

## Next Steps

1. ✅ **Let it run** - Don't interfere, trust the bot
2. ✅ **Monitor once daily** - Check stats, not every trade
3. ✅ **Compound profits** - Keep profits in wallet to grow position sizes
4. ✅ **Read strategy doc** - Understand the edge: `STRATEGY.md`
5. ✅ **Scale up slowly** - After 1 week of success, add more capital

---

**You're ready to trade! Run `python run.py` and let the bot work.**

*Remember: This is a low-edge, high-frequency strategy. Profit comes from consistency and compounding, not big wins.*
