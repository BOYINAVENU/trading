# 🎯 Polymarket Sniper Strategy - Deep Dive

## The $205k Strategy Explained

This document explains the trading strategy that generated $205k+ in returns and how this bot implements it.

## Core Principles

### 1. High Probability Arbitrage

The strategy focuses on markets where the outcome is almost certain (≥98% probability) but still offers small profit opportunities.

**Why it works:**
- Market makers need to maintain liquidity on both sides
- Some traders exit positions late, creating mispricing
- Information spreads slowly in prediction markets
- 2-5% return on near-certain outcomes compounds quickly

**Example:**
```
Market: "Will [Team A] win match that ends in 3 minutes?"
Current score: Team A winning 15-2 with destroyed base
Polymarket odds: 98.5% YES

Bot action: Buy YES shares at $0.985
Expected return: $1.00 payout = 1.5% profit in 3 minutes
Risk: Very low (only lose if miracle comeback)
```

### 2. Time-Based Certainty

Markets become more certain as closing time approaches. The bot only trades when:
- **<5 minutes to close**: Maximum certainty, minimum reversal risk
- **Outcome nearly certain**: One side already at 98%+

**Why 5 minutes?**
- In esports: Game outcomes clear in final moments
- In sports: Last-minute plays rarely reverse clear victories
- In crypto: 5-min price windows have momentum
- Less time = less risk of unexpected events

### 3. Kelly Criterion Position Sizing

The bot uses a modified Kelly Criterion for position sizing:

```
Position Size = (Edge × Bankroll) / Odds

Where:
- Edge = Your probability - Market probability
- Bankroll = Current USDC balance
- Odds = Market implied odds

Simplified to: 0.5-1% of bankroll per trade
```

**Example:**
```
Bankroll: $1,000
Market probability: 98%
Your edge: Assume true probability is 99%
Position size: $10 (1% of bankroll)

If win: +$0.20 (2% return on $10)
If lose: -$10 (1% of bankroll)

Expected value: 0.99 × $0.20 - 0.01 × $10 = +$0.098
```

## Market Categories

### Esports (LoL, Dota 2)

**Best opportunities:**
- Live games in final moments
- Clear gold/kill advantages
- Ancient/Nexus about to fall
- Team composition counters

**Edge sources:**
1. **Live game data**: Track gold leads, building HP
2. **Game knowledge**: Understand when games are unwinnable
3. **Speed**: Place bets before odds adjust

**Example workflow:**
```
1. Dota 2 game: Team A has 25k gold lead at 40 minutes
2. Check Polymarket: "Will Team A win?" at 92%
3. Your analysis: 25k lead = 98% win rate historically
4. Edge: 98% - 92% = 6% edge
5. Bot action: Buy YES at 92%, likely profit when odds → 98%
```

### Sports

**Best opportunities:**
- Final minutes of blowout games
- Certain point spreads about to hit
- Clear winner with time running out

**Example:**
```
NBA game: Lakers up 125-95 with 2 minutes left
Market: "Will Lakers win?" at 98.5%
Bot: Buy YES at $0.985, collect $1.00 in 2 minutes
Return: 1.5% in 2 minutes = 43,200% APY (theoretical)
```

### Crypto (5-min price windows)

**Best opportunities:**
- Strong directional momentum
- 5-min windows with clear trend
- High volatility = more extreme probabilities

**Example:**
```
BTC 5-min prediction: "Will BTC be above $50,000 in 5 minutes?"
Current: $50,500 with strong upward momentum
Market: 96% YES
Bot: Buy YES, collect profit in 5 minutes
```

## Risk Management Philosophy

### 1. Daily Loss Limit (5%)

Protects against:
- Bad luck streaks
- Market anomalies
- Technical errors
- Your own mistakes

**Implementation:**
- Track cumulative daily P&L
- Stop trading when -5% of starting balance
- Reset at midnight UTC

### 2. Consecutive Loss Protection

Stops after 3 losses in a row because:
- Something might be wrong (bot error, market issue)
- Psychological pressure increases mistakes
- Time to review strategy

### 3. Position Size Caps

Never risk >1% per trade because:
- Kelly Criterion suggests small positions for low edge
- Preserves capital for compounding
- Limits impact of unexpected losses

## Compounding Effect

The power of this strategy comes from compounding small wins:

**Example over 30 days:**
```
Starting balance: $1,000
Average trades per day: 10
Win rate: 97%
Average return per winning trade: 2%
Position size: 1% of balance

Day 1: 10 trades, 9 wins, 1 loss
  Wins: 9 × $10 × 2% = +$1.80
  Loss: 1 × $10 = -$10
  Net: -$8.20 (bad day)

But more typically:
Day 1: 10 trades, 10 wins
  Profit: 10 × $10 × 2% = +$2.00
  New balance: $1,002

Day 2: 10 trades, 10 wins
  Profit: 10 × $10.02 × 2% = +$2.00
  New balance: $1,004.00

After 30 days (300 trades, 97% win rate):
  Expected balance: ~$1,180 - $1,250
  Return: 18-25% monthly
```

## Why This Strategy Works

1. **Market Inefficiency**: Polymarket is still relatively new, inefficiencies exist
2. **Liquidity Provision**: Market makers provide liquidity even at extreme odds
3. **Late Traders**: People exit positions late, creating opportunities
4. **Information Delay**: Real-world events → odds adjustment has lag
5. **Psychology**: Traders hold losing positions hoping for reversal

## Risks & Limitations

### What Can Go Wrong

1. **Unexpected Reversals** (rare)
   - Sports: Miracle plays
   - Esports: Game-breaking bugs
   - Crypto: Flash crashes

2. **Liquidity Issues**
   - Large positions might not fill
   - Slippage on entry/exit
   - Markets can close suddenly

3. **Technical Risks**
   - API downtime
   - Network issues
   - Smart contract bugs

4. **Market Changes**
   - Polymarket adjusts fee structure
   - Market makers leave
   - Regulations change

### Mitigation Strategies

- **Small positions**: Minimize single-trade impact
- **Diversification**: Trade multiple market types
- **Fast execution**: WebSocket for real-time data
- **Stop losses**: Daily limits and consecutive loss protection
- **Monitoring**: Constant logging and alerts

## Advanced Techniques

### 1. Live Data Integration

Get edge by:
- Tracking live esports stats (gold, kills, buildings)
- Monitoring sports play-by-play
- Analyzing crypto order flow

### 2. Odds Prediction

Build models to:
- Predict odds movement
- Identify mispriced markets
- Calculate true probabilities

### 3. Multi-Market Arbitrage

Exploit:
- Correlated markets (if A wins, B likely wins)
- Same event on different platforms
- Hedging strategies

## Performance Metrics

Track these metrics:
- **Sharpe Ratio**: Risk-adjusted returns
- **Win Rate**: % of profitable trades
- **Average Win**: Profit per winning trade
- **Average Loss**: Loss per losing trade
- **Max Drawdown**: Largest peak-to-trough decline
- **Compound Growth Rate**: Daily/monthly compounding

## Realistic Expectations

### Conservative Scenario
- Win rate: 95%
- Average return: 1.5% per trade
- 5-10 trades/day
- Monthly return: 10-15%

### Base Case
- Win rate: 97%
- Average return: 2% per trade
- 10-15 trades/day
- Monthly return: 20-30%

### Optimistic Scenario
- Win rate: 98%
- Average return: 3% per trade
- 15-20 trades/day
- Monthly return: 40-60%

**Note**: These are theoretical. Actual results vary based on:
- Market conditions
- Opportunity availability
- Execution quality
- Luck

## Psychological Factors

### Avoiding Common Mistakes

1. **Chasing losses**: Stick to daily limits
2. **Over-confidence**: Don't increase position sizes after wins
3. **FOMO**: Don't trade markets >5 minutes out
4. **Ignoring signals**: If consecutive losses, stop and review

### Maintaining Discipline

- Let the bot run automatically
- Don't override position sizes
- Trust the risk management
- Review performance weekly, not hourly

## Conclusion

This strategy works by:
1. Finding near-certain outcomes
2. Taking small positions repeatedly
3. Compounding gains over time
4. Protecting capital with strict risk limits

**The key**: Consistency and discipline. Small edges + high frequency + compounding = significant returns.

**Remember**: No strategy is risk-free. Start small, test thoroughly, and only risk what you can afford to lose.

---

*"It's not about big wins. It's about consistent small wins that compound exponentially."*
