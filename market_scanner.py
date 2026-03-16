"""Market scanning module to find high-probability opportunities"""
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config import Config
from ssl_helper import get_aiohttp_connector

class MarketScanner:
    def __init__(self, clob_client):
        self.clob_client = clob_client
        self.gamma_url = Config.GAMMA_API_URL
        
    async def scan_markets(self) -> List[Dict]:
        """
        Scan for markets matching criteria:
        - Active esports (LoL/Dota), sports, or 5-min crypto markets
        - <5 minutes to close
        - One side >=98% probability
        """
        opportunities = []
        
        # Get SSL connector for corporate networks
        connector = get_aiohttp_connector()
        
        async with aiohttp.ClientSession(connector=connector) as session:
            # Get active markets from Gamma API
            markets = await self._get_active_markets(session)
            
            for market in markets:
                try:
                    # Check if market matches our criteria
                    opportunity = await self._analyze_market(market)
                    if opportunity:
                        opportunities.append(opportunity)
                except Exception as e:
                    print(f"Error analyzing market {market.get('condition_id', 'unknown')}: {e}")
                    
        return opportunities
        
    async def _get_active_markets(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Fetch active markets from Gamma API"""
        try:
            # Get markets from multiple categories
            all_markets = []
            
            # Esports markets (LoL, Dota)
            esports_tags = ['lol', 'dota', 'league-of-legends', 'dota-2', 'esports']
            for tag in esports_tags:
                markets = await self._fetch_markets_by_tag(session, tag)
                all_markets.extend(markets)
                
            # Sports markets
            sports_tags = ['sports', 'nba', 'nfl', 'soccer', 'tennis', 'ufc']
            for tag in sports_tags:
                markets = await self._fetch_markets_by_tag(session, tag)
                all_markets.extend(markets)
                
            # Crypto markets (5-min, short-term)
            crypto_tags = ['crypto', 'bitcoin', 'ethereum', 'btc', 'eth']
            for tag in crypto_tags:
                markets = await self._fetch_markets_by_tag(session, tag)
                all_markets.extend(markets)
                
            return all_markets
            
        except Exception as e:
            print(f"Error fetching markets: {e}")
            return []
            
    async def _fetch_markets_by_tag(self, session: aiohttp.ClientSession, tag: str) -> List[Dict]:
        """Fetch markets by tag from Gamma API"""
        try:
            url = f"{self.gamma_url}/markets"
            params = {
                'tag': tag,
                'active': 'true',
                'closed': 'false'
            }
            
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data if isinstance(data, list) else []
                return []
                
        except Exception as e:
            print(f"Error fetching markets for tag '{tag}': {e}")
            return []
            
    async def _analyze_market(self, market: Dict) -> Optional[Dict]:
        """
        Analyze market to check if it meets criteria
        Returns opportunity dict if criteria met, None otherwise
        """
        try:
            # Check if market is closing soon
            end_date_str = market.get('end_date_iso') or market.get('endDate')
            if not end_date_str:
                return None
                
            end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
            time_to_close = end_date - datetime.now().astimezone()
            
            # Must have <5 minutes to close
            if time_to_close.total_seconds() > Config.TIME_TO_CLOSE_THRESHOLD_MINUTES * 60:
                return None
                
            # Must have >0 time (not already closed)
            if time_to_close.total_seconds() <= 0:
                return None
                
            # Get orderbook for each outcome
            condition_id = market.get('condition_id')
            tokens = market.get('tokens', [])
            
            if not condition_id or not tokens:
                return None
                
            best_opportunity = None
            highest_prob = 0
            
            for token in tokens:
                token_id = token.get('token_id')
                outcome = token.get('outcome')
                
                if not token_id:
                    continue
                    
                # Get orderbook midpoint to calculate probability
                try:
                    orderbook = self.clob_client.get_order_book(token_id)
                    
                    if not orderbook or not orderbook.get('bids') or not orderbook.get('asks'):
                        continue
                        
                    # Calculate midpoint price
                    best_bid = float(orderbook['bids'][0]['price']) if orderbook['bids'] else 0
                    best_ask = float(orderbook['asks'][0]['price']) if orderbook['asks'] else 1
                    midpoint_price = (best_bid + best_ask) / 2
                    
                    # Probability is approximately the price (in decimal form)
                    probability = midpoint_price * 100
                    
                    # Check if meets threshold
                    if probability >= Config.MIN_PROBABILITY_THRESHOLD:
                        if probability > highest_prob:
                            highest_prob = probability
                            best_opportunity = {
                                'condition_id': condition_id,
                                'token_id': token_id,
                                'market_name': market.get('question', 'Unknown'),
                                'outcome': outcome,
                                'probability': probability,
                                'time_to_close_seconds': int(time_to_close.total_seconds()),
                                'best_bid': best_bid,
                                'best_ask': best_ask,
                                'midpoint_price': midpoint_price,
                                'category': self._get_category(market)
                            }
                            
                except Exception as e:
                    print(f"Error getting orderbook for token {token_id}: {e}")
                    continue
                    
            return best_opportunity
            
        except Exception as e:
            print(f"Error in _analyze_market: {e}")
            return None
            
    def _get_category(self, market: Dict) -> str:
        """Determine market category"""
        tags = market.get('tags', [])
        question = market.get('question', '').lower()
        
        # Check for esports
        esports_keywords = ['lol', 'dota', 'league of legends', 'esports']
        if any(tag in esports_keywords for tag in tags) or any(kw in question for kw in esports_keywords):
            return 'esports'
            
        # Check for sports
        sports_keywords = ['nba', 'nfl', 'soccer', 'tennis', 'ufc', 'sports']
        if any(tag in sports_keywords for tag in tags) or any(kw in question for kw in sports_keywords):
            return 'sports'
            
        # Check for crypto
        crypto_keywords = ['btc', 'eth', 'bitcoin', 'ethereum', 'crypto']
        if any(tag in crypto_keywords for tag in tags) or any(kw in question for kw in crypto_keywords):
            return 'crypto'
            
        return 'other'
