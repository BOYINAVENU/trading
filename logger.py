"""Logging and monitoring module"""
import logging
import os
from datetime import datetime
from typing import Dict, List
import json
from config import Config

class BotLogger:
    def __init__(self):
        self._setup_logging()
        self.performance_file = 'data/performance.json'
        self._ensure_data_dir()
        
    def _ensure_data_dir(self):
        """Ensure data and logs directories exist"""
        os.makedirs('data', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
    def _setup_logging(self):
        """Setup logging configuration"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Create logger
        self.logger = logging.getLogger('PolymarketBot')
        self.logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # File handler
        fh = logging.FileHandler(Config.LOG_FILE)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(log_format))
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter(log_format))
        
        # Add handlers
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
    def log_trade(self, trade_data: Dict):
        """Log trade execution"""
        self.logger.info(f"TRADE EXECUTED: {trade_data.get('market_name')} | "
                        f"Outcome: {trade_data.get('outcome')} | "
                        f"Prob: {trade_data.get('probability', 0):.2f}% | "
                        f"Size: ${trade_data.get('position_size', 0):.2f}")
                        
    def log_opportunity(self, opportunity: Dict):
        """Log found opportunity"""
        self.logger.info(f"OPPORTUNITY: {opportunity.get('market_name')} | "
                        f"Outcome: {opportunity.get('outcome')} | "
                        f"Prob: {opportunity.get('probability', 0):.2f}% | "
                        f"Closes in: {opportunity.get('time_to_close_seconds', 0)}s")
                        
    def log_scan_summary(self, markets_scanned: int, opportunities_found: int):
        """Log scan summary"""
        self.logger.debug(f"Scan complete: {markets_scanned} markets, {opportunities_found} opportunities")
        
    def log_daily_summary(self, stats: Dict):
        """Log daily performance summary"""
        self.logger.info(f"DAILY SUMMARY: PNL: ${stats.get('daily_pnl', 0):.2f} | "
                        f"Trades: {stats.get('total_trades', 0)} | "
                        f"Win Rate: {stats.get('win_rate', 0):.1f}% | "
                        f"Consecutive Losses: {stats.get('consecutive_losses', 0)}")
                        
    def log_error(self, error: str, exc_info=None):
        """Log error"""
        self.logger.error(error, exc_info=exc_info)
        
    def log_info(self, message: str):
        """Log info message"""
        self.logger.info(message)
        
    def log_debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
        
    def record_performance(self, balance: float, daily_pnl: float):
        """Record performance metrics for charting"""
        performance = self._load_performance()
        
        performance.append({
            'timestamp': datetime.now().isoformat(),
            'balance': balance,
            'daily_pnl': daily_pnl
        })
        
        with open(self.performance_file, 'w') as f:
            json.dump(performance, f, indent=2)
            
    def _load_performance(self) -> List[Dict]:
        """Load performance history"""
        if os.path.exists(self.performance_file):
            with open(self.performance_file, 'r') as f:
                return json.load(f)
        return []
        
    def generate_pnl_chart(self):
        """Generate PNL chart using matplotlib"""
        try:
            import matplotlib.pyplot as plt
            from datetime import datetime
            
            performance = self._load_performance()
            
            if not performance:
                self.logger.warning("No performance data to chart")
                return
                
            # Extract data
            timestamps = [datetime.fromisoformat(p['timestamp']) for p in performance]
            balances = [p['balance'] for p in performance]
            
            # Create chart
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, balances, linewidth=2, color='#00ff00')
            plt.title('Polymarket Sniper Bot - Balance Over Time', fontsize=16, fontweight='bold')
            plt.xlabel('Time', fontsize=12)
            plt.ylabel('Balance (USDC)', fontsize=12)
            plt.grid(True, alpha=0.3)
            
            # Format y-axis as currency
            ax = plt.gca()
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.2f}'))
            
            # Rotate x-axis labels
            plt.xticks(rotation=45, ha='right')
            
            # Tight layout
            plt.tight_layout()
            
            # Save chart
            chart_path = 'data/pnl_chart.png'
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"PNL chart saved to {chart_path}")
            
        except ImportError:
            self.logger.warning("matplotlib not available, cannot generate chart")
        except Exception as e:
            self.logger.error(f"Error generating PNL chart: {e}")
