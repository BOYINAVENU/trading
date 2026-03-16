"""Position manager - track and manage open positions with profit targets"""
from datetime import datetime, timedelta

class PositionManager:
    """Manage open trading positions and exit strategies"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.positions = {}
        self.closed_positions = []
    
    def open_position(self, token_data, buy_result):
        """Record a new position"""
        if not buy_result or not buy_result.get('success'):
            return None
        
        token_address = token_data['address']
        
        position = {
            'token_address': token_address,
            'token_symbol': token_data['symbol'],
            'token_name': token_data['name'],
            'decimals': token_data['decimals'],
            'entry_price': buy_result['entry_price'],
            'token_amount': buy_result['token_amount'],
            'amount_matic': token_data.get('spent_matic', 0),
            'entry_time': datetime.now(),
            'highest_price': buy_result['entry_price'],
            'targets': {
                '3x': {'hit': False, 'sold_percent': 0},
                '5x': {'hit': False, 'sold_percent': 0},
                '10x': {'hit': False, 'sold_percent': 0}
            }
        }
        
        self.positions[token_address] = position
        
        self.logger.success(f"Position opened: {token_data['symbol']}")
        self.logger.info(f"   Entry: ${position['entry_price']:.8f}")
        self.logger.info(f"   Amount: {position['token_amount']:.2f} tokens")
        
        return position
    
    def update_position(self, token_address, current_price):
        """Update position with current price and check targets"""
        if token_address not in self.positions:
            return None
        
        position = self.positions[token_address]
        entry_price = position['entry_price']
        
        # Update highest price for trailing stop
        if current_price > position['highest_price']:
            position['highest_price'] = current_price
        
        # Calculate current multiplier
        multiplier = current_price / entry_price
        
        # Check profit targets
        sell_actions = []
        
        # 3x target
        if multiplier >= 3.0 and not position['targets']['3x']['hit']:
            position['targets']['3x']['hit'] = True
            sell_percent = self.config.take_profit_3x
            sell_actions.append(('3x', sell_percent))
            self.logger.opportunity(f"3x TARGET HIT: {position['token_symbol']}")
        
        # 5x target
        if multiplier >= 5.0 and not position['targets']['5x']['hit']:
            position['targets']['5x']['hit'] = True
            sell_percent = self.config.take_profit_5x
            sell_actions.append(('5x', sell_percent))
            self.logger.opportunity(f"5x TARGET HIT: {position['token_symbol']}")
        
        # 10x target
        if multiplier >= 10.0 and not position['targets']['10x']['hit']:
            position['targets']['10x']['hit'] = True
            sell_percent = self.config.take_profit_10x
            sell_actions.append(('10x', sell_percent))
            self.logger.opportunity(f"10x TARGET HIT: {position['token_symbol']}")
        
        # Check trailing stop
        drawdown_from_high = (position['highest_price'] - current_price) / position['highest_price'] * 100
        
        if drawdown_from_high >= self.config.trailing_stop_percent:
            self.logger.warning(f"Trailing stop triggered: {position['token_symbol']}")
            return {'action': 'close_all', 'reason': 'Trailing Stop'}
        
        # Check max hold time
        hold_time = (datetime.now() - position['entry_time']).total_seconds() / 60
        if hold_time >= self.config.max_hold_time_minutes:
            self.logger.warning(f"Max hold time reached: {position['token_symbol']}")
            return {'action': 'close_all', 'reason': 'Max Hold Time'}
        
        # Return sell actions if any targets hit
        if sell_actions:
            return {'action': 'partial_sell', 'sells': sell_actions}
        
        return None
    
    def close_position(self, token_address, exit_price, reason):
        """Close a position completely"""
        if token_address not in self.positions:
            return None
        
        position = self.positions.pop(token_address)
        
        # Calculate P&L
        pnl_percent = ((exit_price - position['entry_price']) / position['entry_price']) * 100
        hold_time = (datetime.now() - position['entry_time']).total_seconds() / 60
        
        # Update position with exit data
        position['exit_price'] = exit_price
        position['exit_time'] = datetime.now()
        position['pnl_percent'] = pnl_percent
        position['hold_time_minutes'] = hold_time
        position['close_reason'] = reason
        
        # Add to closed positions
        self.closed_positions.append(position)
        
        # Log the close
        self.logger.log_position_closed(position, exit_price, reason)
        
        return position
    
    def get_position(self, token_address):
        """Get a specific position"""
        return self.positions.get(token_address)
    
    def get_all_positions(self):
        """Get all open positions"""
        return list(self.positions.values())
    
    def has_position(self, token_address):
        """Check if we have a position in this token"""
        return token_address in self.positions
    
    def get_total_invested(self):
        """Get total MATIC invested in open positions"""
        return sum(p['amount_matic'] for p in self.positions.values())
    
    def get_current_value(self, prices):
        """Get current value of all positions"""
        total = 0
        for token_address, position in self.positions.items():
            current_price = prices.get(token_address, position['entry_price'])
            position_value = position['token_amount'] * current_price
            total += position_value
        return total
    
    def get_unrealized_pnl(self, prices):
        """Get unrealized P&L for all positions"""
        total_invested = 0
        current_value = 0
        
        for token_address, position in self.positions.items():
            current_price = prices.get(token_address, position['entry_price'])
            
            invested = position['amount_matic']
            value = (current_price / position['entry_price']) * invested
            
            total_invested += invested
            current_value += value
        
        if total_invested == 0:
            return 0
        
        return ((current_value - total_invested) / total_invested) * 100
    
    def get_performance_stats(self):
        """Get overall performance statistics"""
        if not self.closed_positions:
            return {
                'total_trades': 0,
                'wins': 0,
                'losses': 0,
                'win_rate': 0,
                'avg_pnl': 0,
                'total_pnl': 0,
                'best_trade': 0,
                'worst_trade': 0
            }
        
        wins = [p for p in self.closed_positions if p['pnl_percent'] > 0]
        losses = [p for p in self.closed_positions if p['pnl_percent'] <= 0]
        
        total_pnl = sum(p['pnl_percent'] for p in self.closed_positions)
        avg_pnl = total_pnl / len(self.closed_positions)
        
        best_trade = max(p['pnl_percent'] for p in self.closed_positions)
        worst_trade = min(p['pnl_percent'] for p in self.closed_positions)
        
        return {
            'total_trades': len(self.closed_positions),
            'wins': len(wins),
            'losses': len(losses),
            'win_rate': (len(wins) / len(self.closed_positions)) * 100,
            'avg_pnl': avg_pnl,
            'total_pnl': total_pnl,
            'best_trade': best_trade,
            'worst_trade': worst_trade
        }
    
    def log_positions_summary(self):
        """Log summary of all positions"""
        if not self.positions:
            self.logger.info("No open positions")
            return
        
        self.logger.header("OPEN POSITIONS")
        for token_address, pos in self.positions.items():
            hold_time = (datetime.now() - pos['entry_time']).total_seconds() / 60
            self.logger.info(f"\n{pos['token_symbol']}")
            self.logger.info(f"   Entry: ${pos['entry_price']:.8f}")
            self.logger.info(f"   Highest: ${pos['highest_price']:.8f}")
            self.logger.info(f"   Hold Time: {hold_time:.1f} min")
            self.logger.info(f"   Targets Hit: ", end="")
            
            targets_hit = [k for k, v in pos['targets'].items() if v['hit']]
            if targets_hit:
                self.logger.info(", ".join(targets_hit))
            else:
                self.logger.info("None")
