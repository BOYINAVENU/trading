"""Esports match tracker for LoL and Dota 2 - provides live match data for edge"""
import aiohttp
from typing import List, Dict, Optional
from config import Config

class EsportsTracker:
    """
    Track live esports matches to get early signals for Polymarket bets
    
    This gives you an edge by:
    1. Knowing when games are about to end (live game time)
    2. Seeing current score/gold lead before odds fully adjust
    3. Detecting when a team is about to win (Ancient/Nexus HP)
    """
    
    def __init__(self):
        self.riot_api_key = Config.RIOT_API_KEY
        self.dota_api_key = Config.DOTA_STEAM_API_KEY
        
    async def get_lol_live_matches(self) -> List[Dict]:
        """
        Get live League of Legends professional matches
        
        Riot API endpoints:
        - Live matches: https://developer.riotgames.com/apis#match-v5
        - Esports API: https://esports-api.lolesports.com/persisted/gw/
        
        Returns list of live matches with current state
        """
        if not self.riot_api_key or self.riot_api_key == 'your_riot_api_key_here':
            return []
            
        try:
            async with aiohttp.ClientSession() as session:
                # Use LoL Esports API to get live games
                url = 'https://esports-api.lolesports.com/persisted/gw/getLive'
                params = {'hl': 'en-US'}
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        live_matches = []
                        events = data.get('data', {}).get('schedule', {}).get('events', [])
                        
                        for event in events:
                            if event.get('state') == 'inProgress':
                                match_info = {
                                    'match_id': event.get('match', {}).get('id'),
                                    'team1': event.get('match', {}).get('teams', [{}])[0].get('name'),
                                    'team2': event.get('match', {}).get('teams', [{}])[1].get('name') if len(event.get('match', {}).get('teams', [])) > 1 else None,
                                    'tournament': event.get('league', {}).get('name'),
                                    'game_number': event.get('match', {}).get('strategy', {}).get('count', 1),
                                    'status': 'live'
                                }
                                live_matches.append(match_info)
                                
                        return live_matches
                        
        except Exception as e:
            print(f"Error fetching LoL live matches: {e}")
            
        return []
        
    async def get_dota_live_matches(self) -> List[Dict]:
        """
        Get live Dota 2 professional matches
        
        Steam API endpoints:
        - Live league games: https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1/
        
        Returns list of live matches with current state including:
        - Gold difference
        - Kill score
        - Game time
        - Building status
        """
        if not self.dota_api_key or self.dota_api_key == 'your_steam_api_key_here':
            return []
            
        try:
            async with aiohttp.ClientSession() as session:
                url = 'https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1/'
                params = {'key': self.dota_api_key}
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        live_matches = []
                        games = data.get('result', {}).get('games', [])
                        
                        for game in games:
                            radiant_team = game.get('radiant_team', {})
                            dire_team = game.get('dire_team', {})
                            scoreboard = game.get('scoreboard', {})
                            
                            # Calculate advantage
                            radiant_score = scoreboard.get('radiant', {}).get('score', 0)
                            dire_score = scoreboard.get('dire', {}).get('score', 0)
                            game_time = scoreboard.get('duration', 0)
                            
                            # Gold lead (indicates who's winning)
                            radiant_gold = scoreboard.get('radiant', {}).get('net_worth', 0)
                            dire_gold = scoreboard.get('dire', {}).get('net_worth', 0)
                            gold_lead = radiant_gold - dire_gold
                            
                            match_info = {
                                'match_id': game.get('match_id'),
                                'radiant_team': radiant_team.get('team_name', 'Radiant'),
                                'dire_team': dire_team.get('team_name', 'Dire'),
                                'radiant_score': radiant_score,
                                'dire_score': dire_score,
                                'game_time_seconds': game_time,
                                'gold_lead': gold_lead,
                                'gold_lead_team': 'radiant' if gold_lead > 0 else 'dire',
                                'league_id': game.get('league_id'),
                                'status': 'live'
                            }
                            
                            live_matches.append(match_info)
                            
                        return live_matches
                        
        except Exception as e:
            print(f"Error fetching Dota live matches: {e}")
            
        return []
        
    async def analyze_match_for_edge(self, match: Dict, market_data: Dict) -> Optional[Dict]:
        """
        Analyze live match data against Polymarket odds to find edge
        
        Example: If Dota match shows Team A with 15k gold lead at 30 minutes,
        but Polymarket odds are still 60-40, there's potential edge
        
        Returns edge opportunity or None
        """
        # This is where you'd implement your edge detection logic
        # For example:
        # - If gold lead > 10k and game time > 25min in Dota, team is heavily favored
        # - If LoL team is at enemy nexus, game is about to end
        # - Compare this to current Polymarket odds
        
        # Placeholder for now
        return None

# HOW TO GET API KEYS:
"""
RIOT API KEY (for League of Legends):
1. Go to https://developer.riotgames.com/
2. Sign in with your Riot account (create one if needed)
3. Register your project
4. Get your API key (free tier available)
5. Add to .env: RIOT_API_KEY=your_key_here

Note: Riot API rate limits:
- Development: 20 requests/second, 100 requests/2 minutes
- Production: Apply for higher limits

STEAM API KEY (for Dota 2):
1. Go to https://steamcommunity.com/dev/apikey
2. Sign in with Steam account
3. Register domain (can use localhost for testing)
4. Get your API key (free, unlimited for reasonable use)
5. Add to .env: DOTA_STEAM_API_KEY=your_key_here

ALTERNATIVE DATA SOURCES:
- PandaScore API: https://pandascore.co/ (unified esports API)
- Abios Gaming API: https://abiosgaming.com/
- Strafe Esports API: https://strafe.com/

USAGE STRATEGY:
1. Track live games to see current state
2. When game is close to ending (low HP on base, big gold lead, etc.)
3. Check Polymarket odds - if they haven't adjusted yet, you have edge
4. Place bet before odds adjust (usually 1-2 minutes delay)
5. Example: Dota team with 20k gold lead at 35min has ~95% win rate
   If Polymarket shows 85%, that's a 10% edge opportunity
"""
