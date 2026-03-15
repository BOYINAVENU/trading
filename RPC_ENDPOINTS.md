# 🌐 Polygon RPC Endpoints - Fix Connection Issues

## Problem
`Cannot connect to Polygon RPC: https://polygon-rpc.com`

This happens when the RPC endpoint is:
- Down or experiencing issues
- Blocked by corporate firewall
- Rate limited

## ✅ Solution: Use Alternative RPC Endpoints

### **Recommended RPC URLs (Try in order)**

Update your `.env` file with one of these:

#### 1. Polygon Public RPC (Most Reliable)
```env
POLYGON_RPC_URL=https://polygon-rpc.com
```

#### 2. Alchemy (Fast, Reliable - FREE)
```env
POLYGON_RPC_URL=https://polygon-mainnet.g.alchemy.com/v2/demo
```
**Note**: For production, get free API key at https://www.alchemy.com/

#### 3. Ankr (Free Public Endpoint)
```env
POLYGON_RPC_URL=https://rpc.ankr.com/polygon
```

#### 4. Chainstack (Reliable)
```env
POLYGON_RPC_URL=https://polygon-mainnet.public.blastapi.io
```

#### 5. MaticVigil (Fast)
```env
POLYGON_RPC_URL=https://rpc-mainnet.maticvigil.com
```

#### 6. Public Node (Backup)
```env
POLYGON_RPC_URL=https://polygon.llamarpc.com
```

---

## 🎯 Quick Fix Instructions

### Option 1: Edit .env Manually

1. Open `.env` file in editor
2. Find line: `POLYGON_RPC_URL=https://polygon-rpc.com`
3. Replace with: `POLYGON_RPC_URL=https://rpc.ankr.com/polygon`
4. Save file
5. Run: `python test_setup.py`

### Option 2: Use PowerShell to Update

```powershell
# Copy and paste this into PowerShell
(Get-Content .env) -replace 'POLYGON_RPC_URL=.*', 'POLYGON_RPC_URL=https://rpc.ankr.com/polygon' | Set-Content .env
```

Then test:
```bash
python test_setup.py
```

---

## 🔍 Testing Different Endpoints

Try each endpoint until one works:

```bash
# Test Ankr
python -c "from web3 import Web3; w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/polygon')); print('Connected:', w3.is_connected())"

# Test Alchemy
python -c "from web3 import Web3; w3 = Web3(Web3.HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/demo')); print('Connected:', w3.is_connected())"

# Test Chainstack
python -c "from web3 import Web3; w3 = Web3(Web3.HTTPProvider('https://polygon-mainnet.public.blastapi.io')); print('Connected:', w3.is_connected())"
```

---

## 🚀 Best Practice: Get Free API Key

For production use, get a free API key from:

### **Alchemy (Recommended)**
1. Sign up: https://www.alchemy.com/
2. Create new app → Select Polygon Mainnet
3. Copy API key
4. Update .env:
   ```env
   POLYGON_RPC_URL=https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY
   ```

**Benefits**:
- Faster responses
- Higher rate limits
- Better reliability
- Free tier: 300M compute units/month (plenty for this bot)

### **Infura (Alternative)**
1. Sign up: https://www.infura.io/
2. Create project → Add Polygon
3. Copy endpoint URL
4. Update .env:
   ```env
   POLYGON_RPC_URL=https://polygon-mainnet.infura.io/v3/YOUR_PROJECT_ID
   ```

---

## 📊 RPC Endpoint Comparison

| Endpoint | Speed | Reliability | Rate Limit | Notes |
|----------|-------|-------------|------------|-------|
| Ankr | Fast | High | Good | Public, works well |
| Alchemy | Very Fast | Very High | Excellent | Free API key |
| Chainstack | Fast | High | Good | Public |
| MaticVigil | Medium | Medium | Low | May rate limit |
| LlamaRPC | Fast | High | Good | Community run |

---

## 🔧 Corporate Network Issues

If ALL endpoints fail, your corporate firewall might be blocking:

### Solution 1: Use Corporate Proxy
```env
# Add to .env if you have proxy
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080
```

### Solution 2: Use VPN
- Connect to VPN that allows blockchain RPC access
- Then run bot

### Solution 3: Test on Personal Network
- Try running from home/mobile hotspot first
- Confirm it works outside corporate network

---

## ✅ After Fixing RPC Connection

Once `python test_setup.py` shows all tests passing:

1. **Verify your wallet has funds**:
   - USDC on Polygon (for trading)
   - MATIC on Polygon (for gas fees)

2. **Run the bot**:
   ```bash
   python run.py
   ```

3. **Monitor logs**:
   ```bash
   # In another terminal
   tail -f logs/trading.log
   ```

---

## 🆘 Still Not Connecting?

Try this diagnostic:

```bash
# Test internet connectivity
ping google.com

# Test HTTPS in Python
python -c "import requests; print(requests.get('https://google.com').status_code)"

# Test specific RPC
python -c "import requests; print(requests.post('https://rpc.ankr.com/polygon', json={'jsonrpc':'2.0','method':'eth_blockNumber','params':[],'id':1}).json())"
```

If these fail, it's a network/firewall issue. Contact IT or try from different network.

---

**Quick Fix**: Update `.env` line 3 to:
```env
POLYGON_RPC_URL=https://rpc.ankr.com/polygon
```

Then run `python test_setup.py` again!
