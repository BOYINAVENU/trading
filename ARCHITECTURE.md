# 🏗️ System Architecture

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     POLYMARKET SNIPER BOT                       │
│                   (Main Orchestrator: bot.py)                   │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────┐
        │          INITIALIZATION PHASE              │
        │  • Load config from .env                   │
        │  • Initialize py-clob-client SDK           │
        │  • Connect to Polygon wallet               │
        │  • Start WebSocket connection              │
        │  • Verify USDC balance                     │
        └────────────────────────────────────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────┐
        │          MAIN TRADING LOOP                 │
        │      (Runs every 30 seconds)               │
        └────────────────────────────────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                ▼                                 ▼
    ┌───────────────────────┐         ┌──────────────────────┐
    │   MARKET SCANNER      │         │   RISK MANAGER       │
    │  market_scanner.py    │         │  risk_manager.py     │
    │                       │         │                      │
    │ • Query Gamma API     │         │ • Check daily P&L    │
    │ • Filter by category  │◄────────┤ • Count losses       │
    │ • Check time to close │         │ • Verify balance     │
    │ • Calculate prob      │         │ • Calculate size     │
    │ • Get orderbook       │         │                      │
    └───────────────────────┘         └──────────────────────┘
                │                                 │
                └────────────┬────────────────────┘
                             ▼
                ┌────────────────────────┐
                │  OPPORTUNITY FOUND?    │
                │  • Prob ≥ 98%          │
                │  • Time < 5 min        │
                │  • Liquidity OK        │
                └────────────────────────┘
                             │
                    YES ─────┤───── NO (Skip, continue scanning)
                             ▼
                ┌────────────────────────┐
                │   TRADING ENGINE       │
                │  trading_engine.py     │
                │                        │
                │ • Calculate position   │
                │ • Create limit order   │
                │ • Submit to CLOB       │
                │ • Track order ID       │
                └────────────────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │   POSITION TRACKING    │
                │                        │
                │ • Monitor order fills  │
                │ • Update via WebSocket │
                │ • Calculate P&L        │
                │ • Log results          │
                └────────────────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │   LOGGER & ANALYTICS   │
                │      logger.py         │
                │                        │
                │ • Save to trades.json  │
                │ • Update performance   │
                │ • Generate PNL chart   │
                │ • Log to file          │
                └────────────────────────┘
```

---

## Component Interactions

### 1. Bot.py (Main Orchestrator)
```python
┌──────────────────────┐
│      bot.py          │
│                      │
│  • Initialize all    │
│    components        │
│  • Run main loop     │
│  • Handle errors     │
│  • Coordinate flows  │
│  • Manage shutdown   │
└──────────────────────┘
         │
         ├──► config.py (Configuration)
         ├──► risk_manager.py (Risk checks)
         ├──► market_scanner.py (Find opportunities)
         ├──► trading_engine.py (Execute trades)
         ├──► websocket_handler.py (Real-time data)
         └──► logger.py (Logging & analytics)
```

### 2. Market Scanner Flow
```
Gamma API
    │
    ▼
┌─────────────────────┐
│ Get Active Markets  │
│ • Esports           │
│ • Sports            │
│ • Crypto            │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Filter Markets      │
│ • By category       │
│ • By end time       │
│ • By status         │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ For each market:    │
│ 1. Get orderbook    │
│ 2. Calc midpoint    │
│ 3. Check prob ≥98%  │
│ 4. Check time <5min │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Return list of      │
│ opportunities       │
└─────────────────────┘
```

### 3. Risk Management Flow
```
Trade Request
    │
    ▼
┌──────────────────────┐
│ Check Balance        │
│ > min threshold?     │
└──────────────────────┘
    │ YES
    ▼
┌──────────────────────┐
│ Check Daily P&L      │
│ < -5% limit?         │
└──────────────────────┘
    │ NO
    ▼
┌──────────────────────┐
│ Check Consecutive    │
│ Losses < 3?          │
└──────────────────────┘
    │ YES
    ▼
┌──────────────────────┐
│ Calculate Position   │
│ Size (Kelly)         │
│ = 0.5-1% of balance  │
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│ APPROVE TRADE        │
└──────────────────────┘
```

### 4. Trading Execution Flow
```
Opportunity
    │
    ▼
┌──────────────────────┐
│ Get Position Size    │
│ from Risk Manager    │
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│ Calculate Shares     │
│ shares = size/price  │
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│ Create Limit Order   │
│ via py-clob-client   │
│ • token_id           │
│ • price              │
│ • size (shares)      │
│ • side = BUY         │
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│ Submit to Polymarket │
│ CLOB API             │
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│ Track Order ID in    │
│ active_positions{}   │
└──────────────────────┘
```

### 5. WebSocket Integration
```
WebSocket Connection
wss://ws-subscriptions-clob.polymarket.com
    │
    ▼
┌──────────────────────┐
│ Subscribe to Tokens  │
│ (active positions)   │
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│ Receive Updates:     │
│ • Orderbook changes  │
│ • Order fills        │
│ • Price movements    │
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│ Update Cache &       │
│ Trigger Callbacks    │
└──────────────────────┘
```

---

## Data Flow

### Configuration Flow
```
.env file
    │
    ▼
config.py
    │
    ├──► PRIVATE_KEY ──────────► Web3/CLOB Client
    ├──► Trading Params ───────► Market Scanner
    ├──► Risk Params ──────────► Risk Manager
    └──► API URLs ─────────────► HTTP Clients
```

### Trade Data Flow
```
Market Opportunity
    │
    ▼
Trading Engine
    │
    ├──► Create trade_data{}
    │
    ▼
Risk Manager
    │
    ├──► Record to trades.json
    │
    ▼
Logger
    │
    ├──► Append to trading.log
    ├──► Update performance.json
    └──► Generate pnl_chart.png
```

---

## External Integrations

### Polymarket APIs
```
┌────────────────────────────────────────────┐
│         POLYMARKET ECOSYSTEM               │
├────────────────────────────────────────────┤
│                                            │
│  Gamma API (gamma-api.polymarket.com)     │
│  ├─ Market discovery                       │
│  ├─ Market metadata                        │
│  └─ Market categories                      │
│                                            │
│  CLOB API (clob.polymarket.com)           │
│  ├─ Order placement                        │
│  ├─ Order status                           │
│  ├─ Orderbook data                         │
│  └─ Balance queries                        │
│                                            │
│  WebSocket (ws-subscriptions...)          │
│  ├─ Real-time orderbook                    │
│  ├─ Order fills                            │
│  └─ Price updates                          │
│                                            │
└────────────────────────────────────────────┘
                    ▲
                    │
            ┌───────┴────────┐
            │                │
    ┌───────▼─────┐   ┌─────▼──────┐
    │ Market      │   │ Trading    │
    │ Scanner     │   │ Engine     │
    └─────────────┘   └────────────┘
```

### Blockchain Integration
```
┌────────────────────────────────────────────┐
│         POLYGON BLOCKCHAIN                 │
├────────────────────────────────────────────┤
│                                            │
│  RPC Endpoint (polygon-rpc.com)           │
│  ├─ Balance queries                        │
│  ├─ Transaction signing                    │
│  └─ Network state                          │
│                                            │
│  USDC Contract (0x2791Bca...)             │
│  ├─ Balance checks                         │
│  └─ Allowances                             │
│                                            │
└────────────────────────────────────────────┘
                    ▲
                    │
            ┌───────┴────────┐
            │                │
        Web3.py        py-clob-client
```

### Optional: Esports APIs
```
┌────────────────────────────────────────────┐
│         ESPORTS DATA SOURCES               │
├────────────────────────────────────────────┤
│                                            │
│  Riot API (developer.riotgames.com)       │
│  ├─ Live LoL matches                       │
│  ├─ Match status                           │
│  └─ Game events                            │
│                                            │
│  Steam API (api.steampowered.com)         │
│  ├─ Live Dota matches                      │
│  ├─ Gold leads                             │
│  └─ Game time                              │
│                                            │
└────────────────────────────────────────────┘
                    ▲
                    │
            ┌───────┴────────┐
            │ Esports        │
            │ Tracker        │
            └────────────────┘
```

---

## File System Structure

### Runtime Directories
```
polymarket-sniper/
│
├── data/                      # Generated at runtime
│   ├── trades.json           # All trade history
│   ├── performance.json      # Performance metrics
│   └── pnl_chart.png         # Auto-generated chart
│
└── logs/                      # Generated at runtime
    ├── trading.log           # Main application log
    └── systemd.log           # Systemd output (VPS only)
```

### State Management
```
┌──────────────────────────┐
│   In-Memory State        │
├──────────────────────────┤
│ • current_balance        │
│ • active_positions{}     │
│ • consecutive_losses     │
│ • daily_pnl              │
│ • orderbook_cache{}      │
└──────────────────────────┘
         │
         ▼
┌──────────────────────────┐
│   Persistent State       │
├──────────────────────────┤
│ • trades.json            │
│ • performance.json       │
│ • trading.log            │
└──────────────────────────┘
```

---

## Error Handling & Recovery

### Error Handling Hierarchy
```
┌─────────────────────────────────────┐
│     run.py (Wrapper Process)        │
│  • Catches crashes                  │
│  • Auto-restart (max 10/hour)       │
│  • Logs restart events              │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│     bot.py (Main Process)           │
│  • Try/catch in main loop           │
│  • Continue on non-fatal errors     │
│  • Graceful shutdown on fatal       │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Component-Level Error Handling    │
│  • market_scanner.py: Skip bad      │
│    markets, continue scanning       │
│  • trading_engine.py: Log failed    │
│    trades, don't crash              │
│  • websocket_handler.py: Auto       │
│    reconnect on disconnect          │
└─────────────────────────────────────┘
```

### Recovery Mechanisms
```
Error Type          →  Recovery Action
─────────────────────────────────────────────
API Timeout         →  Retry with backoff
Network Error       →  Continue next cycle
WebSocket Dropped   →  Auto-reconnect
Invalid Order       →  Log & skip trade
Insufficient Funds  →  Wait for next cycle
Rate Limit          →  Sleep & retry
Critical Error      →  Shutdown & restart
```

---

## Performance Optimizations

### Concurrent Operations
```python
# Market scanning (parallel API calls)
async with aiohttp.ClientSession() as session:
    tasks = [
        fetch_esports_markets(session),
        fetch_sports_markets(session),
        fetch_crypto_markets(session)
    ]
    results = await asyncio.gather(*tasks)
```

### Caching Strategy
```
┌──────────────────────────┐
│   WebSocket Cache        │
│  • Live orderbook data   │
│  • Updated real-time     │
│  • Reduces API calls     │
└──────────────────────────┘
         │
         ▼
┌──────────────────────────┐
│   Trade History Cache    │
│  • In-memory for session │
│  • Persisted to JSON     │
│  • Fast daily stats      │
└──────────────────────────┘
```

---

## Security Architecture

### Credential Management
```
.env file (gitignored)
    │
    ├──► PRIVATE_KEY (encrypted in transit)
    │         │
    │         ▼
    │    Web3 signing (local only)
    │         │
    │         ▼
    │    Transaction broadcast
    │
    └──► API_KEYS (optional, for esports)
              │
              ▼
         HTTP requests (HTTPS)
```

### Best Practices
- ✅ Private key never logged
- ✅ `.env` in `.gitignore`
- ✅ HTTPS for all API calls
- ✅ Local transaction signing
- ✅ No credentials in code
- ✅ Minimal permissions

---

## Monitoring & Observability

### Logging Levels
```
DEBUG   →  Scan summaries, market checks
INFO    →  Trades, opportunities, daily stats
WARNING →  Low balance, missed opportunities
ERROR   →  Failed trades, API errors
```

### Metrics Tracked
```
Real-time:
• Current balance
• Active positions count
• Consecutive losses
• Daily P&L

Historical:
• All trades (JSON)
• Win rate
• Average return
• Max drawdown
• Sharpe ratio
```

### Visualization
```
performance.json
    │
    ▼
matplotlib
    │
    ▼
pnl_chart.png
    │
    ├─ Balance over time
    ├─ Cumulative P&L
    └─ Daily returns
```

---

## Deployment Models

### Local Development
```
Windows/Mac/Linux
    │
    ▼
Python venv
    │
    ▼
python run.py
    │
    ├──► Auto-restart on crash
    └──► Manual start/stop
```

### VPS Production
```
Ubuntu VPS (DigitalOcean/Vultr)
    │
    ▼
systemd service
    │
    ├──► Auto-start on boot
    ├──► Auto-restart on crash
    ├──► Logs to journalctl
    └──► Remote management
```

---

## Scalability Considerations

### Current Limits
- **Single account**: One wallet, one bot instance
- **API rate limits**: Polymarket CLOB limits
- **Position size**: 1% max per trade
- **Sequential trades**: One at a time

### Future Scaling Options
1. **Multi-account**: Run multiple instances with different wallets
2. **Parallel execution**: Trade multiple markets simultaneously
3. **Advanced strategies**: Combine with other signals
4. **Cross-platform**: Arbitrage across prediction markets

---

## Testing Strategy

### Manual Testing
```bash
# 1. Setup verification
python test_setup.py

# 2. Dry run (monitor only, no trading)
# Set position size to 0 in .env
MAX_POSITION_SIZE_PCT=0

# 3. Small capital test
# Start with $50-100, run for 24 hours

# 4. Monitor logs
tail -f logs/trading.log
```

### Automated Checks
- Configuration validation (config.py)
- Balance checks (before each trade)
- Order validation (trading_engine.py)
- Daily limit checks (risk_manager.py)

---

## Production Readiness Checklist

✅ **Code Quality**
- Modular architecture
- Error handling everywhere
- Comprehensive logging
- Clean code structure

✅ **Security**
- No hardcoded credentials
- Gitignored .env
- Secure API usage
- Local key signing

✅ **Reliability**
- Auto-restart on crash
- WebSocket auto-reconnect
- Graceful error handling
- State persistence

✅ **Monitoring**
- Real-time logging
- Performance tracking
- PNL visualization
- Daily summaries

✅ **Documentation**
- Setup guides
- Strategy explanation
- Troubleshooting docs
- Code comments

---

## System Requirements

### Minimum
- Python 3.9+
- 512MB RAM
- 1GB disk space
- Internet connection

### Recommended
- Python 3.10+
- 1GB RAM
- 5GB disk space
- Stable internet (low latency to Polygon RPC)

### VPS Specs
- $5-6/month tier sufficient
- Ubuntu 20.04+ recommended
- 1 vCPU, 1GB RAM
- 25GB SSD

---

*This architecture is designed for reliability, performance, and ease of maintenance. Each component is modular and can be enhanced independently.*
