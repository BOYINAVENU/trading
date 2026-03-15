"""Main Polymarket Sniper Bot orchestrator"""
import asyncio
import sys
import signal
from datetime import datetime
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from config import Config
from risk_manager import RiskManager
from market_scanner import MarketScanner
from trading_engine import TradingEngine
from websocket_handler import WebSocketHandler
from logger import BotLogger
from ssl_helper import setup_ssl_context

class PolymarketSniperBot:
    def __init__(self):
        self.config = Config
        self.logger = BotLogger()
        self.risk_manager = RiskManager()
        self.clob_client = None
        self.market_scanner = None
        self.trading_engine = None
        self.ws_handler = WebSocketHandler()
        self.running = False
        self.current_balance = 0.0
        
    def initialize(self):
        """Initialize bot components"""
        try:
            # Validate configuration
            self.config.validate()
            
            # Setup SSL context for corporate networks
            setup_ssl_context()
            
            # Initialize CLOB client
            self.logger.log_info("Initializing Polymarket CLOB client...")
            
            # Create API credentials
            creds = ApiCreds(
                api_key="",  # Will be derived from private key
                api_secret="",
                api_passphrase=""
            )
            
            # Initialize client with private key
            self.clob_client = ClobClient(
                host=Config.CLOB_API_URL,
                chain_id=Config.CHAIN_ID,
                key=Config.PRIVATE_KEY
            )
            
            # Get initial balance
            self.current_balance = self._get_balance()
            self.logger.log_info(f"Initial balance: ${self.current_balance:.2f} USDC")
            
            # Initialize components
            self.market_scanner = MarketScanner(self.clob_client)
            self.trading_engine = TradingEngine(self.clob_client, self.risk_manager)
            
            self.logger.log_info("Bot initialized successfully!")
            return True
            
        except Exception as e:
            self.logger.log_error(f"Failed to initialize bot: {e}", exc_info=True)
            return False
            
    def _get_balance(self) -> float:
        """Get current USDC balance"""
        try:
            # Get balance from CLOB client
            balances = self.clob_client.get_balances()
            
            # Find USDC balance
            for balance in balances:
                if balance.get('asset', '').upper() == 'USDC':
                    return float(balance.get('balance', 0))
                    
            return 0.0
            
        except Exception as e:
            self.logger.log_error(f"Error getting balance: {e}")
            return self.current_balance  # Return cached balance on error
            
    async def run(self):
        """Main bot loop"""
        self.running = True
        
        # Start WebSocket handler
        await self.ws_handler.start()
        
        # Setup signal handlers for graceful shutdown
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, lambda s, f: asyncio.create_task(self.shutdown()))
        
        self.logger.log_info("=" * 80)
        self.logger.log_info("POLYMARKET SNIPER BOT STARTED")
        self.logger.log_info("=" * 80)
        self.logger.log_info(f"Strategy: High-probability sniper (≥{Config.MIN_PROBABILITY_THRESHOLD}%)")
        self.logger.log_info(f"Time threshold: ≤{Config.TIME_TO_CLOSE_THRESHOLD_MINUTES} minutes")
        self.logger.log_info(f"Position size: {Config.MAX_POSITION_SIZE_PCT}% per trade")
        self.logger.log_info(f"Daily loss limit: {Config.DAILY_LOSS_LIMIT_PCT}%")
        self.logger.log_info("=" * 80)
        
        scan_count = 0
        
        while self.running:
            try:
                scan_count += 1
                self.logger.log_debug(f"\n--- Scan #{scan_count} at {datetime.now().strftime('%H:%M:%S')} ---")
                
                # Update balance
                self.current_balance = self._get_balance()
                
                # Check if trading is allowed
                can_trade, reason = self.risk_manager.can_trade(self.current_balance)
                
                if not can_trade:
                    self.logger.log_info(f"Trading halted: {reason}")
                    
                    # Log daily summary and generate chart
                    stats = self.risk_manager.get_daily_stats()
                    self.logger.log_daily_summary(stats)
                    self.logger.generate_pnl_chart()
                    
                    # Wait before checking again
                    await asyncio.sleep(Config.POLL_INTERVAL_SECONDS)
                    continue
                
                # Scan for opportunities
                opportunities = await self.market_scanner.scan_markets()
                
                self.logger.log_scan_summary(
                    markets_scanned=len(opportunities),
                    opportunities_found=len(opportunities)
                )
                
                # Process opportunities
                for opportunity in opportunities:
                    self.logger.log_opportunity(opportunity)
                    
                    # Check if we should trade this opportunity
                    can_trade, reason = self.risk_manager.can_trade(self.current_balance)
                    
                    if not can_trade:
                        self.logger.log_info(f"Skipping trade: {reason}")
                        break
                    
                    # Execute trade
                    trade_result = self.trading_engine.execute_trade(
                        opportunity, 
                        self.current_balance
                    )
                    
                    if trade_result:
                        self.logger.log_trade(trade_result)
                        
                        # Subscribe to WebSocket for this token
                        token_id = opportunity['token_id']
                        await self.ws_handler.subscribe_to_token(
                            token_id,
                            callback=lambda ob: self._on_orderbook_update(token_id, ob)
                        )
                        
                        # Update balance
                        self.current_balance = self._get_balance()
                
                # Check status of active positions
                active_positions = list(self.trading_engine.active_positions.keys())
                for order_id in active_positions:
                    self.trading_engine.check_position_status(order_id)
                
                # Log daily stats periodically
                if scan_count % 10 == 0:  # Every 10 scans
                    stats = self.risk_manager.get_daily_stats()
                    self.logger.log_daily_summary(stats)
                    self.logger.record_performance(self.current_balance, stats['daily_pnl'])
                    
                    # Generate chart every hour
                    if scan_count % 120 == 0:  # Every 120 scans (1 hour at 30s intervals)
                        self.logger.generate_pnl_chart()
                
                # Wait before next scan
                await asyncio.sleep(Config.POLL_INTERVAL_SECONDS)
                
            except Exception as e:
                self.logger.log_error(f"Error in main loop: {e}", exc_info=True)
                await asyncio.sleep(Config.POLL_INTERVAL_SECONDS)
                
    async def _on_orderbook_update(self, token_id: str, orderbook: dict):
        """Handle real-time orderbook updates"""
        # You can implement real-time trading adjustments here
        # For now, just log updates for active positions
        pass
        
    async def shutdown(self):
        """Graceful shutdown"""
        self.logger.log_info("\n" + "=" * 80)
        self.logger.log_info("SHUTTING DOWN BOT...")
        self.logger.log_info("=" * 80)
        
        self.running = False
        
        # Stop WebSocket
        await self.ws_handler.stop()
        
        # Log final stats
        stats = self.risk_manager.get_daily_stats()
        self.logger.log_daily_summary(stats)
        
        # Generate final chart
        self.logger.generate_pnl_chart()
        
        self.logger.log_info("Bot stopped successfully")
        sys.exit(0)

async def main():
    """Main entry point"""
    bot = PolymarketSniperBot()
    
    if not bot.initialize():
        print("Failed to initialize bot. Check logs for details.")
        return
    
    try:
        await bot.run()
    except KeyboardInterrupt:
        await bot.shutdown()
    except Exception as e:
        bot.logger.log_error(f"Fatal error: {e}", exc_info=True)
        await bot.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
