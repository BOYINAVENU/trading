"""WebSocket handler for real-time orderbook updates"""
import asyncio
import websockets
import json
from typing import Dict, Set, Callable
from config import Config

class WebSocketHandler:
    def __init__(self):
        self.ws_url = Config.WS_URL
        self.subscribed_tokens: Set[str] = set()
        self.orderbook_cache: Dict[str, Dict] = {}
        self.callbacks: Dict[str, Callable] = {}
        self.ws = None
        self.running = False
        
    async def connect(self):
        """Connect to WebSocket"""
        try:
            self.ws = await websockets.connect(self.ws_url)
            self.running = True
            print(f"WebSocket connected to {self.ws_url}")
            return True
        except Exception as e:
            print(f"Failed to connect to WebSocket: {e}")
            return False
            
    async def disconnect(self):
        """Disconnect from WebSocket"""
        self.running = False
        if self.ws:
            await self.ws.close()
            self.ws = None
            
    async def subscribe_to_token(self, token_id: str, callback: Callable = None):
        """Subscribe to orderbook updates for a token"""
        if token_id in self.subscribed_tokens:
            return
            
        try:
            subscription_msg = {
                'type': 'subscribe',
                'channel': 'orderbook',
                'market': token_id
            }
            
            await self.ws.send(json.dumps(subscription_msg))
            self.subscribed_tokens.add(token_id)
            
            if callback:
                self.callbacks[token_id] = callback
                
            print(f"Subscribed to token {token_id}")
            
        except Exception as e:
            print(f"Error subscribing to token {token_id}: {e}")
            
    async def unsubscribe_from_token(self, token_id: str):
        """Unsubscribe from orderbook updates"""
        if token_id not in self.subscribed_tokens:
            return
            
        try:
            unsubscribe_msg = {
                'type': 'unsubscribe',
                'channel': 'orderbook',
                'market': token_id
            }
            
            await self.ws.send(json.dumps(unsubscribe_msg))
            self.subscribed_tokens.remove(token_id)
            
            if token_id in self.callbacks:
                del self.callbacks[token_id]
                
            if token_id in self.orderbook_cache:
                del self.orderbook_cache[token_id]
                
            print(f"Unsubscribed from token {token_id}")
            
        except Exception as e:
            print(f"Error unsubscribing from token {token_id}: {e}")
            
    async def listen(self):
        """Listen for WebSocket messages"""
        while self.running:
            try:
                if not self.ws:
                    await asyncio.sleep(1)
                    continue
                    
                message = await asyncio.wait_for(self.ws.recv(), timeout=5.0)
                data = json.loads(message)
                
                # Handle orderbook updates
                if data.get('type') == 'orderbook':
                    token_id = data.get('market')
                    
                    if token_id:
                        # Update cache
                        self.orderbook_cache[token_id] = {
                            'bids': data.get('bids', []),
                            'asks': data.get('asks', []),
                            'timestamp': data.get('timestamp')
                        }
                        
                        # Call callback if registered
                        if token_id in self.callbacks:
                            await self.callbacks[token_id](self.orderbook_cache[token_id])
                            
            except asyncio.TimeoutError:
                # No message received, continue
                continue
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed, reconnecting...")
                await self.connect()
            except Exception as e:
                print(f"Error in WebSocket listener: {e}")
                await asyncio.sleep(1)
                
    def get_cached_orderbook(self, token_id: str) -> Dict:
        """Get cached orderbook for a token"""
        return self.orderbook_cache.get(token_id, {})
        
    async def start(self):
        """Start WebSocket handler"""
        connected = await self.connect()
        if connected:
            asyncio.create_task(self.listen())
            
    async def stop(self):
        """Stop WebSocket handler"""
        await self.disconnect()
