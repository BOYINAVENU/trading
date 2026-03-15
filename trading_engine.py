"""Trading execution engine for Polymarket"""
from typing import Dict, Optional
from datetime import datetime
from config import Config

class TradingEngine:
    def __init__(self, clob_client, risk_manager):
        self.clob_client = clob_client
        self.risk_manager = risk_manager
        self.active_positions = {}
        
    def execute_trade(self, opportunity: Dict, current_balance: float) -> Optional[Dict]:
        """
        Execute a trade on the given opportunity
        Returns trade details if successful, None otherwise
        """
        try:
            # Calculate position size
            position_size = self.risk_manager.calculate_position_size(
                current_balance, 
                opportunity['probability']
            )
            
            # Ensure we have enough balance
            if position_size > current_balance * 0.95:  # Leave some buffer
                print(f"Insufficient balance for trade. Need ${position_size:.2f}, have ${current_balance:.2f}")
                return None
                
            # Determine order side and price
            # We want to BUY the high-probability outcome at current best ask (or slightly better)
            token_id = opportunity['token_id']
            price = opportunity['best_ask']  # Buy at ask price
            
            # Adjust price slightly to improve fill probability (0.1% better than ask)
            price = min(0.99, price * 1.001)  # Cap at 0.99 to avoid edge cases
            
            # Calculate shares to buy
            # Each share costs 'price' USDC and pays out 1 USDC if correct
            shares = position_size / price
            
            print(f"\n{'='*60}")
            print(f"EXECUTING TRADE")
            print(f"{'='*60}")
            print(f"Market: {opportunity['market_name']}")
            print(f"Outcome: {opportunity['outcome']}")
            print(f"Probability: {opportunity['probability']:.2f}%")
            print(f"Price: ${price:.4f}")
            print(f"Position Size: ${position_size:.2f}")
            print(f"Shares: {shares:.2f}")
            print(f"Time to Close: {opportunity['time_to_close_seconds']}s")
            print(f"{'='*60}\n")
            
            # Place limit order
            order = self.clob_client.create_order(
                token_id=token_id,
                price=price,
                size=shares,
                side='BUY',  # Always buying high-probability outcome
                order_type='GTC'  # Good-till-cancelled
            )
            
            if not order:
                print("Failed to create order")
                return None
                
            order_id = order.get('orderID')
            
            # Record trade
            trade_data = {
                'order_id': order_id,
                'token_id': token_id,
                'market_name': opportunity['market_name'],
                'outcome': opportunity['outcome'],
                'category': opportunity['category'],
                'probability': opportunity['probability'],
                'price': price,
                'shares': shares,
                'position_size': position_size,
                'time_to_close': opportunity['time_to_close_seconds'],
                'status': 'pending',
                'entry_time': datetime.now().isoformat(),
                'pnl': 0  # Will update when position closes
            }
            
            # Track active position
            self.active_positions[order_id] = trade_data
            
            return trade_data
            
        except Exception as e:
            print(f"Error executing trade: {e}")
            import traceback
            traceback.print_exc()
            return None
            
    def check_position_status(self, order_id: str) -> Optional[Dict]:
        """
        Check status of an active position
        Returns updated position data if changed, None otherwise
        """
        try:
            if order_id not in self.active_positions:
                return None
                
            # Get order status
            order = self.clob_client.get_order(order_id)
            
            if not order:
                return None
                
            position = self.active_positions[order_id]
            status = order.get('status', 'unknown').lower()
            
            # Update position status
            if status == 'matched' or status == 'filled':
                position['status'] = 'filled'
                position['fill_time'] = datetime.now().isoformat()
                
                # Calculate current value (will update PNL when market resolves)
                # For now, just mark as filled
                print(f"Order {order_id} filled!")
                
            elif status == 'cancelled' or status == 'expired':
                position['status'] = status
                position['pnl'] = 0
                self.risk_manager.record_trade(position)
                del self.active_positions[order_id]
                print(f"Order {order_id} {status}")
                
            return position
            
        except Exception as e:
            print(f"Error checking position status: {e}")
            return None
            
    def update_pnl(self, order_id: str, pnl: float):
        """Update PNL for a position"""
        if order_id in self.active_positions:
            position = self.active_positions[order_id]
            position['pnl'] = pnl
            position['exit_time'] = datetime.now().isoformat()
            
            # Record trade
            self.risk_manager.record_trade(position)
            
            # Remove from active positions
            del self.active_positions[order_id]
            
            # Log result
            result = "WIN" if pnl > 0 else "LOSS"
            print(f"\n{'='*60}")
            print(f"TRADE {result}: ${pnl:.2f}")
            print(f"Market: {position['market_name']}")
            print(f"Outcome: {position['outcome']}")
            print(f"{'='*60}\n")
            
    def get_active_positions_count(self) -> int:
        """Get number of active positions"""
        return len(self.active_positions)
