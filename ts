================================================================================
BOT STARTED - SCANNING FOR OPPORTUNITIES
================================================================================

------------------------------------------------------------
Scan #1 - 19:54:13
------------------------------------------------------------
[X] Error scanning for tokens: 400 Client Error: Bad Request for url: https://polygon-mainnet.g.alchemy.com/v2/jDw4YYLZ4bWSF-DtNhbb1
Found 0 new token(s)
# Create test_rpc.py
from web3 import Web3

rpc_url = "YOUR_RPC_URL_HERE"
w3 = Web3(Web3.HTTPProvider(rpc_url))

if w3.is_connected():
    print(f"✓ Connected! Block: {w3.eth.block_number}")
else:
    print("✗ Connection failed")
C:\Users\boyin\Downloads\memecoin-sniper\memecoin-sniper>python rpctest.py
✓ Connected! Block: 84275607
