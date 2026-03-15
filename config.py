"""Configuration management for Polymarket Sniper Bot"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Authentication
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    POLYGON_RPC_URL = os.getenv('POLYGON_RPC_URL', 'https://polygon-rpc.com')
    CHAIN_ID = int(os.getenv('CHAIN_ID', '137'))
    
    # Trading Parameters
    MAX_POSITION_SIZE_PCT = float(os.getenv('MAX_POSITION_SIZE_PCT', '1.0'))
    MIN_PROBABILITY_THRESHOLD = float(os.getenv('MIN_PROBABILITY_THRESHOLD', '98.0'))
    TIME_TO_CLOSE_THRESHOLD_MINUTES = int(os.getenv('TIME_TO_CLOSE_THRESHOLD_MINUTES', '5'))
    POLL_INTERVAL_SECONDS = int(os.getenv('POLL_INTERVAL_SECONDS', '30'))
    
    # Risk Management
    DAILY_LOSS_LIMIT_PCT = float(os.getenv('DAILY_LOSS_LIMIT_PCT', '5.0'))
    MAX_CONSECUTIVE_LOSSES = int(os.getenv('MAX_CONSECUTIVE_LOSSES', '3'))
    MIN_BALANCE_USDC = float(os.getenv('MIN_BALANCE_USDC', '10.0'))
    
    # API Keys (Optional)
    RIOT_API_KEY = os.getenv('RIOT_API_KEY')
    DOTA_STEAM_API_KEY = os.getenv('DOTA_STEAM_API_KEY')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/trading.log')
    
    # Corporate Network Settings
    DISABLE_SSL_VERIFICATION = os.getenv('DISABLE_SSL_VERIFICATION', 'False').lower() == 'true'
    
    # Polymarket API
    GAMMA_API_URL = 'https://gamma-api.polymarket.com'
    CLOB_API_URL = 'https://clob.polymarket.com'
    WS_URL = 'wss://ws-subscriptions-clob.polymarket.com/ws/market'
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.PRIVATE_KEY:
            raise ValueError("PRIVATE_KEY is required in .env file")
        if cls.PRIVATE_KEY == 'your_ethereum_private_key_here':
            raise ValueError("Please set a valid PRIVATE_KEY in .env file")
        return True
