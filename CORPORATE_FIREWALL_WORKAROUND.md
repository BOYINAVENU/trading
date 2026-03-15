# 🔥 Corporate Firewall Blocking RPC - Solutions

## Problem
Your corporate network is blocking ALL Polygon RPC endpoints. This is a common security policy in enterprise environments.

## 🔍 Diagnosis

Run this to confirm the issue:
```bash
python test_network.py
```

This will test:
- Basic internet connectivity
- DNS resolution
- Multiple RPC endpoints
- HTTPS POST requests
- Proxy configuration

---

## ✅ Solutions (In Order of Ease)

### **Solution 1: Run on Personal Network (EASIEST)**

The bot needs to connect to blockchain RPC endpoints. Test if it works outside your corporate network:

**Option A: Mobile Hotspot**
```
1. Enable mobile hotspot on your phone
2. Connect laptop to hotspot
3. Run: python test_setup.py
4. If it works → Run bot from home/hotspot when trading
```

**Option B: Home Network**
```
1. Take laptop home
2. Connect to home WiFi
3. Test if RPC connections work
4. If yes → Run bot from home
```

**Why this works**: Home/mobile networks typically don't block blockchain RPC endpoints.

---

### **Solution 2: Deploy on VPS (RECOMMENDED)**

Run the bot on a cloud VPS instead of your corporate laptop:

**Benefits**:
- No corporate firewall restrictions
- 24/7 uptime
- Fast, reliable connection
- Only $5-6/month

**Quick VPS Setup**:
```bash
# 1. Get VPS (DigitalOcean, Vultr, Linode)
#    - Select Ubuntu 22.04
#    - Choose $6/month plan
#    - Takes 2 minutes to create

# 2. SSH into VPS
ssh root@your-vps-ip

# 3. Setup bot
git clone <your-repo-url>
cd polymarket-sniper
chmod +x setup.sh
./setup.sh

# 4. Configure
nano .env
# Add your PRIVATE_KEY

# 5. Setup systemd service
sudo cp polymarket-bot.service /etc/systemd/system/
sudo nano /etc/systemd/system/polymarket-bot.service  # Edit username
sudo systemctl enable polymarket-bot
sudo systemctl start polymarket-bot

# 6. Monitor remotely
sudo journalctl -u polymarket-bot -f
```

**VPS Providers**:
- **DigitalOcean**: https://www.digitalocean.com/ ($6/month)
- **Vultr**: https://www.vultr.com/ ($6/month)
- **Linode**: https://www.linode.com/ ($5/month)
- **AWS**: Free tier for 12 months (t2.micro)

---

### **Solution 3: Request IT Firewall Exception**

Ask IT to whitelist these domains:

```
rpc.ankr.com
polygon-rpc.com
polygon-mainnet.g.alchemy.com
polygon-mainnet.public.blastapi.io
polygon.llamarpc.com
```

**Email template**:
```
Subject: Firewall Exception Request - Blockchain RPC Access

Hi IT Team,

I need access to Polygon blockchain RPC endpoints for a development project.

Could you please whitelist these domains:
- rpc.ankr.com
- polygon-mainnet.g.alchemy.com
- polygon-rpc.com

These are read-only blockchain data endpoints (similar to API calls).

Thank you!
```

**Likelihood**: Low - Many companies won't allow blockchain access

---

### **Solution 4: Configure Corporate Proxy**

If your network uses a proxy, configure it:

**Find your proxy settings**:
```
1. Windows Settings → Network & Internet → Proxy
2. Note the proxy address and port
```

**Configure in .env**:
```env
# Add to .env file
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080

# If proxy requires authentication
HTTP_PROXY=http://username:password@proxy.company.com:8080
HTTPS_PROXY=http://username:password@proxy.company.com:8080
```

**Test**:
```bash
python test_network.py
```

---

### **Solution 5: Use VPN**

Some VPNs can bypass corporate restrictions:

**Personal VPN** (if allowed):
```
1. Connect to personal VPN (NordVPN, ExpressVPN, etc.)
2. Run: python test_setup.py
3. If works → Use VPN when running bot
```

**⚠️ Warning**: Check your company's VPN policy before using personal VPN on corporate device.

---

### **Solution 6: SSH Tunnel (Advanced)**

If you have access to an external server:

```bash
# On your laptop (corporate network)
ssh -D 8080 user@your-external-server.com

# In another terminal
export HTTP_PROXY=socks5://localhost:8080
export HTTPS_PROXY=socks5://localhost:8080
python test_setup.py
```

---

## 🎯 Recommended Approach

### **For Testing/Development**:
1. Use mobile hotspot or home network
2. Verify bot works correctly
3. Test with small amounts

### **For Production/24-7 Trading**:
1. Deploy on VPS ($5-6/month)
2. Monitor remotely
3. No dependency on corporate network

---

## 📊 Comparison

| Solution | Ease | Cost | Reliability | Corporate Compliant |
|----------|------|------|-------------|---------------------|
| Mobile Hotspot | ⭐⭐⭐⭐⭐ | Free | Medium | ✓ |
| Home Network | ⭐⭐⭐⭐⭐ | Free | High | ✓ |
| VPS | ⭐⭐⭐⭐ | $5-6/mo | Very High | ✓ |
| IT Exception | ⭐⭐ | Free | High | ✓ |
| Corporate Proxy | ⭐⭐⭐ | Free | Medium | ✓ |
| Personal VPN | ⭐⭐⭐ | $5-10/mo | Medium | ⚠️ Check policy |
| SSH Tunnel | ⭐⭐ | Varies | Medium | ⚠️ |

---

## 🚀 Quick Start: Mobile Hotspot Method

**Right now, try this**:

1. **Enable mobile hotspot** on your phone
2. **Connect laptop** to the hotspot
3. **Run test**:
   ```bash
   python test_network.py
   ```
4. **If successful**, run:
   ```bash
   python test_setup.py
   ```
5. **If all tests pass**:
   ```bash
   python run.py
   ```

This confirms the bot works - it's just your corporate network blocking it.

---

## 💡 Long-Term Strategy

**Week 1**: Test on mobile hotspot/home
- Verify bot functionality
- Test with small amounts
- Build confidence in strategy

**Week 2+**: Deploy to VPS
- 24/7 operation
- No corporate restrictions
- Professional setup
- Monitor via SSH

**Cost**: $5-6/month for VPS
**Benefit**: Fully automated trading, no network restrictions

---

## 🆘 Still Stuck?

1. **Run diagnostic**: `python test_network.py`
2. **Share results** to identify exact issue
3. **Try mobile hotspot** as immediate test
4. **Consider VPS** for production

---

**Next Step**: Try connecting to mobile hotspot and run `python test_network.py`
