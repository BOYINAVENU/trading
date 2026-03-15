"""Risk management module for position sizing and loss limits"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional
from config import Config

class RiskManager:
    def __init__(self):
        self.consecutive_losses = 0
        self.daily_pnl = 0.0
        self.daily_reset_time = datetime.now().date()
        self.trades_file = 'data/trades.json'
        self.starting_balance = None
        self._ensure_data_dir()
        
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs('data', exist_ok=True)
        
    def _reset_daily_stats(self):
        """Reset daily statistics if new day"""
        current_date = datetime.now().date()
        if current_date > self.daily_reset_time:
            self.daily_pnl = 0.0
            self.daily_reset_time = current_date
            
    def can_trade(self, current_balance: float) -> tuple[bool, str]:
        """
        Check if trading is allowed based on risk limits
        Returns: (can_trade: bool, reason: str)
        """
        self._reset_daily_stats()
        
        # Set starting balance on first check
        if self.starting_balance is None:
            self.starting_balance = current_balance
            
        # Check minimum balance
        if current_balance < Config.MIN_BALANCE_USDC:
            return False, f"Balance ${current_balance:.2f} below minimum ${Config.MIN_BALANCE_USDC}"
            
        # Check consecutive losses
        if self.consecutive_losses >= Config.MAX_CONSECUTIVE_LOSSES:
            return False, f"Hit max consecutive losses ({Config.MAX_CONSECUTIVE_LOSSES})"
            
        # Check daily loss limit
        daily_loss_limit = self.starting_balance * (Config.DAILY_LOSS_LIMIT_PCT / 100)
        if self.daily_pnl < -daily_loss_limit:
            return False, f"Hit daily loss limit (${abs(self.daily_pnl):.2f} / ${daily_loss_limit:.2f})"
            
        return True, "OK"
        
    def calculate_position_size(self, current_balance: float, probability: float) -> float:
        """
        Calculate position size based on balance and probability
        Uses Kelly Criterion adjusted for high-probability bets
        """
        # Base position size (0.5-1% of balance)
        base_size = current_balance * (Config.MAX_POSITION_SIZE_PCT / 100)
        
        # Adjust based on probability (higher prob = slightly larger size)
        # For 98% prob, use ~1%, for 99%+ use full 1%
        prob_multiplier = min(1.0, (probability - 97) / 2)  # 98% = 0.5, 99% = 1.0
        
        position_size = base_size * prob_multiplier
        
        # Minimum $1, maximum 1% of balance
        return max(1.0, min(position_size, current_balance * 0.01))
        
    def record_trade(self, trade_data: Dict):
        """Record trade and update statistics"""
        trade_data['timestamp'] = datetime.now().isoformat()
        
        # Load existing trades
        trades = self._load_trades()
        trades.append(trade_data)
        
        # Save trades
        with open(self.trades_file, 'w') as f:
            json.dump(trades, f, indent=2)
            
        # Update statistics
        pnl = trade_data.get('pnl', 0)
        self.daily_pnl += pnl
        
        if pnl < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
            
    def _load_trades(self) -> list:
        """Load trade history"""
        if os.path.exists(self.trades_file):
            with open(self.trades_file, 'r') as f:
                return json.load(f)
        return []
        
    def get_daily_stats(self) -> Dict:
        """Get daily trading statistics"""
        self._reset_daily_stats()
        trades = self._load_trades()
        
        # Filter today's trades
        today = datetime.now().date()
        today_trades = [
            t for t in trades 
            if datetime.fromisoformat(t['timestamp']).date() == today
        ]
        
        total_pnl = sum(t.get('pnl', 0) for t in today_trades)
        winning_trades = sum(1 for t in today_trades if t.get('pnl', 0) > 0)
        
        return {
            'total_trades': len(today_trades),
            'winning_trades': winning_trades,
            'losing_trades': len(today_trades) - winning_trades,
            'daily_pnl': total_pnl,
            'consecutive_losses': self.consecutive_losses,
            'win_rate': winning_trades / len(today_trades) * 100 if today_trades else 0
        }
