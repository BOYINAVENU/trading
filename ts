"""Token scanner - detects newly launched tokens on Polygon"""
import asyncio
import aiohttp
from web3 import Web3
from datetime import datetime, timedelta
import time

class TokenScanner:
    """Scan for newly launched tokens on DEXes"""
    
    def __init__(self, config, logger, w3):
        self.config = config
        self.logger = logger
        self.w3 = w3
        self.seen_tokens = set()
        self.pair_created_topic = "0x0d3648bd0f6ba80134a33ba9275ac585d9d315f0ad8355cddefde31afa28d0e9"  # PairCreated event
        
        # QuickSwap Factory ABI (minimal)
        self.factory_abi = [
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "name": "token0", "type": "address"},
                    {"indexed": True, "name": "token1", "type": "address"},
                    {"indexed": False, "name": "pair", "type": "address"},
                    {"indexed": False, "name": "", "type": "uint256"}
                ],
                "name": "PairCreated",
                "type": "event"
            }
        ]
        
        # ERC20 ABI (minimal)
        self.erc20_abi = [
            {"constant": True, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "type": "function"},
            {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "type": "function"},
            {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
            {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
            {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}
        ]
        
        # Pair ABI (minimal)
        self.pair_abi = [
            {"constant": True, "inputs": [], "name": "getReserves", "outputs": [
                {"name": "reserve0", "type": "uint112"},
                {"name": "reserve1", "type": "uint112"},
                {"name": "blockTimestampLast", "type": "uint32"}
            ], "type": "function"},
            {"constant": True, "inputs": [], "name": "token0", "outputs": [{"name": "", "type": "address"}], "type": "function"},
            {"constant": True, "inputs": [], "name": "token1", "outputs": [{"name": "", "type": "address"}], "type": "function"}
        ]
    
    async def scan_for_new_tokens(self):
        """Scan blockchain for newly created token pairs"""
        try:
            current_block = self.w3.eth.block_number
            from_block = current_block - self.config.lookback_blocks
            
            self.logger.debug(f"Scanning blocks {from_block} to {current_block}")
            
            # Get PairCreated events from QuickSwap factory
            factory_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.config.quickswap_factory),
                abi=self.factory_abi
            )
            
            # Query PairCreated events (web3.py v7+ uses snake_case)
            events = factory_contract.events.PairCreated.get_logs(
                from_block=from_block,
                to_block=current_block
            )
            
            new_tokens = []
            for event in events:
                token0 = event['args']['token0']
                token1 = event['args']['token1']
                pair_address = event['args']['pair']
                block_number = event['blockNumber']
                
                # Determine which token is new (not WMATIC/USDC)
                new_token = self._identify_new_token(token0, token1)
                if not new_token:
                    continue
                
                # Skip if already seen
                if new_token in self.seen_tokens:
                    continue
                
                # Get token age
                block_data = self.w3.eth.get_block(block_number)
                token_age = int(time.time()) - block_data['timestamp']
                
                # Filter by age
                if token_age < self.config.min_age_seconds or token_age > self.config.max_age_seconds:
                    continue
                
                # Get token details
                token_data = await self._get_token_details(new_token, pair_address, token_age)
                if token_data:
                    new_tokens.append(token_data)
                    self.seen_tokens.add(new_token)
                    self.logger.log_token_found(token_data)
            
            return new_tokens
            
        except Exception as e:
            self.logger.error(f"Error scanning for tokens: {e}")
            return []
    
    def _identify_new_token(self, token0, token1):
        """Identify which token is the new memecoin (not WMATIC/USDC)"""
        wmatic = self.config.wmatic_address.lower()
        usdc = self.config.usdc_address.lower()
        
        token0_lower = token0.lower()
        token1_lower = token1.lower()
        
        # Skip if pair doesn't include WMATIC or USDC
        if not (wmatic in [token0_lower, token1_lower] or usdc in [token0_lower, token1_lower]):
            return None
        
        # Return the token that's NOT WMATIC/USDC
        if token0_lower in [wmatic, usdc]:
            return token1
        else:
            return token0
    
    async def _get_token_details(self, token_address, pair_address, age_seconds):
        """Get detailed information about a token"""
        try:
            token_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=self.erc20_abi
            )
            
            pair_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(pair_address),
                abi=self.pair_abi
            )
            
            # Get token info
            name = token_contract.functions.name().call()
            symbol = token_contract.functions.symbol().call()
            decimals = token_contract.functions.decimals().call()
            total_supply = token_contract.functions.totalSupply().call()
            
            # Get pair reserves
            reserves = pair_contract.functions.getReserves().call()
            token0_address = pair_contract.functions.token0().call()
            
            # Calculate liquidity
            is_token0 = token0_address.lower() == token_address.lower()
            token_reserve = reserves[0] if is_token0 else reserves[1]
            quote_reserve = reserves[1] if is_token0 else reserves[0]
            
            # Estimate liquidity in USD (rough estimate using MATIC price ~$0.50)
            liquidity_usd = (quote_reserve / 1e18) * 0.50 * 2  # Rough estimate
            
            return {
                'address': token_address,
                'name': name,
                'symbol': symbol,
                'decimals': decimals,
                'total_supply': total_supply,
                'pair_address': pair_address,
                'liquidity_usd': liquidity_usd,
                'token_reserve': token_reserve,
                'quote_reserve': quote_reserve,
                'age_seconds': age_seconds,
                'discovered_at': datetime.now()
            }
            
        except Exception as e:
            self.logger.debug(f"Error getting token details for {token_address}: {e}")
            return None
    
    async def get_token_holders(self, token_address):
        """Get number of token holders (using Polygonscan API)"""
        try:
            async with aiohttp.ClientSession() as session:
                # Note: This requires Polygonscan API key
                # For now, return estimated holders based on transaction count
                return await self._estimate_holders(token_address)
        except:
            return 0
    
    async def _estimate_holders(self, token_address):
        """Estimate holders based on recent transactions"""
        try:
            # Get recent transfer events
            token_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=self.erc20_abi
            )
            
            # Rough estimate: count unique addresses in recent transfers
            # In production, use Polygonscan API or indexer
            return 10  # Placeholder
        except:
            return 0
    
    async def get_recent_volume(self, pair_address, minutes=5):
        """Get recent trading volume for a pair"""
        try:
            # Get Swap events from the pair
            current_block = self.w3.eth.block_number
            blocks_back = int((minutes * 60) / 2)  # ~2 sec per block on Polygon
            from_block = max(0, current_block - blocks_back)
            
            # This is a simplified version
            # In production, properly decode Swap events
            return 0  # Placeholder
        except:
            return 0
